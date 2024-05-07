from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer

import cgi
import json
import signal
import sys
import threading

class ServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.log_message("Ran a get command")
        self.send_response(200)

        #send header
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        

        message = "Thanks for running a get!\n"
        self.wfile.write(message.encode())
    
    def do_POST(self):
        self.log_message("Ran a POST command")
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data)

        self.send_response(200)

        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        response_data = {'Message' : "Got your json data", 'data' : json_data}
        self.wfile.write(json.dumps(response_data).encode())



def run(server_class=HTTPServer, handler_class=ServerHandler):
    server_address = ('localhost', 4444)
    httpd = server_class(server_address, handler_class)

    def signal_handler(signum, frame):
        print("Caught signal for {} --- closing server connection now...".format(signum))
        httpd.socket.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    httpd.serve_forever()


run()