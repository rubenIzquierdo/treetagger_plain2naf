#!/usr/bin/env python
#-*- coding: utf8 *-*


##############################################
# Author:   Ruben Izquierdo Bevia            # 
#           VU University of Amsterdam       #
# Mail:     ruben.izquierdobevia@vu.nl       #
#           rubensanvi@gmail.com             #
# Webpage:  http://rubenizquierdobevia.com   #
# Version:  1.0                              #
# Modified: 27-jan-2015                      #
##############################################

__version__ = '1.0'

### List of changes ####################
# 1.0 --> using KafNafParserPy
#
########################################

import sys
import operator
import time
import argparse
import string
import subprocess
import os

try:
    from lib.KafNafParserPy import *
except:
    try:
        from KafNafParserPy import *
    except:
        print>>sys.stderr,'KafNafParserPy not found in your system or in the lib subfolder.'
        print>>sys.stderr,'It is required before you can use this module'
        sys.exit(-1)
        

os.environ['LC_ALL'] = 'en_US.UTF-8'

def loadMapping(mapping_file):
    map={}
    filename = os.path.join(os.path.dirname(__file__),mapping_file)
    fic = open(filename)
    for line in fic:
        fields = line.strip().split()
        map[fields[0]] = fields[1]
    fic.close()
    return map
	
def find_treetagger():
    '''
    This function tries to find the treetagger via 2 ways:
    1) Checking the TREE_TAGGER_PATH variable in the file ./lib/__init__.py
    2) Checking the environment variable TREE_TAGGER_PATH
       '''
    path_to_treetagger = None
    try:
        from lib import TREE_TAGGER_PATH
        path_to_treetagger = TREE_TAGGER_PATH
    except:
        if 'TREE_TAGGER_PATH' in os.environ:
            path_to_treetagger = os.environ['TREE_TAGGER_PATH']
    
    return path_to_treetagger



if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Applies TreeTagger parser for a given plain input text and generates KAF/NAF with tokens and terms',
                                     version = __version__)
    parser.add_argument('-l',choices=['en','nl','it','es','de','fr'], dest='lang', required=True, help='Language of the input text')
    parser.add_argument('-kaf', action='store_true', dest='generate_kaf', help='Generate KAF output (default NAF)')
   
    args = parser.parse_args()

    if sys.stdin.isatty():
        print>>sys.stderr,'Input stream required.'
        print>>sys.stderr,'Example usage: cat myUTF8file.txt |',sys.argv[0]
        parser.print_help(sys.stderr)
        sys.exit(-1)
    
    this_folder = os.path.dirname(os.path.realpath(__file__))
    complete_path_to_treetagger = find_treetagger()
    if complete_path_to_treetagger is None:
        print>>sys.stderr,'Treetagger could not be found. You need to specify there treetagger is installed in 2 ways:'
        print>>sys.stderr,'\t1)Update the TREE_TAGGER_PATH variable in the file lib/__init__.py'
        print>>sys.stderr,'\t2_Update your TREE_TAGGER_PATH environment variable'
        sys.exit(0)
        
    # In the last version of treetagger all the names of commands have been change from X-utf to just X
    # /cmd/tree-tagger-english-utf8 ==> /cmd/tree-tagger-english
    # This could be a problem in case other version of treetagger is being used.
    treetagger_cmd = mapping_file = model = ''
    if args.lang == 'en':
        treetagger_cmd = complete_path_to_treetagger+'/cmd/tree-tagger-english'
        mapping_file = this_folder +'/mappings/english.map.treetagger.kaf.csv'
        model = 'English models'
    elif args.lang == 'nl':
        treetagger_cmd = complete_path_to_treetagger+'/cmd/tree-tagger-dutch'
        mapping_file = this_folder +'/mappings/dutch.map.treetagger.kaf.csv'
        model = 'Dutch models'
    elif args.lang == 'de':
        treetagger_cmd = complete_path_to_treetagger+'/cmd/tree-tagger-german'
        mapping_file = this_folder +'/mappings/german.map.treetagger.kaf.csv'
        model = 'German models'
    elif args.lang == 'fr':
        treetagger_cmd = complete_path_to_treetagger+'/cmd/tree-tagger-french'
        mapping_file = this_folder +'/mappings/french.map.treetagger.kaf.csv'
        model = 'French models'
    elif args.lang == 'it':
        treetagger_cmd = complete_path_to_treetagger+'/cmd/tree-tagger-italian'
        mapping_file = this_folder +'/mappings/italian.map.treetagger.kaf.csv'
        model = 'Italian models'
    elif args.lang == 'es':
        treetagger_cmd = complete_path_to_treetagger+'/cmd/tree-tagger-spanish'
        mapping_file = this_folder +'/mappings/spanish.map.treetagger.kaf.csv'
        model = 'Spanish models'
    else: ## Default is dutch
        print>>sys.stderr,'Language',my_lang,'not supported by this wrapper'
        sys.exit(0)

    map_tt_to_kaf = loadMapping(mapping_file)
    input_text = sys.stdin.read()
    unicode_input_text = input_text.decode('utf-8','ignore')
    tt_proc = subprocess.Popen(treetagger_cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)

    output, error = tt_proc.communicate(unicode_input_text.encode('utf-8'))
    
    
    if args.generate_kaf:
        my_type = 'KAF'
    else:
        my_type = 'NAF'
    knaf_obj = KafNafParser(type=my_type)
        
    num_token = num_sent = this_offset = 0
    for line in output.splitlines():
        unicode_line = line.strip().decode('utf-8')
        fields = unicode_line.split()
        if len(fields) != 3:
            print>>sys.stderr,'Problem parsing:', unicode_line.encode('utf-8'),' . Line skipped'
            continue
        token,pos,lemma = line.strip().split()
        if lemma=='<unknown>': 
                lemma = token.lower()
                pos+=' unknown_lemma'
        pos_kaf = map_tt_to_kaf.get(pos,'O')
        if pos_kaf in ['N','R','G','V','A','O']:
            type_term = 'open'
        else:
            type_term = 'close'
        token_id = 'w%d' % (num_token + 1)
        lemma_id = 't%d' % (num_token + 1)
        
        # Token
        new_token = Cwf(type=my_type)
        new_token.set_id(token_id)
        new_token.set_length(str(len(token)))
        new_token.set_offset(str(this_offset))
        new_token.set_sent(str(num_sent+1))
        new_token.set_text(token)
        
        #term
        new_term = Cterm(type=my_type)
        new_term.set_id(lemma_id)
        new_term.set_lemma(lemma)
        new_term.set_morphofeat(pos)
        new_term.set_pos(pos_kaf)
        this_span = Cspan()
        this_span.add_target_id(token_id)
        new_term.set_span(this_span)
        
        knaf_obj.add_wf(new_token)
        knaf_obj.add_term(new_term)
        num_token += 1
        this_offset = this_offset + len(token) + 1
        if pos=='$.' or pos =='SENT':
            num_sent += 1
    
    lp_text = Clp()
    lp_text.set_name('Treetagger tokenization')
    lp_text.set_version(__version__)
    lp_text.set_timestamp()
    knaf_obj.add_linguistic_processor('text', lp_text)
    
    lp_term = Clp()
    lp_term.set_name('Treetagger pos-tagger model: '+model)
    lp_term.set_version(__version__)
    lp_term.set_timestamp()
    knaf_obj.add_linguistic_processor('term', lp_term)
    
    knaf_obj.dump(sys.stdout)
 