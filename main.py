# source venv/bin/activate
import re
import os
from pathlib import Path
import shutil
import logging
import time
from send2trash import send2trash

from progress import copyfile
from plex_update import update_plexapi

# TODO send hook to plex to re search
logging.basicConfig(filename='log films.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(message)s')

extensions = ["avi", "mkv", "mp4"]
# paths = "/Users/eysteingulbrandsen/Downloads/test"
paths = '/Users/Eystein/Downloads'
path_tv = "/Volumes/homes/plex/TV Shows"
path_mov = "/Volumes/homes/plex/Movies"

before = dict([(f, None) for f in os.listdir(paths)])


def camel_case(s):
    s = re.sub(r"(_|-)+", " ", s).title()
    return ''.join([s[:]])


while True:
    time.sleep(10)
    after = dict([(f, None) for f in os.listdir(paths)])
    added = [f for f in after if f not in before]
    removed = [f for f in before if f not in after]
    if added:
        logging.info(f"Added: {added}")
        film_lst = []
        path_lst = []

        for path, subdirs, files in os.walk(f"{paths}"):
            for name in files:
                for extension in extensions:
                    if re.findall(extension, name):
                        film_lst.append(name)
                        path_lst.append(path + "/" + name)

        for name in film_lst:

            # TV
            tv = re.findall(r"""
            (.*)  # Title
            [ .]
            S(\d{1,2})  # Season
            E(\d{1,2})  # Episode
            [ .a-zA-Z]* # Space, period or words like Proper/buried
            (\d{3,4}p)? # Quality
            """, camel_case(name), re.VERBOSE)

            if tv:
                p = Path(path_lst[0])
                path_old_tv = p.rename(Path(p.parent, f"{tv[0][0]}.S{tv[0][1]}E{tv[0][2]}{p.suffix}"))
                for path, subdirs, files in os.walk(f"{path_tv}"):
                    tvs = tv[0][0].replace(".", " ")
                    tvs = camel_case(tvs)
                    season = tv[0][1]

                    if season[0] == '0':
                        season = season.replace("0", "")
                    if tvs in subdirs:
                        # print(f"{tv[0][0]}.S{tv[0][1]}E{tv[0][2]}")
                        new_path = path_tv \
                                   + "/" \
                                   + tvs \
                                   + "/" \
                                   + "Season " + season + "/" \
                                   + f"{tv[0][0]}.S{tv[0][1]}E{tv[0][2]}" \
                                     f" - {time.asctime(time.localtime(time.time()))}{p.suffix}"
                        print(new_path)
                        break

                copyfile(path_old_tv, new_path)
                send2trash(path_old_tv)
                logging.info(f"{tvs} was add to: {new_path}")
                update_plexapi()
                print("\n Done")
                logging.info("Done")

            # Movie
            movie = re.findall(r"""
            (.*?[ .]\d{4})  # Title including year
            [ .a-zA-Z]*  # Space,period, or words
            (\d{3,4}p)?  #Quality
            """, name, re.VERBOSE)

            if movie:
                p = Path(path_lst[0])
                try:
                    path_old_mov = p.rename(Path(p.parent, f"{movie[0][0]}{p.suffix}"))
                except FileNotFoundError as e:
                    logging.info(e)
                movs = movie[0][0].replace(".", " ")

                new_path = path_mov + "/" + movs + "/" + movs + f"{p.suffix}"

                if not os.path.exists(path_mov + "/" + movs):
                    os.makedirs(path_mov + "/" + movs.title())

                    copyfile(path_old_mov, new_path)
                    send2trash(path_old_mov)
                    logging.info(f"{movs} was add to: {new_path}")
                    update_plexapi()
                    print("\n Done")
                    logging.info("Done")

    if removed:
        logging.info(f"Removed: {removed}")
    before = after
