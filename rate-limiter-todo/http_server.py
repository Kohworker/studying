from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import time
import threading


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    #System can do GET 6 times per 5 minutes before being rate limited
    #System can POST 3 times per 5 minutes before being rate limited
    #Users can GET 4 times per 5 minutes before being rate limited
    #Users can POST 2 times per 5 minutes before being rate limited

    #System GET tokens and POST tokens
    #Users GET tokens and POST tokens

    #Tokens left = [GET, POST]
    #{users : [GET, POST] tokens_left}

    #refill function that refills every 5 minutes
    sys_tokens = [6, 3]
    users = {}
    users_get_refill = 4
    users_post_refill = 2
    dummy_db = []

    def refresh_tokens(self):
        while True:
            print("Refreshing tokens")
            self.sys_tokens = [6, 3]
            for i in self.users:
                self.users[i] = [self.users_get_refill, self.users_post_refill]
            time.sleep(15) 

    def check_tokens(self, command: str) -> bool:
        rate_limited = False
        if command == "GET":
            for i in self.users:
                if int(self.users[i][0]) <= 0:
                    print("user is rate limited")
                    rate_limited = True
            if self.sys_tokens[0] <= 0:
                rate_limited = True
        elif command == "POST":
            for i in self.users:
                if int(self.users[i][1]) <= 0:
                    rate_limited = True
            if self.sys_tokens[1] <= 0:
                rate_limited = True
        return rate_limited
    
    # Handler for the GET requests
    def do_GET(self):
        
        client_id = self.client_address

        if not self.check_tokens(client_id, "GET"):
            if client_id in self.users:
                self.users[client_id][0] -= 1
            else : 
                self.users[client_id] = [self.users_get_refill - 1, self.users_post_refill]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("sys tokens : {} user tokens : {}".format(self.sys_tokens, self.users).encode())  # Response message
            self.sys_tokens[0] -= 1
        else:
            self.send_response(429)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("You've been rate limited! sys tokens : {} user tokens : {}".format(self.sys_tokens, self.users).encode())

    # Handler for the GET requests
    def do_POST(self):
        
        client_id = self.client_address

        if not self.check_tokens(client_id, "POST"):
            if client_id in self.users:
                self.users[client_id][1] -= 1
            else : 
                self.users[client_id] = [self.users_get_refill, self.users_post_refill - 1]
            
            self.dummy_db.append(time.strftime('%H:%M:%S', time.localtime()))

            self.send_response(201)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("dummy_data : {}, sys tokens : {} user tokens : {}".format(self.dummy_db, self.sys_tokens, self.users).encode())  # Response message
            self.sys_tokens[1] -= 1
        else:
            self.send_response(429)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("You've been rate limited! sys tokens : {} user tokens : {}".format(self.sys_tokens, self.users).encode())


# Define the server address and port
server_address = ('localhost', 3333)  # Empty string means listen on all interfaces

# Create an instance of the HTTP server
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# Start the server
print('Server running on port 3333...')
refresh_thread = threading.Thread(target=httpd.RequestHandlerClass.refresh_tokens, args=(httpd.RequestHandlerClass,))
refresh_thread.start()
httpd.serve_forever()