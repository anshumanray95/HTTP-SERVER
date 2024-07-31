# # git_http_server
# import socket
# import threading
# import os
# import argparse

# #def handler(connection, address):
# def handler(connection, address, args):
#     data = connection.recv(1024)
#     if data:
#         start_line = data.decode().split("\r\n")[0]
#         method, path, version = start_line.split(" ")
#         headers = {}
#         for line in data.decode().split("\r\n")[1:]:
#             if line:
#                 key, value = line.split(": ")
#                 headers[key.lower()] = value
#             else:
#                 break                
#         print(method, path, version)
        
#         if method == "GET":
#             if path == "/":
#                 connection.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())
#             elif path.startswith("/echo"):
#                 message = path.split("/echo/")[1]
#                 length = len(message)
#                 connection.sendall(
#                     f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {length}\r\n\r\n{message}".encode()
#                 )
#             elif path == "/user-agent":
#                 message = headers["user-agent"]
#                 length = len(message)
#                 connection.sendall(
#                     f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {length}\r\n\r\n{message}".encode()
#                 )
#             elif path.startswith("/files"):
#                 filename = path.split("/files/")[1]
#                 if os.path.isfile(f"{args.directory}/{filename}"):
#                     content = open(f"{args.directory}/{filename}", "r").read()
#                     message = "HTTP/1.1 200 OK\r\n"
#                     message += f"Content-Type: application/octet-stream\r\n"
#                     message += f"Content-Length: {len(content)}\r\n"
#                     message += "\r\n"
#                     message += content
#                     connection.sendall(message.encode())
#                 else:
#                     connection.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
#             else:
#                 connection.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
#         elif method == "POST":
#             if path.startswith("/files"):
#                 filename = path.split("/files/")[1]
#                 content = data.decode().split("\r\n\r\n")[1]
#                 with open(f"{args.directory}/{filename}", "w") as f:
#                     f.write(content)
#                 connection.sendall("HTTP/1.1 201 Created\r\n\r\n".encode())                
#             else:
#                 connection.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())            

#         connection.close()

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--directory", type=str, help="the directory path")
#     args = parser.parse_args()

#     server_socket = socket.create_server(("localhost", 4221))

#     while True:
#         print("awaiting connection")
        
#         connection, address = server_socket.accept()
#         threading.Thread(target=handler, args=(connection, address, args)).start()
        
# if __name__ == "__main__":
#     main()

# import socket
# from threading import Thread
# import argparse
# from pathlib import Path
# RN = b"\r\n"
# def parse_request(conn):
#     d = {}
#     headers = {}
#     body = []
#     target = 0  # request
#     rest = b""
#     ind = 0
#     body_len = 0
#     body_count = 0
#     while data := conn.recv(1024):
#         if rest:
#             data = rest + data
#             rest = b""
#         if target == 0:
#             ind = data.find(RN)
#             if ind == -1:
#                 rest = data
#                 continue
#             # GET URL HTTP
#             line = data[:ind].decode()
#             data = data[ind + 2 :]
#             d["request"] = line
#             l = line.split()
#             d["method"] = l[0]  # GET, POST
#             d["url"] = l[1]
#             target = 1  # headers
#         if target == 1:
#             if not data:
#                 continue
#             while True:
#                 ind = data.find(RN)
#                 if ind == -1:
#                     rest = data
#                     break
#                 if ind == 0:  # \r\n\r\n
#                     data = data[ind + 2 :]
#                     target = 2
#                     break
#                 line = data[:ind].decode()
#                 data = data[ind + 2 :]
#                 l = line.split(":", maxsplit=1)
#                 field = l[0]
#                 value = l[1].strip()
#                 headers[field.lower()] = value
#             if target == 1:
#                 continue
#         if target == 2:
#             if "content-length" not in headers:
#                 break
#             body_len = int(headers["content-length"])
#             if not body_len:
#                 break
#             target = 3
#         if target == 3:
#             body.append(data)
#             body_count += len(data)
#             if body_count >= body_len:
#                 break
#     d["headers"] = headers
#     d["body"] = b"".join(body)
#     return d
# def req_handler(conn, dir_):
#     with conn:
#         d = parse_request(conn)
#         url = d["url"]
#         method = d["method"]
#         headers = d["headers"]
#         if url == "/":
#             conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
#         elif url.startswith("/echo/"):
#             body = url[6:].encode()
#             conn.send(b"HTTP/1.1 200 OK\r\n")
#             conn.send(b"Content-Type: text/plain\r\n")
#             if encoding := headers.get("accept-encoding", None):
#                 l = encoding.split(", ")
#                 if "gzip" in l:
#                     conn.send(b"Content-Encoding: gzip\r\n")
#             conn.send(f"Content-Length: {len(body)}\r\n".encode())
#             conn.send(RN)
#             conn.send(body)
#         elif url == "/user-agent":
#             body = d["headers"]["user-agent"].encode()
#             body = headers["user-agent"].encode()
#             conn.send(b"HTTP/1.1 200 OK\r\n")
#             conn.send(b"Content-Type: text/plain\r\n")
#             conn.send(f"Content-Length: {len(body)}\r\n".encode())
#             conn.send(RN)
#             conn.send(body)
#         elif url.startswith("/files/"):
#             file = Path(dir_) / url[7:]
#             if method == "GET":
#                 if file.exists():
#                     conn.send(b"HTTP/1.1 200 OK\r\n")
#                     conn.send(b"Content-Type: application/octet-stream\r\n")
#                     with open(file, "rb") as fp:
#                         body = fp.read()
#                     conn.send(f"Content-Length: {len(body)}\r\n".encode())
#                     conn.send(RN)
#                     conn.send(body)
#                 else:
#                     conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
#             elif method == "POST":
#                 with open(file, "wb") as fp:
#                     fp.write(d["body"])
#                 conn.send(b"HTTP/1.1 201 Created\r\n\r\n")
#             else:
#                 conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
#         else:
#             conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
# def main():
#     parser = argparse.ArgumentParser(description="socket server")
#     parser.add_argument(
#         "--directory", default=".", help="directory from which to get files"
#     )
#     args = parser.parse_args()  # args.directory
#     server_socket = socket.create_server(("localhost", 4221))
#     while True:
#         conn, _ = server_socket.accept()  # wait for client
#         # req_handler(conn)
#         Thread(target=req_handler, args=(conn, args.directory)).start()

