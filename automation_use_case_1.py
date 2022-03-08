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

    conn.request("GET", "/incidents?date_range=all&user_ids%5B%5D=PU0UXLG&urgencies%5B%5D=high&statuses%5B%5D=acknowledged&include%5B%5D=users", headers=headers)


    res = conn.getresponse()
    data = res.read()

    # changing the response into a dictionary
    data_dict = loads(data.decode("utf-8"))

    #getting the title of first incident in the response
    incidents = data_dict["incidents"]

    return(incidents)

#-------------------------------------------- function get_incident_data FINISHED --------------------------------------------------------



#-------------------------------------------- function resolve_incident STARTED --------------------------------------------------------

def resolve_incident(incident_id):
    """ this function will mark the incident resolved"""
	
    import http.client

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
    update_resolution_note(incident_id)
    
    print(data.decode("utf-8"))
	



#-------------------------------------------- function resolve_incident FINISHED --------------------------------------------------------




#-------------------------------------------- function update_resolution_note STARTED --------------------------------------------------------
def update_resolution_note(incident_id):
    """this function will update the resolution notes on the incident"""
    import http.client

    conn = http.client.HTTPSConnection("api.pagerduty.com")

    payload = "{\n  \"note\": {\n    \"content\": \"automated resolution: USER BOT\"\n  }\n}"

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





# ssh banner
banner = """<ssh banner>"""



# regex to copy the hostname 
regex = re.compile('(.+).prod.ultradns.net-rdns-high-servfail-percentage')

for incident in get_incident_data():
    if "-rdns-high-servfail-percentage" in incident['title']:
        hostname = regex.search(incident['title']).group(1)
       
        # storing incident id
        incident_id = incident["id"]
        print(incident_id)

        # getting alert id related to the incident
        #alert_id = get_alert_id(incident_id)
        #print(alert_id)   

        # getting the resolver location for which issue occured
        resolver_location = (hostname.split('.'))[1]
        print(resolver_location)

        #command to run rtar script on chulhprjump3.ultra.neustar.com jumphost
        command = "command"
        rtar_output = popen(command).read()
        rtar_output = rtar_output.replace(banner, '')

        #drop percentages in integers
        drop_prct_int_list = []
        #logic to store the output from rtar_queries
        with open("rtar_output.txt", "w") as file:
            data = file.writelines(rtar_output)

        #logic to get the drop percent from the rtar script output
        with open("rtar_output.txt", "r") as file:
            lines = file.readlines()
            lines.remove(lines[0])                     #to remove all the headings from the output
            lines.remove(lines[0])                     # to remove additional line from the output
            lines.remove(lines[-1])                    # to remove the blank lines from output
            lines.remove(lines[-1])                    # to remove the blank lines from output
            
            # logic to remove all extra spaces from the drop percent values
            for line in lines:
                #it converts '   6.9892 | ' to 6
                line = (((line[48:-47]).replace('|', '')).strip()).split('.')
                line = int(line[0])
                drop_prct_int_list.append(line)

            # counter for exceeded threshold 
            counter = 0

            # comparing drop percentage values with acceptable threshold
            for value in drop_prct_int_list:
                if value > 20 :
                    counter += 1 
            
            # logic to check if all values are below 20
            if counter == 0 :
               resolve_incident(incident_id)
               popen("mail -s '" + incident['title'] + " - " + incident_id + "' chetan.thakre@impetus.com <<< \"" + rtar_output + "\n incident resolved automatically \"")
            else :
               popen("mail -s '" + incident['title'] + "' chetan.thakre@impetus.com <<< \"" + rtar_output + "\"")   

# mail command 
#popen("mail -s '" + incident['title'] + "' chetan.thakre@impetus.com <<< \"" + str(drop_prct_int_list) + "\"")

