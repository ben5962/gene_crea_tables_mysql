# coding: utf-8
import copy
dico = "rdm.dico"
mr = "rdm.mr"
nom_base="rdm"



liste_champs_types = []
liste_des_pk = []
liste_des_fk = []
liste_des_ck = []
liste_des_tables = []

def lire_dico():
    with open(dico) as f:
        for ligne in f:
            nom_var, type_champ = ligne.split()
            liste_champs_types.append({"nom_var": nom_var, "type_champ": type_champ})
         


def lire_mr():
    with open(mr) as g:
        for ligne in g:
            #forcer nv ref vers liste_champs
            liste_champs = []
            nom_table, reste = ligne.split('(')
            print("nom_table: ", nom_table)
            sans_parenth, _ = reste.split(')')
            liste_champs = sans_parenth.split(",")
            print("liste_champs:", liste_champs)
        
        
            score = 0
            cpt_champs = 0
            has_a_fk = False
            while(True):
                if (cpt_champs == len(liste_champs)):
                    break
                else:
                    champ = liste_champs[cpt_champs]
                    if champ[-1] == "#":
                        score +=1
                        print("le champ" + champ + "de " + nom_table + "est une fk")
                cpt_champs += 1
            print(nom_table + "a un score de" + str(score))
            liste_des_tables.append({"score": score, "nom_table":nom_table, "liste_champs": liste_champs})
        


def acces_score(elem):
    return elem['score']

def acces_nom_table(elem):
    return elem['nom_table']

def acces_liste_champs(elem):
    return elem['liste_champs']
                
def acces_nom_champ(elem):
    return elem['nom_var']

def acces_chaine_type(elem):
    return elem['type_champ']


def positionpluspetit(l,accesseur):
    # init:
    # une valeur elevee pour valeur_min
    # dvp
    # à chaque fois que le contenu à la positon i est inferieur à valeur_min
    # il remplace valeur_min et son indice est candidat.
    # la valeur de retour est le dernier candidat
    # arret: 
    # la fin de la liste
    
    # init
    candidat = 0
    valeur_min = accesseur(l[0])
    position_elem = 0
    for elem in l:
        contenu = accesseur(elem)
        if contenu < valeur_min:
            valeur_min = contenu
            candidat = position_elem
        position_elem = position_elem + 1
    return candidat

def echanger(to, fromm, liste):
    liste[to], liste[fromm] = liste[fromm], liste[to]
    return liste 

def tri(l, accesseur):
    
    print("examen de la liste:", l)
    for index in range(len(l) - 1):
        
        for index_parcours_reste_liste in range(index + 1, len(l)):
            if (accesseur(l[index]) > accesseur(l[index_parcours_reste_liste])):
                echanger(index,index_parcours_reste_liste,l)
    return l                    
def estTrie(l,accesseur):
    triOk = True
    
def idem(elem):
    return elem

liste_t = tri(liste_des_tables, acces_score)
#ll = tri([1,3,2],idem)
#print(ll)

def nettoyer(chainePk):
    if chainePk[0] == "#":
        chainePk = chainePk[1:]
    if chainePk[-1] == "#":
        chainePk = chainePk[:-1]
    return chainePk

def isPk(chainePk):
    verite = False
    if chainePk[0] == "#":
        verite = True
        print("ai trouve pk", chainePk)
    return verite

def isFk(chaineFk):
    verite = False
    print("test de", chaineFk)
    if chaineFk[-1] == "#":
        verite = True
        print("ai trouve fk", chaineFk)
    return verite

def getTypeFromNomChamp(nom_champ):
    chaineType = ""
    for elem in liste_champs_types:
        if acces_nom_champ(elem) == nom_champ:
            chaineType = acces_chaine_type(elem)
            break
    return chaineType

#print("apres_tri")
#print(liste_des_tables)

def deguiser_en_pk(chaine_fk_nettoyee):
    if chaine_fk_nettoyee[0] != "#":
        chaine_fk_nettoyee = "#" + chaine_fk_nettoyee
    return chaine_fk_nettoyee


