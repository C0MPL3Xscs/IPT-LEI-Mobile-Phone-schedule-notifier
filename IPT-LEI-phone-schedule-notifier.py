import requests
import hashlib
import time
import http.client, urllib

# Initialize the hash of the initial webpage content
url = "https://portal2.ipt.pt/pt/cursos/licenciaturas/l_-_ei/horarios/"
previous_hash = None
firstAUX = True

# Pushover credentials
api_token = 'YOUR_API_TOKEN_HERE'
user_key = 'YOUR_USER_KEY_KEY'

# Function to calculate the MD5 hash of a string
def calculate_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

# Function to send a notification with a message to your mobile phone using Pushover API
def sendNotification(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": api_token,
                     "user": user_key,
                     "message": message,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()

while True:
    try:
        # Fetch the current content of the webpage
        response = requests.get(url)
        current_content = response.text

        # Calculate the hash of the current content
        current_hash = calculate_hash(current_content)

        # Check if the content has changed
        if current_hash != previous_hash:
            if(not firstAUX):
                print("HORARIOS UPDATED")
                sendNotification("HORARIOS UPDATED")
            else:
                firstAUX = not firstAUX
            previous_hash = current_hash

        # Wait 1 minute time before checking again
        time.sleep(60)

    except Exception as e:
        print(f"An error occurred: {e}")


