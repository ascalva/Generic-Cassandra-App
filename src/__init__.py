from flask      import Flask
from src.config import Config

# Init Flask app using config.
app = Flask(__name__)
app.config.from_object(Config)


from src.routes        import api
from src.CassandraConn import CassandraConn

app.register_blueprint(api)

# Connect to Cassandra db
app.db = CassandraConn(
    hosts    = Config.CASSANDRA_HOSTS,
    keyspace = Config.CASSANDRA_KEYSPACE
)
