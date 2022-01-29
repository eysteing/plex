import os
from io import BytesIO
from tqdm import tqdm

# files = '/Users/eysteingulbrandsen/Downloads/test/SEAL.Team.S05E13.WEBRip.x264-ION10/SEAL.Team.S05E13.mp4'
# news = '/Users/eysteingulbrandsen/Downloads/SEAL.Team.S05E13.mp4'


def progressbar(file, new, text_in_front):
    fsize = int(os.path.getsize(file))
    with open(file, 'rb') as f:
        with open(new, 'ab') as n:
            with tqdm(ncols=100, total=fsize,
                      desc=f"{text_in_front}") as pbar:
                buffer = bytearray()
                while True:
                    buf = f.read(8192)
                    n.write(buf)
                    if len(buf) == 0:
                        break
                    buffer += buf
                    pbar.update(len(buf))
