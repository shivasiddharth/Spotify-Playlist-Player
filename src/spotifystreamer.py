#!/usr/bin/env python


import argparse
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import mediaplayer
import subprocess
import os.path
import os
import time
import re
import json
import pafy
import yaml

ROOT_PATH = os.path.realpath(os.path.join(__file__, '..', '..'))
USER_PATH = os.path.realpath(os.path.join(__file__, '..', '..','..'))


with open('{}/src/config.yaml'.format(ROOT_PATH),'r', encoding='utf8') as conf:
    configuration = yaml.load(conf)


vlcplayer=mediaplayer.vlcplayer()

Spotify_credentials=False
Youtube_credentials=False

if configuration['Spotify']['client_id']!= 'ENTER YOUR SPOTIFY CLIENT ID HERE' and configuration['Spotify']['client_secret']!='ENTER YOUR SPOTIFY CLIENT SECRET HERE':
    Spotify_credentials=True
if configuration['Google_cloud_api_key']!='ENTER-YOUR-GOOGLE-CLOUD-API-KEY-HERE':
    Youtube_credentials=True

spotifyplaylists= configuration['Spotify']['playlist_names']

thescope='playlist-read-private'

redirecturi='http://localhost:8888'

# Spotify Declarations
# Register with spotify for a developer account to get client-id and client-secret
if Spotify_credentials:
    clientid = configuration['Spotify']['client_id']
    clientsecret = configuration['Spotify']['client_secret']
    username=configuration['Spotify']['username']
    spotify_token = util.prompt_for_user_token(username,scope=thescope,client_id=clientid,client_secret=clientsecret,redirect_uri=redirecturi)

class SpotifyMusic():
    def __init__(self):
        self.sp = spotipy.Spotify(auth=spotify_token)
        self.userplaylists=[]
        self.playlistnums=[]

    def show_spotify_track_names(self,tracks):
        spotify_tracks=[]
        for i, item in enumerate(tracks['items']):
            track = item['track']
    ##        print ("%d %32.32s %s" % (i, track['artists'][0]['name'],track['name']))
            # print ("%s %s" % (track['artists'][0]['name'],track['name']))
            spotify_tracks.append("%s %s" % (track['artists'][0]['name'],track['name']))
        return spotify_tracks

    def scan_spotify_playlists(self):
        if spotify_token:
            i=0
            playlistdetails=[]
            spotify_tracks_list=[]
            # print(self.sp.user(username))
            # print("")
            # print("")
            #playlists = self.sp.user_playlists(username)
            playlists = self.sp.current_user_playlists()
            print("")
            print("")
            print("Nuber of playlists: " + str(len(playlists['items'])))
            print("")
            print("Playlist names: ")
            num_playlists=len(playlists['items'])
            spotify_playlists={"Playlists":[0]*(len(playlists['items']))}
            # print(spotify_playlists)
            # print("")
            # print("")
            for playlist in playlists['items']:
                # print (playlist['name'])
                playlist_name=playlist['name']
                print(playlist_name)
                #print("")
                # print("")
    ##            print ('  total tracks', playlist['tracks']['total'])
    ##            print("")
    ##            print("")
                results = self.sp.user_playlist(playlist['owner']['id'], playlist['id'],fields="tracks,next")
                tracks = results['tracks']
                spotify_tracks_list=self.show_spotify_track_names(tracks)
                playlistdetails.append(i)
                playlistdetails.append(playlist_name)
                playlistdetails.append(spotify_tracks_list)
                spotify_playlists['Playlists'][i]=playlistdetails
                playlistdetails=[]
                i=i+1
            # print("")
            # print("")
            # print(spotify_playlists['Playlists'])
            return spotify_playlists, num_playlists
        else:
            print("Can't get token for ", username)

    def spotify_playlist_select(self,playlistname):
        trackslist=[]
        currenttrackid=0
        playlistname=playlistname.lower()
        print("Trying to fetch your " + playlistname + " playlist")
        if self.userplaylists==[] and self.playlistnums==[]:
            self.userplaylists,self.playlistnums=self.scan_spotify_playlists()
        if not self.playlistnums==[]:
            for i in range(0,self.playlistnums):
                #print(str(userplaylists['Playlists'][i][1]).lower())
                if playlistname in str(self.userplaylists['Playlists'][i][1]).lower():
                    trackslist=self.userplaylists['Playlists'][i][2]
                    break
            if not trackslist==[]:
                vlcplayer.media_manager(trackslist,'Spotify')
                vlcplayer.spotify_player(currenttrackid)
        else:
            print("Unable to find matching playlist")
