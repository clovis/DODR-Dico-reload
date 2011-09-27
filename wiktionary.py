#!/usr/bin/env python

from wiktionary_parsers import wikparser_step2, wikparser_step3
from os import listdir
from subprocess import call


def parse_step1(file):
    process = subprocess.call('wiktionary_parsers/wikparser_step1.pl %s' % file, shell=True)


def parser(dico_path):
    dico_path = dico_path + 'wiktionary/'
    parse_step1(dico_path + listdir(dico_path)[0])
    
    