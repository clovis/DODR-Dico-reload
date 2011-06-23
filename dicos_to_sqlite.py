#!/usr/bin/env python

## This script will parse all DAF dicos as well as reload them
## in MySQL. It will also rebuild the TLFI from the entry pickles.

## It will then process whatever dico(s) you give as an argument. 
## If you don't give arguments, it will process every dico.

import sqlite3
import cPickle
import json
import sys
import os
import re
import littre
import feraud
import nicot
import acad1694
import acad1762
import acad1798
import acad1835
import acad1932


def dico_handler(dico):
    if dico == 'littre':
        dico_dict = littre.parser(dico_path)
    elif dico == 'feraud':
        dico_dict = feraud.parser(dico_path)
    elif dico == 'nicot':
        dico_dict = nicot.parser(dico_path)
    elif dico == 'acad1694':
        dico_dict = acad1694.parser(dico_path)
    elif dico == 'acad1762':
        dico_dict = acad1762.parser(dico_path)
    elif dico == 'acad1798':
        dico_dict = acad1798.parser(dico_path)
    elif dico == 'acad1835':
        dico_dict = acad1835.parser(dico_path)
    elif dico == 'acad1932':
        dico_dict = acad1932.parser(dico_path)
    print "Parsing done"
    daf_loader(dico, dico_dict)


def tlfi_loader():
    tlfi_dict = {}
    tlfi_dir = dico_path + 'tlfi/entry_pickles'
    
    cursor.executescript ('drop table if exists tlfi')
    cursor.execute ('create table tlfi (headword text primary key, entry blob)')
                    
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
    
    count = 0
    for word in tlfi_dict:
        count += 1
        entry = cPickle.dumps({'content': tlfi_dict[word]['content'], 'prons': tlfi_dict[word]['prons']}, -1)
        cursor.execute ("insert into tlfi values (?, ?)", (word.encode('utf-8'), buffer(entry)))
        if count == 100:
            count = 0
            conn.commit()
       
       
def daf_loader(table, dico_dict):
    cursor.executescript ('drop table if exists ' + table)
    cursor.execute ('create table ' + table + ' (headword text primary key, entry blob)')
    
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
      
        cursor.execute('insert into ' + table + ' values (?,?)', (headword,buffer(entries)))
                        
    del dico_dict


## Specify dico path
dico_path = "../dicos/"


## Dico selection :load all dicos if no arguments
dicos = []
try:
    if sys.argv[1]:
        for dico in sys.argv[1:]:
            dicos.append(dico)
except IndexError:
    dicos = ['feraud', 'nicot', 'acad1694', 'acad1762',
            'acad1798', 'acad1835', 'acad1932', 'littre', 'tlfi']

## SQLite instantiation
dvlf_path = '/home/clovis/DVLF/'
conn = sqlite3.connect(dvlf_path + 'dvlf.sqlite')
conn.text_factory = str
cursor = conn.cursor()


## Dico parsing and loading
for dico in dicos:
    print "\n## Processing %s ##" % dico
    if dico != 'tlfi':
        dico_handler(dico)
    else:
        tlfi_loader()
    conn.commit()
    print 'SQLite load done'
    
cursor.close()
        
print "\nAll dicos loaded\n"