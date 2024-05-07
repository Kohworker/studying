from typing import List
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

SERVER = "localhost"
PORT = 4444

class NamesHTTPServer(BaseHTTPRequestHandler):
    names_dict = {}

    def add_name(self, name: str, age: int) -> bool:
        if name not in self.names_dict:
            self.names_dict[name] = age
            return True
        else: 
            return False

    def get_names_with_age(self, age: int) -> List[str]:
        output = []
        for name, age_ in self.names_dict.items():
            if age_ == age:
                output.append(name)
        return output

    def do_GET(self):
        if self.path == '/':
            self.send_response(200, "Success")
            self.end_headers()
            self.wfile.write("Dictionary : {}\n".format(self.names_dict).encode())
        elif self.path.startswith('/names'):
            age = None
            if "?" in self.path:
                query_string = self.path.split("?")[1]
                params = {param.split("=")[0]: param.split("=")[1] for param in query_string.split("&")}
                if 'age' in params:
                    age = int(params['age'])
            names_list = list(self.names_dict.keys())
            if age is not None:
                names_list = self.get_names_with_age(age)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Names : {}\n".format(names_list).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Endpoint not found\n".encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data)
        name = json_data["name"]
        age = json_data["age"]
        if self.add_name(name, age):
            self.send_response(201)
            self.end_headers()
            self.wfile.write("Name added successfully\n".encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Name already exists\n".encode())

http_server = HTTPServer((SERVER, PORT), NamesHTTPServer)

print("Starting the server on http://{}:{}".format(SERVER, PORT))
http_server.serve_forever()
