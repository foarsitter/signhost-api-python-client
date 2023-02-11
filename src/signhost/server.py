# flake8: ignore
# mypy: ignore-errors

import http.server
import socketserver

from devtools import debug

from signhost.models import Transaction


PORT = 8000


class PostbackServer(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):  # noqa: N802
        self._set_headers()
        print("in post method")
        data_string = self.rfile.read(int(self.headers["Content-Length"]))

        self.send_response(200)
        self.end_headers()

        transaction = Transaction.parse_raw(data_string)

        print(f"received transaction: {transaction.Id}")

        with open(f"{transaction.Id}.json", "w") as outfile:
            outfile.write(data_string.decode("utf-8"))

        debug(transaction)

        return


with socketserver.TCPServer(("", PORT), PostbackServer) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
