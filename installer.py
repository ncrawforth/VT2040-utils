import socket, ssl
def install(filename):
  a = socket.getaddrinfo("raw.githubusercontent.com", 443)[0][-1]
  s = socket.socket()
  s.connect(a)
  ssl.wrap_socket(s)
  s.write("GET /ncrawforth/VT2040-utils/main/" + filename + " HTTP/1.0\r\nHost: raw.githubusercontent.com\r\n\r\n")
  d = s.read()
  s.close()
  f = open(filename, "w")
  f.write(d.decode().split("\r\n\r\n")[-1])
  f.close()
