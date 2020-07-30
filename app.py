from flask import Flask, render_template, Response, request, g
from pykafka import KafkaClient
from datetime import datetime
import sqlite3

# define the function to connect to kafka
def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

# create an instance of Flask
app = Flask(__name__)

## Setup route that creates a Sqlite3 database and inserts some default values
@app.route('/setup/')
def setup():
	## Create and initialize DB with default values
	conn = sqlite3.connect('user.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS user(user_id varchar(60) NOT NULL,user_name varchar(60) NOT NULL, email varchar(60) NOT NULL,password varchar(256) NOT NULL,PRIMARY KEY (user_id))")
	c.execute("INSERT INTO user VALUES ('C0775761', 'Aggrey Ennis', 'C0775761@mylambton.ca', 'password');")
	c.execute("INSERT INTO user VALUES ('C0777013', 'Gayathri Sasidharan', 'C0777013@mylambton.ca', 'password');")
	c.execute("INSERT INTO user VALUES ('C0777014', 'Elizebeth Shiju', 'C0777014@mylambton.ca', 'password');")
	c.execute("INSERT INTO user VALUES ('C0777017', 'Kalhaar Savaj', 'C07770137@mylambton.ca', 'password');")
	c.execute("INSERT INTO user VALUES ('C0777011', 'Bhargava Muralidharan', 'C0777011@mylambton.ca', 'password');")
	conn.commit()
	conn.close()

	## Initialize the Kafka client within this scope
	client = get_kafka_client()

	## List of topics to be created
	list_items = ['cbd_2204_big_data_strategies', 'cbd_2234_introduction_to_cloud_computing', 'cpp_1001_coop_preparation', 'itp_2123_server_admin_1']

	for item in list_items:
		topic = client.topics[item]
		producer = topic.get_sync_producer()
		producer.produce('This is the beginning of this thread.\n\n'.encode('ascii'))

	return "Setup Complete"


# Defines a default route for Flask which leads to the index page
@app.route('/')
def index():

	# Get a list of topics from the server
	client = get_kafka_client()
	topics_list = client.topics
	topics = []

	# convert the values from bytes to utf-8 and store them in topics list
	for i in topics_list:
		topics.append(str(i.decode("utf-8")))

	# render the template along with the list data
	return render_template('index.html', topics=topics)
	# python app.py


## CONSUMER
## Returns the messages for a particular topic
@app.route('/getmessages/<topicname>')
def get_messages(topicname):
	client = get_kafka_client()
	def events():
		for i in client.topics[topicname].get_simple_consumer():
			yield '\n{0}\n'.format(i.value.decode())
	return Response(events(), mimetype="text/event-stream")


## Route used for sending messages to a particular topic
@app.route('/send_message/<topicname>', methods=['POST'])
def send_message(topicname):
	## Only accept post requests for this route
	if request.method == 'POST':
		client = get_kafka_client()
		topic = client.topics[topicname]
		producer = topic.get_sync_producer()

		## Data values collected from the form
		user_id = request.form['user_id'].strip()
		password = request.form['password'].strip()
		message = request.form['message'].strip()

		## Authentication using values stored in the sqlite3 database
		conn = sqlite3.connect('user.db')
		c = conn.cursor()
		c.execute('SELECT * FROM user WHERE user_id=? AND password=? LIMIT 1', (user_id,password,))
		user = c.fetchone()

		## If no rows are returned by the query
		if user is None:
		    print('Account Credentials Incorrect')
		    return "credentials"
		else:
			## Generate timestamp values
			dateTimeObj = datetime.now()
			dateObj = dateTimeObj.date()
			timeObj = dateTimeObj.time()

			dateStr = dateObj.strftime("%b/%d/%Y ")
			timeStr = timeObj.hour, ':', timeObj.minute, ':', timeObj.second

			## create tuple with all the values
			raw_tuple = str(dateStr), str(timeObj.hour), ':', str(timeObj.minute), ':', str(timeObj.second),' ', user[1], ' (', user[0], '): ', message, '\n'
			## Join tuple values into one string
			string_rep =  ''.join(raw_tuple)

			## Pass string representation encoded in ascii format to the producer
			producer.produce(string_rep.encode('ascii'))

			return "true"

	return "error"

## Route for adding new messages to a particular topic
@app.route('/new_message/<topicname>')
def new_message(topicname):
	return render_template('new_message.html', topicname=topicname)

	return "true"

## ---
if __name__ == '__main__':
    app.run(debug=True, port=5001)