def trouver_table_referencee_par_fk(chaine_fk_nettoyee):
    la_table =  {"score": False, "nom_table": "PASTROUVEE", "liste_champs":False }
    for table in liste_des_tables:
        #je cherche une clef primaire de meme nom que la clef etrangere
        nom_clef_primaire_recherchee = deguiser_en_pk(chaine_fk_nettoyee)
        # pour chaque "enregistrement" "table", acceder au champ "liste_champs"
        liste_champs = acces_liste_champs(table)
        # (c est une liste) et y rechercher un champ dont le nom correspondrait
        # si ca matche on ecrit dans la_table et on breake
        for nom_champ in liste_champs:
            if nom_champ == nom_clef_primaire_recherchee:
                la_table = copy.deepcopy(table)

            

    return la_table


def creer_chaine_base():
    lire_dico()
    lire_mr()
    liste_t = tri(liste_des_tables, acces_score)
    print("-- ordre de creation:")
    for structure_table in liste_des_tables:
        print(acces_nom_table(structure_table), ",")
    chaine = "DROP DATABASE IF EXISTS " + nom_base + ";"
    chaine += "\nCREATE DATABASE " + nom_base + ";"
    chaine += "\nUSE " + nom_base + ";"
    for structure_table in liste_des_tables:
        liste_des_pk = []
        liste_des_fk = []
        chaine += "\n\nCREATE TABLE " + acces_nom_table(structure_table) + "("
        for champ in acces_liste_champs(structure_table):
            #tester avant de nettoyer
            if isPk(champ):
                liste_des_pk.append(nettoyer(champ))
            if isFk(champ):
                liste_des_fk.append(nettoyer(champ))
            #nettoyer avant d inserer dans la chaine
            champ = nettoyer(champ)
            chaine += "\n " + champ + " " + getTypeFromNomChamp(champ) +","
        if liste_des_pk:
            chaine_pk = "CONSTRAINT pk_"
            for champ_sur_lequel_sapplique_pk in liste_des_pk:
               chaine_pk = chaine_pk + "_" + champ_sur_lequel_sapplique_pk
            chaine_pk = chaine_pk + " PRIMARY KEY("
            for champ_sur_lequel_sapplique_pk in liste_des_pk:
                chaine_pk = chaine_pk + champ_sur_lequel_sapplique_pk + ","
            if chaine_pk[-1] == ",":
                chaine_pk = chaine_pk[:-1]
            chaine_pk += ")"
            if liste_des_fk or liste_des_ck:
                chaine_pk += ","
            liste_des_pk = []

            
        chaine += "\n" + chaine_pk
        if liste_des_fk:
            for nom_champ_sur_lequel_contrainte_fk in liste_des_fk:
                chaine_fk = ""
                table_trouvee = {}
                table_trouvee = trouver_table_referencee_par_fk(nom_champ_sur_lequel_contrainte_fk)
                chaine_fk = "\nCONSTRAINT fk_"
                chaine_fk += acces_nom_table(structure_table) + "_"
                chaine_fk += nom_champ_sur_lequel_contrainte_fk 
                chaine_fk += " FOREIGN KEY (" 
                chaine_fk += nom_champ_sur_lequel_contrainte_fk 
                chaine_fk += ") REFERENCES " 
                chaine_fk += acces_nom_table(table_trouvee) 
                chaine_fk += "(" 
                chaine_fk += nom_champ_sur_lequel_contrainte_fk 
                chaine_fk += "),"
                chaine += chaine_fk
            chaine = chaine[:-1]
        chaine += "\n);"

    return chaine


def main():
    chaine = creer_chaine_base()
    nom_fichier = "creer_" + nom_base + ".sql"
    with open(nom_fichier, mode = 'w') as w:
        w.write(chaine)
        w.close()
    print("ai ecrit le fichier ", nom_fichier)
                
main()
#print(chaine)
