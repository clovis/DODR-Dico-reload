#!/usr/bin/env python

## This script will parse all DAF dicos as well as reload them
## in MySQL. It will also rebuild the TLFI from the entry pickles.

## It will then process whatever dico(s) you give as an argument. 
## If you don't give arguments, it will process every dico.

import MySQLdb
import cPickle
import sys
import os
import re
import htmlentitydefs
from glob import glob


def convert(s):
    """Take an input string s, find all things that look like SGML character
    entities, and replace them with the Unicode equivalent.

    Function is from:
    http://stackoverflow.com/questions/1197981/convert-html-entities-to-ascii-in-python/1582036#1582036

    """
    matches = re.findall("&#\d+;", s)
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
            name = hit[2:-1]
            try:
                entnum = int(name)
                s = s.replace(hit, unichr(entnum))
            except ValueError:
                pass
    matches = re.findall("&\w+;", s)
    hits = set(matches)
    amp = "&"
    if amp in hits:
        hits.remove(amp)
    for hit in hits:
        name = hit[1:-1]
        if name in htmlentitydefs.name2codepoint:
            s = s.replace(hit,
                          unichr(htmlentitydefs.name2codepoint[name]))
    s = s.replace(amp, "&")
    return s


def dico_handler(dico):
    if dico == 'littre':
        dico_dict = parse_littre()
    elif dico == 'feraud':
        dico_dict = parse_feraud()
    elif dico == 'nicot':
        dico_dict = parse_nicot()
    elif dico == 'acad1694':
        dico_dict = parse_acad1694()
    elif dico == 'acad1762':
        dico_dict = parse_acad1762()
    elif dico == 'acad1798':
        dico_dict = parse_acad1798()
    elif dico == 'acad1835':
        dico_dict = parse_acad1835()
    elif dico == 'acad1932':
        dico_dict = parse_acad1932()
    print "Parsing done"
    daf_loader(dico, dico_dict)


def parse_acad1694():
    ## Body
    body = re.compile('<body>')
    ## Headword regex
    head = re.compile('<div1 type="entry')
    clean_head = re.compile('(?u)([^,]+),.+')
    clean_head2 = re.compile('\..*')
    find_ou = re.compile(' ou ')
    find_et = re.compile(' et ')

    ## entry regex
    definition = re.compile('</div1')

    my_data = glob(dico_path + 'academie/DAF1694*')

    dico = {}
    for chunk in my_data:
        headwords = []
        entry = ''
        begin = False
        for line in open(chunk.rstrip()):
            if body.search(line):
                begin = True
            if not begin:
                continue
            
            if head.search(line):
                my_match = re.search('<div1 type="entry" id="([^"]+)', line)
                headword = my_match.group(1).decode('utf-8').lower()
                headword = clean_head.sub('\\1', headword)
                headword = clean_head2.sub('', headword)
                headword = headword.replace('_', ' ')
                if find_ou.search(headword):
                    headwords = headword.split(' ou ')
                elif find_et.search(headword):
                    headwords = headword.split(' et ')
                else:
                    headwords = [headword,]
                for word in headwords:
                    if word not in dico:
                        dico[word] = []
                continue
            
            line = line.replace('</p>', '')
            line = line.replace('<p>', '<br>')
            
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('latin-1')
            if definition.search(line):
                entry = re.sub('^\s*<br>', '', entry)
                for word in headwords:
                    dico[word].append(entry)
                entry = ''
                continue
            
            entry += line

    return dico
    
    
def parse_acad1762():
    ## Body
    body = re.compile('<body>')
    ## Headword regex
    head = re.compile('<div1 type="article')
    clean_head = re.compile('(?u)([^,]+),.+')
    clean_head2 = re.compile('\..*')
    find_ou = re.compile(' ou ')
    find_et = re.compile(' et ')
    ## entry regex
    definition = re.compile('</div1')

    my_data = glob(dico_path + 'academie/DAF1762*')

    dico = {}
    for chunk in my_data:
        headwords = []
        entry = ''
        begin = False
        for line in open(chunk.rstrip()):
            if body.search(line):
                begin = True
            if not begin:
                continue
            if head.search(line):
                my_match = re.search('<div1 type="article" id="([^"]+)', line)
                headword = my_match.group(1).decode('utf-8').lower()
                headword = headword.replace('_', ' ')
                headword = clean_head.sub('\\1', headword)
                headword = clean_head2.sub('', headword)
                if find_ou.search(headword):
                    headwords = headword.split(' ou ')
                elif find_et.search(headword):
                    headwords = headword.split(' et ')
                else:
                    headwords = [headword,]
                for word in headwords:
                    if word not in dico:
                        dico[word] = []
                continue
            
            line = line.replace('</p>', '')
            line = line.replace('<p>', '<br>')
            
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('latin-1')
            if definition.search(line):
                entry = re.sub('^\s*<br>', '', entry)
                for word in headwords:
                    dico[word].append(entry)
                entry = ''
                continue
            
            entry += line

    return dico


