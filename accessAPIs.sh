#!/bin/bash
main(){
  password="hejhej"
  userName="johannes.esbjornsson@gmail.com"
  command=$1
  if [ "$command" == "getAllTickets" ] 
  then
    page=$2
    getAllTickets $page
  elif [ "$command" == "getTicket" ]
  then
    ticketId=$2
    getTicket $ticketId
  fi
 
}
getTicket(){
  ticketId=$1
  output=$(curl "https://johannese.zendesk.com/api/v2/tickets/$ticketId.json" -u $userName:$password)
  exitCode=$?   # Gets the returncode from the curl command
  if [ $exitCode -eq 0 ]   # If curl command successful
  then
    echo $output   # Echos the API response
    exit 0
  else
    echo $exitCode   # Echoes the exit code of API command
    exit 1
  fi
}
getAllTickets(){
  page=$1
  output=$(curl "https://johannese.zendesk.com/api/v2/tickets.json?per_page=25&page=$page" -u $userName:$password) 
  exitCode=$?
  if [ $exitCode -eq 0 ]
  then
    echo $output
    exit 0
  else
    echo $exitCode
    exit 1
  fi
}
main "$@"

