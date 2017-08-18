# romer_backend
back-end to analyse form results
You'll need the following packages:

* pydrive (pip install pydrive)
* pandas (pip install pandas; or conda install pandas)
* fuzzywuzzy (pip install fuzzywuzzy) [for fuzzy string comparisons]
* python-firebase (pip install python-firebase)
* Pyrebase (pip install pyrebase) [replaces python-firebae]

run using:
python run.py

full-setup using anaconda
```
conda create -n a_whole_new_world python=2.7
activate a_whole_new_world  # on windows
conda install pandas
conda install xlrd
conda install requests
pip install pyrebase  # install this one first!
pip install pydrive   # annoying dependancies!
pip install fuzzywuzzy
pip install python-firebase # depricated
python run.py
```
