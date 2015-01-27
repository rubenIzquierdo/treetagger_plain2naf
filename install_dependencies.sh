#!/bin/bash

##############################################
# Author:   Ruben Izquierdo Bevia            # 
#           VU University of Amsterdam       #
# Mail:     ruben.izquierdobevia@vu.nl       #
#           rubensanvi@gmail.com             #
# Webpage:  http://rubenizquierdobevia.com   #
# Version:  1.0                              #
# Modified: 27-jan-2015                      #
##############################################


this_folder=$(pwd)
rm -rf lib 2> /dev/null
mkdir lib
cd lib

#####################################
###   Install the KafNafParserPy
#####################################
git clone https://github.com/cltl/KafNafParserPy.git



#####################################
###   Install the TreeTagger software
#####################################
mkdir treetagger
cd treetagger


url_treetagger=""
if [ "$(uname)" == "Darwin" ]; then
  url_treetagger=http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-MacOSX-3.2-intel.tar.gz 
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  url_treetagger=http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.tar.gz
else
  echo "`uname` platform not supported by this script. Install TreeTagger manually"
fi

wget $url_treetagger
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/dutch-par-linux-3.2-utf8.bin.gz	# Dutch models
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/english-par-linux-3.2-utf8.bin.gz	# English models
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/french-par-linux-3.2-utf8.bin.gz 	# French models
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/german-par-linux-3.2-utf8.bin.gz	# German models
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/italian-par-linux-3.2-utf8.bin.gz	# Italian models
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/spanish-par-linux-3.2-utf8.bin.gz	# Spanish
sh install-tagger.sh
rm *.gz
cd .. ## back to lib

#Set the path in the lib/__init__.py script
echo "TREE_TAGGER_PATH=\"$this_folder/lib/treetagger\"" >> __init__.py

echo "ALL INSTALLED"
cd .. #back to the root
