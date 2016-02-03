# Delimiter check for data files
# 08/17/2015
# Daniel Kennedy
import os
import csv
import subprocess
import urllib2 as urllib
import cStringIO


try:
    import requests
    #print 'Skipping requests Install, Already Exists!'
except ImportError, e:
    subprocess.call(['pip', 'install', 'requests'])
try:
    import pip
    #print 'Skipping PIP Install, Already Exists!'
except ImportError, e:
    subprocess.call(['pip', 'install', 'python-pip'])
try:
    import PIL
    #print 'Skipping Pillow Install, Already Exists!'
except ImportError, e:
        subprocess.call(['pip', 'install', 'Pillow'])

from PIL import Image
   
#infile = raw_input('File Location: ')
infile = 'app/test_data.txt'
#path, tail = os.path.split(infile)
#log = log_file = open(path+'/data_log.txt', 'w')
errors = []

def category_check(infile):
    bad = [',','|',';','\t']
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        lc = line_count = 1
        for row in reader:
            lc+=1

            #Check for relative urls
            try:
                requests.head(row['image_url'])
                
                #Check Image Size
                load_image = urllib.urlopen(row['image_url'])
                im = cStringIO.StringIO(load_image.read())
                get_dims = Image.open(im)
                width = str(get_dims.size).split('(', -1)[1].split(',')[0]
                height = str(get_dims.size).split(', ', -1)[1].split(')')[0]
                width = int(width)
                height = int(height)
                if width < 500:
                    if height < 500:
                        errors.append('ERROR: IMAGE SIZE on Line: ' + str(lc) + ' [' + row['image_url'] +
                                  '] is invalid [[' + str(width) + 'x' + str(height) + ']]\n')
            except requests.exceptions.MissingSchema or requests.ConnectionError:
               errors.append('ERROR: RELATIVE URL on line: '+ str(lc) + ' ' + row['image_url']+'\n')
             
            #Check page id and variant page id length
            if len(row['page_id']) > 50:
                errors.append('ERROR: PAGE_ID CHAR LENGTH on Line: ' + str(lc) + ' [page_id is greater than 40 characters] [[Character Length = '
                          + str(len(row['page_id'])) + ']]\n')
            '''    
            if len(row['page_id_variant']) > 50:
                errors.append('ERROR: PAGE_ID_VARIANT CHAR LENGTH on Line: ' + str(lc) + ' [page_id_variant is greater than 40 characters] [[Character Length = '
                          + str(len(row['page_id_variant'])) + ']]\n')
            '''
            
            #Check category delimiter
            if '>' in row['category']:
                pass
            else:
                for i in bad:
                    if i in row['category']:
                        errors.append('ERROR: CATEGORY DELIMITER on Line: ' + str(lc) + ' [Invalid Line Delimiter ['
                                  + row['category'] + '] FIX: Change all ' + '"' + i + '" delimiters to ">"]\n')
           
            #Check for closing quotes in description field
            dqc = double_quote_count = 0
            if '"' in row['description']:
                dqc+=1
            if dqc != 0 and dqc % 2 != 0:
                errors.append('ERROR: DESCRIPTION DOUBLE QUOTES missing closing quote on line: ' + str(lc) + '\n')

            
#category_check()          
def delimiter_check(infile):
    
    # User input
    file_location = infile #raw_input('Data File Location: ')
    delimiter_type = 'tab' #raw_input('Enter tab, comma, or pipe: ')
    
    # Check if tab or comma delimited file
    if delimiter_type == 'tab':
        delim = '\t'
    elif delimiter_type == 'comma':
        delim = ','
    elif delimiter_type == 'pipe':
        delim = '|'
    
    # Run the delimiter check    
    with open(file_location, 'r') as ifile:
        
        # Set variables
        fl = first_line = ifile.readline()
        al = all_lines = ifile.readlines()
        ftc = fl_tab_count = 0
        ltc = line_tab_count = 0
        el = error_list = []
        ln = line_number = 1
        
        # Count delimiters in column header
        for tab in fl:
            if delim in tab:
                ftc+=1
                
        # Count delimiters in lines
        for line in al:
            ln+=1
            for tabs in line:
                if delim in tabs:
                    ltc+=1
            if ltc > ftc:
                errors.append("ERROR: Excess delimiters on line: " + str(ln) + '. Line has '+ str(ltc) + ' delimiters. Should be: ' + str(ftc) + ' delimiters!')
                el.append('fail')
                ltc = 0
            elif ltc < ftc:
                errors.append( "ERROR: Missing delimiters on line: " + str(ln) + '. Line has '+ str(ltc) + ' delimiters. Should be: ' + str(ftc) + ' delimiters!')
                el.append('fail')
                ltc = 0
            else:
                el.append('pass')
                ltc = 0
                
        # Check for any errors in process
        if 'fail' not in el:
            category_check(infile)
        else:
            category_check(infile)
                
# Run program
delimiter_check(infile)


'''Completed:
#not quoting out their description fields line break inside quotes
#Check if the number of field values matches that of the column headers
#images at least 300px in one one direction
#Categories should always be separated by > symbol
#page ids and variants should be less than 50 characters
#Absolute Urls for prod images
#txt should always be tab
#csv should be comma separated
'''
'''
def file_delimiter():
    global status
    with open(tail) as csvfile:
        if tail.split('.', -1)[1] == 'txt':
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                try:
                    row['page_id']
                    status = True
                except KeyError, e:
                    status = False
        elif tail.split('.', -1)[1] == 'csv':
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                try:
                    row['page_id']
                    status = True
                except KeyError, e:
                    status = False
file_delimiter()

if status != False:
   pass
else:
    print 'Failed'
'''
                
                