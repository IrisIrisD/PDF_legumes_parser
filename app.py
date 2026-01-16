import streamlit as st
import re, pdfplumber

st.set_page_config(
    page_title="Analyse du pdf des commandes",
    page_icon="logo.png"
)

def trouver_page1_commande(pages):
    #le pdf fourni récapitule la qté par légume avant de préciser les commandes par personne.
    #du coup on cherche ici la première page avec des commandes par personne
    for i in range(len(pages)):
        if (pages[i].extract_text()[0:7]=="PRODUIT") and (pages[i+1].extract_text()[0:7]!="PRODUIT") :
            return i+1
    return 1

def parse_texte(texte, debut, fin):
    pattern = re.escape(debut) + r"\s*(.*?)\s*" + re.escape(fin)
    return re.findall(pattern, texte, flags=re.DOTALL)[0]

def extraire_dune_page(noms, prix, page):
    tables = page.extract_tables()
    #tables[i] = 1 commande (car un rectangle)
    #len(tables) = nb de commandes sur la page 
    
    for i in range(len(tables)):
        #print(tables[i][0][0][:9])
        if(tables[i][0][0][:9]=="ARTICLES\n"):
            noms+=tables[i][0][0][9:-2]+"\n"
            #a faire : enlever nombre
            prix += parse_texte(tables[i][1][0], "Total", "€") +"\n"
            
        #print(tables[i][0])
        #print(noms+f"i={i}, lautre = {tables[i][0][0]}")
        #noms = noms + tables[i][0][0] +"\n"
        #print(tables[i][1][0])
        
        #noms.append(tables[i][0][0])
        #prix.append(parse_texte(tables[i][1][0], "Montant", "€"))

    return noms, prix

def recuperer_liste(nom_pdf):
    with pdfplumber.open(nom_pdf) as pdf:
        pages = pdf.pages
        premiere_commande = trouver_page1_commande(pages)
        #print("La première page avec des commandes est la page " +str(premiere_commande))
        noms = ""
        prix = ""
        for p in range(premiere_commande, len(pages)):
            noms, prix = extraire_dune_page(noms, prix, pages[p])
        print(noms)
        st.text(noms)
        st.text(prix)




#Interface "web"
st.title("Parsing du pdf des légumes 🥦 ")
st.write("importe ici le fichier des commandes ")
uploaded_file = st.file_uploader("Choisis un fichier")
if uploaded_file is not None:
    recuperer_liste(uploaded_file)
    st.write("**Tu peux maintenant copier coller les deux colonnes dans le sheet de la semaine :)**")