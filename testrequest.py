import requests
import json
import os

class SpotifyApp():

    def __init__(self, cID: str, cSecret: str):
        self.clientID = cID
        self.clientSecret = cSecret

    def get_auth_token(self, cID: str, cSecret: str)->str:
        token_req = {"method":"POST",
                    "url":"https://accounts.spotify.com/api/token",
                    "header":{"Content-Type":"application/x-www-form-urlencoded"},
                    "body":{"grant_type":"client_credentials", "client_id":cID, "client_secret":cSecret}}

        try:
            resp = requests.request(method=token_req["method"], url=token_req["url"],
                                    headers=token_req["header"], data=token_req["body"])
        except requests.HTTPError as herr:
            print(f"HTTP Error: {herr}")
            exit(1)
        except requests.ConnectionError as cerr:
            print(f"Connection Error: {cerr}")
            exit(1)
        except requests.Timeout as terr:
            print(f"Timeout Error: {terr}")
            exit(1)
        except requests.RequestException as rerr:
            print(f"Other Error: {rerr}")
            exit(1)

        token = json.loads(resp.text)["access_token"]

        return token

    def get_artist_info(self, aID: str, authToken: str):
        artist_req = {"method":"GET",
                  "url":f"https://api.spotify.com/v1/artists/{aID}",
                  "headers":{"Authorization":f"Bearer {authToken}"}}

        try:
            artist_info = requests.request(method=artist_req["method"], url=artist_req["url"],
                                        headers=artist_req["headers"])
        except requests.HTTPError as herr:
            print(f"HTTP Error: {herr}")
            exit(1)
        except requests.ConnectionError as cerr:
            print(f"Connection Error: {cerr}")
            exit(1)
        except requests.Timeout as terr:
            print(f"Timeout Error: {terr}")
            exit(1)
        except requests.RequestException as rerr:
            print(f"Other Error: {rerr}")
            exit(1)        

        return artist_info

    def get_current_user(self, authToken: str):
        user_req = {"method":"GET",
                    "url":"https://api.spotify.com/v1/me",
                    "headers":{"Authorization":f"Bearer {authToken}"}}
        # add scopes

        user_info = requests.request(method=user_req["method"], url=user_req["url"],
                                     headers=user_req["headers"])
        
        return user_info
    
    def get_playlist(self, plID: str, authToken: str):
        playlist_req = {"method":"GET",
                        "url":f"https://api.spotify.com/v1/playlists/{plID}",
                        "headers":{"Authorization":f"Bearer {authToken}"}}
        
        try:
            playlist_info = requests.request(method=playlist_req["method"], url=playlist_req["url"],
                                            headers=playlist_req["headers"])
        except requests.HTTPError as herr:
            print(f"HTTP Error: {herr}")
            exit(1)
        except requests.ConnectionError as cerr:
            print(f"Connection Error: {cerr}")
            exit(1)
        except requests.Timeout as terr:
            print(f"Timeout Error: {terr}")
            exit(1)
        except requests.RequestException as rerr:
            print(f"Other Error: {rerr}")
            exit(1)        
        return playlist_info


def get_Auth_File(filePath:str):

    with open(filePath, "r") as client_file:
        client = client_file.read()
        client_dict = json.loads(client)["client"]
        client_id = client_dict["id"]
        client_secret = client_dict["secret"]

        return client_id, client_secret

def main():
    client_id, client_secret = get_Auth_File("spoofy/auth.json")

    app = SpotifyApp(client_id, client_secret)

    token = app.get_auth_token(client_id, client_secret)
    print(token)

    artist_id = "5o5dFyK0UODK3sYQp5ao8V"
    artist_info = app.get_artist_info(artist_id, token)
    print(artist_info.json())

main()