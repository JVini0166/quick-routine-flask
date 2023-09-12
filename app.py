from flask import Flask
import migrations
import repository


app = Flask(__name__)

migrations.execute_migrations()

@app.route('/get_all_tables')
def get_all_tables():
    return repository.get_all_tables()


@app.route('/')
def hello_world():
    return 'Hello, World!'