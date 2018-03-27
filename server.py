from http.server import BaseHTTPRequestHandler
from os import curdir, sep
import validator
import json


class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self, ending="html"):
        self.send_response(200)
        if ending == "js":
            self.send_header('Content-type', 'application/javascript')
        elif ending == "css":
            self.send_header('Content-type', 'text/css')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            f = open(curdir + sep + self.path + "index.html", 'rb')
        else:
            f = open(curdir + sep + self.path, 'rb')
        self._set_headers(self.path.split(".")[-1])
        self.wfile.write(f.read())
        f.close()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        length = int(self.headers['content-length'])
        data_json = self.rfile.read(length)
        data = json.loads(data_json)
        if data['do'] == "analyze":
            board = []
            for i in range(len(data.keys()) - 4):
                board.append(data[str(i)])
            print(data["duden"])
            result = validator.play_hands_on_board(board, data["hand"], int(data["max-results"]), data["duden"])
            print(result)
        self.wfile.write(b'HTTP/1.0 200 OK\r\nContent-Length: 11\r\nContent-Type: text/html; charset=UTF-8\r\n\r\nHello World\r\n')


