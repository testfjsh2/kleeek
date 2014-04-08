import SocketServer

cross = """<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="*" /></cross-domain-policy>"""
HOST = ''
PORT = 843

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            print "%s wrote:" % self.client_address[0]
            print self.data
            if '<policy-file-request/>' in self.data:
                print 'received policy'
                conn.send(cross + '\0')

def main():
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()