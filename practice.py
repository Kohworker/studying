# websocket or http server
from http.server import HTTPServer, BaseHTTPRequestHandler


address = "localhost"
port = 11111

class ServerHandlerClass(BaseHTTPRequestHandler):
    def do_GET(self) -> str:
        if self.path == '/':
            self.send_response(200, "Success")
            self.end_headers()
            self.wfile.write("Thanks for the GET call!\n".encode())
        elif self.path.startswith('/names'):
            print("{}".format(self.path))
            print("{}".format(self.path.split("?")[1:]))
            #After the ?, split to key/value with "=" and also split with &
            self.send_response(200, "Success")
            self.end_headers()
            self.wfile.write("Thanks for the GET to the names endpoint call!\n".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not supported! We can't do {}".format(self.path).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Thanks for the POST call!\n".encode())

server_i = HTTPServer((address, port), ServerHandlerClass)

print("Starting server")
server_i.serve_forever()
