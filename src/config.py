import os

class Config(object) :
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-secret-key'
    DEBUG   = True
    TESTING = True

    CASSANDRA_KEYSPACE = "cqlengine"
    CASSANDRA_HOSTS    = ["cassandra-1"]
    TEST_VAR = os.environ.get("TEST_VAR").split(",")


