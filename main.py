import re
import os
from pathlib import Path
import shutil
import logging
import time

# TODO send hook to plex to re search
logging.basicConfig(filename='log films.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(message)s')

extensions = ["avi", "mkv", "mp4"]
paths = "/Users/eysteingulbrandsen/Downloads/test"
path_tv = "/Volumes/homes/plex/TV Shows"
path_mov = "/Volumes/homes/plex/Movies"

before = dict([(f, None) for f in os.listdir(paths)])

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
            """, name, re.VERBOSE)
            if tv:
                p = Path(path_lst[0])
                path_old_tv = p.rename(Path(p.parent, f"{tv[0][0]}.S{tv[0][1]}E{tv[0][2]}{p.suffix}"))
                for path, subdirs, files in os.walk(f"{path_tv}"):
                    if tv[0][0].replace(".", " ") in subdirs:
                        tvs = tv[0][0].replace(".", " ")
                        season = tv[0][1]
                        if season[0] == '0':
                            season.replace("0", "")
                        new_path = path_tv \
                                   + "/" \
                                   + tvs \
                                   + "/" \
                                   + "Season " + season + "/" \
                                   + f"{tv[0][0]}.S{tv[0][1]}E{tv[0][2]}{p.suffix}"
                        break
                if new_path is None:
                    pass  # TODO make new dirr
                shutil.move(path_old_tv, new_path)
                logging.info(f"{tvs} was add to: {new_path}")
                # print(new_path)

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
                    shutil.move(path_old_mov, new_path)
                    logging.info(f"{movs} was add to: {new_path}")

    if removed:
        logging.info(f"Removed: {removed}")
    before = after
