from __future__ import absolute_import
from __future__ import print_function
import os
import logging
import warnings
import time
from itertools import repeat
import concurrent.futures
from config import DatabasePath,mode,FingerprintDirectory,RecordingTime

warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

if __name__ == '__main__':
    
    dburl = os.getenv('DATABASE_URL', 'sqlite:///'+DatabasePath)

    strpath = "mp3/Brad-Sucks--Total-Breakdown.mp3"
    t = time.time()

    djv = Dejavu(dburl=dburl)
    if( mode == 'fingerprint'):
        djv.fingerprint_directory( FingerprintDirectory, [".mp3"] )
    
    elif( mode == 'file' ):
        match_list =  djv.recognize( FileRecognizer, strpath )
        for match in match_list:
            print(match)

    elif( mode == 'mic' ):
        match_list = djv.recognize(MicrophoneRecognizer, RecordingTime)
        #print(match_list)
        for match in match_list:
            print(match)
    t2 = time.time() - t
    print(t2)
    