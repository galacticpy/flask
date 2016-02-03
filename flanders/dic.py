dic = {}

passw = 'test'
dic[passw] = passw

for item in dic:
    if passw == item:
        newp = dic[item]
print newp

passw = 'test2'
dic[passw] = passw

for item in dic:
    if passw == item:
        newp = dic[item]
print newp

print dic