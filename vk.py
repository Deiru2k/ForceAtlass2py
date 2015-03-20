import json
import requests
import pymongo

ACCESS_TOKEN = "6c2aa2143a29a413a30cf13330275354688697f4bcb4f484ea3ad0f51339a1e1a4435a2ee2aa31d87b881"
API_URL = "https://api.vk.com/method/"


class VKApi:

    API_URL = "https://api.vk.com/method/"

    def __init__(self, oauth_token):
        self.ACCESS_TOKEN = oauth_token

    def __getattr__(self, api_method):

        def method(**args):

            if '_' in api_method: url = self.API_URL + api_method.replace("_", ".")
            else: url = self.API_URL + api_method
            args['access_token'] = self.ACCESS_TOKEN
            try:
                r = requests.get(url=url, params=args)
            except:
                return None
            if r.status_code is not 200: return None
            response = json.loads(r.content.decode())
            if 'error' in response:
                return None
            else:
                return response['response']
        return method


connection = pymongo.Connection()
db = connection.graph
users = db.users
vk = VKApi(ACCESS_TOKEN)
initial = vk.friends_get(user_id=151659519, fields="photo_50")
for user in initial:
    friends = vk.friends_get(user_id=user['user_id'])
    if not friends: continue
    user['friends'] = friends
    print(user['friends'])
    users.update({"user_id": user['user_id']}, user, upsert=True)
    try:
        for friend in vk.friends_get(user_id=user['user_id'], fields="photo_50"):
            friends = vk.friends_get(user_id=friend['user_id'])
            if not friends: continue
            friend['friends'] = friends
            users.update({"user_id": friend['user_id']}, friend, upsert=True)
    except TypeError:
        print(user)

# my_friends = vk.friends_get(user_id="151659519")
# my_friends_friends = for
