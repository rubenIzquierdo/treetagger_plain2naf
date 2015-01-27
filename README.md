#Treetagger wrapper#

This module implements a wrapper around [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) that allows to work with [KAF](https://github.com/opener-project/kaf/wiki/KAF-structure-overview) or
[NAF](http://www.newsreader-project.eu/files/2013/01/techreport.pdf) as input/output files. The following languages are allowed by the wrapper: English, Dutch, German, Spanish, Italian and French, although is very
easy to add new languages.

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
git clone https://github.com/rubenIzquierdo/treetagger_kaf_naf
cd treetagger_kaf_naf
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

The requirement as input is a valid KAF/NAF file which has been processed by one tokeniser and it contains a correct text layer.
Once installed you can try one of the example files on the `examples` subfolder, by running:
```shell
$ cat examples/input.en.kaf | python treetagger.py > my_output.en.kaf
```

This will process the file `examples/input.en.kaf` and the result will be storef in the file `my_output.en.kaf`, which should be the same
(with exception of the time stamps) than the file `examples/output.en.kaf`. You will find example files for the rest of languages in the same
`examples` folder.

##Contact##

* Ruben Izquierdo Bevia
* ruben.izquierdobevia@vu.nl
* http://rubenizquierdobevia.com/
* Vrije University of Amsterdam

##License##

Sofware distributed under GPL.v3, see LICENSE file for details.

