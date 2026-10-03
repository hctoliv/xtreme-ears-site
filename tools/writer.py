import http.server, os, urllib.parse
OUT = os.path.join(os.getcwd(), "out")
os.makedirs(OUT, exist_ok=True)

class H(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        q = urllib.parse.urlparse(self.path)
        name = urllib.parse.parse_qs(q.query).get("name", ["x.jpg"])[0]
        name = os.path.basename(name)
        n = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(n)
        with open(os.path.join(OUT, name), "wb") as f:
            f.write(data)
        self.send_response(200); self.send_header("Content-Length","2"); self.end_headers()
        self.wfile.write(b"ok")
    def log_message(self, *a): pass

http.server.HTTPServer(("127.0.0.1", 4180), H).serve_forever()
