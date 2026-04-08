from http.server import BaseHTTPRequestHandler
import json
import subprocess
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Запустить MCP сервер как subprocess
        result = subprocess.run(
            ['python', '-m', 'garmin_workouts_mcp'],
            input=post_data,
            capture_output=True,
            env={
                'GARMIN_EMAIL': os.getenv('GARMIN_EMAIL'),
                'GARMIN_PASSWORD': os.getenv('GARMIN_PASSWORD')
            }
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(result.stdout)
        
    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
