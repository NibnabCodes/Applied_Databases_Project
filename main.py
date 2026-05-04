# main.py
# Conference Management System
# Applied Databases Final Project
# Main file - displays menu and calls functions from other files
 
 
from mysql_functions import view_attendees_by_company, view_rooms, view_speakers, view_attendees_by_company, add_new_attendee 
from neo4j_functions import view_connected_attendees #, add_attendee_connection
# from recommendations import get_recommendations
 
from colours import (print_header, print_menu_item,
                     print_prompt, print_info) 
  
 
# MAIN MENU DISPLAY
 
def show_main_menu():
    print()
    print_header("Conference Management")
    print()
    print_info("MENU")
    print_info("====")
    print_menu_item("1 - View Speakers & Sessions")
    print_menu_item("2 - View Attendees by Company")
    print_menu_item("3 - Add New Attendee")
    print_menu_item("4 - View Connected Attendees")
    print_menu_item("5 - Add Attendee Connection")
    print_menu_item("6 - View Rooms")
    print_menu_item("7 - Get Recommendations")
    print_menu_item("x - Exit application")
    print()
    return print_prompt("Choice: ")
 
 
# MAIN LOOP
 
def main():
    while True:
        choice = show_main_menu()
 
        if choice == "1":
            view_speakers()
 
        elif choice == "2":
            view_attendees_by_company()
 
        elif choice == "3":
            add_new_attendee() 
 
        elif choice == "4":
            view_connected_attendees()
 
        elif choice == "5":
            # add_attendee_connection()
            print_info("Coming soon - Add Attendee Connection")
 
        elif choice == "6":
            view_rooms()
 
        elif choice == "7":
            # get_recommendations()
            print_info("Coming soon - Get Recommendations")
 
        elif choice == "x":
            print_info("Goodbye! :)")
            break
 
        else:
            # spec says show menu again for anything else
            # the while loop handles this automatically
            pass
 
if __name__ == "__main__":
    main()