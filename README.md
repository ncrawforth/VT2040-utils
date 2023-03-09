# VT2040-utils
Small utilities to make a VT2040 serial terminal useful.

## installer.py
MicroPython module to download utilities from this GitHub repository.

To bootstrap:
``` python
>>> import socket, ssl
>>> a = socket.getaddrinfo("raw.githubusercontent.com", 443)[0][-1]
>>> s = socket.socket()
>>> s.connect(a)
>>> s = ssl.wrap_socket(s)
>>> s.write("GET /ncrawforth/VT2040-utils/main/installer.py HTTP/1.0\r\n")
57
>>> s.write("Host: raw.githubusercontent.com\r\n\r\n")
35
>>> d = s.read()
>>> s.close()
>>> f = open("installer.py", "w")
>>> f.write(d.decode().split("\r\n\r\n")[-1])
395
>>> f.close()
```

## editor.py
MicroPython text editor. Modeless  -  i.e. use cursor keys to move cursor, and type to insert text. Ctrl-D saves and quits, ctrl-C quits without saving.
``` python
>>> from installer import install
>>> install("editor.py")
>>> from editor import edit
>>> edit(<filename>)
```
### Limitations
* No tab support. Tabs are replaced with 2 spaces for now.
* Unicode probably doesn't work very well yet.
* There might still be file-corrupting bugs, so the original file is always backed up before saving.
