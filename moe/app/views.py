from flask import render_template, request, render_template, redirect, url_for, abort, flash
from werkzeug import secure_filename
from app import app
import csv




@app.route('/')
def index():
	return render_template('home.html')

@app.route('/daily')
def daily():
	csvfile = open('/Users/danielkennedy/dev/flask/moe/app/data/data.txt')
	reader = csv.DictReader(csvfile, delimiter='\t')
	print reader
	return render_template('daily.html', reader=reader)

		
				


	

