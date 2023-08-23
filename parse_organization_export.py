# _______________________________________________________________
# Parse the Zendesk organizations export report and create a CSV
# _______________________________________________________________

# _______________________________________________________________
# Importing requirements
# _______________________________________________________________
import json, re, numpy, pandas

# _______________________________________________________________
# Set filenames of input and output file
# Input is expected to be JSON and output is expected to be CSV
# _______________________________________________________________
input_file = 'zendesk_orgs'
output_file = 'organizations'

# _______________________________________________________________
# Read the Zendesk export file
# _______________________________________________________________
with open( input_file + '.json') as organization_file:
    contents = organization_file.read()

# _______________________________________________________________
# Parsing the file and putting the values into arrays
# _______________________________________________________________
id = re.findall('","id":(.+?),"name"', contents)
name = re.findall('"name":"(.+?)","shared_tickets"', contents)
domains = re.findall('"domain_names":(.+?),"details"', contents)

# _______________________________________________________________
# # Provide some feedback to the user
# _______________________________________________________________
print('IDs found: ' + str(len(id)))
print('Names found: ' + str(len(name)))
print('Domains found: ' + str(len(domains)))

# _______________________________________________________________
# Export to CSV
# _______________________________________________________________
df = pandas.DataFrame({
    'id' : id,
    'name': name,
    'domains': domains,
})
df.to_csv(output_file + '.csv', index=False)

