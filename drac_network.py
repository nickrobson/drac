import socket, SocketServer, threading

import drac_config

class ForkedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        print data
        response = bytes("%s" % data)
        self.request.send(response)

class ForkedTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(message)
    response = sock.recv(1024)
    print "Received: %s" % response
    sock.close()

def setup(stdscr):

    stdscr.clear()

    HOST = drac_config.networked_server_ip
    PORT = drac_config.networked_server_port
    CONN = (HOST, PORT)

    if drac_config.networked_i_am_client:

        stdscr.addstr("Attempting to connect to %s:%s" % CONN)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(CONN)
            sock.send("drac_connect:")

            sock.close()
        except socket.error:
            stdscr.addstr("Error: Could not connect")
    else:
        server = ForkedTCPServer((HOST, PORT), ForkedTCPRequestHandler)

        server_thread = threading.Thread(target=server.serve_forever) # Process forking upon request
        server_thread.setDaemon(True) # Exit the server thread when the main thread terminates
        server_thread.start()

        addr = server.server_address

        stdscr.addstr("Server loop running in thread: %s" % server_thread.getName())
        stdscr.addstr("Running on %s:%s" % (addr[0], addr[1]))

        server.shutdown()