def parse_acad1798():
    ## Body
    body = re.compile('<body>')
    ## Headword regex
    head = re.compile('<div1 type="article')
    clean_head = re.compile('(?u)([^,]+),.+')
    clean_head2 = re.compile('\..*')
    find_ou = re.compile(' ou ')
    find_et = re.compile(' et ')
    ## entry regex
    definition = re.compile('</div1')

    my_data = glob(dico_path + 'academie/DAF1798*')

    dico = {}
    first = 1
    for chunk in my_data:
        headwords = []
        entry = ''
        begin = False
        for line in open(chunk.rstrip()):
            if body.search(line):
                begin = True
            if not begin:
                continue
            
            if head.search(line):
                if re.search('<div1 type="article">', line):
                    if first == 1:
                        headword = u'A'
                        first = 2
                    else:
                        headword = u'L'
                else:
                    my_match = re.search('<div1 type="article" id="([^"]+)', line)
                    headword_dup = my_match.group(1)
                    headword = my_match.group(1).decode('utf-8').lower()
                    headword = headword.replace('_', ' ')
                    headword = clean_head.sub('\\1', headword)
                    headword = clean_head2.sub('', headword)
                    headword = headword.replace('--', '-')
                if find_ou.search(headword):
                    headwords = headword.split(' ou ')
                elif find_et.search(headword):
                    headwords = headword.split(' et ')
                else:
                    headwords = [headword,]
                for word in headwords:
                    if word not in dico:
                        dico[word] = []
                continue
            
            try:
                todel = '<p>' + headword_dup
                line = line.replace(todel, '<p>') ## delete duplicate headwords in entry
                line = re.sub('(?u)<p>[A-Z]*,* *[A-Z]*', '<p>', line)
            except NameError:
                pass
            
            line = line.replace('</p>', '')
            line = line.replace('<p>', '<br>')
            
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('latin-1')
            if definition.search(line):
                entry = re.sub('^\s*<br>', '', entry)
                for word in headwords:
                    dico[word].append(entry)
                entry = ''
                continue
            
            entry += line

    return dico


def parse_acad1835():
    ## Body
    body = re.compile('<body>')
    ## Headword regex
    head = re.compile('<div1 type="article')
    clean_head = re.compile('(?u)([^,]+),.+')
    clean_head2 = re.compile('_.*')
    clean_head3 = re.compile('\..*')
    find_ou = re.compile(' ou ')
    find_et = re.compile(' et ')
    ## entry regex
    definition = re.compile('</div1')

    my_data = glob(dico_path + 'academie/DAF1835*')

    dico = {}
    first = 1
    for chunk in my_data:
        headwords = []
        entry = ''
        begin = False
        for line in open(chunk.rstrip()):
            if body.search(line):
                begin = True
            if not begin:
                continue
            
            if head.search(line):
                my_match = re.search('<div1 type="article" id="([^"]+)', line)
                headword = my_match.group(1).decode('utf-8').lower()
                headword = clean_head.sub('\\1', headword)
                headword = clean_head2.sub('', headword)
                headword = clean_head3.sub('', headword)
                if find_ou.search(headword):
                    headwords = headword.split(' ou ')
                elif find_et.search(headword):
                    headwords = headword.split(' et ')
                else:
                    headwords = [headword,]
                for word in headwords:
                    if word not in dico:
                        dico[word] = []
                continue
            
            line = line.replace('</p>', '')
            line = line.replace('<p>', '<br>')
            
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('latin-1')
            if definition.search(line):
                entry = re.sub('^\s*<br>', '', entry)
                
                for word in headwords:
                    dico[word].append(entry)
                entry = ''
                continue
            
            entry += line

    return dico
    
    
