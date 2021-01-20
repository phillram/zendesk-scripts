# _______________________________________________________________
# Delete users without any requested, assigned, or CC'd tickets
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
zendesk_user_ids = [] # Initializing user ID array
zendek_nonticket_users = [] # Initializing user ID array for those with no tickets
zendesk_user_count = 0 # Initializing count of Zendesk users
api_new_page = True # Initializing if there is a new page of data from API
api_page_counter = 0 # Initializing page of API calls

# _______________________________________________________________
# Getting users existing in Zendesk
# _______________________________________________________________
def retrieve_users():
    get_url = 'https://' + zendesk_subdomain + '.zendesk.com/api/v2/users.json?page=' + str(api_page_counter)

    payload = {}
    headers = {
        'Authorization': zendesk_authorization,
    }

    # Empty array from previous loops
    zendesk_user_ids.clear()

    # API call to get users
    response = requests.request("GET", get_url, headers = headers, data = payload)

    # Parse the response to JSON
    response_data = response.json()

    # Getting a list of the user IDs
    for i in response_data['users']:
        # Don't add them to the deletion list if they have an external ID or on a Rollbar email
        if not i['external_id'] and "@rollbar.com" not in i['email']:
            zendesk_user_ids.append(i['id'])

    # First return is the number of total responses, the second is the page number for the following data
    return len(zendesk_user_ids), response_data['next_page'] 

# _______________________________________________________________
# Getting tickets associated with the user IDs
# _______________________________________________________________
def retrieve_user_tickets():

    zendek_nonticket_users.clear() # Restart the array for this run

    payload = {}
    headers = {
        'Authorization': zendesk_authorization,
    }


    for i in zendesk_user_ids: # IDs of users
        get_url = 'https://' + zendesk_subdomain + '.zendesk.com/api/v2/users/' + str(i) + '/related'
        # API call to get users
        response = requests.request("GET", get_url, headers = headers, data = payload)

        # Parse the response to JSON
        response_data = response.json()

        # Searching feedback records for people with tickets associated
        for count, value in enumerate(response_data['user_related'].values(), 1): 
            if value != 0: # If there's a non-zero, then don't mark this user as having no tickets
                break
            elif count == len(response_data['user_related']): # Add user ID to array if they have no tickets associated
                zendek_nonticket_users.append(i)

    return zendek_nonticket_users


# _______________________________________________________________
# Deleting users found above
# _______________________________________________________________
def delete_users():
    # print('Starting deletion')

    delete_url = 'https://' + zendesk_subdomain + '.zendesk.com/api/v2/users/destroy_many?ids='

    payload = {}
    headers = {
        'Authorization': zendesk_authorization,
    }

    # Convert the array of users into a comma delimited string
    users_list = ''
    for i in zendesk_user_ids:    
        users_list += str(i) + ','

    response = requests.request("DELETE", delete_url + str(users_list), headers=headers, data=payload)

    return(response.text)


# _______________________________________________________________
# Running the functions above   
# Find how many users exist, pull user IDs
# then performing the deletions
# _______________________________________________________________

while api_new_page:
    api_page_counter += 1
    api_new_page = False
    
    # Pulling the list of users
    retrieved_user_information = retrieve_users()
    api_new_page = retrieved_user_information[1]
    print('Retrieved user information on API page: ' + str(api_page_counter) + '. Number of found users: ' + str(retrieved_user_information[0]))
    
    # Fetching associated tickets with the users
    retrieve_user_tickets()
    print('Users with no associated tickets:' + str(zendek_nonticket_users))

    # Delete users that don't have any associated tickets
    print(delete_users())

