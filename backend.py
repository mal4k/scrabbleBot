import server
import validator
import board
import socketserver


PORT = 7999
try:
    server = socketserver.TCPServer(("", PORT), server.MyHandler)
    print("serving at http://localhost:" + str(PORT))
    server.serve_forever()
except OSError:
    print("Port is taken, try to use a free port")