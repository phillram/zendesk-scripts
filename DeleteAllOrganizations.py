# _______________________________________________________________
# Delete every organization in Zendesk
# _______________________________________________________________

# _______________________________________________________________
# Importing requirements 
# _______________________________________________________________
import requests, json, time

# _______________________________________________________________
# Initializing variables
# Place your Zendesk subdomain and authorization here
# _______________________________________________________________
zendesk_subdomain = ''
zendesk_authorization = ''
zendesk_organization_ids = [] # Initializing organization ID array
zendesk_organization_count = 0 # Initializing count of Zendesk organizations

# _______________________________________________________________
# Getting Organizations existing in Zendesk
# _______________________________________________________________
def retrieve_organizations():
    get_url = 'https://' + zendesk_subdomain + '.zendesk.com/api/v2/organizations.json'

    payload = {}
    headers = {
        'Authorization': zendesk_authorization,
    }

    # Empty array from previous loops
    zendesk_organization_ids.clear()

    # API call to get organizations
    response = requests.request("GET", get_url, headers = headers, data = payload)

    # Parse the response to JSON
    response_data = response.json()

    # Getting a list of the organization IDs
    for i in response_data['organizations']:
        zendesk_organization_ids.append(i['id'])

    # print('There are ' + str(response_data['count']) + ' organizations')
    return response_data['count']

    # print('Zendesk organization IDs: ' + str(zendesk_organization_ids))

# _______________________________________________________________
# Deleting organizations found above
# _______________________________________________________________
def delete_organizations():
    # print('Starting deletion')

    delete_url = 'https://' + zendesk_subdomain + '.zendesk.com/api/v2/organizations/destroy_many?ids='

    payload = {}
    headers = {
        'Authorization': zendesk_authorization,
    }

    # Convert the array of organizations into a comma delimited string
    organizations_list = ''
    for i in zendesk_organization_ids:    
        organizations_list += str(i) + ','

    response = requests.request("DELETE", delete_url + str(organizations_list), headers=headers, data=payload)

    return(response.text)


# _______________________________________________________________
# Running the functions above   
# Find how many organizations exist, pull organization IDs
# then performing the deletions
# _______________________________________________________________

# Check if there are organizations
zendesk_organization_count = retrieve_organizations()
print('Organizations starting: ' + str(zendesk_organization_count))

while zendesk_organization_count != 0:
    print(delete_organizations())
    zendesk_organization_count = retrieve_organizations()
    print('Organizations left: ' + str(zendesk_organization_count))
    time.sleep(2)