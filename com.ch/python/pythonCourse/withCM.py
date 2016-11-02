
#without context manager
f=open("new.txt","w")
print(f.closed)
f.write("hello world")
f.close()
print(f.closed)

#with context manager
with open("new.txt","w") as f:
  print(f.closed)
  f.write("hello world")
print(f.closed)
