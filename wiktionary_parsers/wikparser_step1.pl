#! /usr/bin/perl

use Encode;
use utf8;
use Data::Dumper;

####################
## a tag hash     ##
## for doc        ##
## structure      ##
####################

%TAG_HASH = (
	abrev => "abr\xc3\xa9viation",
	adj => "adjectif",
	adjnum => "adjectif num\xc3\xa9ral",
	adv => "adverbe",
	artdef => "article d\xc3\xa9fini",
	artindef => "article ind\xc3\xa9fini",
	aff => "affixe",
	anagr => "anagrammes",
	anagrammes => "anagrammes",
	ant => "antonymes",
	app => "apparent\xc3\xa9s \xc3\xa9tymologiques",
	apr => "apparent\xc3\xa9s \xc3\xa9tymologiques",
	aux => "verbe auxiliaire",
	cit => "citations",
	compos => "compos\xc3\xa9s",
	conjcoord => "conjonction de coordination",
	deriv => "d\xc3\xa9riv\xc3\xa9s",
	dial => "variantes dialectales",
	drv => "d\xc3\xa9riv\xc3\xa9s",
	derives => "d\xc3\xa9riv\xc3\xa9s",
	etym => "\xc3\xa9tymologie",
	etymologie => "\xc3\xa9tymologie",
	exp => "expressions",
	expr => "expressions",
	fauxamis => "faux amis",
	flexadj => "forme d'adjectif",
	flexadjnum => "forme d'adjectif num\xc3\xa9ral",
	flexadv => "forme d'adverbe",
	flexartdef => "forme d'article d\xc3\xa9fini",
	flexartindef => "forme d'article ind\xc3\xa9fini",
	flexinterj => "forme d'interjection",
	flexnom => "forme de nom",
	flexpronomindef => "forme de pronom ind\xc3\xa9fini",
	flexpronomint => "forme de pronom interrogatif",
	flexpronompers => "forme de pronom personnel",
	flexpronomrel => "forme de pronom relatif",
	flexprep => "forme de pr\xc3\xa9position",
	flexsuf => "forme de suffixe",
	flexverb => "forme de verbe",
	gent => "gentil\xc3\xa9s",
	hist => "attestations historiques",
	holo => "holonymes",
	hom => "homophones",
	homo => "homophones",
	hyper => "hyperonymes",
	hypo => "hyponymes",
	loc => "locution",
	locution => "locution",
	locadj => "locution adjectivale",
	locadv => "locution adverbiale",
	locconj => "locution conjonctive",
	locinterj => "locution interjective",
	locnom => "locution nominale",
	locphr => "locution phrase",
	locphrase => "locution phrase",
	locprep => "locution pr\xc3\xa9positive",
	locverb => "locution verbale",
	mero => "m\xc3\xa9ronymes",
	nom => "nom commun",
	nomfam => "nom de famille",
	nompr => "nom propre",
	not => "note",
	note => "note",
	onoma => "onomatop\xc3\xa9e",
	orthoalt => "variantes orthographiques",
	paro => "paronymes",
	part => "particule",
	post => "postposition",
	pron => "prononciation",
	pronomdem => "pronom d\xc3\xa9monstratif",
	pronomindef => "pronom ind\xc3\xa9fini",
	pronomint => "pronom interrogatif",
	pronompers => "pronom personnel",
	pronompos => "pronom possessif",
	pronomrel => "pronom relatif",
	prononciation => "prononciation",
	prov => "proverbe",
	pref => "pr\xc3\xa9fixe",
	prenom => "pr\xc3\xa9nom",
	prep => "pr\xc3\xa9position",
	ref => "r\xc3\xa9f\xc3\xa9rences",
	references => "r\xc3\xa9f\xc3\xa9rences",
	suf => "suffixe",
	suffixe => "suffixe",
	syll => "syllabation",
	symb => "symbole",
	syn => "synonymes",
	tropo => "troponyme",
	var => "variantes orthographiques",
	varortho => "variantes orthographiques",
	verb => "verbe",
	verbe => "verbe",
	voc => "vocabulaire apparent\xc3\xa9 par le sens",
	voir => "voir aussi"
	);

