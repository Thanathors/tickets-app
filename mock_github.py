"""Test helper: a tiny stand-in for the GitHub Contents API, serving the app too.

    python mock_github.py [seed.json]   ->  http://localhost:8766/
In the app's Settings > Advanced set API URL to http://localhost:8766 (any owner/repo/token).
"""
import base64, hashlib, json, sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

HERE = Path(__file__).parent
FILES = {}  # path -> bytes

def sha(b): return hashlib.sha1(b).hexdigest()

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send(self, code, body=b"", ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self): self.send(204)

    def path_of(self):
        p = self.path.split("?")[0]
        return p.split("/contents/", 1)[1] if "/contents/" in p else None

    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/__file":  # test hook: raw file
            return self.send(200, FILES.get("tickets.json", b""))
        f = self.path_of()
        if f is None:
            name = {"/": "index.html"}.get(p, p.lstrip("/"))
            fp = HERE / name
            if fp.is_file() and fp.suffix in (".html", ".svg", ".webmanifest"):
                ct = {".html": "text/html", ".svg": "image/svg+xml", ".webmanifest": "application/manifest+json"}[fp.suffix]
                return self.send(200, fp.read_bytes(), ct)
            return self.send(404, b"{}")
        if f not in FILES: return self.send(404, b'{"message":"Not Found"}')
        b = FILES[f]
        self.send(200, json.dumps({"sha": sha(b), "content": base64.encodebytes(b).decode()}).encode())

    def do_PUT(self):
        f = self.path_of()
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if f == "__external":  # test hook: simulate another device writing
            FILES["tickets.json"] = base64.b64decode(body["content"])
            return self.send(200, b"{}")
        if f == "__drop":
            FILES["__drop"] = b"1"
            return self.send(200, b"{}")
        cur = FILES.get(f)
        if cur is not None and body.get("sha") != sha(cur):
            return self.send(409, b'{"message":"sha mismatch"}')
        FILES[f] = base64.b64decode(body["content"])
        if FILES.pop("__drop", None):  # test hook: save, then lose the reply
            self.close_connection = True
            return
        print("commit:", body["message"].encode("ascii", "replace").decode(), flush=True)
        self.send(200, json.dumps({"content": {"sha": sha(FILES[f])}}).encode())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        FILES["tickets.json"] = Path(sys.argv[1]).read_bytes()
        dl = Path(sys.argv[1]).with_name("devlog.json")
        if dl.is_file(): FILES["devlog.json"] = dl.read_bytes()
    ThreadingHTTPServer(("127.0.0.1", 8766), H).serve_forever()
