from _datetime import datetime

start = datetime.now()
y = 0
for x in range(1 << 25):
    y += x
end = datetime.now()
print()
print(str(end-start))
