# Innovation Feature - Attendee Recommendation Engine 
# Suggests attendees to connect with based on shared sessions attended 

import pymysql

from db_connections import get_mysql_connection, get_neo4j_driver

from colours import (print_header, print_error, 
                     print_data_row, print_info, print_prompt)

def get_recommendations():
        while True:
            try:
                attendee_id = print_prompt("Enter Attendee ID : ")
            
                if not attendee_id.isnumeric():
                    print_error("Invalid attendee ID: Attendee ID must be a number")
                    continue

                attendee_id = int(attendee_id.strip())
            
                # Check attendee exists in MySQL
                # & get their name for display
                conn    = get_mysql_connection()
                cursor  = conn.cursor()
                
                cursor.execute(
                    "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
                    (attendee_id,)
                )
                attendee = cursor.fetchone()

                # If attendee doesnt exist stop here
                if not attendee:
                    print_error("Attendee does not exist")
                    cursor.close()
                    conn.close()
                    return
                
                # Get all sessions this attendee attended
                # from registration table
                cursor.execute("""
                    SELECT sessionID 
                    FROM registration 
                    WHERE attendeeID = %s
                """, (attendee_id,))
                
                # Store session ids in a list
                session_ids = [row['sessionID'] for row in cursor.fetchall()]
                
                # if attendee hasnt any sessions
                # no basis for recommendations
                if not session_ids:
                    print_info(f"{attendee['attendeeName']} has not attended any sessions.")
                    cursor.close()
                    conn.close()
                    return
                
                # Find other attendees who attended
                # the same sessions
                # IN clause searches multiple sessions at once
                
                # build placeholders for IN clause
                placeholders = ','.join(['%s'] * len(session_ids))
                
                cursor.execute(f"""
                    SELECT DISTINCT a.attendeeID, a.attendeeName, s.sessionTitle
                    FROM registration r
                    JOIN attendee a ON r.attendeeID = a.attendeeID
                    JOIN session s ON r.sessionID = s.sessionID
                    WHERE r.sessionID IN ({placeholders})
                    AND r.attendeeID != %s
                    ORDER BY a.attendeeName
                """, tuple(session_ids) + (attendee_id,)) # session_id converted to tuple for 
                                                          # concatenation with attendee_id tuple
                 
                # Store candidates - people who attend same session
                candidates = cursor.fetchall()
                
                cursor.close() 
                conn.close()
                
                if not candidates:
                    print_info("No other attendees found at the same sessions.")
                    return
                    
                # Get already connected attendees
                # from Neo4j to filter them out
                neo4j_driver = get_neo4j_driver()
                    
                with neo4j_driver.session() as session:
                    result = session.run("""
                        MATCH (a:Attendee {AttendeeID: $attendee_id})-[:CONNECTED_TO]-(b:Attendee)
                        RETURN b.AttendeeID AS connectedID
                    """, attendee_id=attendee_id)
                    
                    # Store already connected IDS in a set for fast lookup
                    already_connected = {record["connectedID"] for record in result}
                    
                neo4j_driver.close()
                
                # FIlter out already connected attendess
                # & display recommendations
                
                # Use dict to avoid showing same person twice
                # (may share multiple sessions)
                recommendations = {}
                for row in candidates:
                    rec_id = row['attendeeID']
                    if rec_id not in already_connected:
                        if rec_id not in recommendations:
                            recommendations[rec_id] = (
                                row['attendeeName'],
                                row['sessionTitle']
                            )
                            
                # Display results
                print()
                print_header(f"Recommendation for {attendee['attendeeName']}")
                print()
                
                if not recommendations:
                    print_info("No new recommendations found")
                    print_info("Already connected to everyone at shared sessions!")
                    return
                    
                print_info("These attendees attended the same sessions but are not yet connected:")
                print()
                
                for rec_id, (rec_name, session_title) in recommendations.items():
                    print_data_row(
                        f"{rec_id:6} | {rec_name:20} | Both attended: {session_title}"
                    )
                return

            except Exception as e:
                print_error(f"Error: {e}")
                    