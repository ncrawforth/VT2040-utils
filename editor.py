import sys, os

def edit(filename):
  def puts(*args):
    for s in args:
      sys.stdout.write(str(s))
  def getc():
    return ord(sys.stdin.read(1))

  # Load file into array
  f = open(filename, "r")
  lines = f.readlines()
  f.close()
  
  # Strip newlines, carriage returns, trailing whitespace, tabs
  for i in range(len(lines)):
    lines[i] = lines[i].rstrip().replace("\t", "  ")
  
  # Find out terminal dimensions
  puts("\x1bc\x1b[9999;9999f\x1b[6n")
  height = c = 0
  while c != 59:
    c = getc()
    if c > 47 and c < 58:
      height = height * 10 + c - 48
  width = c = 0
  while c != 82:
    c = getc()
    if c > 47 and c < 58:
      width = width * 10 + c - 48

  # Initialise cursor
  x = y = oldy = left = 0
  
  # Force redraw
  top = height
  
  # Main loop
  while True:
    puts("\x1b[?25l")
    if lines[-1] != "":
      lines.append("")
    if oldy != y and left != 0:
      left = 0
      puts("\x0d", lines[oldy][:width])
    oldy = y
    while y - top >= height: # Scroll up
      top += 1
      puts("\x1b[9999f\x1bD", lines[min(len(lines) - 1, top + height - 1)][:width])
    while y - top < 0: # Scroll down
      top -= 1
      puts("\x1b[f\x1bM", lines[min(len(lines) - 1, top)][:width])
    puts("\x1b[", 1 + y - top, "d")
    if min(x, len(lines[y])) - left >= width: # Scroll left
      amount = min(x, len(lines[y])) + 1 - left - width
      left += amount
      puts("\x0d\x1b[", amount, "P\x1b[", width + 1 - amount, "`", lines[y][left + width - amount:left + width])
    if min(x, len(lines[y])) - left < 0: # Scroll right
      amount = left - min(x, len(lines[y]))
      left -= amount
      puts("\x0d\x1b[", amount, "@", lines[y][left:left + amount])
    puts("\x1b[", 1 + min(len(lines[y]), x) - left, "`\x1b[?25h")
    c = getc()
    if c == 3: # Ctrl-C
      raise(KeyboardInterrupt)
    elif c == 4: # Ctrl-D
      break
    elif c == 9: # Tab
      lines[y] = lines[y][:min(x, len(lines[y]))] + "  " + lines[y][x:]
      x += 2
      puts("\x1b[2@")
    elif c == 10: # Enter
      x = min(x, len(lines[y]))
      lines.insert(y + 1, lines[y][x:])
      lines[y] = lines[y][:x]
      y += 1
      x = 0
      puts("\x1b[s\x1b[K")
      if y - top < height:
        puts("\x1b[B\x1b[L\x0d", lines[y][:width], "\x1bB")
    elif c == 27: # Escape
      getc()
      c = getc()
      if c == 65: # Cursor up
        y = max(0, y - 1)
      elif c == 66: # Cursor down
        y = min(len(lines) - 1, y + 1)
      elif c == 67: # Cursor right
        x = min(len(lines[y]), x + 1)
      elif c == 68: # Cursor left
        x = max(0, min(x, len(lines[y])) - 1)
      elif c == 49 or c == 72: # Home
        x = 0
      elif c == 51: # Delete      
        lines[y] = lines[y][:min(x, len(lines[y]))] + lines[y][x + 1:]
        puts("\x1b[P\x1b[9999C", lines[y][left + width - 1:left + width])
      elif c == 52 or c == 70: # End
        x = len(lines[y])
      elif c == 53: # Page up
        y = max(0, y + 1 - height)
      elif c == 54: # Page down
        y = min(len(lines) - 1, y + height - 1)
      while c > 47 and c < 58:
        c = getc()
    elif c > 31 and c < 127: # Printable
      x = min(x, len(lines[y])) + 1
      lines[y] = lines[y][:x - 1] + chr(c) + lines[y][x - 1:]
      puts("\x1b[@", chr(c))
    elif c == 127: # Backspace
      x = min(x, len(lines[y]))
      if x > 0:
        x -= 1
        lines[y] = lines[y][:min(x, len(lines[y]))] + lines[y][x + 1:]
        puts("\x08\x1b[P\x1b[9999C", lines[y][left + width - 1:left + width])
      elif y > 0:
        y -= 1
        x = len(lines[y])
        lines[y] += lines[y + 1]
        del(lines[y + 1])
        puts("\x1b[A\x0d", lines[y][:width])
        if y >= top:
          puts("\x1b[B\x1b[M\x1b[9999f", lines[min(len(lines) - 1, top + height - 1)][:width])
        else:
          top -= 1
  puts("\x1b[9999f\x1bD")
  os.rename(filename, filename + ".bak")
  f = open(filename, "w")
  f.write("\n".join(lines))
  f.close()
