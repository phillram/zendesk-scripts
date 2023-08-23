# _______________________________________________________________
# Delete users without emails
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

# _______________________________________________________________
# Getting users existing in Zendesk
# _______________________________________________________________
def retrieve_users():
    get_url = 'https://' + zendesk_subdomain + '.zendesk.com/api/v2/users/search.json?query=email:none'

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

    # Quit if the API returns an error
    if 'error' in response_data:
        print('Zendesk API error: ' + response_data['error'])
        exit()

    # Getting a list of the user IDs
    for i in response_data['users']:
        # Don't add them to the deletion list if they have an external ID or on a Rollbar email
        # if not i['external_id'] and "@rollbar.com" not in i['email']:
        zendesk_user_ids.append(i['id'])

    # First return number of users with no email
    return response_data['count']


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

# Check if there are users with no emails
zendesk_user_count = retrieve_users()
print('Users starting: ' + str(zendesk_user_count))

while zendesk_user_count != 0:
    # Delete users
    print(delete_users())
    
    # Pulling new list of users
    zendesk_user_count = retrieve_users()
    print('Users left: ' + str(zendesk_user_count))
    # time.sleep(2)
