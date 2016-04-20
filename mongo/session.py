dic = {}
session = {}
usr_id = '543'
session['user'] = "dken"
session['pass'] = '123'
dic[usr_id] = session
user_id = '234'
session['user'] = "bill"
session['pass'] = 'bob'
dic[user_id] = session
print dic['234']['user']