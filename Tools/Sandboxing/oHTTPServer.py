import os, SimpleHTTPServer, SocketServer;

# This is fail if the server is already up and running
uPort = 28876;
os.chdir("ServerSideContent");

oHTTPServer = SocketServer.TCPServer(
  server_address = ("", uPort),
  RequestHandlerClass = SimpleHTTPServer.SimpleHTTPRequestHandler,
);

print "Please leave this process running during testing; it is a small web server used to serve loopback and intranet webpages.";
print "You can kill it after testing is completed, or leave it to be re-used in the next test run.";

oHTTPServer.serve_forever();