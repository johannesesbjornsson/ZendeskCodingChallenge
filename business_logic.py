#!/usr/local/bin/python3
import json
import subprocess
import os
import error_handler
import datetime

def get_all_tickets(pageToGet):
  apiResponse = call_api(["getAllTickets", str(pageToGet)])

  if 'error' not in apiResponse:
    pageCountToRound = (apiResponse['count'] / 25) + 0.5   # Adding 0.5 so round() function will always round up. Not importing math module for single use
    numberOfPages = int(round(pageCountToRound))
    apiResponse['numberOfPages'] = numberOfPages   # Adds to total number of pages to the dict

  return apiResponse

def get_single_ticket(ticketId):
  apiResponse = call_api(["getTicket", ticketId])
  
  if 'error' not in apiResponse:
    for key in ['created_at','updated_at']:   # Loops through the values of the dict to change
      dateRaw = apiResponse['ticket'][key]   # Gets the date as returned from the API
      dateObj = datetime.datetime.strptime(dateRaw,'%Y-%m-%dT%I:%M:%SZ')   # creates a datetime object
      date = dateObj.strftime('%d %B %Y %I:%M')   # Formats the date object to be nice and readable
      apiResponse['ticket'][key] = date   # Replaces old date with new nicley formatted date

  return apiResponse

def call_api(commandToRun):
  commandToRun.insert(0,"./accessAPIs.sh")   # Specifiying accessAPIs.sh and the arugments to pass
  try:
    devNull = open(os.devnull, 'w')
    output = subprocess.check_output(commandToRun,shell=False,stderr=devNull)   # Running accessAPIs.sh and capturing outputin in the output variable and redirects standard error to devnull. If an error occured only an exitcode will be capuered
    apiJson = json_converter(output)
    
    if 'error' in apiJson:
      errorMessage = error_handler.error_in_request(apiJson)
      return errorMessage
    else:
      return apiJson
  except subprocess.CalledProcessError as e:   # If accessAPIs.sh ran unsuccessfully
    error = e.output.decode('utf-8')   
    error = error.strip()
    errorMessage = error_handler.handle_bash_errors(error)
    return errorMessage

def json_converter(apiResponseRaw):
  try:
    json_object = json.loads(apiResponseRaw)
    return json_object
  except ValueError as e:
    json_object = json.loads("{\"error\":\"API error: response couldn't be converted to json format\"}")
   #return "{\"error\":\"API error: response couldn't be converted to json format\"}"
    return json_object

def determine_listing_options(numberOfPages, currentPage):
  if numberOfPages == 1:
    listOption = "only"
  elif numberOfPages > 1 and currentPage == 1:
    listOption= "first"
  elif (currentPage) == numberOfPages:
    listOption = "last"
  else:
    listOption = "middle"
  return listOption

def acceptable_answers_menu(userInput):
  acceptableAnswers=["1","2","quit"]
  if userInput in acceptableAnswers:
    return userInput
  else:
    return "invalid"

def acceptable_answer_ticket_listing(userInput, useCase):
  if useCase == "first":
     acceptableAnswers=["next","quit","menu","last","view"]
  elif useCase == "middle":
     acceptableAnswers=["next","prev","quit","menu","first","last","view"]
  elif useCase == "only":
    acceptableAnswers=["quit","menu","view"]
  elif useCase == "last":
    acceptableAnswers=["prev","quit","menu","first","view"]

  if userInput in acceptableAnswers:
    return userInput
  else:
    return "invalid"

def acceptable_answer_ticket_search(userInput):
  if userInput == "back":
    return userInput
  elif userInput.isdigit() == True:
    return userInput
  else:
    return "invalid"

def interpret_input(currentPage,userInput,numberOfPages): 
  if userInput == "next":
    currentPage += 1
  elif userInput == "prev":
    currentPage -= 1
  elif userInput == "last":
    currentPage = numberOfPages
  elif userInput == "first":
    currentPage = 1
  elif userInput == "quit":
   return "quit"
  elif userInput == "view":
    view_specific_ticket()
  else:
    return "menu"
  return currentPage

