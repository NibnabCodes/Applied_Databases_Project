
[![Typing SVG](https://readme-typing-svg.demolab.com?font=Playfair+Display&size=25&pause=1000&color=B113F7&width=435&lines=Conference+Management+System)](https://git.io/typing-svg)

---

## Project Description 

This repository contains my final project for the Applied Databases module at Atlantic Technological University - Galway, 2026.

The project contains a Python command-line application that manages conference data using two databases:
- **MySQL** - stores attendees, sessions, companies, rooms & registrations
- **Neo4j** - stores CONNECTED_TO relationships between attendees

The application provides a menu-driver interface allowing users to:
- View speakers & their sessions
- View attendees by company
- Add new attendees
- View & create connections between attendees
- View conference rooms
- Get attendee recpmmendations based on shared sessions attended

--- 

## Project Structure

```
G00473038/  
├── main.py                      - run this to start application  
├── colours.py                   - innovation: colorama colour helper functions  
├── mysql_functions.py           - all MySQL query functions  
├── neo4j_functions.py           - all Neo4j query functions  
├── recommendations.py           - innovation: recommendtion engine  
├── db_connections_template.py   - rename this to db_connections.py  
├── requirements.txt             - all required Python packages  
├── appdbproj.sql                - MySQL database file  
├── appdbprojNeo4j.json          - Neo4j database file  
├── GitLink.txt                  - link to GitHub repository  
├── innovation.pdf               - innovation document  
└── README.md  
```

---

## Setup Instructions

### Step 1 - Install required packages

**Option A - Automatic**  

All required packages will be auto installed when main.py is run.  

**Option B - Using requirements.txt**

```
pip install -r requirements.txt
```

---

### Step 2 - Set Up MySQL Database  

Import the SQL file into MySQL Workbench:  
- Go to Server - Data Import  
- Select Import from Self-Contained File  
- Browse to appdbproj.sql  
- Set target Schema to appdbproj  
- Click Start Import  

Or using the terminal:  
```
mysql -u root -p < appdbproj.sql  
```

Verify it worked:  
```sql
USE appdbproj;
SHOW TABLES;  
```

You should see following tables:  
```  
attendee  
company  
registration  
room  
session  
```  

### Step 3 - Set Up Neo4j Database  

- Open Neo4j Browser at http://localhost:7474  
- Log in with your Neo4j credentials  
- RUn the commands from appbdprojNeo4j.json in the broswer  

Verify it worked:  
```cypher  
MATCH (n) RETURN n LIMIT 25  
```  

You should see attendee nodes with CONNECTED_TO relationships between them.  

---  

### Step 4 - Configure Database Connections  

- Rename db_connections_template.py to db_connections.py  
- Open db_connections.py  
- Update MySql & Neo4j passwords  

Test both connections:  
```  
python db_connections.py  
```

---  

### Step 5 - Run Application  

```  
python main.py  
```

---  
