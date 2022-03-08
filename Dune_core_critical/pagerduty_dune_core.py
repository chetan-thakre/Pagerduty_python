import http.client
import json
import re
from os import popen


#-------------------------------------------- function get_alert_id STARTED --------------------------------------------------------




#get_alert_id function
def get_alert_id(incident_id):
    """ this functions fetchs the alert id for the incident id provided """

    import http.client
    from json import loads
    conn = http.client.HTTPSConnection("api.pagerduty.com")

    headers = {
               'Content-Type': "application/json",
               'Accept': "application/vnd.pagerduty+json;version=2",
               'Authorization': "Token token="
    }

    #api request to get the alert
    request = "/incidents/" + incident_id + "/alerts?statuses%5B%5D=triggered&sort_by=created_at&include%5B%5D=services"
    conn.request("GET", request, headers=headers)
    res = conn.getresponse()
    data = res.read()
    alerts_dict = loads(data.decode("utf-8"))
    # first alert id
    alert_id = alerts_dict['alerts'][0]['id']

    return alert_id

#-------------------------------------------- function get_alert_id FINISHED --------------------------------------------------------



#-------------------------------------------- function get_incident_data STARTED --------------------------------------------------------

def get_incident_data():
    """ this function will retrive all acknowledged incident data from pagerduty"""
    import http.client
    from json import loads

    # api authentication and GET request for acknowledged incidents list
    conn = http.client.HTTPSConnection("api.pagerduty.com")

    headers = {
              'Content-Type': "application/json",
              'Accept': "application/vnd.pagerduty+json;version=2",
              'Authorization': "Token token="
    }

    conn.request("GET", "/incidents?date_range=all&user_ids%5B%5D=PQR6X9T&urgencies%5B%5D=high&statuses%5B%5D=acknowledged&include%5B%5D=users", headers=headers)


    res = conn.getresponse()
    data = res.read()

    # changing the response into a dictionary
    data_dict = loads(data.decode("utf-8"))

    #getting the title of first incident in the response
    incidents = data_dict["incidents"]
    return(incidents)

#-------------------------------------------- function get_incident_data FINISHED --------------------------------------------------------



#-------------------------------------------- function resolve_incident STARTED --------------------------------------------------------

def resolve_incident(incident_id, resolution_note):
    """ this function will mark the incident resolved"""
	
    import http.client
    from os import popen

    conn = http.client.HTTPSConnection("api.pagerduty.com")

    payload = "{\n  \"incident\": {\n    \"type\": \"incident_reference\",\n    \"status\": \"resolved\",\n    \"resolution\": \"resolved with the help of automated script (Author: Chetan Thakre)\"\n  }\n}"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/vnd.pagerduty+json;version=2",
        'From': "email",
        'Authorization': "Token token="
    }
    
    request = "/incidents/" + incident_id

    conn.request("PUT", request, payload, headers)

    res = conn.getresponse()
    data = res.read()
    print(resolution_note)
    update_resolution_note(incident_id, resolution_note)

    popen("mail -s '" + incident['title'] + "' chetan.thakre@impetus.com <<< \"" + resolution_note + "\n incident resolved automatically \"")
    print(data.decode("utf-8"))
	



#-------------------------------------------- function resolve_incident FINISHED --------------------------------------------------------


#-------------------------------------------- function update_resolution_note STARTED --------------------------------------------------------
def update_resolution_note(incident_id, resolution_note):
    """this function will update the resolution notes on the incident"""
    import http.client

    conn = http.client.HTTPSConnection("api.pagerduty.com")

    payload = "{\n  \"note\": {\n    \"content\":\"" + resolution_note + "\n\n automated resolution: USER CHETAN THAKRE\"\n  }\n}"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/vnd.pagerduty+json;version=2",
        'From': "email",
        'Authorization': "Token token="
    }
    url = "/incidents/"+ incident_id + "/notes"
    conn.request("POST", url , payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


#-------------------------------------------- function update_resolution_note FINISHED --------------------------------------------------------




# regex to copy the hostname 
regex = re.compile('(.+)/Dune Server created a core file is CRITICAL ')


for incident in get_incident_data():
    
    incident_title = (incident['title']) #.split())[1]
    if "/Dune Server created a core file is CRITICAL **" in incident_title:
        hostname = regex.search(incident_title).group(1)
        hostname_split = hostname.split('.')

        # storing incident id
        incident_id = incident["id"]
        print(incident_id)
        
        word_split = hostname_split[0].split(':')
        host_id = word_split[1]
        location = hostname_split[1]
        # getting the resolver location for which issue occured
        resolver_location = host_id + '.' + location
        print(resolver_location)
       
        #command to run purgearch script 
        command = "sh <scriptlocation>.sh " + resolver_location
        print(command)
        script_output = popen(command).read()
    
        print(script_output)
          
        resolve_incident(incident_id, script_output)


            # logic to check if all values are below 20
        #    if counter == 0 :
        #       resolve_incident(incident_id)
        #       popen("mail -s '" + incident['title'] + "' chetan.thakre@impetus.com <<< \"" + rtar_output + "\n incident resolved automatically \"")
        #    else :
        #       popen("mail -s '" + incident['title'] + "' chetan.thakre@impetus.com <<< \"" + rtar_output + "\"")   

# mail command 
#popen("mail -s '" + incident['title'] + "' chetan.thakre@impetus.com <<< \"" + str(drop_prct_int_list) + "\"")

