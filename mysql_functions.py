
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
        
## Option 2 - VIEW ATTENDEES BY COMPANY

def view_attendees_by_company():
    try:
        # Keep asking until valid numeric ID > 0 is entered
        while True:
            company_id = print_prompt("Enter Company ID : ")
            
            # Check input is numberic
            try:
                company_id = int(company_id)
                if company_id <= 0:
                    print_error("Company ID must be greater than 0!")
                    continue
                break
            except ValueError:
                print_error("Company ID must be a number!")
                continue
        
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        # Check if company exists
        cursor.execute("SELECT * FROM company WHERE companyID = %s", (company_id,))
        company = cursor.fetchone()  
        
        if not company:
            print_error(f"Company with ID {company_id} doesn't exist!")
            cursor.close()
            conn.close()
            return
            
        # Company exists - show company name
        print_info(f"{company['companyName']} Attendees")
        
        # JOIN tables 
        query = """
            SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle,
                s.speakerName, s.sessionDate, r.roomName
            FROM attendee a
            JOIN registration reg ON a.attendeeID = reg.attendeeID
            JOIN session s ON reg.sessionID = s.sessionID
            JOIN room r ON s.roomID = r.roomID
            WHERE a.attendeeCompanyID = %s
            ORDER BY a.attendeeName
        """
        
        cursor.execute(query, (company_id,))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Check if any attendees found for this company
        if not results:
            print_info(f"No attendees found for {company['companyName']}")
            return
        
        # Display results
        for row in results:
            print_data_row(
                f"{row['attendeeName']:<20} | "
                f"{str(row['attendeeDOB']):<12} | " 
                f"{row['sessionTitle']:<35} | "  
                f"{row['speakerName']:<20} | "
                f"{str(row['sessionDate']):<12} | " 
                f"{row['roomName']}" 
            )
            
    except pymysql.Error as e:
        print_error(f"{e}")   
        
## Option 3 - ADD NEW ATTENDEE

def add_new_attendee():
    try:
        print_header("Add New Attendee")
        print()
        
        attendee_id     = print_prompt("Attendee ID : ")
        attendee_name   = print_prompt("Name : ") 
        attendee_dob    = print_prompt("DOB : ")
        attendee_gender = print_prompt("Gender : ")
        company_id      = print_prompt("Company ID : ")
        
        # Check if Gender Male/Female
        if attendee_gender not in ("Male", "Female"):
            print_error("Gender must be Male/Female")
            return 
        
        conn   = get_mysql_connection()
        cursor = conn.cursor()
        
        # Check attendee ID does not already exist
        cursor.execute("SELECT * FROM attendee WHERE attendeeID = %s", (attendee_id,))
        if cursor.fetchone():
            print_error(f"Attendee ID: {attendee_id} already exists")
            cursor.close()
            conn.close()
            return
        
        # Check company ID exists
        cursor.execute("SELECT * FROM company WHERE companyID = %s", (company_id,))
        if not cursor.fetchone():
            print_error(f"Company ID: {company_id} does not exist")
            cursor.close()
            conn.close()
            return
        
        # Insert new attendee into DB
        query = """
            INSERT INTO attendee 
            (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
            VALUES (%s, %s, %s, %s, %s) 
        """
        cursor.execute(query, (attendee_id, attendee_name,
                               attendee_dob, attendee_gender, company_id))
        conn.commit()

        cursor.close()
        conn.close()
        
        print_success("Atendee successfully added")
        
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
            