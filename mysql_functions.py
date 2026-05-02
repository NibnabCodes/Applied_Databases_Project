
import pymysql

from db_connections import get_mysql_connection

from colours import (print_header, print_error, 
                     print_data_row, print_prompt, print_success, print_info) 

## OPTION 6 - VIEW ROOMS

# Cache variable - rooms are loaded once & stored here
rooms_cache = None

def view_rooms():
    global rooms_cache
    
    try:
        # only query DB if rooms haven't been loaded ye
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
            