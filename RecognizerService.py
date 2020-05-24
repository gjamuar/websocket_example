import os
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from config import FingerprintDirectory, RecordingTime
import dejavu.decoder as decoder
from config import ChunksTime,NumberOfChannels,MicChunkTime
import json

class RecognizerService:

    def __init__(self, database_path):
        self.database_path = database_path
        self.dburl = os.getenv('DATABASE_URL', 'sqlite:///' + self.database_path)
        self.djv = Dejavu(dburl=self.dburl)

    def recognize(self, filename, dir='uploads/'):
        str_path = dir + filename
        return self.recognize_file_path(str_path)

    def finger_print(self, filename_path):
        self.djv.fingerprint_file(filename_path)
        return self.recognize_file_path(filename_path)

    def recognize_file_path(self, file_path):
        match_list = self.djv.recognize(FileRecognizer, file_path)
        result = list(match_list)
        return result

    def recognize_stream(self, filename, dir='uploads/'):
        str_path = dir + filename
        return self.stream_recognize_file_path(str_path)

    def stream_recognize_file_path(self, file_path):
        match_list = self.djv.recognize(FileRecognizer, file_path)
        return match_list
        # for match in match_list:
        #     yield match

    def nonblocking_recognize_file_path(self, file_path,ws):
        r = FileRecognizer(self.djv)
        frames, r.Fs = decoder.read_chunks(file_path, r.dejavu.limit)
        for i, val in enumerate(frames):
            match = r._recognize(*val)
            if match is not None:
                match['segment_id'] = i
                match['start_time'] = i * ChunksTime / 1000
                ws.write_message(json.dumps(match))
            else:
                ws.write_message(json.dumps({}))
