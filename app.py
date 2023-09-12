from flask import Flask
import migrations
import repository


app = Flask(__name__)

migrations.execute_migrations()


print("As seguintes tabelas foram encontradas:" + str(repository.get_all_tables()))

@app.route('/get_all_tables')
def get_all_tables():
    return repository.get_all_tables()


@app.route('/')
def hello_world():
    return 'Hello, World!'