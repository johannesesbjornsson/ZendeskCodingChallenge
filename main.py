#!/usr/local/bin/python3
import display_output 
import business_logic as model

def main():
  userInput = "None"
  display_output.app_start_up()
  while userInput != "quit":
     display_output.menu_display()
     userInput = input("")
     verifiedUserInput = model.acceptable_answers_menu(userInput)
     if verifiedUserInput == "1":
       userInput = list_all_tickets()
     elif verifiedUserInput == "2":
       view_specific_ticket()
     elif verifiedUserInput == "invalid":
       display_output.invalid_input(userInput)

  display_output.app_exit()


def view_specific_ticket():
  userInput = ""
  while userInput != "back":
    display_output.ticket_search()
    userInput = input()
    verifiedUserInput = model.acceptable_answer_ticket_search(userInput)   # Check if input matches the acceptable answers for this use case
    if verifiedUserInput == "back":
      userInput = verifiedUserInput
    elif verifiedUserInput != "invalid":
      apiResponse = model.get_single_ticket(userInput)   #  Calls the api from the model
      if 'error' in apiResponse:
        display_output.json_error_message(apiResponse)
      else:
        display_output.print_single_ticket(apiResponse)
    else:
      display_output.invalid_input(userInput) 

def list_all_tickets():
  currentPage = 1
  userInput = ""
  apiResponse = ""
  numberOfPages = ""
  apiResponse = {}

  pageHistory = [1,0,0]

  while userInput != "menu" and userInput != "quit":
    if currentPage != pageHistory[1] or 'error' in apiResponse:
       apiResponse = model.get_all_tickets(currentPage)
    if 'error' in apiResponse:
      display_output.json_error_message(apiResponse)
      if pageHistory[1] == 0:
        return "menu"
      currentPage=pageHistory[1]

    else:
      numberOfPages = apiResponse['numberOfPages']
      display_output.print_all_tickets(apiResponse,currentPage,numberOfPages)

    listOptions = model.determine_listing_options(numberOfPages,currentPage)
    verifiedUserInput="invalid"   # Sets standard value to invalid to enter the loop
    while verifiedUserInput == "invalid":
      display_output.list_tickets_options(listOptions)
      userInput=input("")
      verifiedUserInput = model.acceptable_answer_ticket_listing(userInput,listOptions)
      if verifiedUserInput == "invalid":
        display_output.invalid_input(userInput)

    if 'error' in apiResponse:
      currentPage = currentPage
    elif verifiedUserInput == "quit" or verifiedUserInput == "menu":
      userInput = verifiedUserInput
    elif verifiedUserInput == "view":
      view_specific_ticket()
      pageHistory.insert(0,currentPage)   # Sets current page to page history
    else:
      currentPage = model.interpret_input(currentPage,verifiedUserInput,numberOfPages)
      pageHistory.insert(0,currentPage)   # currentPage in this case acutally holds the destination for next iteration (Bad naming maybe, don't judge me)
    pageHistory = pageHistory[:3]   # Cuts the list so it only holds three entries (currentPage and the two previous pages visited)

  return userInput   

main()
