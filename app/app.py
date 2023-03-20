#### Les Imports / Dependances ####
import random
import base64
import datetime
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
from flask import Flask
import unidecode
import re

#### Les collections Python ####
alphabet = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M", 14:"N", 15:"O", 16:"P", 17:"Q", 18:"R", 19:"S", 20:"T", 21:"U", 22:"V", 23:"W", 24:"X", 25:"Y", 26:"Z"}
alphabet_inverse = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10, "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26}
cartes = {1: "1C", 2: "2C", 3: "3C", 4: "4C", 5: "5C", 6: "6C", 7: "7C", 8: "8C", 9: "9C", 10: "10C", 11: "JC", 12: "QC", 13: "KC",
         14: "1D", 15: "2D", 16: "3D", 17: "4D", 18: "5D", 19: "6D", 20: "7D", 21: "8D", 22: "9D", 23: "10D", 24: "JD", 25: "QD", 26: "KD",
         27: "1H", 28: "2H", 29: "3H", 30: "4H", 31: "5H", 32: "6H", 33: "7H", 34: "8H", 35: "9H", 36: "10H", 37: "JH", 38: "QH", 39: "KH",
         40: "1S", 41: "2S", 42: "3S", 43: "4S", 44: "5S", 45: "6S", 46: "7S", 47: "8S", 48: "9S", 49: "10S", 50: "JS", 51: "QS", 52: "KS",
         53: "JN", 54: "JR"}

#### Les fonctions pour l'algo du chiffrement dit Solitaire ####

# Transformation du fichier texte en chaine de caractere possible a chiffré
def transform_text(texte):
    # Converti les accents
    sans_accents = unidecode.unidecode(texte)
    # Supprime les caractères spéciaux
    sans_caracteres_spec = re.sub(r'[^\w\s]', '', sans_accents)
    # Supprime les espaces
    sans_espaces = re.sub(r'\s+', '', sans_caracteres_spec)
    # Supprime tout les chiffres
    sans_chiffres = re.sub(r'\d+', '', sans_espaces)
    # Transforme tout en minuscule
    chaine = sans_chiffres.upper()
    return chaine

# Passer d'un nombre a un caractere
def nombreToCaractere(liste_nombre):
    nombreToCaractere = ""
    alphabet = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M", 14:"N", 15:"O", 16:"P", 17:"Q", 18:"R", 19:"S", 20:"T", 21:"U", 22:"V", 23:"W", 24:"X", 25:"Y", 26:"Z"}
    for i in range(0, len(liste_nombre)):
        nombreToCaractere += alphabet[liste_nombre[i]]
    return nombreToCaractere

# Passer d'un caractere a un nombre
def caractereToNombre(liste_caractere):
    caractereToNombre = []
    alphabet_inverse = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10, "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26}
    for i in range(0, len(liste_caractere)):
        caractereToNombre.append(alphabet_inverse[liste_caractere[i]])
    return caractereToNombre

# Initialisation des cartes au debut de l'algorithme
def initCartes():
    cartes_numeros = list(range(1, 55))
    clef_cartes_nombre = []
    for i in range(54):
        carte_choisi = random.choice(cartes_numeros)
        clef_cartes_nombre.append(carte_choisi)
        cartes_numeros.remove(carte_choisi)
    return clef_cartes_nombre

#### ALGO SOLITAIRE ####
# Changer emplacement Joker Noir (53)
def interpolationJokerNoir(liste_cartes):
    JokerNoir = liste_cartes.index(53)
    if JokerNoir == 53:
        liste_cartes[JokerNoir], liste_cartes[1] = liste_cartes[1], liste_cartes[JokerNoir]
    else:
        liste_cartes[JokerNoir], liste_cartes[JokerNoir + 1] = liste_cartes[JokerNoir + 1], liste_cartes[JokerNoir]
    return liste_cartes

