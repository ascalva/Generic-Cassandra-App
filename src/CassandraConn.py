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
        self.tables   = {
            "person"  : self.createTableUser,
            "movie"   : self.createTableMovie
        }

        # Start session.
        self.createSession()

        # Use supplied keyspace.
        if keyspace is not None :
            self.updateKeySpace(keyspace)

        # Create tables if they don't exist yet.
        for k,v in self.tables.items() :
            if not self.tableExists(k) : v()


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


    def tableExists(self, table_name) :
        c_sql = f"""
                SELECT table_name
                FROM system_schema.tables
                WHERE keyspace_name='{self.keyspace}';
                """

        # Check if row with table name exists.
        return any(table_name.lower() in row for row in self.execute(c_sql))


    def createTableUser(self) :
        c_sql = """
                CREATE TABLE IF NOT EXISTS Person (
                    user_id uuid
                    , fname varchar
                    , lname varchar
                    , role  varchar
                    , PRIMARY KEY (fname, lname));
                 """
        self.execute(c_sql)


    def createTableMovie(self) :
        c_sql = """
                CREATE TABLE IF NOT EXISTS Movie (
                    title      varchar
                    , director varchar
                    , year     int
                    , PRIMARY KEY (title));
                """
        self.execute(c_sql)


    def createPerson(self, fname, lname, role) :
        c_sql  = "INSERT INTO Person (user_id, fname, lname, role) VALUES (%s,%s,%s,%s)"
        uid    = uuid.uuid4()
        params = [uid, fname, lname, role]
        self.execute(c_sql, params)

    def createMovie(self, movie_name, director, year) :
        c_sql  = "INSERT INTO Movie (title, director, year) VALUES (%s,%s,%s)"
        params = [movie_name, director, year]
        self.execute(c_sql, params)

    def getMovie(self,title):
        c_sql = "SELECT * FROM Movie WHERE title = %s"
        return self.execute(c_sql,[''.join(title)])

    def getPerson(self,fname,lname):
        fname = ''.join(fname)
        lname = ''.join(lname)
        if(fname == ""):
            c_sql = "SELECT * FROM Person WHERE lname = %s ALLOW FILTERING"
            param = [lname]
        elif (lname == ""):
            c_sql = "SELECT * FROM Person WHERE fname = %s ALLOW FILTERING"
            param = [fname]
        else:
            c_sql = "SELECT * FROM Person WHERE fname = %s AND lname = %s ALLOW FILTERING"
            param = [fname,lname]
        return self.execute(c_sql,param)

    def removeMovie(self,title):
        c_sql = "DELETE FROM Movie WHERE title = %s IF EXISTS"
        return self.execute(c_sql,[''.join(title)])

    def removePerson(self,fname,lname):
        fname = ''.join(fname)
        lname = ''.join(lname)
        if(fname == ""):
            c_sql = "DELETE FROM Person WHERE lname = %s IF EXISTS"
            param = [lname]
        elif (lname == ""):
            c_sql = "DELETE FROM Person WHERE fname = %s IF EXISTS"
            param = [fname]
        else:
            c_sql = "DELETE FROM Person WHERE fname = %s AND lname = %s IF EXISTS"
            param = [fname,lname]
        return self.execute(c_sql,param)

    def getTable(self, table_name) :
        c_sql = f"SELECT * FROM {table_name}"

        return self.execute(c_sql)


