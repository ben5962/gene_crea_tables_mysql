

CREER UNE BDD
prendre BDD Ecole.pdf
a.dans un fichier "machin.mr", ecrire la structure des tables sous la forme
nomtable (nomchamp1, .... ,nomchampn1)
cas de la clef primaire:
nomtable(#lapk,....)
cas de la clef etrangere:
nontable(champ1,...,lafk#)
cas de la clef primaire composee:
nomtable(#partie1,#partie2,..)
cas de la clef primaire composee de fk:
nomtable(#champ1#,#champ2#,...)

regle de nommage: la fk doit avoir le meme nom que la pk pointee

limitation: pas de fk pointant vers une pk composee
limitation: pas de contrainte ck


prendre BDD Ecole.pdf
b. dans un fichier "machin.dico", ecrire la structure des champs et leur type sous la forme
champ1 typemysql
champZ typemysql
(..)


c. mettre le nom des fichiers machin.dico et machin.mr dans le fichier "creer_une_base.py"
lancer la crea de base:
python3 creer_une_base.py




