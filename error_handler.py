#!/usr/local/bin/python3
import json

def handle_bash_errors(errorMessage):
  if errorMessage == "6":   # Exit code of curl command from accessAPIs.sh if Curl couldn't connect to API
    errorMessage = json.loads("{\"error\":\"API error: Couldn't connect to host, check you internet connection\"}")
    return errorMessage
  else:
    errorMessage = json.loads("{\"error\":\"Unknown error in accessAPIs.sh: get someone super qualified to investigate\"}")
    return errorMessage

def error_in_request(apiResponse):
  jsonObject = apiResponse
  if 'error' in jsonObject:   # Check if the key error is defined in the dict
    if 'message' in jsonObject['error']:   # Checks if error is defined in API respons
      updatedJsonObject = json.loads("{\"error\": \""+jsonObject['error']['message']+"\"}")
      return updatedJsonObject
    else:
      return apiResponse
  else:
    return jsonObject








