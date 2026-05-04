
import pymysql 

from db_connections import get_mysql_connection, get_neo4j_driver

from colours import (print_header, print_prompt, print_error, 
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
            driver = get_neo4j_driver()
            
            with driver.session() as session:
                    result = session.run("""
                    MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(b:Attendee)
                    RETURN b.AttendeeID AS connectedID
                    ORDER BY b.AttendeeID
                """, id=attendee_id)
                
                    connections = [record["connectedID"] for record in result]
                
            driver.close()
            
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
            