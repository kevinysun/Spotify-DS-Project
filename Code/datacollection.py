import spotipy as sp
import spotipy.util as sputil
import pandas as pd

CLIENT_ID = "c5c68c3313a746518d5d50ab26da5729"
CLIENT_SECRET = "8e8129ecb3574a6aa8240f1cd321d0c0"

token = sputil.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
cache_token = token.get_access_token()
sp = sp.Spotify(cache_token)




def get_playlist_data(creator, playlist_id):
    # Create empty dataframe
    playlist_features_list = ["artist","album","track_name", "track_id", "danceability",
        "energy","key","loudness","mode", "speechiness","instrumentalness",
        "liveness","valence","tempo", "duration_ms","time_signature"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    # Loop through every track in the playlist, extract features and append the features to the playlist df
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    
    for track in playlist:
        # Create empty dict 
        
        playlist_features = {}
        
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"] 
        playlist_features["track_name"] = track["track"]["name"] 
        playlist_features["track_id"] = track["track"]["id"]
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]: 
            playlist_features[feature] = audio_features[feature]

        # combine dataframes
        track_df = pd.DataFrame(playlist_features, index = [0]) 
        playlist_df = pd.concat([playlist_df, track_df],ignore_index = True) 
    return playlist_df