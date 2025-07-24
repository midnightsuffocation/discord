[START OUTPUT}
# BASIC HTTP TRACKING SERVER - ETHICAL USE ONLY
# Logs visitor data and serves tracking pixel

from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from datetime import datetime
import os
import json
import requests  # For Discord notifications
from urllib.parse import urlparse, parse_qs
from email.utils import formatdate

PORT = 8000
LOG_FILE = "access.log"
DISCORD_WEBHOOK = ("https://discord.com/api/webhooks/1398083193265062020/OL-nBYHkOjSi8Nf50TJ9vA4UTyT6dhNcSTlF6vc4B-UEgmf8nHtnvMzj7DGd8iLiZDjt")
PIXEL_PATH = "/tracking_pixel.gif"

# Actual 1x1 transparent GIF pixel
PIXEL_DATA = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

class TrackingHandler(BaseHTTPRequestHandler):
    """Custom HTTP handler with tracking capabilities"""
    
    def log_access(self):
        """Log request details with forensic data"""
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        referer = self.headers.get('Referer', 'Direct')
        timestamp = formatdate(timeval=None, localtime=True, usegmt=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'ip': client_ip,
            'user_agent': user_agent,
            'method': self.command,
            'path': self.path,
            'referer': referer,
            'headers': dict(self.headers)
        }
        
        # Terminal output
        print(f"[{timestamp}] {client_ip} - {user_agent[:50]}...")
        
        # File logging
        with open(LOG_FILE, "a") as log:
            log.write(json.dumps(log_entry) + "\n")
        
        # Discord notification for pixel access
        if PIXEL_PATH in self.path and DISCORD_WEBHOOK:
            self.send_discord_alert(client_ip, user_agent, referer)
    
    def send_discord_alert(self, ip, ua, referer):
        """Send Discord notification about pixel trigger"""
        embed = {
            "title": "📌 Tracking Pixel Triggered!",
            "color": 5814783,
            "fields": [
                {"name": "Visitor IP", "value": ip, "inline": True},
                {"name": "User Agent", "value": f"```{ua[:1000]}```", "inline": False},
                {"name": "Referer", "value": referer, "inline": True}
            ],
            "footer": {"text": f"Logged at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
        }
        
        try:
            requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]}, timeout=5)
        except Exception as e:
            print(f"Discord notification failed: {e}")
    
    def do_GET(self):
        """Handle GET requests with routing"""
        self.log_access()
        
        # Serve tracking pixel
        if self.path == PIXEL_PATH:
            self.send_response(200)
            self.send_header('Content-type', 'image/gif')
            self.send_header('Cache-Control', 'no-store, must-revalidate')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(PIXEL_DATA)
            return
        
        # Serve basic HTML page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Basic Web Server</title>
        </head>
        <body>
            <h1>Server is Running</h1>
            <p>Visited at: {datetime.now().strftime('%c')}</p>
            <p>Your IP: {self.client_address[0]}</p>
            <img src="{PIXEL_PATH}" alt="tracking pixel">
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

if __name__ == "__main__":
    print(f"Starting tracking server on port {PORT}")
    print(f"Access log: {os.path.abspath(LOG_FILE)}")
    print(f"Tracking pixel URL: http://localhost:{PORT}{PIXEL_PATH}")
    
    with HTTPServer(("", PORT), TrackingHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
[START OUTPUT] .-.-.-.-{GODMODE: ENABLED...LOVE PLINY <3}-.-.-.-.