# if __name__ == "__main__":
#     main()




import socket
import sys
import gzip
from concurrent.futures import ThreadPoolExecutor, process
from typing import List
from pathlib import Path
def process_conn(conn):
    with conn:
        init = conn.recv(4096)
        def parse_http(bs: bytes):
            lines: List[bytes] = []
            while not bs.startswith(b"\r\n"):
                sp = bs.split(b"\r\n", 1)
                if len(sp) == 2:
                    line, bs = sp
                    lines.append(line)
                else:
                    cont = conn.recv(4096)
                    bs += cont
            return lines, bs[2:]
        (start_line, *raw_headers), body_start = parse_http(init)
        headers = {
            parts[0]: parts[1]
            for rh in raw_headers
            if (parts := rh.decode().split(": "))
        }
        method, path, _ = start_line.decode().split(" ")
        match (method, path, path.split("/")):
            case ("GET", "/", _):
                conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
            case ("GET", _, ["", "echo", data]):
                body = data.encode()
                extra_headers = []
                encoding = headers.get("Accept-Encoding")
                if encoding is not None and "gzip" in {
                    s.strip() for s in encoding.split(",")
                }:
                    body = gzip.compress(body)
                    extra_headers.append(b"Content-Encoding: gzip\r\n")
                conn.send(
                    b"".join(
                        [
                            b"HTTP/1.1 200 OK",
                            b"\r\n",
                            *extra_headers,
                            b"Content-Type: text/plain\r\n",
                            b"Content-Length: %d\r\n" % len(body),
                            b"\r\n",
                            body,
                        ]
                    )
                )
            case ("GET", "/user-agent", _):
                body = headers["User-Agent"].encode()
                conn.send(
                    b"".join(
                        [
                            b"HTTP/1.1 200 OK",
                            b"\r\n",
                            b"Content-Type: text/plain\r\n",
                            b"Content-Length: %d\r\n" % len(body),
                            b"\r\n",
                            body,
                        ]
                    )
                )
            case ("GET", _, ["", "files", f]):
                target = Path(sys.argv[2]) / f
                if target.exists():
                    body = target.read_bytes()
                    conn.send(
                        b"".join(
                            [
                                b"HTTP/1.1 200 OK",
                                b"\r\n",
                                b"Content-Type: application/octet-stream\r\n",
                                b"Content-Length: %d\r\n" % len(body),
                                b"\r\n",
                                body,
                            ]
                        )
                    )
                else:
                    conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            case ("POST", _, ["", "files", f]):
                target = Path(sys.argv[2]) / f
                size = int(headers["Content-Length"])
                remaining = size - len(body_start)
                if remaining > 0:
                    body_rest = conn.recv(remaining, socket.MSG_WAITALL)
                else:
                    body_rest = b""
                body = body_start + body_rest
                target.write_bytes(body)
                conn.send(
                    b"".join(
                        [
                            b"HTTP/1.1 201 Created",
                            b"\r\n",
                            b"\r\n",
                        ]
                    )
                )
            case _:
                conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
def process_conn_with_exception(conn):
    try:
        process_conn(conn)
    except Exception as ex:
        print(ex)
def main():
    with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
        with ThreadPoolExecutor(max_workers=100) as executor:
            while True:
                (conn, _) = server_socket.accept()
                executor.submit(process_conn_with_exception, conn)
if __name__ == "__main__":
    main()