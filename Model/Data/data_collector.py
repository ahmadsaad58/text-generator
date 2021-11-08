from argparse import ArgumentParser
import lyricsgenius as lg
import pandas as pd

# terminal colors
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# get token
GENIUS_API_TOKEN = "NUbU0kk1cP9Dqimz9hjp-YqSN8bbEwsHz5KZZbruKDMI_uCE_6Xgn8FmuUPXcVS1"


def get_lyrics(artist, song_cap):
    genius = lg.Genius(
        GENIUS_API_TOKEN,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
        remove_section_headers=True,
    )
    try:
        songs = genius.search_artist(
            artist, max_songs=song_cap, sort="popularity"
        ).songs
        return [song.lyrics for song in songs]
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # create parser
    parser = ArgumentParser(description="Get Songs from Artist")
    parser.add_argument("--fn", "--file", type=str, default="data.txt")
    args = parser.parse_args()

    print(bcolors.WARNING + "Enter Quit to Exit" + bcolors.ENDC)

    # write to text file
    with open(args.fn, "a+") as write_out:
        while (
            artist_name := input(
                bcolors.OKCYAN + "Enter Artist Name: " + bcolors.ENDC
            ).lower()
        ) != "quit":
            song_cap = input(
                bcolors.OKCYAN
                + "Enter Nummber of Songs you want to pull: "
                + bcolors.ENDC
            )
            # get lyrics for songs
            for song in get_lyrics(artist_name, int(song_cap)):
                write_out.write(song)

    # write to csv
    with open(args.fn, "r+") as file_:
        df = pd.DataFrame([line.strip() for line in file_])
        df.to_csv(args.fn.split(".")[0] + ".csv")
