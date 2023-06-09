import re
import sqlite3 
from urllib.request import urlopen



print ("nos differentes options de web scraping de mon site nkms les presidents")
print ("1- creation de ma base de donnee president ")
print ("2- insertion  de donnee des presidents a partir de mon site ")
print ("3- telechharger mon site ")
print ("4- faire l extraction et netoyage grace aux expressions regulieres ")


# mettre en place une table
def setup_database():
    conn = sqlite3.connect("./presidents.db")
    cur = conn.cursor()
    cur.execute(
        """
        create table if not exists presidents(
         eid integer primary key autoincrement,
         name text not null,
         birthdate text not null,
         sex text not null,
         address text not null, 
         country text not null,
         telephone text not null,
         email text not null
        )
        """)
    conn.close()
    

# inserer les données extraites ds la table
def insert_president(attributes):
    conn = sqlite3.connect("./presidents.db")
    cur = conn.cursor()
    query = """
        insert into presidents (name, birthdate, sex, address, country, telephone, email) 
        values (?, ?, ?, ?, ?, ?, ?)
    """
    cur.execute(query, attributes)
    conn.commit()
    conn.close()
    
    
# telecharger le document html
# sauvegarder le doc html ds un fichier sur mon ordi
def download_html_document(link):
    doc = urlopen(link).read().decode()
    f = open("./mon_document.html", "w")
    f.write(doc)
    print("document telechargé avec succes")
    f.close()
    
# faire l'extraction des données
def extract(filename="./mon_document.html"):
    f = open(filename, "r")
    html = f.read()
    
    motif = r'<div class="table-row">\n.*?\t\t\t</div>\n'
    rows = re.findall(motif, html, re.DOTALL)
    
    for r in rows:
        motif2 = r'<div class="table-col">(.*)</div>'
        cols = re.findall(motif2, r)
        # inserer ds la table
        insert_president(cols)
        
        
        
# execution
saisi = int(input("Choisissez une option : "))
if saisi == 1:
   setup_database()
elif saisi == 2:
    download_html_document("https://nskm.xyz/index3.html")
elif saisi == 3:
    extract()