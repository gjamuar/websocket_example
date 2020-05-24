from __future__ import absolute_import
from __future__ import print_function
import os
import logging
import warnings
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    dburl = os.getenv('DATABASE_URL', 'sqlite://')
    djv = Dejavu(dburl=dburl)

    # Fingerprint all the mp3's in the directory we give it
    djv.fingerprint_directory("mp3", [".mp3"])

    # Recognize audio from a file
    song = djv.recognize(
        FileRecognizer, "mp3/Sean-Fournier--Falling-For-You.mp3"
    )
    print("From file we recognized: %s\n" % song)

    # Or recognize audio from your microphone for `secs` seconds
    secs = 5
    song = djv.recognize(MicrophoneRecognizer, seconds=secs)
    if song is None:
        print(
            "Nothing recognized -- did you play the song out loud so your mic could hear it? :)"
        )
    else:
        print("From mic with %d seconds we recognized: %s\n" % (secs, song))

    # Or use a recognizer without the shortcut, in anyway you would like
    recognizer = FileRecognizer(djv)
    song = recognizer.recognize_file(
        "mp3/Josh-Woodward--I-Want-To-Destroy-Something-Beautiful.mp3"
    )
    print("No shortcut, we recognized: %s\n" % song)
