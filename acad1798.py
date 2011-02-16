import re
from glob import glob


def parser(dico_path):
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