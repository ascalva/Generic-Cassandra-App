import uuid
import cassandra
from cassandra.cluster import Cluster
from time              import sleep


class CassandraConn :

    def __init__(self, hosts, keyspace = None) :
        self.cluster  = None
        self.session  = None
        self.keyspace = None
        self.hosts    = hosts

        # Start session.
        self.createSession()

        # Use supplied keyspace.
        if keyspace is not None :
            self.updateKeySpace(keyspace)


    def createSession(self) :
        retries      = 20
        self.cluster = Cluster(self.hosts, port=9042)

        # Cassandra db can take a few seconds to startup, keep retrying.
        while (retries := retries - 1) > 0 :
            try :
                self.session = self.cluster.connect()
                break

            except cassandra.cluster.NoHostAvailable :
                print(f"Waiting for database (NoHostAvailableException)")
                sleep(5)

            except cassandra.DriverException :
                print(f"Waiting for database (DriverException)")
                sleep(5)

        print(f"Connection has been established: {self.hosts}")


    def updateKeySpace(self, keyspace) :
        c_sql = f"""
                CREATE KEYSPACE IF NOT EXISTS {keyspace}
                WITH REPLICATION =
                    {{ 'class' : 'SimpleStrategy', 'replication_factor' : 2 }}
                """

        # Ececute CQL command, and set keyspace to current.
        self.execute(c_sql)
        self.session.set_keyspace(keyspace)
        self.keyspace = keyspace

        print(f"KeySpace has been updated: {self.keyspace}")


    def execute(self, cql_command, extras=[]) :
        return self.session.execute(cql_command, extras)


    def createTableUser(self) :
        c_sql = """
                CREATE TABLE IF NOT EXISTS User (
                    user_id uuid
                    , uname varchar
                    , fname varchar
                    , lname varchar
                    , PRIMARY KEY (user_id));
                 """
        self.execute(c_sql)


    def createUser(self, uname, fname, lname) :
        c_sql  = "INSERT INTO User (user_id, uname, fname, lname) VALUES (%s,%s,%s,%s)"
        uid    = uuid.uuid4()
        params = [uid, uname, fname, lname]
        self.execute(c_sql, params)


    def getUserTable(self) :
        c_sql = "SELECT * FROM User"

        return self.execute(c_sql)


