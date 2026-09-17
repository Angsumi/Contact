import http.server
import socketserver
import json
import csv
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADERS = [
    "First Name", "Middle Name", "Last Name", "Phonetic First Name", "Phonetic Middle Name", "Phonetic Last Name",
    "Name Prefix", "Name Suffix", "Nickname", "File As", "Organization Name", "Organization Title",
    "Organization Department", "Birthday", "Notes", "Photo", "Labels", "E-mail 1 - Label", "E-mail 1 - Value",
    "E-mail 2 - Label", "E-mail 2 - Value", "Phone 1 - Label", "Phone 1 - Value", "Phone 2 - Label",
    "Phone 2 - Value", "Address 1 - Label", "Address 1 - Formatted", "Address 1 - Street", "Address 1 - City",
    "Address 1 - PO Box", "Address 1 - Region", "Address 1 - Postal Code", "Address 1 - Country",
    "Address 1 - Extended Address", "Relation 1 - Label", "Relation 1 - Value", "Website 1 - Label",
    "Website 1 - Value", "Custom Field 1 - Label", "Custom Field 1 - Value"
]

class ContactsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/save_csv':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                contacts = data.get('contacts', [])
                
                # Write to data/contacts.csv
                csv_path_main = os.path.join(DIRECTORY, 'data', 'contacts.csv')
                
                with open(csv_path_main, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=HEADERS, extrasaction='ignore')
                    writer.writeheader()
                    for c in contacts:
                        writer.writerow(c)

                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {'status': 'ok', 'saved_count': len(contacts)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ContactsHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    run()
