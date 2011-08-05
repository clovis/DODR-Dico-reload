#!/usr/bin/python

import os
import re

filenames = open('/Users/Zsofia/BOB/bobfiles.txt')

def parser(dico_path):
    
    dico = {}
    
    for file in filenames:
        file = re.sub('\n', '', file)
        file = file.decode('iso8859_15').encode('utf-8')
        outfile = file
        output = os.path.join('/Users/Zsofia/BOB/bob_new/', outfile)
        output = open(output, 'w')
        filename = os.path.join('/Users/Zsofia/BOB/bob/', file)
        incoming = open(filename)
        
        entry = ''
        
        for line in incoming:
                line = line.decode('iso8859_15').encode('utf-8')
                    
                if re.search('<div class="g_mot">', line):
                        m = re.search('<div class="g_mot">([^<]+)', line)
                        head = m.group(1)
                        head = re.sub('&nbsp;', '', head)
                        
                        head = head.decode('utf-8')
                        dico[head] = []
                        
                        head = head.upper()
                        entry = '<li>'
                        entry += head.encode('utf-8')
                        entry += ','
                        entry += '\n'
                    
                    try:
                        if re.search('class="g_connexion">date :</span> <span class="cap">', line):
                            m = re.search('class="g_connexion">date :</span> <span class="cap">([^<]+)', line)
                            date = m.group(1)
                            
                            entry += date
                            entry += '.'
                            entry += '\n'
                    except IndexError:
                        print 'got exception'
                    
                    
                    if re.search('<span class="g_gram">', line):
                            m = re.search('<span class="g_gram">([^<]+)', line)
                            gram_ps = m.group(1)
                            gram_ps = re.sub('&nbsp;', '', gram_ps)
                            gram_ps = re.sub('\|', '', gram_ps)
                            entry += gram_ps
                            entry += '\n'
                    if re.search('</span> <span class="g_gram">', line):
                            m = re.search('</span> <span class="g_gram">([^<]+)', line)
                            gram_case = m.group(1)
                            gram_case = re.sub('&nbsp;', '', gram_case)
                            gram_case = re.sub('\|', '', gram_case)
                            entry += gram_case
                            entry += '\n'
                        
                    if re.search('<div class="g_def">', line):
                            m = re.search('<div class="g_def">([^<]+)', line)
                            defn = m.group(1)
                            defn = re.sub('&para;', '', defn)
                            defn = defn.rstrip()
                            entry += defn
                            entry += '.'
                            entry += '<br>'
                            entry += '\n'
            
                    if re.search('<span class="g_etymo">', line):
                            m = re.search('<span class="g_etymo">([^<]+)', line)
                            etymo = m.group(1)
                            etymo = re.sub('&loz', '', etymo)
                            etymo = etymo.rstrip()
                            entry += etymo
                            entry += '<br>'
                            entry += '\n'
                
                    if re.search('<span class="g_cit">&loz;', line):
                            citation = re.findall('<span class="g_cit">&loz;([^<]+)', line)
                            citation_date = re.findall('<span class="g_cit_date">([^<]+)', line)
                            citations = zip(citation, citation_date)
                            for c, d in citations:
                                entry += '<i>'
                                entry += c
                                entry += ' ('
                                entry += d
                                entry += ').'
                                entry += '</i>'
                                entry += '<br>'
                                entry += '\n'
                
                    if re.search('<span class="g_connexion">', line):
                            m = re.findall('<span class="g_connexion">synonyme&nbsp;:&nbsp;<span class="cap">([^(]+)', line)
                            for synonym in m:
                                synonym = synonym.rstrip()
                                entry += synonym
                                entry += '.'
                                entry += '<br>'
                                entry += '\n'
                    
                    dico[head].append(entry)
                    
        return dico
            