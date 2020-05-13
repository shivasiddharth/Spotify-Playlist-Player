![github-small](https://user-images.githubusercontent.com/18142081/81770496-0c77c000-94fe-11ea-9ad6-9593469e6f18.png)
 
## How to setup or use   

### Create Spotify credentials   
1. Click [here](https://developer.spotify.com/dashboard/login) and register for a spotify developer account, if you already don't have one.  
2. In the developer's dashboard, choose **CREATE A CLIENT ID**. In the pop-up window provide the requested details.  
3. Set the Redirect URIs to **http://localhost:8888**    
4. Click on the new app created and copy the CLIENT ID and CLIENT SECRET. Paste it in the config.yaml file in the indicated space.  
5. Access spotify from [here]( https://www.spotify.com/account/overview/) and copy the username and enter it in the config.yaml   

### Create YouTube API Key   
1. Go to the projects page on Google Cloud Console-> https://console.cloud.google.com/project and sign in using your google account.    
2. Create a new project and give it a name.  
3. On the left top corner, click on the hamburger icon or three horizontal stacked lines.  
4. Move your mouse pointer over **API and services** and choose **credentials**.
5. Click on create credentials and select API Key and choose close. Make a note of the created API Key and enter it in the **config.yaml** script at the indicated location.  
6. From the **API and services** option, select library and in the search bar type **youtube**, select **YouTube Data API v3** API and click on **ENABLE**.  

### Install dependencies
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

### Example usages   
   Open a terminal and run the example as follows:  
   Example 1-Playback by supplying playlistname as argument:   
   ```   
   python3 -i /home/pi/Spotify-Playlist-Player/src/example-1-parseargs.py -p "Name of your playlist"   
   ```
   
   Example 2-Playback control using Pimoroni's Button-SHIM:      
   ```     
   python3 /home/pi/Spotify-Playlist-Player/src/example-2-button-shim.py   
   ```

## Note   
1. For premium or paid users there are a number of programs like mopidy-spotify, spotify connect, volumio plugin, etc. For free users, there is limited scope of playing back spotify playlists such as mpsyt.   

2. Spotify API currently only supports playback in a web browser, but DRM content is being blocked in the Raspberry Pi.    

3. As a roundabout approach, these scripts get playlist details using Spotipy API and then fetch those tracks from YouTube.      

4. This custom program has a better accuracy than spotify playlist playback using mpsyt.     
