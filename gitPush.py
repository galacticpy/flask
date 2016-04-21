import os
import sys
comment = sys.argv

print 'Adding Files to Git'
os.system('git add .')
print 'Commiting Files to Git'
os.system('git commit -m'+comment[1])
print 'Pushing Files to Heroku'
os.system('git push https://github.com/galacticpy/flask.git master')
