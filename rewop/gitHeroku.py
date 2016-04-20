import os
print 'Adding Files to Git'
os.system('git add .')
print 'Commiting Files to Git'
os.system('git commit -m "fix"')
print 'Pushing Files to Heroku'
os.system('git push heroku master')