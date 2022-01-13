from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
import json
import datetime

# Rudderstack's transformer (https://github.com/rudderlabs/rudder-transformer)
# didn't work on my M1 machine (neither locally nor on Docker, where it hangs
# without responding to requests) so I wrote this fake transformer, which responds
# with something useful enough to get rudderstack-server running locally.


class Decepticon(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(""))
        self.end_headers()
        self.wfile.write(b"")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        body = post_data.decode("utf-8")
        payload = json.loads(body)[0]
        message = payload.get("message")
        now = (
            datetime.datetime.utcnow()
            .replace(tzinfo=datetime.timezone.utc, microsecond=0)
            .isoformat()
        )
        message["receivedAt"] = now
        metadata = payload.get("metadata")
        columns = {key: "string" for key in message.keys()}
        message["metadata"] = {
            "receivedAt": now,
            "table": "tracks",
            "columns": columns,
        }  # metadata  # ???
        message["destination"] = payload.get("destination")
        output = {
            "output": message,
            "metadata": metadata,
            "statusCode": 200,
        }
        print(output)
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.send_header("apiVersion", "2")
        self.end_headers()
        self.wfile.write(bytes(json.dumps([output], sort_keys=True), "UTF-8"))


if __name__ == "__main__":
    httpd = HTTPServer(("127.0.0.1", 9090), Decepticon)
    httpd.serve_forever()
