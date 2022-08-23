#Author: Pradeep CH
#Version: 1.0
echo Installing qgenerator
git clone https://github.com/ramsrigouthamg/Questgen.ai.git
cp Questgen.ai\Questgen .
rm -r Questgen.ai
echo Installing web servers and development derver
pip install flask
pip install waitress
echo Installing question generator dependancies
pip install torch
pip install transformers
pip install sense2vec
pip install strsim
pip install six
pip install networkx
pip install numpy
pip install scipy
pip install scikit-learn
pip install unidecode
pip install future
pip install joblib
pip install pytz
pip install python-dateutil
pip install flashtext
pip install pandas
pip install SentencePiece
pip install git+https://github.com/boudinfl/pke.git@69337af9f9e72a25af6d7991eaa9869f1322dd72
echo Running configurations
python3 -m nltk.downloader universal_tagset
python3 -m spacy download en
echo Downloading the models
wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
echo Extracting models
tar -xvzf  s2v_reddit_2015_md.tar.gz
echo Removing the extracted files
rm -f s2v_reddit_2015_md.tar.gz
echo Performing test run to pull the remaining model
echo This may take a while....
python3 Script.py
echo Installation completed
echo Start the server by running StartServer.sh