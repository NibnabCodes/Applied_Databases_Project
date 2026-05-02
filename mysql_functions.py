
import pymysql

from db_connections import get_mysql_connection

from colours import (print_header, print_error, 
                     print_data_row, print_prompt, print_success, print_info) 


## Option 1 - VIEW SPEAKERS & SESSIONS

def view_speakers():
    try:
        search_name = print_prompt("Enter speaker name : ")
        
        print()
        print_header(f"Session Details For : {search_name}")
        
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        # JOIN session & room tables to get room name
        query = """
            SELECT s.speakerName, s.sessionTitle, r.roomName
            FROM session s
            JOIN room r ON s.roomID = r.roomID
            WHERE s.speakerName LIKE %s
            ORDER BY s.speakerName
        """
        
        cursor.execute(query, (f"%{search_name}%",))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Check if speakers found
        if not results:
            print_info("No speakers found of that name")
            return
        
        # DIsplay results
        for row in results:
            print_data_row(f"{row['speakerName']:<20} | {row['sessionTitle']:<35} | {row['roomName']}")

    except pymysql.Error as e:
        print_error(f"{e}")
        

## Option 6 - VIEW ROOMS

def view_rooms():
    global rooms_cache
    
    try:
        # only query DB if rooms haven't been loaded yet
        if rooms_cache is None:
            conn = get_mysql_connection()
            cursor = conn.cursor() 
            
            # SELECT all room ordered by roomID
            cursor.execute("SELECT * FROM room ORDER BY roomID")
            
            # Store results in cache so we never query this session again
            rooms_cache = cursor.fetchall()
            
            cursor.close()
            conn.close()
        
        # Print header row
        print_data_row(f"{'roomID':<10} | {'roomName':<20} | {'Capacity'}") # Padding formattera
        print_data_row("-" * 45)                                            # Divider line
        
        # Print each room
        for room in rooms_cache:
            print_data_row(f"{room['roomID']:<10} | {room['roomName']:<20} | {room['capacity']}")
        print()
        print_prompt("Press Enter to return to main menu...")
        
        
    except pymysql.Error as e:
        print_error(f"{e}")
            