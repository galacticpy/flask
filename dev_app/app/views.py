from flask import render_template, request, render_template, redirect, url_for, abort, flash
from werkzeug import secure_filename
from app import app
import dataparse
import feed_check
from siteRip import scrape, full

import os
import sys
import csv
import random

data = dataparse
fc = feed_check

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/products.html')
def products():
    return render_template('products.html',
	product_url = data.d['product_url'],	
	page_id = data.d['page_id'],
	brand = data.d['brand'],
	name = data.d['name'],
	description = data.d['description'],
	image_url = data.d['image_url'],
	price = data.d['price'],
	#category = data.d['category'],
	#in_stock = data.d['in_stock'],
	#manufacturer_id = data.d['manufacturer_id'],
	#upc = data.d['upc'],
	#add_to_cart_link = data.d['add_to_cart_link'],
	#add_to_cart_link = data.d['add_to_cart_url'],
	#page_id_variant = data.d['page_id_variant'],
	rl = data.rl,)


@app.route('/<pageid>.html')
def product(pageid):
    return render_template('product_page.html',
	pageid = pageid,						   
	product_url = data.d['product_url'],	
	page_id = data.d['page_id'],
	brand = data.d['brand'],
	name = data.d['name'],
	description = data.d['description'],
	image_url = data.d['image_url'],
	price = data.d['price'],
	#category = data.d['category'],
	#in_stock = data.d['in_stock'],
	#manufacturer_id = data.d['manufacturer_id'],
	#upc = data.d['upc'],
	#add_to_cart_link = data.d['add_to_cart_link'],
	#add_to_cart_link = data.d['add_to_cart_url'],
	#page_id_variant = data.d['page_id_variant'],
	rl = data.rl,)

   
@app.route('/review.html')
def war():
    return render_template('review.html')


@app.route('/getclient', methods=['GET', 'POST'])
def getclient():
	if request.method == 'POST':		
		url = request.form['url']
		pageid = scrape(url)
		fulljs = full(url)
		location = fulljs.split('pwr/')[0]
		return render_template('client.html', pageid=pageid, fulljs=fulljs, location=location)				
	return render_template('getclient.html')

@app.route('/audio')
def audio():
    return render_template('audio.html')


@app.route('/datafile.txt')
def datafile():
    return url_for('static', filename='datafile.txt')
'''
UPLOAD_FOLDER = '/Users/danielkennedy/dev/flask/dev_app/app/data/'
ALLOWED_EXTENSIONS = set=(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
'''
@app.route('/feedchecker.html')
def feedcheck():
	#errors = ''
	#error = None
	'''
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			infile = UPLOAD_FOLDER+filename
			fc.delimiter_check(infile)
			errors = fc.errors
			return render_template('feedchecker.html', errors = errors,)
	'''
	return render_template('feedchecker.html', errors = fc.errors,)				
				


	

