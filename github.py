import json, binascii, socket, ssl

def _loadconf():
  conf = json.load(open("github.json"))
  username = conf["username"]
  token = conf["token"]
  repo = conf["repo"]
  auth = binascii.b2a_base64(username + ":" + token).decode().strip()
  return username, repo, auth

def _socket():
  a = socket.getaddrinfo("api.github.com", 443)[0][-1]
  s = socket.socket()
  s.connect(a)
  return ssl.wrap_socket(s)

def list():
  username, repo, auth = _loadconf()
  s = _socket()
  s.write("GET /repos/" + username + "/" + repo + "/contents/ HTTP/1.0\r\n")
  s.write("Host: api.github.com\r\n")
  s.write("User-Agent: VT2040-utils\r\n")
  s.write("Authorization: Basic " + auth + "\r\n\r\n")
  while s.readline() != b"\r\n": pass
  d = json.load(s)
  s.close()
  for f in d:
    print(f["name"])

def get(filename):
  username, repo, auth = _loadconf()
  s = _socket()
  s.write("GET /repos/" + username + "/" + repo + "/contents/" + filename + " HTTP/1.0\r\n")
  s.write("Host: api.github.com\r\n")
  s.write("User-Agent: VT2040-utils\r\n")
  s.write("Authorization: Basic " + auth + "\r\n\r\n")
  while s.readline() != b"\r\n": pass
  d = json.load(s)
  s.close()
  if "encoding" in d and d["encoding"] == "base64":
    f = open(filename, "w")
    f.write(binascii.a2b_base64(d))
    f.close()
    print(filename + " downloaded.")
  else:
    print("An error occurred.")
    print(d)

def put(filename, message):
  username, repo, auth = _loadconf()
  s = _socket()
  s.write("GET /repos/" + username + "/" + repo + "/contents/ HTTP/1.0\r\n")
  s.write("Host: api.github.com\r\n")
  s.write("User-Agent: VT2040-utils\r\n")
  s.write("Authorization: Basic " + auth + "\r\n\r\n")
  while s.readline() != b"\r\n": pass
  d = json.load(s)
  s.close()
  sha = None
  for f in d:
    if f["name"] == filename:
      sha = f["sha"]
      break
  s = _socket()
  d = json.dumps({"message": message, "sha": sha, "content": binascii.b2a_base64(open(filename).read())})
  s.write("PUT /repos/" + username + "/" + repo + "/contents/" + filename + " HTTP/1.0\r\n")
  s.write("Host: api.github.com\r\n")
  s.write("User-Agent:VT2040-utils\r\n")
  s.write("Content-Length: " + str(len(d)) + "\r\n")
  s.write("Authorization: Basic " + auth + "\r\n\r\n")
  s.write(d)
  while s.readline() != b"\r\n": pass
  d = json.load(s)
  s.close()
  print(d)
