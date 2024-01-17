# Pré-requis : avoir créé un environnement conda python 3.9
# ==================================================================================================================== #
# Useful librairies


import csv
import requests
from bs4 import BeautifulSoup
import promptlib #pip install prompt
import os

# ----------------------------------------------------------------------------------------------------------------------
#                                               Useful functions
# ----------------------------------------------------------------------------------------------------------------------

#URL for pollutants
CSV_URL = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/2022/"
text=[]
#To select directory to download files
prompter = promptlib.Files()
dir = prompter.dir()
#Set working directory to chosen directory
os.chdir(dir)
#Accessing contents of url
r = requests.get(CSV_URL)
soup = BeautifulSoup(r.text, 'html.parser')
#Get all links tags with href
if soup.findAll('a'):
    for i in soup.findAll('a'):
        text.append(i.get('href'))
else:
    text='NA'
#Store list of urls
textt=text[1:]

text=[]
#Search for links ending with extension .csv
for i in textt:
    if i[-3:]=="csv":
        text.append(i)
#Download all selected links
for i in text:
    with requests.Session() as s:
        download = s.get(CSV_URL+i)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=';')
        my_list = list(cr)
    with open(i, 'w', encoding='utf-8') as f:

        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(my_list[0])
        write.writerows(my_list)