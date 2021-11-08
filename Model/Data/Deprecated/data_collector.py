from argparse import ArgumentParser
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
import requests

# terminal colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# get token
GENIUS_API_TOKEN = "NUbU0kk1cP9Dqimz9hjp-YqSN8bbEwsHz5KZZbruKDMI_uCE_6Xgn8FmuUPXcVS1"


def compile_song_urls(artist_name, song_cap):
    """
    Function to compile a list of song_cap number of song urls in a list 

    Params
    ------
        artist_name : str
            Name of the artist to search for 
        song_cap : int
            Number of songs to look for
    
    Return
    ------
        A list of song urls 
    """

    def search_artist(artist_name, page_number):
        """
            Search for an artist and get a respose with their hits
        """
        url = "https://api.genius.com/search?per_page=10&page={}".format(page_number)
        headers = {"Authorization": "Bearer " + GENIUS_API_TOKEN}
        data = {"q": artist_name.title()}
        return requests.get(url, params=data, headers=headers)

    page, songs, max_songs = 1, [], False

    while not max_songs:
        hits = search_artist(artist_name, page).json["response"]["hits"]
        
        for hit in hits: 
            max_songs = len(songs) == song_cap
            info = hit['result']
            if not max_songs and artist_name in info['artist_names'].lower():
                songs.append(info['url'])
            else:
                break
        
        page += 1 

    return songs


def scrape_song_lyrics(url):
    """
    Function to scrape lyrics from Genius

    Params
    ------
        url : str
            URL for a song
    
    Return
    ------
        A string of lyrics for the song 
    """

    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    # this no longer works
    lyrics = html.find("div", class_="lyrics").get_text()
    # remove identifiers like chorus, verse, etc
    lyrics = re.sub(r"[\[].*?[\]]", "", lyrics)
    # remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics


if __name__ == "__main__":
    # create parser
    parser = ArgumentParser(description="Get Songs from Artist")
    parser.add_argument("--fn", "--file", type=str, default="data.txt")
    args = parser.parse_args()

    print(bcolors.WARNING + "Enter Quit to Exit" + bcolors.ENDC)
    
    # write to text file
    with open(args.fn, "a+") as write_out: 
        while (artist_name := input(bcolors.OKCYAN + "Enter Artist Name: " + bcolors.ENDC).lower()) != "quit":
            song_cap = input(bcolors.OKCYAN  + "Enter Nummber of Songs you want to pull: " +bcolors.ENDC)
            # get lyrics for songs 
            for song in compile_song_urls(artist_name, song_cap):
                lyrics = scrape_song_lyrics(song)
                for line in lyrics.split("\n"):
                    write_out.write(line)
                    write_out.write("\n")

    

    # write to csv
    with open(args.fn, "r+") as file_: 
        df = pd.DataFrame([line.strip() for line in file_])
        df.to_csv(args.fn.split(".")[0] + ".csv")