# apache-kafka-example
A really simple example of how to use Apache Kafka via the PyKafka package.

Submitted in partial fulfillment of the requirements for the course CBD2204 Big Data Strategies (Summer 2020 - Lambton College).

### Windows Installation Instructions

* Download the Apache Kafka and Zookeeper files from the Apache website:  [https://kafka.apache.org/quickstart](https://kafka.apache.org/quickstart)
* Extract the files (you can extract it to your C:/ drive folder)
* Add the Windows bin folder of the files you extracted (ex: C:\kafka\bin\windows) to your Windows system path
* Open a new command prompt window and cd to the folder you created above
* Use the commands below to start the Zookeeper server
```
zookeeper-server-start config/zookeeper.properties
```
* Open a new command prompt window again and cd to the folder above. Run the command below to start the Kafka server
```
kafka-server-start config/server.properties
```
---
* Install the [PyKafka](https://pykafka.readthedocs.io/en/latest/) package. You can install PyKafka from PyPI with
```
pip install pykafka
```
or from conda-forge with
```
conda install -c conda-forge pykafka
```
---
* Download and extract this repository (or clone it in command prompt)
```
git clone https://github.com/aennisjr/apache-kafka-example.git
```
* cd into the repository folder and start the Flask server using the following command (you must have Python installed on your computer. Use ``python --version`` to check if you have it installed)
```
python app.py
```
* Navigate to localhost port 5001 and the setup route on locahost in your browser: [http://127.0.0.1:5001/setup](http://127.0.0.1:5001/setup). This will initialize the project with a few default values

### Routes
* ``@app.route('/setup/')`` - Setup route that creates a Sqlite3 database and inserts some default values. Launch this route on first use or if the values need to be re-initialized
* ``@app.route('/')`` - A route which leads to the index page. Here we initialize the kafka client and use it to pull a list of topics from the server. The data is converted from byte format to utf-8 format, stored in a list called topics_list. The template is then rendered along with the data.
* ``@app.route('/getmessages/<topicname>')`` - Route used for displaying messages that belong to a particular topic. Accepts a topic name as the url parameter.
* ``@app.route('/new_message/<topicname>')`` - Route for adding new messages to a particular topic. The posts requests are sent via the ``/templates/new_message.html`` file, and sent to the route using XMLHttpRequest (AJAX).

### Database
Simple [Sqlite3](https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/) database (passwords are stored in plain-text because this is only a basic example).