# Changer emplacement Joker Rouge (54)
def interpolationJokerRouge(liste_cartes):
    JokerRouge = liste_cartes.index(54)
    if JokerRouge == 53:
        liste_cartes[JokerRouge], liste_cartes[2] = liste_cartes[2], liste_cartes[JokerRouge]
    elif JokerRouge == 52:
        liste_cartes[JokerRouge], liste_cartes[1] = liste_cartes[1], liste_cartes[JokerRouge]
    else:
        liste_cartes[JokerRouge], liste_cartes[JokerRouge + 2] = liste_cartes[JokerRouge + 2], liste_cartes[JokerRouge]
    return liste_cartes

# Interpolation liste des valeurs entre les jokers
def interpolationParJokers(liste_cartes):
    JokerNoir = liste_cartes.index(53)
    JokerRouge = liste_cartes.index(54)
    premierTas = liste_cartes[: min(JokerNoir, JokerRouge)]
    secondTas = liste_cartes[min(JokerNoir, JokerRouge) + 1 : max(JokerNoir, JokerRouge)]
    troisièmeTas = liste_cartes[max(JokerNoir, JokerRouge) + 1:]
    if min(JokerNoir, JokerRouge) == JokerNoir:
        liste_cartes = troisièmeTas + [53] + secondTas + [54] + premierTas
    else:
        liste_cartes = troisièmeTas + [54] + secondTas + [53] + premierTas
    return liste_cartes

# Coupe de la derniere carte
def CoupeCartes(liste_cartes):
    derniereCarte = liste_cartes[-1]
    if derniereCarte == 53 | derniereCarte == 54:
        nbCartesCoupe = 53
    else:
        nbCartesCoupe = derniereCarte
    
    listeCoupe = liste_cartes[: nbCartesCoupe]
    liste_cartes = liste_cartes[nbCartesCoupe : len(liste_cartes) - 1] + listeCoupe + [liste_cartes[-1]]
    return liste_cartes

# Toutes les etapes a realiser 
def etapes(liste_cartes):
    liste_cartes = interpolationJokerNoir(liste_cartes)
    liste_cartes = interpolationJokerRouge(liste_cartes)
    liste_cartes = interpolationParJokers(liste_cartes)
    liste_cartes = CoupeCartes(liste_cartes)
    return liste_cartes


# Creation de la clef
def creerClef(liste_cartes, messageACoder):
    clef = []
    while len(clef) < len(messageACoder):
        premiereCarte = liste_cartes[0]
        carte = liste_cartes[premiereCarte - 1]
        if carte == 53 or carte == 54:
            liste_cartes = etapes(liste_cartes)
        else:
            if carte > 26:
                carte -= 26
            clef.append(carte)
            liste_cartes = etapes(liste_cartes)
    return clef

# Crypter le texte de base en texte crypte
def cryptageFichier(clef, fichierSource):
    fichierSource = caractereToNombre(fichierSource)
    fichier_crypte_nombre = []
    for i in range(0, len(fichierSource)):
        if fichierSource[i] + clef[i] > 26:
            caractere_crypte = fichierSource[i] + clef[i] - 26
        else:
            caractere_crypte = fichierSource[i] + clef[i]
        fichier_crypte_nombre.append(caractere_crypte)
    return fichier_crypte_nombre

# Dechiffrage du message chiffre grace a la cle
def decodageCaractere(liste_nombre_a_decoder, clef_nombre):
    fichier_decode_nombre = []
    fichier_decode = ""
    for i in range(0, len(liste_nombre_a_decoder)):
        if liste_nombre_a_decoder[i] < clef_nombre[i]:
            lettre_decode = liste_nombre_a_decoder[i] + 26 - clef_nombre[i]
        else:
            lettre_decode = liste_nombre_a_decoder[i] - clef_nombre[i]
        fichier_decode_nombre.append(lettre_decode)
    fichier_decode = nombreToCaractere(fichier_decode_nombre)
    return fichier_decode


