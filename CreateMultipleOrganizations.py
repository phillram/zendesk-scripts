# _______________________________________________________________
# Create multiple organizations based on the 'run' parameter
# Will create Pokemon & random string organizations
# _______________________________________________________________

# _______________________________________________________________
# Importing requirements 
# _______________________________________________________________
import requests, json, random, multiprocessing, string

# _______________________________________________________________
# Initializing variables
# Place your Zendesk subdomain and authorization here
# _______________________________________________________________
zendesk_subdomain = ''
zendesk_authorization = ''
run = 10 # How many times to loop

# _______________________________________________________________
# Pull a random Pokemon name to use as the organization names
# _______________________________________________________________
pokemon_names_url = requests.request('GET', 'https://raw.githubusercontent.com/sindresorhus/pokemon/master/data/en.json')
# Parse the response to JSON
pokemon_names = pokemon_names_url.json()

# Create a random string to append to a Pokemon be used as the organization name
random_string = ''
random_name = random.choice(pokemon_names) + random_string.join(random.choice(string.ascii_letters) for i in range(20))

# _______________________________________________________________
# Creating organizations
# _______________________________________________________________
def create_organizations():
    url = 'https://' + zendesk_subdomain + '.zendesk.com/api/v2/organizations.json'
    headers = {
        'Authorization': zendesk_authorization,
        'Content-Type': 'application/json',
    }
    payload = {
        "organization":
            {"name": random_name}
            # {"name": random.choice(pokemon_names)}
    }
    response = requests.request("POST", url, headers = headers, data = json.dumps(payload))
    print(response.text)


if __name__ == '__main__':
    jobs = [] # Array for the jobs
    for i in range(run): # Run the amount of times set above
        jobRun = multiprocessing.Process(target=create_organizations) # Define what function to run multiple times.
        jobs.append(jobRun) # Add to the array.
        jobRun.start() # Start the functions.
        # print('this is the run for: '+ str(i))