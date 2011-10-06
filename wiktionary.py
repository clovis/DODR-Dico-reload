#!/usr/bin/env python

from wiktionary_parsers import wikparser_step3
from os import listdir
from subprocess import call


def parse_step1(dico_path):
    file =  dico_path + listdir(dico_path)[0]
    newfile = dico_path + 'step1.xml'
    command = 'wiktionary_parsers/wikparser_step1.pl %s > %s' % (file, newfile)
    process = call(command, shell=True)
    
def parse_step2(dico_path):
    file =  dico_path + 'step1.xml'
    newfile = dico_path + 'step2.xml'
    command = 'wiktionary_parsers/wikparser_step2.py %s > %s' % (file, newfile)
    process = call(command, shell=True)
    
def parse_step3(dico_path):
    file =  dico_path + 'step2.xml'
    newfile = dico_path + 'step3.xml'
    command = 'wiktionary_parsers/wikparser_step3.py %s > %s' % (file, newfile)
    process = call(command, shell=True)

def parser(dico_path):
    dico_path = dico_path + 'wiktionary/'
    #parse_step1(dico_path)
    #print 'step 1 done...'
    #parse_step2(dico_path)
    #print 'step 2 done...'
    dico = wikparser_step3.parse(dico_path + 'step2.xml')
    print 'step 3 done...'
    #print dico
    return dico
    
    
    
    