#### APPLI VISUEL AVEC DASH ####
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div([
    
    html.Div(["Plateforme Projet Chiffrement Solitaire"], style = {'text-align': 'center',
    'font-size': '30px', 'font-weight': 'bold', 'color': '#c41f1f', 'padding-bottom': '20px'}),
    
    html.Div(["Les masjuscules, accents, caractères spéciaux et espaces seront automatiquement retirés ou transformés lors du chargement du fichier texte."],
            style = {'padding-bottom': '30px',
    'font-size': '25px', 'font-weight': '600', 'color': '#3f3e3e', 'text-align': 'center'}),
    
    # Input Upload fichier
    dcc.Upload(
        id='upload_text_file',
        children=html.Div([
            'Glisser/déposer ou sélectionner un fichier texte'
        ], style={'textAlign': 'center'}),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'margin-bottom': '50px',
            'font-size': '25px',
            'font-weight': 'bold'
        },
        multiple=False),
    
    # Input Button afficher le message du fichier texte
    html.Div([
        html.Button('Afficher le message original', id='show_text_file', n_clicks=0)
    ], style={'text-align': 'center', 'width': '100%', 'margin-bottom': '20px'}),
    
    # Output du bouton afficher le message du fichier texte
    html.Div(id='output_show_file', style={'whiteSpace': 'pre-line', 'margin': '10px', 'text-align': 'center'}),
    
    # Boutons pour les différentes fonctionnalités de l'algo du "solitaire"
    html.Div([
        html.Button("Afficher l'ordre du jeu de carte à l'initialisation", id='button_init_cartes', n_clicks=0),
        html.Button('afficher la clé', id='button_key', n_clicks=0),
        html.Button('afficher le message chiffré', id='button_chiffred', n_clicks=0),
        html.Button('afficher le message déchiffré', id='button_unchiffred', n_clicks=0)
    ], style={'display': 'flex', 'justify-content': 'center', 'width': '100%'}) ,
    
    # Output pour les différentes fonctionnalités de l'algo du "solitaire"
    html.Div([
        html.Div(id='output_init_cartes', style={'word-break': 'break-word', 'margin': '1%', 'width':'22%', 'text-align': 'center'}),
        html.Div(id='output_key'),
        html.Div(id='output_chiffred'),
        html.Div(id='output_unchiffred')
    ], style={'display': 'flex', 'justify-content': 'center', 'width': '100%'})
    
])



def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'txt' in filename:
            # Assure que le contenu est un fichier texte
            return transform_text(decoded.decode('utf-8'))
        else:
            return 'Le fichier chargé n\'est pas un fichier texte.'
    except Exception as e:
        print(e)
        return 'Une erreur est survenue lors de la conversion du fichier.'

@app.callback(Output('output_show_file', 'children'),
              Input('show_text_file', 'n_clicks'), 
              State('upload_text_file', 'contents'),
              State('upload_text_file', 'filename'))

def show_file(n_clicks, contents, filename):
    show_button1 = True
    if n_clicks > 0 and contents is not None:
        content = parse_contents(contents, filename)
        return content
    else:
        return ""

# Afficher ou non le bouton pour voir le contenu du fichier texte
@app.callback(
    Output('show_text_file', 'style'),
    [Input('upload_text_file', 'contents')])
def toggle_button_visibility(contents):
    if contents is not None:
        return {'width':'50%', 'font-size': '15px', 'font-weight': 'bold'}
    else:
        return {'display': 'none'}    
    
# Afficher ou non le bouton pour afficher l'ordre des cartes à l'initialisation
@app.callback(
    Output('button_init_cartes', 'style'),
    [Input('upload_text_file', 'contents')])
def toggle_button_visibility(contents):
    if contents is not None:
        return {'margin': '1%', 'width': '22%', 'font-size': '15px', 'font-weight': 'bold'}
    else:
        return {'display': 'none'}

# Afficher l'initialisation des cartes pour générer la clef
@app.callback(
    Output('output_init_cartes', 'children'),
    Input('button_init_cartes', 'n_clicks'))
def init_cartes(n_clicks):
    if n_clicks:
        tableauxCartes = initCartes()
        chaineCaracteres = ' - '.join(str(e) for e in tableauxCartes)
        return chaineCaracteres
    else:
        return ""
    
