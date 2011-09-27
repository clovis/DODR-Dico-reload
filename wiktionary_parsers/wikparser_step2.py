#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

gram_dict = {'{{absolument': '(Absolument)',
	   '{{abrév': '(Abréviation)',
	   '{{acron': '(Acronyme)',
	   '{{acronyme': '(Acronyme)',
	   '{{agri': '(Agriculture)',
	   '{{analogie': '(Par analogie)',
	   '{{anatomie': '(Anatomie)',
	   '{{archaïque': '(Archaïsme)',
	   '{{architecture': '(Architecture)',
	   '{{argot': '(Argot)',
	   '{{arts': '(Arts)',
	   '{{aviation': '(Aviation)',
	   '{{biologie': '(Biologie)',
	   '{{confiserie': '(Confiserie)',
	   '{{désuet': '(Désuet)',
	   '{{économie': '(Économie)',
	   '{{ellipse': '(Par ellipse)',
	   '{{extrêmement rare': '(Extrêmement rare)',
	   '{{familier': '(Familier)',
	   '{{fauconnerie': '(Fauconnerie)',
	   '{{figuré': '(Figuré)',
	   '{{formel': '(Formel)',
	   '{{géographie': '(Géographie)',
	   '{{héraldique': '(Héraldique)',
	   '{{histoire': '(Histoire)',
	   '{{informatique': '(Informatique)',
	   '{informel': '(Informel)',
	   '{{impersonnel': '(Impersonnel)',
	   '{{ironique': '(Ironique)',
	   '{{irrégulier': '(Irrégulier)',
	   '{{juri': '(Droit)',
	   '{{jurisprudence': '(Droit)',
	   '{{justice': '(Justice)',
	   '{{ling': '(Linguistique)',
	   '{{linguistique': '(Linguistique)',
	   '{{littéraire': '(Littéraire)',
	   '{{littérature': '(Littérature)',
	   '{{litote': '(Litote)',
	   '{{maçonnerie': '(Maçonnerie)',
	   '{{manège': '(Équitation)',
	   '{{mathématiques': '(Mathématiques)',
	   '{{mécanique': '(Mécanique)',
	   '{{médecine': '(Médecine)',
	   '{{mélioratif': '(Mélioratif)',
	   '{{méton': '(Par métonymie)',
	   '{{métonymie': '(Métonymie)',
	   '{{métrol': '(Métrologie)',
	   '{{meuble': '(Mobilier)',
	   '{{militaire': '(Militaire)',
	   '{{mot-valise': '(Mot-valise)',
	   '{{musique': '(Musique)',
	   '{{néologisme': '(Néologisme)',
	   '{{neutre': '(Neutre)',
	   '{{paléontologie': '(Paléontologie)',
	   '{{par ext': '(Par extension)',
	   '{{particulier': '(En particulier)',
	   '{{péjoratif': '(Péjoratif)',
	   '{{physique': '(Physique)',
	   '{{plantes': '(Botanique)',
	   '{{pluri': '(Au pluriel)',
	   '{{poétique': '(Poétique)',
	   '{{politique': '(Politique)',
	   '{{populaire': '(Populaire)',
	   '{{propre': '(Propre)',
	   '{{rare': '(Rare)',
	   '{{sic': '(Sic)',
	   '{{sigle': '(Sigle)',
	   '{{sing': '(Au singulier)',
	   '{{soutenu': '(Soutenu)',
	   '{{spécialement': '(Spécialement)',
	   '{{sport': '(Sport)',
	   '{{synérèse': '(Synérèse)',
	   '{{technique': '(Technique)',
	   '{{term': '(Collectivement)',
	   '{{très rare': '(Très rare)',
	   '{{vieilli': '(Vieilli)',
	   '{{vieux': '(Vieux)',
	   '{{vulgaire': '(Vulgaire)',
	   '{{zoologie': '(Zoologie)',
	   '{{m': ': gen Masculin.>',
	   '{{f': ': gen Féminin.>'}

etyl_dict = {'{{étyl|la': 'latin',
		'{{étyl|it': 'italien',
		'{{étyl|grc': 'grec ancien',
		'{{étyl|frk': 'francique',
		'{{étyl|fr': 'français',
		'{{étyl|fro': 'ancien français',
		'{{étyl|nl': 'néerlandais',
		'{{étyl|zh': 'chinois',
		'{{étyl|ja': 'japonais',
		'{{étyl|ang':'anglo-saxon',
		'{{étyl|1=gem': 'langues germaniques',
		'{{étyl|1=la': 'latin',
		'{{étyl|1=grc': 'grec ancien',
		'{{étyl|1=fro': 'ancien français',
		'{{étyl|1=de': 'allemend'
					}
		
gram_list = '{{-anagr-}}','{{-apr-}}','{{-drv-}}','{{-étym-}}','{{-exp-}}','{{-flex-verb-}}','{{-flex-verb-|fr}}','{{-homo-}}','{{-hyper-}}','{{-hypo-}}','{{-nom-|fr}}','{{-note-}}','{{-nom-|nl}}','{{-paro-}}','{{-pron-}}','{{-réf-}}','{{-syn-}}','{{-voir-}}','{{-verb-|fr}}','{{-voc-}}' 
		

