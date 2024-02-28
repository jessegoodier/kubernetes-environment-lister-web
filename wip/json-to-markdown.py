import json
from json2html import *
import http.server
import socketserver

# Load the JSON data
with open('docs/index.json') as f:
    data = json.load(f)

# Convert the JSON data to HTML
html_data = json2html.convert(json = data,table_attributes="")

# Write the HTML data to a file
with open('docs/index1.html', 'w') as f:
    f.write(html_data)
PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
