import requests

# The URL of a specific user profile (User ID #1) inside a mock database
api_url = "https://jsonplaceholder.typicode.com/users/1"

# Fire the GET request
response = requests.get(api_url)

# Inspect what the server sent back
print(f"Server Status Code: {response.status_code}") 
print(f"Content-Type Header sent by server: {response.headers.get('Content-Type')}")
print("---" * 10)

# The requests library has a built-in JSON parser!
# It instantly converts the text payload into a native Python Dictionary.
if response.status_code == 200:
    user_data = response.json()
    
    # Now we can extract information using standard Python keys!
    name = user_data["name"]
    email = user_data["email"]
    city = user_data["address"]["city"]
    
    print(f"Successfully extracted data from the payload:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Location: {city}")