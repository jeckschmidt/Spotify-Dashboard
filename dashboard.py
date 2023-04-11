import requests
from urllib.parse import urlencode
import base64
import webbrowser
import json



# personalized spotify given credentials after making an app on the spotify for developers website
CLIENT_ID = '24120c9b0e484e77af61e070bf899ae7'
CLIENT_SECRET = 'bb7ef1395d7f40caa81bcdad4d9d2b21'



# requesting access token from Spotify API in order to grab user information; requires user to log in securely through Spotify; returns token
def get_authorization():
    auth_headers = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-library-read user-read-currently-playing user-top-read"
    }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

    url_code = input("enter the text after 'code=' in the re-direct url after logging in: ")
    print("\n")
    encoded_credentials = base64.b64encode(CLIENT_ID.encode() + b':' + CLIENT_SECRET.encode()).decode("utf-8")

    token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
    "grant_type": "authorization_code",
    "code": url_code,
    "redirect_uri": "http://localhost:7777/callback"
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    token = r.json()["access_token"]
    return token



# returns the user's top artists
def get_top_artists(token):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_top_artists_response = requests.get("https://api.spotify.com/v1/me/top/artists", headers=user_headers)
    info_json = user_top_artists_response.json()

    for artist in range(len(info_json['items'])):
        artist_name = info_json['items'][artist]['name']
        print(artist_name)
    
    print("\n")


#gets user's top songs
def get_top_songs(token):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_top_songs_response = requests.get("https://api.spotify.com/v1/me/top/tracks",  headers=user_headers)
    info_json = user_top_songs_response.json()
    
    
    
    for song in range(len(info_json['items'])):
        song_name = info_json['items'][song]['name']
        artist_list = info_json['items'][song]['artists']
        artist_names = ", ".join([artist['name'] for artist in artist_list])
        print(song_name + " by " + artist_names)
    

    print("\n")


# returns currently playing song
def get_current_playing_song(token):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_currently_playing_response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=user_headers)
    info_json = user_currently_playing_response.json()

    if info_json['is_playing'] == True:
        track_name = info_json['item']['name']
        artist_list = info_json['item']['artists']
        artist_names = ", ".join([artist['name'] for artist in artist_list])
        print("\nThe currently playing song is: " + track_name + " by " + artist_names + "\n")
    else:
        print("Nothing is currently playing\n")



# returns x number of user's liked songs
def get_liked_songs(token):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    number_of_liked_songs = input("How many? (max 50): ")
    print("\n")
    

    user_params = {
        "limit": number_of_liked_songs
    }

    user_tracks_response = requests.get("https://api.spotify.com/v1/me/tracks", params=user_params, headers=user_headers)
    info_json = user_tracks_response.json()

    for song in range(len(info_json['items'])):
        song_name = info_json['items'][song]['track']['name']
        artist_list = info_json['items'][song]['track']['artists']
        artist_names = ", ".join([artist['name'] for artist in artist_list])
        print(song_name + " by " + artist_names)
    
    print("\n")



# accesses various program functions through user inputs
def prompts(token):
    prompt = input("What would you like to do from the following options? (get currently playing song, get liked songs, get top artists, get top songs, terminate program,): ")

    if prompt == "get currently playing song":
        get_current_playing_song(token)
        prompt_helper(token)
    elif prompt == "get liked songs":
        get_liked_songs(token)
        prompt_helper(token)
    elif prompt == "get top artists":
        get_top_artists(token)
        prompt_helper(token)
    elif prompt == "get top songs":
        get_top_songs(token)
        prompt_helper(token)
    elif prompt == "terminate program":
        print("See you next time!")
    else:
        print("Your input wasn't valid.")
        prompts(token)



# helper function to reduce redundant code in the prompts function
def prompt_helper(token):
    prompt = input("What you like to do anything else? (Y/N): ")
    if prompt == "Y":
        prompts(token)
    elif prompt == "N":
        print("See you next time!")
    else:
        print("Your input wasn't valid.")
        prompts(token)



def main():
    token = get_authorization()
    prompts(token)



if __name__ == '__main__':
    main()
