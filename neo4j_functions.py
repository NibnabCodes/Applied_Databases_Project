# neo4j_functions.py
# Neo4j Database Functions 
# for the Conference Management System storted here.
# Author: Niamh Hogan

from db_connections import get_mysql_connection, get_neo4j_driver

from colours import (print_prompt, print_error, 
                     print_data_row, print_success, print_info)

## Option 4 - VIEW CONNECTED ATTENDEES

def view_connected_attendees():
    while True:
        try:
            attendee_id = print_prompt("Enter Attendee ID : ")
            
            if not attendee_id.isnumeric():
                print_error("Invalid attendee ID")
                continue
            
            attendee_id = int(attendee_id.strip())
            
            # Check MySQL for attendee name
            conn    = get_mysql_connection()
            cursor  = conn.cursor()
            
            cursor.execute(
                "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
                (attendee_id,) 
            )
            attendee = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            # If not in MySQL - not in either DB
            if not attendee:
                print_error("Attendee does not exist")
                return
            
            print_info(f"Attendee Name: {attendee['attendeeName']}")
            print_info("-------------------")
            
            # Check Neo4j for connections
            neo4j_driver = get_neo4j_driver()
            
            with neo4j_driver.session() as session: 
                    result = session.run("""
                    MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(b:Attendee)
                    RETURN b.AttendeeID AS connectedID
                    ORDER BY b.AttendeeID
                """, id=attendee_id)
                
                    connections = [record["connectedID"] for record in result]
                
            neo4j_driver.close()
            
            # Attendee exists in MySQL but no connections in Neo4j
            if not connections:
                print_info("No connections")
                break
                
            # Get names of connected attendees from MySQL
            conn    = get_mysql_connection()
            cursor  = conn.cursor()
                
            print_info("These attendees are connected:")
                
            for connected_id in connections:
                cursor.execute(
                    "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
                    (connected_id,)         
                )
                connected_attendee = cursor.fetchone()
                    
                if connected_attendee:
                    print_data_row(
                        f"{connected_id:<6} | {connected_attendee['attendeeName']}"
                    )
                        
            cursor.close()
            conn.close()
            break
        
        except Exception as e:
            print_error(f"{e}")
            break  
        
## Option 5 - ADD ATTENDEE CONNECTION
    
def add_attendee_connection():
    while True:
        try:
            attendee_id1 = print_prompt("Enter Attendee 1 ID : ")
            attendee_id2 = print_prompt("Enter Attendee 2 ID : ")
                
            # Vaildate both IDs = numeric
            if not attendee_id1.isnumeric() or not attendee_id2.isnumeric():
                print_error("Attendee IDs must be numbers")
                continue
                
            attendee_id1 = int(attendee_id1.strip())
            attendee_id2 = int(attendee_id2.strip())
                
            # Check attendee cannot connect to themselves
            if attendee_id1 == attendee_id2:
                print_error("An attendee cannot connect to him/herself")
                continue 
                    
            # Check both attendees exist in MySQL 
            conn    = get_mysql_connection()
            cursor  = conn.cursor()
                
            cursor.execute(
                "SELECT attendeeID FROM attendee WHERE attendeeID = %s",
                (attendee_id1,)
            )
            attendee1 = cursor.fetchone()

            cursor.execute(
                "SELECT attendeeID FROM attendee WHERE attendeeID = %s",
                (attendee_id2,)
            )
            attendee2 = cursor.fetchone()

            cursor.close()
            conn.close()
                
            # If either attendee doesn't exist in MySQL
            if not attendee1 or not attendee2:
                print_error("One or both attendee IDs do not exist")
                continue
                
            # Check if already connected in Neo4j
            # If either attendee does not exist in neo4j yet
            # they cant be connected - skip straight to creating
            neo4j_driver = get_neo4j_driver()
                
            with neo4j_driver.session() as session:
                result = session.run("""
                    OPTIONAL MATCH (a:Attendee {AttendeeID: $id1})
                    OPTIONAL MATCH (b:Attendee {AttendeeID: $id2})
                    RETURN a, b
                """, id1=attendee_id1, id2=attendee_id2)
                    
                record = result.single()
                node_a = record["a"]
                node_b = record["b"]
                    
            # if either doesnt exist in neo4j - cannot be connected yet
            if node_a is None or node_b is None:
                already_connected = False
            else:
                # Both exist - check connection in either direction
                with neo4j_driver.session() as session:
                    result = session.run("""
                        MATCH (a:Attendee {AttendeeID: $id1})-[r:CONNECTED_TO]-(b:Attendee {AttendeeID: $id2})
                        RETURN a
                    """, id1=attendee_id1, id2=attendee_id2)
                    already_connected = result.single() is not None
                        
            if already_connected:
                print_error("These attendees are already connected")
                neo4j_driver.close()
                continue
                
            # Create relationship
            with neo4j_driver.session() as session:
                session.run("""
                    MERGE (a:Attendee {AttendeeID: $id1})
                    MERGE (b:Attendee {AttendeeID: $id2})
                    MERGE (a)-[:CONNECTED_TO]->(b)
                """, id1=attendee_id1, id2=attendee_id2)
                    
            neo4j_driver.close()
                
            print_success(
                f"Attendee {attendee_id1} is now connected to Attendee {attendee_id2}"
            )
            break
            
        except Exception as e:
            print_error(f"{e}")
            break