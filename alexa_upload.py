import numpy as np
from alexa import Alexa
from precheck import stream_alexa
from multiprocessing import Pool
import argparse
import sys
import time
import datetime

def uploader(id, times=1, fps=24):
    start = time.time()
    frames = 0
    uploads = 0
    for i in range(times):
        f, u = stream_alexa('video.avi', id)
        frames += f
        uploads += u
        end = time.time() - start
    return end, id, frames/fps, uploads
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_nodes', type=int, default=1,
                        help='number of alexa nodes uploading')
    parser.add_argument('--loops', type=int, default=1,
                        help='number of alexa nodes uploading')
    args = parser.parse_args()
    p = Pool(args.num_nodes)
    print(datetime.datetime.now())
    for x in p.imap_unordered(uploader, range(args.num_nodes)):
        print('Alexa {} finished {} long video in {} time with {} uploads'.format(x[1], x[2], x[0], x[3]))