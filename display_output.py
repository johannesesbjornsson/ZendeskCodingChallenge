#!/usr/local/bin/python3

def menu_display():
  print("""    
    press 1 to list all tickets
    press 2 to to view specfic ticket
    type 'quit' to exit application""")

def app_start_up():
  print("""
    Welcome to Johannes's ticket viewer""")

def app_exit():
  print("""    
    Exiting application. You have a lovley, lovley day
  """)

def ticket_search():
  print("""     
    enter ticket id of the ticket you like to view (must be integers[0-9]) or type 'back' to go back
  """)

def invalid_input(userInput):
  print ("\n '",userInput,"' is not a valid option")

def list_tickets_options(case):
  if case == "first":
    print(""" 
      type 'next' to go to next page
      type 'last' to go to last page
      type 'view' to view more information about a ticket
      type 'menu' to go to main menu
      type 'quit' to exit application
      """)
  elif case == "only":
    print("""  
      type 'view' to view more information about a ticket
      type 'menu' to go to main menu
      type 'quit' to exit application
      """)
  elif case == "middle":
    print("""
      type 'next' to go to next page and 'prev' to go to previous page
      type 'first' to go to first page or 'last' to go to last page
      type 'view' to view more information about a ticket
      type 'menu' to go to main menu
      type 'quit' to exit application
      """)
  elif case == "last":
    print("""
      type 'prev' to go to previous page
      type 'first' to go to first page
      type 'view' to view more information about a ticket
      type 'menu' to go to main menu
      type 'quit' to exit application
      """) 

def print_all_tickets(apiResponse,page,numberOfPages):
  print(" ")   # Print a new line to make output too squishy
  tickets = apiResponse['tickets']   # Exctracts the tickets as a list from the json string returned from API
  newLine = '|{:^7}|{:^15}|{:<50}|'.format("ID","requester ID","Subject")   # Format column titles
  print (newLine)
  newLine = '|{:-^7}|{:-^15}|{:-<50}|'.format("-","-","-")   # Prints a nice divider between column titles and ticket information
  print (newLine)
  for ticket in tickets:
    id = ticket['id']
    req = ticket['requester_id']
    subj = ticket['subject']
    if len(subj) > 47:
      subj = subj[:47]+"..."   # Cuts String at 47 characters and adds dots to not break print alignment if string if string is to long
    newLine = '|{:^7}|{:^15}|{:<50}|'.format(id,req,subj)   # Prints the ticket information
    print (newLine)
  print ("Page",(page),"of",numberOfPages,"page(s)")   # Prints current page and number of pages below table

def print_single_ticket(apiResponse):
  print(" ")   # Print a new line to make output too squishy
  ticketInfo = apiResponse['ticket']   # Exctracts the tickets as a dict from the json string returned from AP
  print('{:<20}{:<50}'.format("Ticket ID:",ticketInfo['id']))
  print('{:<20}{:<50}'.format("Subject:",ticketInfo['subject']))
  print('{:<20}{:<50}'.format("Submitter:",ticketInfo['submitter_id']))
  print('{:<20}{:<50}'.format("Description:",ticketInfo['description']))
  print('{:<20}{:<50}'.format("Date raised:",ticketInfo['created_at']))
  print('{:<20}{:<50}'.format("Last updated:",ticketInfo['updated_at']))


def json_error_message(apiResponse):
  jsonObject = apiResponse
  print ("\n", jsonObject['error'])

