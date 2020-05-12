#!/usr/bin/env python

import argparse
import spotifystreamer
import signal
import buttonshim
import subprocess
import time
import mediaplayer
from sys import version_info


print("""
Button SHIM: button-shim-player.py
Control Spotify playback on your Raspberry Pi!
A = Volume Down
B = Single press for previous track and Long press for previous playlist
C = Single press to play/pause the playback and Long press for stopping the playback
D = Single press for next track and Long press for next playlist
E = Volume Up
Press Ctrl+C to exit.
""")

DEVICE = "PCM"
VOL_REPEAT = 0.2
volume = 0
currentplaylistnum=0
playlists=spotifystreamer.spotifyplaylists
spotify = spotifystreamer.SpotifyMusic()
button_was_held = False

def set(action):
    subprocess.Popen(
    ["amixer", "set", DEVICE, action],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_volume():
    actual_volume = subprocess.check_output(
    "amixer get '{}' | awk '$0~/%/{{print $4}}' | tr -d '[]%'".format(DEVICE),
    shell=True)
    if version_info[0] >= 3:
        actual_volume = actual_volume.strip().decode('utf-8')
    else:
        actual_volume = actual_volume.strip()
        actual_volume = int(actual_volume)
        actual_volume = min(100, actual_volume)
        actual_volume = max(0, actual_volume)
    return actual_volume

def main():
    while True:
        # Volume Up
        @buttonshim.on_press(buttonshim.BUTTON_A, repeat=True, repeat_time=VOL_REPEAT)
        def button_a_press(button, pressed):
            global volume
            volume = get_volume()
            volume = int(volume) + 1
            volume = min(100, volume)
            print("Volume: {}%".format(volume))
            set("{}%".format(volume))
            scale = volume / 100.0
            buttonshim.set_pixel(int(0xff * (1.0 - scale)), int(0xff * scale), 0x00)

        @buttonshim.on_press(buttonshim.BUTTON_B)
        def press_handler(button, pressed):
            global button_was_held
            button_was_held = False

        # Change to previous track
        @buttonshim.on_release(buttonshim.BUTTON_B)
        def release_handler(button, pressed):
            if not button_was_held:
                if spotifystreamer.vlcplayer.is_vlc_playing() or str(spotifystreamer.vlcplayer.state())=="State.Paused":
                    spotifystreamer.vlcplayer.stop_vlc()
                    spotifystreamer.vlcplayer.change_media_previous()
                    print("Playing previous track....")
                else:
                    print("Nothing is playing....")

        # Change to previous playlist
        @buttonshim.on_hold(buttonshim.BUTTON_B, hold_time=2)
        def hold_handler(button):
            global button_was_held
            button_was_held = True
            global currentplaylistnum
            if currentplaylistnum == 0:
                print("Currently first playlist is playing....")
            else:
                if spotifystreamer.vlcplayer.is_vlc_playing() or str(spotifystreamer.vlcplayer.state())=="State.Paused":
                    spotifystreamer.vlcplayer.stop_vlc()
                    currentplaylistnum = currentplaylistnum - 1
                    spotify.spotify_playlist_select(playlists[currentplaylistnum])
                else:
                    print("Nothing is playing....")

        @buttonshim.on_press(buttonshim.BUTTON_C)
        def press_handler(button, pressed):
            global button_was_held
            button_was_held = False

        # Play/Pause
        @buttonshim.on_release(buttonshim.BUTTON_C)
        def release_handler(button, pressed):
            if not button_was_held:
                global currentplaylistnum
                if spotifystreamer.vlcplayer.is_vlc_playing():
                    spotifystreamer.vlcplayer.pause_vlc()
                elif str(spotifystreamer.vlcplayer.state())=="State.Paused":
                    spotifystreamer.vlcplayer.play_vlc()
                else:
                    print("Nothing is playing....")
                    print("Starting your playlist playback....")
                    print(playlists)
                    print(playlists[currentplaylistnum])
                    spotify.spotify_playlist_select(playlists[currentplaylistnum])

        # Stop
        @buttonshim.on_hold(buttonshim.BUTTON_C, hold_time=2)
        def hold_handler(button):
            global button_was_held
            button_was_held = True
            if spotifystreamer.vlcplayer.is_vlc_playing() or str(spotifystreamer.vlcplayer.state())=="State.Paused":
                spotifystreamer.vlcplayer.stop_vlc()
            else:
                print("Nothing is playing....")

        @buttonshim.on_press(buttonshim.BUTTON_D)
        def press_handler(button, pressed):
            global button_was_held
            button_was_held = False

        # Change to previous track
        @buttonshim.on_release(buttonshim.BUTTON_D)
        def release_handler(button, pressed):
            if not button_was_held:
                if spotifystreamer.vlcplayer.is_vlc_playing() or str(spotifystreamer.vlcplayer.state())=="State.Paused":
                    spotifystreamer.vlcplayer.stop_vlc()
                    spotifystreamer.vlcplayer.change_media_next()
                    print("Playing next track....")
                else:
                    print("Nothing is playing....")

        # Change to previous playlist
        @buttonshim.on_hold(buttonshim.BUTTON_D, hold_time=2)
        def hold_handler(button):
            global button_was_held
            button_was_held = True
            global currentplaylistnum
            if currentplaylistnum == len(playlists) -1 :
                print("Currently last playlist is playing....")
            else:
                if spotifystreamer.vlcplayer.is_vlc_playing() or str(spotifystreamer.vlcplayer.state())=="State.Paused":
                    spotifystreamer.vlcplayer.stop_vlc()
                    currentplaylistnum = currentplaylistnum + 1
                    spotify.spotify_playlist_select(playlists[currentplaylistnum])
                else:
                    print("Nothing is playing....")

        # Volume Down
        @buttonshim.on_press(buttonshim.BUTTON_E, repeat=True, repeat_time=VOL_REPEAT)
        def button_e_press(button, pressed):
            global volume
            volume = get_volume()
            volume = int(volume) - 1
            volume = max(0, volume)
            print("Volume: {}%".format(volume))
            set("{}%".format(volume))
            scale = volume / 100.0
            buttonshim.set_pixel(int(0xff * (1.0 - scale)), int(0xff * scale), 0x00)

if __name__ == '__main__':
    main()
