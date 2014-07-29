#!/usr/bin/env python

from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import json
import os
import sys

ALL_APPS = 'all'

def parse_path(path):
    """Parse URL path into API components
    """

    parts = path.split('/')

    if parts[1] != 'api' or len(parts) != 5:
        return None

    return {'version': parts[2],
            'resource': parts[3],
            'action': parts[4]}

def check_directory(name):
    """Check if the app directory exists in the current working directory
    """

    if name == ALL_APPS:
        return True
    else:
        return os.path.exists(name)

def stop_demo():
    os.system('killall -9 java')

def perform_action(name, action):
    """Perform the action in the demo application directory.
    Also terminates any running application.
    """

    if action == 'demo':
        stop_demo()
        # start the demo
        os.system('cd %s && ./run.sh demo &' % name)
        return True
    elif action == 'stop':
        stop_demo()
        return True
    else:
        return False

class SimpleRestHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        """The API path has the form /api/version/appname/action
        """

        api_req = parse_path(self.path)
        err_code = 200
        # response contains either the dashboard location or an error message
        resp = dict()

        if api_req == None or api_req['version'] != '0.1':
            err_code = 400
        else:
            if not check_directory(api_req['resource']):
                err_code = 404
                resp['error'] = '%s is not a valid app name' % api_req['resource']
            if not perform_action(api_req['resource'], api_req['action']):
                err_code = 400
                resp['error'] = 'Failed to %s %s' % (api_req['action'], api_req['resource'])

            if err_code == 200 and api_req['resource'] != ALL_APPS:
                resp['location'] = '/%s/web' % api_req['resource']

        self.send_response(err_code)
        self.send_header('Content-Type', self.extensions_map['.json'])
        self.end_headers()

        self.wfile.write(json.dumps(resp))
        self.wfile.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Usage: %s port' % sys.argv[0]
        sys.exit(-1)

    httpd = SocketServer.TCPServer(("", int(sys.argv[1])), SimpleRestHandler)
    print "Serving at port", sys.argv[1]
    httpd.serve_forever()
