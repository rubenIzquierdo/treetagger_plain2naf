#Treetagger wrapper#

This module implements a wrapper around [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) that allows to generate[KAF](https://github.com/opener-project/kaf/wiki/KAF-structure-overview) or
[NAF](http://www.newsreader-project.eu/files/2013/01/techreport.pdf) output files, and accepts UTF-8 plain text as input. The following languages are allowed by the wrapper: English, Dutch, German, Spanish, Italian and French, although is very
easy to add new languages.
* Input: UTF-8 plain text
* Output: KAF/NAF files
* Langs: English, Dutch, German, Spanish, Italian and French

##Installation##

There are two only dependencies for this wrapper:

1. [KafNafParserPy](https://github.com/cltl/KafNafParserPy) library which allows to parse and modify KAF or NAF files
2. TreeTagger itself, which needs to be installed and available on your machine.

There is one script that will perform the whole installation for you, the script `install_dependencies.sh`. This script will install
first the KafNafParserPy library and then the TreeTagger and all the models.

**QUICK INSTALLATION** Basically these are the only steps you need to run
from the command line to get this treetagger-wrapper installed 
```shell
cd your_local_path
git clone https://github.com/rubenIzquierdo/treetagger_plain2naf
cd treetagger_plain2naf$
bash install_dependencies.sh
````

This 3 steps will clone this repository and install all the required dependencies. In case of an error you can try to inspect the installation
script and run the commands one by one.


###If you have already TreeTagger installed###

In this case you just need to run the part of the installation script that clones the KafNafParserPy and then specify where your TreeTagger is installed.
You can do this using two different ways:

1. Edit the file `lib/__init__.py` and set the variable `TREE_TAGGER_PATH` to point to the root path of your installation of treetagger
2. Set the environment variable `TREE_TAGGER_PATH` pointing again to the local path of treetagger


##Usage##

The requirements are:
* Input: UTF-8 plain text
* Output: KAF/NAF files
* Langs: English, Dutch, German, Spanish, Italian and French

Example:

```shell
$ echo 'This is a very simple text in English' | python treetagger_plain2naf.py -l en > my_output.en.naf
```

This will process the given text considering that is English (-l en) and the result will be storef in the file `my_output.en.naf`. You can find the whole
description of the parameters by calling to the program with the parameter `-h`:
```shell
python treetagger_plain2naf.py -h
usage: treetagger_plain2naf.py [-h] [-v] -l {en,nl,it,es,de,fr} [-kaf]

Applies TreeTagger parser for a given plain input text and generates KAF/NAF
with tokens and terms

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l {en,nl,it,es,de,fr}
                        Language of the input text
  -kaf                  Generate KAF output (default NAF)

```

##Contact##

* Ruben Izquierdo Bevia
* ruben.izquierdobevia@vu.nl
* http://rubenizquierdobevia.com/
* Vrije University of Amsterdam

##License##

Sofware distributed under GPL.v3, see LICENSE file for details.

