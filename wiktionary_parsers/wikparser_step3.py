#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys


def parse(file):
    lines = 0
    ent = ''
    entry = ''
    wiki_dict = {}
    for line in open(file):
        line = line.decode('utf-8')

        if re.search('<div1 type="entry"', line):
            if ent != '':
                headword = entry.replace('.', '')
                headword = re.sub('([^ ]+).*', '\\1', headword)
                if headword not in wiki_dict:
                    wiki_dict[headword] = []
                wiki_dict[headword].append(ent)
                ent = ''
            m = re.search('<div1 type="entry" word="([^"]+)', line)
            entry = m.group(1)
            if entry in line:
                lines = 0
                entry = entry.strip() + '.'
            ent = entry.upper()
            

        if re.search('etym:', line):
            m = re.search('etym:([^<]+)', line)
            etym = m.group(1)
            try:
                ent += etym
            except TypeError:
                pass
            
        if re.search('date<', line):
            m = re.search('date<([^<]+)', line)
            etym2 = m.group(1)
            ent += etym2
        
        if re.search('pron', line):
            m = re.search('pron([^$]+)', line)
            pron = m.group(1)
            ent += unicode(pron)
            
        if re.search(' gen ', line):
            m = re.search('gen ([^>]+)', line)
            gender = m.group(1)
            ent += gender
        
        
        if re.search('<div2 type="def"', line):
            m = re.search('# ([^>]+)', line)
            defn = m.group(1)
            #print defn
            if defn in line:
                lines += 1
                ent += '<br>' + unicode(lines) + '. ' + defn
                
            
        if re.search('<div3 type="subdef"', line):
            m = re.search('# ([^>]+)', line)
            subdefn = m.group(1)
            ent += '<BLOCKQUOTE>' + '<li>' + subdefn + '<br>' + '</BLOCKQUOTE>'
        
        if re.search('<div4 type="example"', line):
            m = re.search('# ([^>]+)', line)
            example = m.group(1)
            ent += '<BLOCKQUOTE>' + '<BLOCKQUOTE>' + '<i>' + example + '</i>' + '</BLOCKQUOTE>' + '</BLOCKQUOTE>'

        if re.search('syn # ', line):
            m = re.search('# ([^$]+)', line)
            syn = m.group(1)
            ent += syn

        if re.search('drv # ', line):
            m = re.search('# ([^$]+)', line)
            drv = m.group(1)
            ent += drv

        if re.search('apr # ', line):
            m = re.search('# ([^$]+)', line)
            apr = m.group(1)
            ent += apr
        
        if re.search('exp # ', line):
            m = re.search('# ([^$]+)', line)
            exp = m.group(1)
            ent += exp
            
        if re.search('hyper # ', line):
            m = re.search('# ([^$]+)', line)
            hyper = m.group(1)
            ent += hyper
        
        if re.search('hypo # ', line):
            m = re.search('# ([^$]+)', line)
            hypo = m.group(1)
            ent += hypo
        
        if re.search('anagr # ', line):
            m = re.search('# ([^$]+)', line)
            anagr = m.group(1)
            ent += anagr
    
    return wiki_dict
		
		
		
