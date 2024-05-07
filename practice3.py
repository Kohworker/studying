from http.server import HTTPServer, BaseHTTPRequestHandler


HOST = "localhost"
PORT = 1234

class ServerHTTPRequestHandler(BaseHTTPRequestHandler):
    #do_GET
    #do_POST
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Thanks for the get".encode())
        self.path
        return "stub"
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        msg_len = int(self.headers["Content-Length"])
        msg = self.rfile.read(msg_len).decode()
        self.wfile.write("Thanks for the post with data {}".format(msg).encode())
        return "stub"



server = HTTPServer((HOST, PORT), ServerHTTPRequestHandler)
server.serve_forever()
