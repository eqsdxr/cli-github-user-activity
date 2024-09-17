import http.client
import argparse
import json


# function that determine type of events
def parsing_results(event:list)->None:
        ev_type = event['type']
        match ev_type:
            case 'PushEvent':
                if event['payload']['size'] == 1:
                    print(f"Pushed {event['payload']['size']} commit to {event['repo']['name']}")
                else:
                    print(f"Pushed {event['payload']['size']} commits to {event['repo']['name']}")
            case 'WatchEvent':
                print(f"Starred {event['repo']['name']}")
            case 'CommitCommentEvent':
                print(f"Commented on a commit in {event['repo']['name']}")
            case 'CreateEvent':
                print(f"Created {event['payload']['ref_type']} in {event['repo']['name']}")
            case 'DeleteEvent':
                print(f"Deleted {event['payload']['ref_type']} in {event['repo']['name']}")
            case 'ForkEvent':
                print(f"Forked {event['repo']['name']} to {event['payload']['forkee']['full_name']}")
            case 'GollumEvent':
                print(f"Updated the wiki in {event['repo']['name']}")
            case 'IssueCommentEvent':
                print(f"Commented on an issue in {event['repo']['name']}")
            case 'IssuesEvent':
                match event['payload']['action']:
                    case 'opened':
                        print(f"Opened an issue in {event['repo']['name']}")
                    case 'edited':
                        print(f"Edited an issue in {event['repo']['name']}")
                    case 'closed':
                        print(f"Closed an issue in {event['repo']['name']}")
                    case 'reopened':
                        print(f"Reopened an issue in {event['repo']['name']}")
                    case 'assigned':
                        assignee = event['payload']['assignee']['login']
                        print(f"Assigned issue to {assignee} in {event['repo']['name']}")
                    case 'unassigned':
                        assignee = event['payload']['assignee']['login']
                        print(f"Unassigned issue from {assignee} in {event['repo']['name']}")
                    case 'labeled':
                        label = event['payload']['label']['name']
                        print(f"Labeled issue with '{label}' in {event['repo']['name']}")
                    case 'unlabeled':
                        label = event['payload']['label']['name']
                        print(f"Unlabeled issue removing '{label}' in {event['repo']['name']}")
            case 'MemberEvent':
                print(f"Added {event['payload']['member']['login']} to {event['repo']['name']}")
            case 'PublicEvent':
                print(f"Made {event['repo']['name']} public")
            case 'PullRequestEvent':
                print(f"Opened a pull request in {event['repo']['name']}")
            case 'PullRequestReviewEvent':
                print(f"Reviewed a pull request in {event['repo']['name']}")
            case 'PullRequestReviewCommentEvent':
                print(f"Commented on a pull request in {event['repo']['name']}")
            case 'PullRequestReviewThreadEvent':
                print(f"Created a review thread in {event['repo']['name']}")
            case 'ReleaseEvent':
                print(f"Published a release in {event['repo']['name']}")
            case 'SponsorshipEvent':
                print(f"Sponsored {event['payload']['sponsor']['login']}")
            case _:
                pass

# function that gathers user activity
def fetch_user_activity_data(username:str)-> dict | None:
    if username:
        # connection to the api.github.com and gathering data
        try:
            conn = http.client.HTTPSConnection('api.github.com')
            conn.request('GET', f'/users/{username}/events', headers={'User-Agent': 'Python'})
            response = conn.getresponse()
            try:
                response_dict = json.loads(response.read().decode())
            except json.JSONDecodeError:
                print('# Error parsing JSON responce.')
                return 1 # it returns one in order to prevent printing "# This user exists but doesn\'t have any activity to show"
            if response.status == 200:
                    return response_dict
            else:
                if response.status == 404:
                    print(f'# Username "{username}" not found on GitHub')
                    return 1
        except ConnectionError:
            print('# Connection error. Please check you network.')
            return 1
        except http.client.HTTPException:
            print('# HTTP error:', http.client.HTTPException)
            return 1
        finally:
            conn.close()
    else:
        print ("# Please provide a GitHub username.")
        return 1

def print_user_activity(username:str, response_dict_or_one:dict|int)->None:
    if response_dict_or_one and response_dict_or_one != 1:
        print(f'{username}\'s activity:')
        # every element of the responce json is a new event
        for event in response_dict_or_one:
            print('- ', end='')
            parsing_results(event)
    elif response_dict_or_one != 1:
        print(f'# The user "{username}" exists but doesn\'t have any activity to show')


# parsing an argument in terminal
parser = argparse.ArgumentParser()
parser.add_argument('username', help='GitHub username')
args = parser.parse_args()

# checking if a user wants to check multiple usernames
if '/' in args.username:
    usernames = args.username.split('/')
    for username in usernames:
        print_user_activity(username, fetch_user_activity_data(username))
else:
    print_user_activity(args.username, fetch_user_activity_data(args.username))
    