$parts_o_speech = qr/adj|adv|artdef|artindef|aux|conjcoord|flexadj|flexadjnum|flexadv|flexartdef|flexartindef|flexinterj|flexnom|flexpronomindef|flexpronomint|flexpronompers|flexpronomrel|flexprep|flexsuf|flexverb|loc|locution|locadj|locadv|locconj|locinterj|locnom|locphr|locphrase|locprep|locverb|pronomdem|pronomindef|pronomint|pronompers|pronompos|pronomrelprep|nom|verb/;

## I'd love it if this worked....

#$utf8_chars = qr/\xc3[\xa0-\xbe]/;

## but apparently I have to write out every character. ah well....

$utf8_chars = qr/\xc3\xa0|\xc3\xa1|\xc3\xa2|\xc3\xa3|\xc3\xa4|\xc3\xa5|\xc3\xa6|\xc3\xa7|\xc3\xa8|\xc3\xa9|\xc3\xaa|\xc3\xab|\xc3\xac|\xc3\xad|\xc3\xae|\xc3\xaf|\xc3\xb0|\xc3\xb1|\xc3\xb2|\xc3\xb3|\xc3\xb4|\xc3\xb5|\xc3\xb6|\xc3\xb7|\xc3\xb8|\xc3\xb9|\xc3\xba|\xc3\xbb|\xc3\xbc|\xc3\xbd|\xc3\xbe/;

#print Dumper(%TAG_HASH);

#####################
## loop to read in ##
## data and select ##
## text to format  ##
#####################

