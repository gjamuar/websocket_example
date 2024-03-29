import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 

https://os.mbed.com/cookbook/Websockets-Server
'''

from RecognizerService import RecognizerService
from config import DatabasePath, mode, FingerprintDirectory, RecordingTime
import json





class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('new connection')

    # def on_message(self, message):
    #     print('message received:  %s' % message)
    #     # Reverse Message and send it back
    #     print('sending back message: %s' % message[::-1])
    #     self.write_message(message[::-1])
    #     match_list = recognizer.stream_recognize_file_path("mp3/Brad-Sucks--Total-Breakdown.mp3")
    #     for match in match_list:
    #         self.write_message(json.dumps(match))

    def on_message(self, message):
        print('message received:  %s' % message)
        # Reverse Message and send it back
        print('sending back message: %s' % message[::-1])
        self.write_message(message[::-1])
        recognizer = RecognizerService(DatabasePath)
        recognizer.nonblocking_recognize_file_path("mp3/Brad-Sucks--Total-Breakdown.mp3",self)


    def on_close(self):
        print('connection closed')

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/ws', WSHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    # myIP = socket.gethostbyname(socket.gethostname())
    # print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