for filename in sys.argv[1:]:
	line_count = 0
	printme = ''
	for line in open(filename):
		#line = line.decode('utf-8')
		#line = line.encode('utf-8')
		
		if re.search('<div', line):
			if re.search('type="entry"', line):
				printme = 1
			elif re.search('type="pos"', line):
				printme = 1
			elif re.search('type="etym"', line):
				printme = 1
			elif re.search('type="def"', line):
				printme = 1
			elif re.search('type="example"', line):
				printme = 1
			elif re.search('type="apr"', line):
				printme = 1
			elif re.search('type="anagr"', line):
				printme = 1
			elif re.search('type="subdef"', line):
				printme = 1
			elif re.search('type="syn"', line):
				printme = 1
			elif re.search('type="drv"', line):
				printme = 1
			elif re.search('type="exp"', line):
				printme = 1
			elif re.search('type="hyper"', line):
				printme = 1
			elif re.search('type="hypo"', line):
				printme = 1
			elif re.search('type="note"', line):
				printme = 1
			else:
				printme = 0
	
	
		if re.search("{{étyl", line):
			dif = ""
			mot = ""
			sens = ""
			etyl_matches = re.findall("({{étyl[^\}]*)}}", line)
			for etyl_match in etyl_matches:
				if re.search("sens=[^}]*}}", line):
					etyl_lookup_form = re.search("({{étyl\|[a-z1=]{2,5})-?.*",etyl_match)
					etyl_lookup_form1 = etyl_lookup_form.group(1)
					if re.search("mot=[^}]*}}", line):
						mot = re.search("[motr]{2,3}=([^\|^}]*)[\|}]?", line).group(1)
					if re.search("dif=[^}]*}}", line):
						dif = re.search("dif=([^\|]*)\|", line).group(1)
					sens = re.search("sens=([^}]*)}}", line).group(1)
					if dif:
						insert = " " + dif + " («" + sens + "»)"
					else:
						insert = " " + mot + " («" + sens + "»)"	
					if etyl_lookup_form1 in etyl_dict:
                                                etyl_replacement = etyl_dict[etyl_lookup_form1]
                                                line = line.replace(etyl_match,etyl_replacement,1)
                                                line = re.sub('}}', insert, line, 1)

				elif re.search("mot=[^}]*}}", line):
					etyl_lookup_form = re.search("({{étyl\|[a-z1=]{2,5})-?.*",etyl_match)
                                        etyl_lookup_form1 = etyl_lookup_form.group(1)
					mot = re.search("[motr]{2,3}=([^\}]*)}}", line).group(1)
					mot = " ", mot
					if etyl_lookup_form1 in etyl_dict:
                                                etyl_replacement = etyl_dict[etyl_lookup_form1]
                                                line = line.replace(etyl_match,etyl_replacement,1)
						line = re.sub('}}', mot, line, 1)

				elif re.search("{{étyl\|[a-z1=]{2,5}", line):
					#etyl_lookup_form = re.search("({{étyl\|[a-z]{2,3})\|.*",etyl_match)
					etyl_lookup_form = re.search("({{étyl\|[a-z1=]{2,5})-?.*",etyl_match)
					etyl_lookup_form1 = etyl_lookup_form.group(1)
					if etyl_lookup_form1 in etyl_dict:
						etyl_replacement = etyl_dict[etyl_lookup_form1]
						line = line.replace(etyl_match,etyl_replacement,1)
						line = re.sub('}}', '', line)
		
		if re.search("{{", line):
			gram_matches = re.findall("{{[^\}]*}}", line)
			for gram_match in gram_matches:
				lookup_form = re.search("({{[^\}\|]*)",gram_match).group(1)
				if lookup_form in gram_dict:				
					replacement = gram_dict[lookup_form]
					line = line.replace(gram_match,replacement,1)
		
		if re.search("{{", line):
			for gram in gram_list:
				line = line.replace(gram, '', 1)
		
		if re.search('{{siècle', line):
			line = re.sub('{{siècle\|', '', line)
			line = re.sub('}}', 'e siècle.', line)
	
	 	line = re.sub('{{', '(', line)
	 	line = re.sub('}}', ')', line)	
	 	
	 	line = re.sub('\: \(date\|', 'date<', line)
	 	line = re.sub('\(date\|', 'date<', line)
	 	
	 	line = re.sub('\(e siècle', 'e siècle', line)
	 	
	 	line = re.sub('^: ', 'etym:', line)
	 	line = re.sub('^:', 'etym:', line)
 	
	 	if re.search('\(polytonique\|', line):
	 		line = re.sub('\(polytonique\|', '', line)
	 	
	 	if re.search('\(source\|\(w\|', line):
	 		line = re.sub('source\|\(w\|', 'Source: ', line)
	 	if re.search('\(source\|', line):
	 		line = re.sub('source\|', 'Source: ', line)
	 	if re.search('\),', line):
	 		line = re.sub('\),', ',', line)
	 	
	 	if re.search('\(fr-rég\|', line):
	 		line = re.sub('\(fr-rég\|', 'pron(', line)
	 	
	 	if re.search('\(pron', line):
	 		line = ''
	 	
	 	if re.search('\[\[Image', line):
	 		line = ''
	 		
	 	if re.search('\(fr-verbe-flexion', line):
	 		line = ''
	 	
	 	line = re.sub('([\']*)', '', line)
		#line = re.sub('\#', '', line)
		line = re.sub('\*', '#', line)
	 	
		if re.search('<div2 type', line):
			m = re.search('<div2 type="([^"]+)', line)
			my_tag = m.group(1)
			#print my_tag
		if re.search('^\#', line):
			print my_tag, line
		if re.search('^\#', line):
			line = ''
		
		if printme:
			print line
			
