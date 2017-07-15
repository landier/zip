#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import shutil

PORT_NUMBER = 8080
FILEPATH = '10M.dat'
GZIP_FILE_PATH = '10G.gzip'

#This class will handles any incoming request from
#the browser

class InfiniteHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", 'application/octet-stream')
        self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(FILEPATH)))
        # fs = os.fstat(f.fileno())
        # self.send_header("Content-Length", str(fs.st_size))
        self.end_headers()
        while True:
            with open(FILEPATH, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)
                # self.wfile.write(f.read())

class GZipBombHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", 'text/html')
        self.send_header('Content-Encoding', 'gzip')
        self.end_headers()
        with open(GZIP_FILE_PATH, 'rb') as f:
            # shutil.copyfileobj(f, self.wfile)
            self.wfile.write(f.read())


try:
	#Create a web server and define the handler to manage the
	#incoming request
    server = HTTPServer(('', PORT_NUMBER), GZipBombHandler)
    print('Started httpserver on port ', PORT_NUMBER)

	#Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
