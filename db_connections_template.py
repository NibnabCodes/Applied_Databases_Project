# db_connections_template.py
# RENAME THIS FILE TO db_connections.py BEFORE RUNNING
# Then update the passwords below to match your setup
 
import pymysql
from neo4j import GraphDatabase
 
# PASSWORDS
 
MYSQL_PASSWORD = "ENTER_YOUR_MYSQL_PASSWORD_HERE"   
NEO4J_PASSWORD = "ENTER_YOUR_NEO4J_PASSWORD_HERE"   
 
# MYSQL CONNECTION
 
def get_mysql_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password=MYSQL_PASSWORD,
        database="appdbproj",
        cursorclass=pymysql.cursors.DictCursor
    )
 

# NEO4J CONNECTION

driver = None
 
def get_neo4j_driver():
    global driver
    url = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(
        url,
        auth=("neo4j", NEO4J_PASSWORD),
        max_connection_lifetime=1000
    )
    return driver