while (<>) {
	$in = $_;

#	$in = Encode::decode( 'utf8', $in);

	if ($in =~ /<title>/) {
		$counter_4_title = 0;
		$in_french_word = 0;
		if ($in =~ /\:/) {
			}
		else {
			$in =~ m/<title>([^<]*)<\/title>/;
			$entry_word = $1; ## okay to have as global?
			}
		}

	if ($in =~ /<text/) {
		$in_entry = 1;
		}

	if ($in =~ /<\/text/) {
		$in_entry = 0;
		}

	if ($in =~ /<comment>/ || $in =~ /^&lt;/ || $in =~ /<text[^>]*>&lt;/) {
		$in_entry = 0;
		}
		
	if ($in =~ /== \{\{=/ || $in =~ /==\{\{=/) { ## this is usually the pattern that sets language; only want french
		if ($in =~ /== \{\{=fr=\}\}/ || $in =~ /==\{\{=fr=\}\}/) {
			$counter_4_title = $counter_4_title + 1;
			$got_french = 1;
			$in_french_word = 1;

			if ($counter_4_title < 2) { ## pop out headword tag at first language declaration to eliminate non-french entries
				$title_count = $title_count +1;
				my $line = "\n<div1 type=\"entry\" word=\"$entry_word\" n=\"$title_count\">\n";
				push(@OUT, $line);
				}

			}
		else {
			$got_french = 0;
			}
		}

	if ($in =~ /\{\{trad/ || $in =~ /^\{\{-trad-/) { ## translations, BAD!
		$got_french = 0;
		}

	if ($in =~ /\{\{-?[a-z\xc3]/) { ## this is a convoluted way of distinguishing good/bad stuff below and inside translations
		if ($in =~ /\{\{-?trad/) {
			}
		elsif ($in =~ /{-?pron/ && $in_french_word) {
			$got_french = 1;
			}
		else {
			if ($in =~ /fr\}\}/ || $in =~ /\|fr\|/) {
				$got_french = 1;
				}
			}
		}

	if ($in_entry && $got_french) {
		&make_entry($entry_word, $in);
		}
	}


######################
## makin' it happen ##
## with some subs   ##
######################

#######################
## just accumulating ##
## lines from the    ##
## definition. don't ##
## really need the   ##
## entry word value  ##
## as it is a global ##
#######################

sub make_entry {
	my($entry_word, $in) = @_;
	$all_lines .= $in;
	&munge_entry($all_lines);
}

###################
## time to munge ##
###################

sub munge_entry {
	my($all_lines) = $_;
	$all_lines =~ s/^{{-/<SPLIT>{{-/;
	@ENTRY_LINES = split ("<SPLIT>", $all_lines);

	foreach my $line(@ENTRY_LINES) {

		$hash_key_match = "";
		$hash_value_match = "";
		$i_am_special = 0; ## typical gymnastics with logic....

		$line =~ s/(\#+\**)/$1 /g; ## no such thing as perfect data.... losing entries

		if ($line =~ m/^\{\{[^\}]*\}\}/) {
			if ($line =~ /\|/) {
				$line =~ m/\{\{-([^\|]*)\|/g;
				$hash_key_match = $1;
				}
			else {
				$line =~ m/\{\{-([^-]*)-/;
				$hash_key_match = $1;
				}
			$hash_key_match =~ s/\xc3\xa9/e/g;
			$hash_key_match =~ s/-//g;
			}

		#print $hash_key_match . "\n";

		$hash_value_match = $TAG_HASH{$hash_key_match};

		#$hash_value_match = Encode::decode('utf8', $hash_value_match);

		if ($hash_value_match) {
			#print $hash_value_match . "-->" . $hash_key_match . "\n";
			$i_am_special = 1;
			if ($hash_key_match =~ /$parts_o_speech/) {
				$line = "\t<div2 type=\"pos\" word=\"$entry_word\" n=\"$hash_value_match\">\t$line";
				}
			else {
				$line = "\t<div2 type=\"$hash_key_match\" word=\"$entry_word\" n=\"$hash_value_match\">\t$line";
				}
			$line = &clean_line($line);
			#print $line;
			push(@OUT, $line);
			}

		if ($line =~ /^\{\{fr-rég/) {
			$i_am_special = 1;
			$line =~ m/\{\{([^\}]*)\}/;
			my $pronunciation = $1;
			$line = "\t<div2 type=\"pronunciation\" word=\"$entry_word\" n=\"$pronunciation\">\t$line";
			$line = &clean_line($line);
			push(@OUT, $line);
			}

		if ($line =~/^\#/) {
			$count = 1;
			$line_depth = $line;
			$line_depth =~ s/^([\#\*]*) .*/$1/;
			$line_depth =~ s/^([\#\*]*).*/$1/g;
			$counter = $line_depth;
			while ($counter =~ /\#/) {
				$count = $count +1;
				$counter =~ s/\#//;
				}
			}

		if ($line =~ /^\# /) {
			$line = "\t<div$count type=\"def\" word=\"$entry_word\">\t$line";
			#print $line;
			$line = &clean_line($line);
			push(@OUT, $line);
			}

		elsif ($line =~ /\#\# /) {
			$line = "\t<div$count type=\"subdef\" word=\"$entry_word\">\t$line";
			$line = &clean_line($line);
			push(@OUT, $line);
			}

		elsif ($line =~ /\#\* /) {
			$count = $count + 1;
			$line = "\t<div$count type=\"example\" word=\"$entry_word\">\t$line";
			$line = &clean_line($line);
			push(@OUT, $line);
			}

		else {
			if ($i_am_special) {
				}
			else {
				$line = &clean_line($line);
				push(@OUT, $line);
				}
			}
		}

}

#######################
## just what it says ##
## format and clean  ##
## out da crap...    ##
#######################

sub clean_line {
	my($line) = $_[0];

	if ($line =~ /\[\[[a-z]*:[^\]]*\]\]/i) {
		if ($line =~ /image:/i) {
			$line = $line;
			return $line;
			}
		else {
			$line = "";
			}
		}
	#$line =~ s/\[\[[a-z]*:[^\]]*\]\]//g;
	#$line =~ s/\[\[([^\|]*)\|([^\]]*)\]\]/$2/g; ## oh my god, kill me now.
	#$line =~ s/\[\[([^\|]*)\|([A-Z][^\]]*)\]\]/$2/g; ## oh my god, kill me now.

	$line =~ s/\[\[([^\]]*)\]\]/<<$1>>/g; ## gotta do what ya gotta do when straightforward regex does not work...
	if ($line =~ /<</) {
		$line =~ s/<<([^\|]*)\|/<<$1<CHUCK>/g;
		}
	$line =~ s/<<([^<]*)<CHUCK>([^>]*)>>/$2/g;
	$line =~ s/<<([a-zA-Z$utf8_chars]*)>>/$1/g;
	$line =~ s/<CHUCK>/\|/g;
	$line =~ s/<<//g;
	$line =~ s/>>//g;

	return $line;
}


#######################
## finally, just     ##
## printing out..... ##
#######################

foreach my $line (@OUT) {
       print $line;
       }

############################
## ---------------------- ##
## Old, unneeded stuff    ##
## ---------------------- ##
############################

#print Dumper(%HASH_TEST);


#for my $entry (keys %HASH_TEST) {
#       print "ENTRY --> $entry: \t @{ $HASH_TEST{$entry} }\n";
#       }

# for building hash 

#push @{ $HASH_TEST{$entry_word} }, $line;
