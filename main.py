import requests
from urllib.parse import urlencode
import base64
import webbrowser
import json
from private.creds import CLIENT_ID, CLIENT_SECRET



# requesting access token from Spotify API in order to grab user information; requires user to log in securely through Spotify; returns token
def get_authorization():
    auth_headers = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-library-read user-read-currently-playing user-top-read playlist-read-private playlist-modify-public playlist-modify-private"
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







# gets a list of user's playlist (NOT DONE)
def get_playlists(token, offset, playlist_list_acc):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }


    user_params = {
        "limit": 50,
        "offset": offset
    }


    user_playlists = requests.get("https://api.spotify.com/v1/me/playlists", params=user_params, headers=user_headers)
    info_json = user_playlists.json()


    playlist_list_curr = []
    


    if info_json['next'] is None:
        for playlist in range(len(info_json['items'])):
            playlist_list_curr.append(info_json['items'][playlist]['name'])
        playlist_list_acc = playlist_list_acc + playlist_list_curr
        return playlist_list_acc
    elif info_json['next'] is not None:
        for playlist in range(len(info_json['items'])):
            playlist_list_curr.append(info_json['items'][playlist]['name'])
        offset += 50
        playlist_list_acc = playlist_list_acc + playlist_list_curr
        return get_playlists(token, offset, playlist_list_acc)
    


# returns currently playing song
def get_current_playing_song(token):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_currently_playing_response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=user_headers)
    info_json = user_currently_playing_response.json()

    if info_json['is_playing'] != True:
        print("Nothing is currently playing\n")
    else:
        track_name = info_json['item']['name']
        artist_list = info_json['item']['artists']
        artist_names = ", ".join([artist['name'] for artist in artist_list])
        print("\nThe currently playing song is: " + track_name + " by " + artist_names + "\n")



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
        print("" + song_name + " by " + artist_names + "")
    print ("\n")
    


# returns the user's top artists
def get_top_artists(token):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    number_of_top_artists = input("How many? (max 50): ")

    time_range_input = input("long_term, medium_term, or short_term?: ")
    #print("\n")
    #time_range = ""
    #if time_range_input == "long term":
    #    time_range = "long_term"
    #elif time_range_input == "medium term":
    #    time_range = "medium_term"
    #elif time_range_input == "short term":
    #    time_range = "short_term"
    #else:
     #   print("Your input wasn't valid.")
     #   get_top_artists(token)
    

    user_params = {
        "time_range": time_range_input,
        "limit": number_of_top_artists
    }

    user_top_artists_response = requests.get("https://api.spotify.com/v1/me/top/artists", params=user_params, headers=user_headers)
    info_json = user_top_artists_response.json()

    print("\n")

    for artist in range(len(info_json['items'])):
        artist_name = info_json['items'][artist]['name']
        print(artist_name)
    
    print("\n")



# gets user's top songs
def get_top_songs(token):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    number_of_top_songs = input("How many? (max 50): ")

    time_range_input = input("long_term, medium_term, or short_term?: ")
    #time_range = ""
    #if time_range_input == "long term":
    #    time_range = "long_term"
    #elif time_range_input == "medium term":
     #   time_range = "medium_term"
    #elif time_range_input == "short term":
     #   time_range = "short_term"
    #else:
    #    print("Your input wasn't valid.")
    #    get_top_songs(token)
    

    user_params = {
        "time_range": time_range_input,
        "limit": number_of_top_songs
    }

    user_top_songs_response = requests.get("https://api.spotify.com/v1/me/top/tracks", params=user_params ,headers=user_headers)
    info_json = user_top_songs_response.json()
    
    print("\n")
    
    for song in range(len(info_json['items'])):
        song_name = info_json['items'][song]['name']
        artist_list = info_json['items'][song]['artists']
        artist_names = ", ".join([artist['name'] for artist in artist_list])
        print(song_name + " by " + artist_names)
    

    print("\n")



# creates playlist with songs from discover weekly playlist
def discover_weekly_playlist(token):
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_params_disover_weekly_info = {
        "q": "discover%weekly",
        "type": ["playlist"],
        "limit": 1
    }

    #gets discover weekly playlist information
    user_discover_weekly_playlist = requests.get("https://api.spotify.com/v1/search", params=user_params_disover_weekly_info, headers=user_headers)
    info_json = user_discover_weekly_playlist.json()
    

    # gets list of weekly discover songs' information
    user_params = {
        "fields": "items.track(uri)",
        "limit": 30
    }

    discover_weekly_playlist_id = info_json['playlists']['items'][0]['id']
    user_discover_weekly_songs = requests.get("https://api.spotify.com/v1/playlists/" + discover_weekly_playlist_id+ "/tracks",  params=user_params, headers=user_headers)
    discover_weekly_songs_json = user_discover_weekly_songs.json()


    user_playlists = get_playlists(token, 0, [])
    user_id = get_user_id(token)


    playlist_exists = False
    

    # checking if "Discover Weekly Playlist" exists
    for playlist in user_playlists:
        if playlist == "Discover Weekly Playlist":
            playlist_exists = True
        else:
            pass
    
    # making playlist if it doesn't exist, and getting playlist id if it does exist
    if playlist_exists == False:
        user_body = json.dumps({
            "name": "Discover Weekly Playlist",
            "description": "all discover weekly playlist songs"
        })

        user_discover_weekly_playlist_info = requests.post("https://api.spotify.com/v1/users/" + user_id + "/playlists", user_body, headers=user_headers)
        info_json = user_discover_weekly_playlist_info.json()
        playlist_id = info_json['id']
    else:
        user_params = {
            "q": "discover%weekly%playlist",
            "type": "playlist",
            "limit": 1,
            "offset": 1
        }
        user_discover_weekly_playlist_info = requests.get("https://api.spotify.com/v1/search", params=user_params, headers=user_headers)
        info_json = user_discover_weekly_playlist_info.json()
        playlist_id = info_json['playlists']['items'][0]['id']


    discover_weekly_songs_uris = []


    for song in range(len(discover_weekly_songs_json['items'])):
        song_uri = discover_weekly_songs_json['items'][song]['track']['uri']
        discover_weekly_songs_uris.append(song_uri)

    user_body = json.dumps({
        "uris": discover_weekly_songs_uris
    })

    error = requests.post("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks", user_body, headers=user_headers)
    info_json = error.json()

    print("The playlist was successfuly created/added to.")
    
    

# get user id
def get_user_id(token):
       
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_info = requests.get("https://api.spotify.com/v1/me", headers=user_headers)
    info_json = user_info.json()

    user_id = info_json['id']
    return user_id
     

    
# accesses various program functions through user inputs
def prompts(token):
    prompt = input("What would you like to do from the following options? (get currently playing song, get liked songs, get top artists, get top songs, create playlist with discover weekly songs, terminate program): ")

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
    elif prompt == "create playlist with discover weekly songs":
        discover_weekly_playlist(token)
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
