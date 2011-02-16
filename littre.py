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

def parser(dico_path):
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