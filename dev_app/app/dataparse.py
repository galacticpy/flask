import csv

file = 'app/test_data.txt'
#file = 'app/static/ulta/product_data.txt'


count = 0
with open(file) as f:
  line = f.readline()
  for lines in f:
  	count+=1
column_length = len(line.split())
cl = column_length
row_length = count
rl = row_length

data_parse = list(csv.reader(open(file, 'rb'), delimiter='\t'))
dp = data_parse
d =dict()	

fields = dp[0]

def tick():
	dp = data_parse
	rl = row_length
	icount = 1
	lst =[]
	while rl > 0:
	  line = dp[icount][count]
	  lst.append("".join([ch for ch in line if ord(ch)<= 128])) #lst.append(line)
	  rl = rl - 1
	  icount+=1
	d[field] = lst

count = 0
for field in fields:
	tick()
	cl = cl -1
	count+=1


