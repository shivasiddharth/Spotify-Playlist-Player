#!/usr/bin/env python

import argparse
import spotifystreamer
import time

spotify = spotifystreamer.SpotifyMusic()

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', type=str,
                        metavar='Playlist Name', required=True,
                        help='Name of the playlist to be played')
    args = parser.parse_args()
    if not args.p and not p:
        raise Exception('Missing -p Input option')
    spotify.spotify_playlist_select(args.p)





if __name__ == '__main__':
    main()
