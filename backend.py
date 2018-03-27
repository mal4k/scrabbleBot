import server
import validator
import board
import socketserver


PORT = 7999

server = socketserver.TCPServer(("", PORT), server.MyHandler)
print("serving at http://localhost:" + str(PORT))
server.serve_forever()