def parse_acad1932():
    ## Body
    body = re.compile('<body>')
    ## Headword regex
    head = re.compile('<div1 type="entry')
    clean_head = re.compile('(?u)([^,]+),.+')
    clean_head2 = re.compile('\..*')
    find_ou = re.compile(' ou ')
    find_et = re.compile(' et ')
    ## entry regex
    definition = re.compile('</div1')
    new_entry = re.compile('<SVED>')

    my_data = glob(dico_path + 'academie/DAF1932*')

    dico = {}
    first = 1
    for chunk in my_data:
        headwords = []
        entry = ''
        begin = False
        for line in open(chunk.rstrip()):
            if body.search(line):
                begin = True
            if not begin:
                continue
            
            if head.search(line):
                my_match = re.search('<div1 type="entry" id="([^"]+)', line)
                headword = my_match.group(1).decode('utf-8').lower()
                headword = headword.replace('_', ' ')
                headword = clean_head.sub('\\1', headword)
                headword = clean_head2.sub('', headword)
                if find_ou.search(headword):
                    headwords = headword.split(' ou ')
                elif find_et.search(headword):
                    headwords = headword.split(' et ')
                else:
                    headwords = [headword,]
                for word in headwords:
                    if word not in dico:
                        dico[word] = []
                continue
            
            line = line.replace('</p>', '')
            line = line.replace('<p>', '<br>')
            
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('latin-1')
                
            if definition.search(line):
                for word in headwords:
                    entry = re.sub('^\s*<br>', '', entry)
                    dico[word].append(entry)
                entry = ''
                continue
            
            if new_entry.search(line):
                for word in headwords:
                    entry = re.sub('^\s*<br>', '', entry)
                    dico[word].append(entry)
                entry = ''
            
            entry += line

    return dico
    
    
def parse_littre():
    ## Headword regex
    head = re.compile('<div type="entree"><head>')
    clean_head = re.compile('(?u)([^,]+),.+')
    clean_head2 = re.compile('\..*')
    find_ou = re.compile(' ou ')
    find_et = re.compile(' et ')

    pron = re.compile('<prononciation>')
    nature = re.compile('<nature>')

    ## entry regex
    begin_def = re.compile('<variante')
    definition = re.compile('</variante')
    rubrique = re.compile('<rubrique nom="REMARQUE">')
    rubrique_etymo = re.compile('<rubrique nom="&Eacute;TYMOLOGIE">')
    end_rubrique = re.compile('</rubrique>')
    indent = re.compile('</indent>')
    citation = re.compile('^<i>')

    my_data = glob(dico_path + 'littre/*')

    dico = {}
    valid_entry = None
    rubrique_entry = None
    for chunk in my_data:
        headwords = []
        entry = ''
        for line in open(chunk.rstrip()):
            if head.search(line):
                my_match = re.search('<div type="entree"><head>([^<]+)', line)
                headword = convert(my_match.group(1).lower())
                headword = clean_head.sub('\\1', headword)
                headword = clean_head2.sub('', headword)
                if find_ou.search(headword):
                    headwords = headword.split(' ou ')
                elif find_et.search(headword):
                    headwords = headword.split(' et ')
                else:
                    headwords = [headword,]
                for word in headwords:
                    if word not in dico:
                        dico[word] = {}
                        dico[word] = {'content': [], 'pron': ''}
                continue
            
            if pron.search(line):
                match = re.search('<prononciation>([^<]+)', line)
                try:
                    dico[word]['pron'] = match.group(1).decode('utf-8')
                except AttributeError:
                    del dico[word]['pron']
                continue
            
            if nature.search(line):
                continue
            
            # This removes all example sentences
            if citation.search(line):
                line = citation.sub('<br><i>', line)
            
            #entry = re.sub('^\s*<p>', '', entry)
            entry = entry.replace('<p>', '')
            #line = re.sub('Fig\.\s*\n*', '<br>Fig.', line)
            
            if begin_def.search(line):
                valid_entry = 1
            
            if rubrique.search(line) or rubrique_etymo.search(line):
                rubrique_entry = 1
                
            if valid_entry:
                try:
                    line = line.decode('utf-8')
                except:
                    line = line.decode('latin-1')
                if indent.search(line):
                    line = line + '<br>'
                line = convert(line)
                entry += line
                if definition.search(line):
                    for word in headwords:
                        dico[word]['content'].append(entry)
                    entry = ''
                    valid_entry = None
                    
            if rubrique_entry and valid_entry == None:
                try:
                    line = line.decode('utf-8')
                except:
                    line = line.decode('latin-1')
                if indent.search(line):
                    line = line + '<br>'
                line = convert(line)
                entry += line
                if end_rubrique.search(line):
                    for word in headwords:
                        dico[word]['content'].append(entry)
                    entry = ''
                    rubrique_entry = None
                
    return dico
    
    
