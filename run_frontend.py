"""
Simple HTTP Server for the Doctor Recommendation Frontend
Run this to serve the HTML/CSS/JS files
"""

import http.server
import socketserver
import os

PORT = 7777
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = os.path.join(BASE_DIR, 'demo_ui')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("="*80)
        print("DOCTOR RECOMMENDATION FRONTEND - RUNNING")
        print("="*80)
        print(f"\n✅ Open your browser and go to:")
        print(f"   👉 http://localhost:{PORT}")
        print(f"\n📁 Serving files from: {DIRECTORY}")
        print(f"\n⚠️  Make sure the API is running on http://localhost:5000")
        print(f"    (Run: python doctor_api.py in a separate terminal)")
        print(f"\n📝 Press Ctrl+C to stop the server")
        print("="*80 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✋ Server stopped!")