# Afficher le bouton pour afficher la clé
@app.callback(
    Output('button_key', 'style'),
    [Input('output_init_cartes', 'children')])
def toggle_button_key_visibility(children):
    if children != '':
        return {'margin': '1%', 'width': '22%', 'font-size': '15px', 'font-weight': 'bold'}
    else:
        return {'display': 'none'}
    
# Afficher l'output pour afficher la clé
@app.callback(
    Output('output_key', 'style'),
    Input('output_init_cartes', 'children'))
def show_output_key(children):
    if children != '':
        return {'word-break': 'break-word', 'margin': '1%', 'width':'22%', 'text-align': 'center'}
    else:
        return {'display': 'none'}
    
# Afficher la clé
@app.callback(
    Output('output_key', 'children'),
    Input('button_key', 'n_clicks'),
    State('output_init_cartes', 'children'),
    State('upload_text_file', 'contents'),
    State('upload_text_file', 'filename'))
def create_key(n_clicks, children, contents, filename):
    if n_clicks:
        texteSource = parse_contents(contents, filename)
        cartes = children
        liste_cartes = cartes.split(' - ')
        init_cartes = []
        for element in liste_cartes:
            init_cartes.append(int(element))
        clef_cartes_nombre = etapes(init_cartes)
        clef = creerClef(clef_cartes_nombre, texteSource)
        clef_caractere = nombreToCaractere(clef)
        return clef_caractere
    else:
        return ""

# Affichage du bouton pour affiché le message crypté
@app.callback(
    Output('button_chiffred', 'style'),
    Input('output_key', 'children'))
def toggle_button_chiffred_visibility(children):
    if children != '':
        return {'margin': '1%', 'width': '22%', 'font-size': '15px', 'font-weight': 'bold'}
    else:
        return {'display': 'none'}
    
# Afficher l'output pour afficher le message crypté
@app.callback(
    Output('output_chiffred', 'style'),
    Input('output_key', 'children'))
def show_output_chiffred(children):
    if children != '':
        return {'word-break': 'break-word', 'margin': '1%', 'width':'22%', 'text-align': 'center'}
    else:
        return {'display': 'none'}

# Affichage du message crypté
@app.callback(
    Output('output_chiffred', 'children'),
    Input('button_chiffred', 'n_clicks'),
    State('output_key', 'children'),
    State('upload_text_file', 'contents'),
    State('upload_text_file', 'filename'))
def create_message_crypted(n_clicks, children, contents, filename):
    if n_clicks:
        texteSource = parse_contents(contents, filename)
        print(children)
        clef = caractereToNombre(children)
        fichier_crypte = cryptageFichier(clef, texteSource)
        fichier_crypte_caractere = nombreToCaractere(fichier_crypte)
        return fichier_crypte_caractere
    else:
        return ""

# Affichage du bouton pour affiché le message décrypté
@app.callback(
    Output('button_unchiffred', 'style'),
    Input('output_chiffred', 'children'))
def toggle_button_dechiffred_visibility(children):
    if children != '':
        return {'margin': '1%', 'width': '22%', 'font-size': '15px', 'font-weight': 'bold'}
    else:
        return {'display': 'none'}

# Afficher l'output pour afficher le message crypté
@app.callback(
    Output('output_unchiffred', 'style'),
    Input('output_chiffred', 'children'))
def show_output_unchiffred(children):
    if children != '':
        return {'word-break': 'break-word', 'margin': '1%', 'width':'22%', 'text-align': 'center'}
    else:
        return {'display': 'none'}
    
# Affichage du message décrypté
@app.callback(
    Output('output_unchiffred', 'children'),
    Input('button_unchiffred', 'n_clicks'),
    State('output_chiffred', 'children'),
    State('output_key', 'children'))
def message_uncrypted(n_clicks, chiffred, key):
    chiffred_number = caractereToNombre(chiffred)
    key_number = caractereToNombre(key)
    return decodageCaractere(chiffred_number, key_number)

if __name__=='__main__':
    app.run_server()