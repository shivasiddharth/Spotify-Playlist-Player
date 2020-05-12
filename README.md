# Spotify-Playlist-Player
  Scripts to play your spotify playlists.

## Create Spotify credentials   
1. Click [here](https://developer.spotify.com/dashboard/login) and register for a spotify developer account, if you already don't have one.  
2. In the developer's dashboard, choose "**CREATE A CLIENT ID**". In the pop-up window provide the requested details.  
3. Set the Redirect URIs to http://localhost:8888    
4. Click on the new app created and copy the CLIENT ID and CLIENT SECRET. Paste it in the config.yaml file in the indicated space.  
5. Access spotify:[here]( https://www.spotify.com/account/overview/) and copy the username to be entered in config.yaml   

## Create YouTube API Key   
1. Go to the projects page on your Google Cloud Console-> https://console.cloud.google.com/project  
2. Select your project from the list or create a new project.  
3. On the left top corner, click on the hamburger icon or three horizontal stacked lines.  
4. Move your mouse pointer over "API and services" and choose "credentials".
5. Click on create credentials and select API Key and choose close. Make a note of the created API Key and enter it in the **config.yaml** script at the indicated location.  
6. "From the API and services" option, select library and in the search bar type **youtube**, select "YouTube Data API v3" API and click on "ENABLE".  

## Install dependencies
   System wide dependencies    
   ```
   sudo apt-get install python3 python3-dev python3-venv python3-pip python3-setuptools -y       
   ```   
   Create a environment    
   ```   
   python3 -m venv spotifyenv      
   ```   
   Setup pip tools   
   ```   
   spotifyenv/bin/python -m pip install --upgrade pip setuptools wheel    
   ```   
   Move into the created environment  
   ```   
   source spotifyenv/bin/activate   
   ```    
   Install pip packages   
   ```   
   pip3 install pafy google-api-python-client python-vlc git+https://github.com/plamere/spotipy.git pyyaml oauth2client youtube_dl   
   ```   

## Example usages   
   Open a terminal and run the example as follows:  
   ```   
   python3 -i /home/pi/Spotify-Playlist-Player/src/example-1-parseargs.py -p "Name of your playlist"   
   python3 /home/pi/Spotify-Playlist-Player/src/example-2-button-shim.py   
   ```

## Note   
1. For premium or paid users there are a number of programs like mopidy-spotify, spotify connect, volumio plugin, etc. For free users, there is limited scope of playing back spotify playlists such as mpsyt.
2. Spotify API currently only supports playback in a web browser, but DRM content is being blocked in the Raspberry Pi.    
3. As a roundabout approach, I have programmed the assistant to get the playlist details using Spotipy API and then fetch those tracks from YouTube.    
4. This custom program has a better accuracy than spotify playlist playback using mpsyt.     