def parse_nicot():
    ## Body
    body = re.compile('<body>')
    ## Headword regex
    head = re.compile('<div1 type="entry')
    clean_head = re.compile('(?u)([^,]+),.+')
    clean_head2 = re.compile('\.')
    find_ou = re.compile(' ou ')
    find_et = re.compile(' et ')
    ## entry regex
    definition = re.compile('</div1')

    my_data = glob(dico_path + 'nicot/*')

    dico = {}
    for chunk in my_data:
        headwords = []
        entry = ''
        begin = False
        for line in open(chunk.rstrip()):
            if body.search(line):
                begin = True
            if not begin:
                continue
            
            if head.search(line):
                my_match = re.search('<div1 type="entry" id="([^"]+)', line)
                headword = my_match.group(1).decode('utf-8').lower()
                headword = clean_head.sub('\\1', headword)
                headword = clean_head2.sub('', headword)
                if find_ou.search(headword):
                    headwords = headword.split(' ou ')
                elif find_et.search(headword):
                    headwords = headword.split(' et ')
                else:
                    headwords = [headword,]
                for word in headwords:
                    if word not in dico:
                        dico[word] = []
                continue
            
            line = line.replace('</p>', '')
            line = line.replace('<p>', '<br>')
            line = line.replace('<b>', '')
            line = line.replace('</b>', '')
            
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('latin-1')
            if definition.search(line):
                entry = re.sub('^\s*<br>', '', entry)
                for word in headwords:
                    dico[word].append(entry)
                entry = ''
                continue
            
            entry += line
                
    return dico
    
    
def parse_feraud():
    ## Body
    body = re.compile('<body>')
    ## Headword regex
    head = re.compile('<div1 type="entry')
    clean_head = re.compile('(?u)([^,]+),.+')
    clean_head2 = re.compile('\.')
    find_ou = re.compile(' ou ')
    find_et = re.compile(' et ')
    ## entry regex
    definition = re.compile('</div1')

    my_data = glob(dico_path + 'feraud/*')

    dico = {}
    for chunk in my_data:
        headwords = []
        entry = ''
        begin = False
        for line in open(chunk.rstrip()):
            if body.search(line):
                begin = True
            if not begin:
                continue
            
            if head.search(line):
                my_match = re.search('<div1 type="entry" id="([^"]+)', line)
                try:
                    headword = my_match.group(1).decode('utf-8').lower()
                    headword = clean_head.sub('\\1', headword)
                    headword = clean_head2.sub('', headword)
                except AttributeError:
                    headword = 'todelete'
                if find_ou.search(headword):
                    headwords = headword.split(' ou ')
                elif find_et.search(headword):
                    headwords = headword.split(' et ')
                else:
                    headwords = [headword,]
                for word in headwords:
                    dico[word] = []
                continue
            
            line = line.replace('</p>', '')
            line = line.replace('<p>', '<br>')
            line = line.replace('<BR><FONT SIZE=+1>', '')
            line = line.replace('</FONT>', '')
            line = re.sub('(?u)<br>([A-Z]{2,})', '\\1', line)
            
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('latin-1')
            if definition.search(line):
                entry = re.sub('^\s*<br>', '', entry)
                for word in headwords:
                    dico[word].append(entry)
                entry = ''
                continue
            
            entry += line

    del dico['todelete']
    return dico


