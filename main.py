import requests
import json

# page = requests.get('https://api.github.com/users/eqsdxr/events')


# BLOCK FOR TESTS TO DO NOT TO MAKE TOO MUCH REQUESTS TO THE GITHUB SERVERS
with open('responce0.txt', 'r') as file:
    content = json.load(file)
    # json.dump(page.text, file, indent=4)


content = content.text


# every element of the main list is a new event
def parsing_results(event):
        ev_type = event['type']
        if ev_type == 'PushEvent':
            print(f"Pushed {event['size']} commits to {event['repo']['name']}")


print('Output:')
if content:
     for event in content:
          parsing_results(event)