def tlfi_loader():
    tlfi_dict = {}
    tlfi_dir = dico_path + 'tlfi/entry_pickles'

    cursor.execute ("DROP TABLE IF EXISTS tlfi")
    cursor.execute ("""
                    CREATE TABLE tlfi
                    (
                        headword    VARCHAR(128) CHARACTER SET utf8, INDEX(headword),
                        entry       MEDIUMTEXT CHARACTER SET binary
                    ) CHARACTER SET utf8 COLLATE utf8_general_ci
                    """)
                    
    ## To avoid unwanted newlines in the HTML
    remove_divs = re.compile('<div[^<]*>')
    remove_divs2 = re.compile('</div>')
    ## Remove numbers for headwords for merge
    remove_nums = re.compile('\d+')
    
    for pickled_file in sorted(os.listdir(tlfi_dir)):
        word = pickled_file.decode('utf-8')
        input_file = open(tlfi_dir + '/' + word)
        entry = cPickle.load(input_file)
        entry['content'] = remove_divs.sub('', entry['content'])
        entry['content'] = remove_divs2.sub('', entry['content'])
        
        ## Remove numbers in headwords
        word = remove_nums.sub('', word)
        
        ## Just keep the first entry for each headword
        if word not in tlfi_dict:
            tlfi_dict[word] = {}
            tlfi_dict[word] = {'content': [], 'prons': ''}
            tlfi_dict[word]['content'].append(entry['content'])
            try:
                if len(entry['prons']) > 0:
                    tlfi_dict[word]['prons'] = entry['prons']
            except KeyError:
                pass
            
    print "Dictionary rebuilding done"
            
    for word in tlfi_dict:
        entry = cPickle.dumps({'content': tlfi_dict[word]['content'], 'prons': tlfi_dict[word]['prons']}, -1)
        cursor.execute ("INSERT INTO tlfi (headword, entry) VALUES (%s, %s)", (word.encode('utf-8'), entry))
       
       
def daf_loader(table, dico_dict):
    cursor.execute ("DROP TABLE IF EXISTS %s" % table)
    cursor.execute ("""
                    CREATE TABLE %s
                    (
                        headword    VARCHAR(128) CHARACTER SET utf8, INDEX(headword),
                        entry       MEDIUMTEXT CHARACTER SET binary
                    ) CHARACTER SET utf8 COLLATE utf8_general_ci
                    """ % table)
    
    for headword in dico_dict:
        if table != 'littre':
            entries = cPickle.dumps({'content': dico_dict[headword]}, -1)
        else:
            entry = dico_dict[headword]['content']
            try:
                pron = dico_dict[headword]['pron']
                entries = cPickle.dumps({'content': entry, 'prons': pron}, -1)
            except KeyError:
                entries = cPickle.dumps({'content': entry}, -1)
        headword = headword.encode('utf-8')
      
        cursor.execute ("INSERT INTO " + table + " (headword, entry) VALUES (%s, %s)", (headword, entries))
                        
    del dico_dict


## Specify dico path
dico_path = "../dicos/"

## Get MySQL password from the command line
## Die if no passwords were provided
try:
    if re.search('--passwd=.+', sys.argv[1]):
        passwd = re.sub('--passwd=(.+)', '\\1', sys.argv[1])
        passwd = passwd.rstrip()
    else:
        print "\nYou forgot to give a password for MySQL\n"
        sys.exit()
except IndexError:
    print "\nYou forgot to give a password for MySQL\n"
    sys.exit()

## Dico selection :load all dicos if no arguments
dicos = []
try:
    if sys.argv[2]:
        for dico in sys.argv[2:]:
            dicos.append(dico)
except IndexError:
    dicos = ['feraud', 'nicot', 'acad1694', 'acad1762',
            'acad1798', 'acad1835', 'acad1932', 'littre', 'tlfi']

## MySQL instantiation
db = MySQLdb.connect(user='root', passwd='%s' % passwd, db='dvlf', use_unicode=True) 
cursor = db.cursor()
db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
cursor.execute('set global character_set_server=utf8;')
cursor.execute('set session character_set_server=utf8;')

## Dico parsing and loading
for dico in dicos:
    print "\n## Processing %s ##" % dico
    if dico != 'tlfi':
        dico_handler(dico)
    else:
        tlfi_loader()
    print 'MySQL load done'
        
print "\nAll dicos loaded\n"