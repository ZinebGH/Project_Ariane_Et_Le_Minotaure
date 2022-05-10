
from upemtk import *
import random
import copy



# Taille de l'affichage.
TAILLE = 40

DIRECTIONS = {'Up':[-1, 0], 'Right':[0, 1], 'Down':[1, 0], 'Left':[0, -1]}


def niveau(chemin):
	"""Fonction qui permet d'ouvrir le fichier voulu. Renvoi la taille du plateau indiquer en début de chaque fichier 
	et le plateau transformé en liste pour pouvoir le manipuler."""
	with open(chemin, "r") as f:
		lines = f.readlines()
		taille = int(lines[0])

		plateau = []
		for i in range(1, len(lines)):
			lst = []
			for e in lines[i]:
				if  e != '\n':
					lst.append(e)
			plateau.append(lst)


		return (taille, plateau)


# Affiche une image dont le chemin et les coordonnées sont en paramètre.
def afficher_image(ligne, colonne, chemin):
	i = ligne * TAILLE + TAILLE/2
	j = colonne * TAILLE + TAILLE/2

	image(j, i, chemin, ancrage='center')


# Affiche sur la fenêtre les murs ainsi que les personnages.
# posA et posT correspond aux coordonnées d'Ariane et de Thésee respectivement.
def dessiner_plateau(plateau, posA, posT, posV, posH, posP):
	"""Cette fonction nous permet d'afficher sur la fenêtre les murs et les personnages.
		Les paramètres indiqué correspondent aux coordonnée de toutes les entitées"""
	taille = len(plateau)

	for i in range(taille):
		for j in range(taille):
			if plateau[i][j] == '-':
				ligne( j * TAILLE, i * TAILLE + TAILLE/2, (j+1) * TAILLE, i * TAILLE + TAILLE/2 )
			if plateau[i][j] == '|':
				ligne( j * TAILLE + TAILLE/2, i * TAILLE, j * TAILLE + TAILLE/2, (i+1) * TAILLE )
			if plateau[i][j] == '+':
				if (i < taille-1 and plateau[i+1][j] == '|'):
					ligne( j * TAILLE + TAILLE/2, i * TAILLE + TAILLE/2, j * TAILLE + TAILLE/2, (i+1) * TAILLE)
				if (i > 0 and plateau[i-1][j] == '|'):
					ligne( j * TAILLE + TAILLE/2, i * TAILLE, j * TAILLE + TAILLE/2, i * TAILLE + TAILLE/2)
				if ( j < taille-1 and plateau[i][j+1] == '-' ):
					ligne( j * TAILLE + TAILLE/2, i * TAILLE + TAILLE/2, (j+1) * TAILLE, i * TAILLE + TAILLE/2)
				if ( j > 0 and plateau[i][j-1] == '-' ):
					ligne( j * TAILLE, i * TAILLE + TAILLE/2, j * TAILLE + TAILLE/2, i * TAILLE + TAILLE/2)


	# On affiche Ariane puis Thésée.
	afficher_image(posP[0], posP[1], "media/porte.png")
	afficher_image(posA[0], posA[1], "media/ariane.png")
	afficher_image(posT[0], posT[1], "media/thesee.png")
	afficher_image(posH[0], posH[1], "media/minoH.png")
	afficher_image(posV[0], posV[1], "media/minoV.png")

	# Affichage des commandes
	
	
	texte(1050,20,'R : Retry', police="Fixedsys", taille= 50 )
	texte(1050,100,'B : Back', police="Fixedsys", taille= 50 )
	texte(1050,200,'M : Menu', police="Fixedsys", taille= 50 )
	texte(1050,300,'Q : Quit', police="Fixedsys", taille= 50 )
	texte(1050,400,'A : Cancel', police="Fixedsys", taille= 50 )




def recuperer_personnages(plateau):
	"""Ici on parcours le plateau tout entier pour récupérer les coordonnées de chaque entitée, puis les renvoie dans cet ordre :
		Position d' Arianne - Thésée - Porte - minotaure Vertical - Minotaure Horizontal."""
	for i in range(len(plateau)):
		for j in range(len(plateau)):
			if plateau[i][j] == 'A':
				posA = [i, j]
			if plateau[i][j] == 'T':
				posT = [i, j]
			if plateau[i][j] == 'P':
				posP = [i, j]
			if plateau[i][j] == 'V':
				posV = [i, j]
			if plateau[i][j] == 'H':
				posH = [i, j]

	return [posA, posT, posP, posV, posH]


# Renvoie Vrai si le coup est légal, c'est à dire si Ariane se déplace vers une case libre.
def est_permis(plateau, perso, direction):
	"""Dans cette fonction on calcule la nouvelle case vers laquelle Arianne va se déplacer. On vérifié si elle ne dépasse pas la taille du plateau.
		On récupère la case du mur, c'est à dire la case qui se trouve entre la case d'Arianne et celle où elle se déplace. Si la nouvelle case est
		 un minotaure, ou s'il y a un mur entre les 2 cases, on renvoie Faux sinon Vrai"""
	i = perso[0] + 2*DIRECTIONS[direction][0]
	j = perso[1] + 2*DIRECTIONS[direction][1]
	t = len(plateau)

	if j < 1 or j >= t - 1:
		return False


	if i < 1 or i >= t - 1:
		return False


	nouvelle_case = plateau[i][j]

	
	i = perso[0] + DIRECTIONS[direction][0]
	j = perso[1] + DIRECTIONS[direction][1]
	mur = plateau[i][j]
	
	
	if (nouvelle_case == 'V') or (nouvelle_case == 'H') or (mur == '-') or (mur == '|'):
		return False
	else:
		return True

# Déplace un personnage dans la direction donnée en paramètre.
def deplacer_perso(plateau, perso, direction):
	"""Dans cette fonction on calcul les nouvelles coordonnées après une certaine direction donnée en paramètre,
	la nouvelle case correspond à la lettre du personnage et on remplace "l'ancienne" position du personnage par un espace. Pour finir
	on met à jour les coordonnées du personnage."""

	nouvelle_case = [0, 0]
	nouvelle_case[0] = perso[0] + 2*DIRECTIONS[direction][0]
	nouvelle_case[1] = perso[1] + 2*DIRECTIONS[direction][1]


	plateau[ nouvelle_case[0] ][ nouvelle_case[1] ] = plateau[ perso[0] ][ perso[1] ]
	
	plateau[ perso[0] ] [ perso[1] ] = ' '
				

	perso[0] += 2*DIRECTIONS[direction][0]
	perso[1] += 2*DIRECTIONS[direction][1]




def est_a_une_case(plateau, perso, perso_a):
	""" Si Thésée peut rejoindre Ariane en une case, renvoie la direction à prendre,
	 Renvoie None sinon. Pour cela on prend les coordonnées de Thésée et d'Ariane en paramètre.
	 Pour chaque direction qui sont répertorié dans un dictionnaire, on prendra les coordonnées que l'on rajoutera à ceux de Thésée dans une nouvelle variable.
	 Ensuite dans cette même boucle on vérifie si la nouvelle case correspond à celle d'Ariane mais aussi si le déplacement d'une case est permis : si c'est le cas
	 on retournera la direction que le personnage Thésée devra prendre.
	 Sinon on ne renvoie rien"""
	for direction in DIRECTIONS:
		i = perso[0] + 2*DIRECTIONS[direction][0]
		j = perso[1] + 2*DIRECTIONS[direction][1]
		nouvelle_case = [i, j]

		if (nouvelle_case == perso_a) and est_permis(plateau, perso, direction):
			return direction

	return None





def alignee_ligne(perso1, perso2):
	"""Indique lorsque le minotaure et Ariane sont sur la meme ligne"""
	return perso1[0] == perso2[0]

def alignee_colonne(perso1, perso2):
	"""Indique lorsque le minotaure et Ariane sont sur la meme colonnee"""
	return perso1[1] == perso2[1]

#Gére les déplacement possible du minotaure V
def deplacer_minotaure_V(plateau, perso, perso_a, taille):
	"""Sert à déplacer le minotaure verticale vers la direction d'Ariane de haut en bas puis de gauche à droite.
		On définit en premier le cas où le minotaure peut enfin ce déplacer de gauche à droite :
		on donne une valeur à direction ('droite') si la position du minotaure est plus petite que celle d'Ariane sur la même ligne sinon la direction est 'gauche'
		donc on vérifie si le minotaure et Ariane sont sur la meme ligne grâce à la fonction 'alignee_ligne' 
		et si c'est le cas, la valeur de la variable directiion ne se modifie pas. Ensuite
		on deplace le minotaure jusqu'a que son déplacement soit interdit (cela est vérifié par la fonction est_permis) et que la valeur de leur coordonnées de 
		leur positions sur la ligne soit différente.
		Sinon direction aura donc les valeurs de bases : 'haut' et 'bas'. Il pourra ainsi ce déplacer de haut en bas tant qu'il ne rencontre pas d'obstacle et
		que la position d'Ariane et du minotaure ne soit pas identiques sur les lignes du plateau. l pourra ce déplacer de gauche à droite seulement lorsqu'il 
		se trouve sur la même ligne qu'Ariane"""
	direction =  'Right' if perso[1] < perso_a[1] else 'Left'	

	if alignee_ligne(perso, perso_a):
		while est_permis(plateau, perso, direction) and  perso[1] != perso_a[1] : 
			deplacer_perso(plateau, perso, direction)

	else:
		direction =  'Down' if perso[0] < perso_a[0] else 'Up'	
		while est_permis(plateau, perso, direction) and  perso[0] != perso_a[0]: 
			deplacer_perso(plateau, perso, direction)

def deplacer_minotaure_H(plateau, perso, perso_a, taille):
	"""Sert à déplacer le minotaure horizontale vers la direction d'Ariane de droite a gauche puis de haut en bas.
		On définit en premier le cas où le minotaure peut enfin ce déplacer de haut en bas :
		on donne une valeur à direction ('bas') si la position du minotaure est plus petite que celle d'Ariane sur la même colonne sinon la direction est 'haut'
		donc on vérifie si la le minotaure et Ariane sont sur la meme colonne grâce à la fonction 'alignee_colonne' 
		et si c'est le cas, la valeur de la variable directiion ne se modifie pas. Ensuite
		on deplace le minotaure jusqu'a que son déplacement soit interdit (cela est vérifié par la fonction est_permis) et que la valeur de leur coordonnées de 
		leur positions sur la colonne soit différente.
		Sinon direction aura donc les valeurs de bases : 'droite' et 'gauche'. Il pourra ainsi ce déplacer de droite a gauche tant qu'il ne rencontre pas d'obstacle et
		que la position d'Ariane et du minitore ne soit pas identique sur les lignes. l pourra ce déplacer de haut en bas seulement lorsqu'il se trouve sur la même
		 colonne qu'Ariane"""
	direction =  'Down' if perso[0] < perso_a[0] else 'Up'	

	if alignee_colonne(perso, perso_a):
		while est_permis(plateau, perso, direction) and  perso[0] != perso_a[0]: 
			deplacer_perso(plateau, perso, direction)

	else:
		direction =  'Right' if perso[1] < perso_a[1] else 'Left'	
		while est_permis(plateau, perso, direction) and  perso[1] != perso_a[1]: 
			deplacer_perso(plateau, perso, direction)

	

def afficher_fin(res, taille,ancien_p):
	"""Permet d'afficher un message au joueur suivant son résultat obtenu"""
	if res == 1:
		texte(((2*taille+1)*TAILLE/2) - 150,((2*taille+1)*TAILLE/2)-150,'DÉFAITE !', couleur='red', police="Fixedsys", taille=50)
		texte(((2*taille+1)*TAILLE/2) + 500,((2*taille+1)*TAILLE/2)+100, 'Pour relancer la partie ')
		texte(((2*taille+1)*TAILLE/2) + 500,((2*taille+1)*TAILLE/2)+150, 'appuyer sur la touche R')
		texte(((2*taille+1)*TAILLE/2) + 500,((2*taille+1)*TAILLE/2)+ 300, 'Pour retourner au choix')
		texte(((2*taille+1)*TAILLE/2) + 530,((2*taille+1)*TAILLE/2)+ 350, 'du labyrinthe cliquez ')
		texte(((2*taille+1)*TAILLE/2) + 570,((2*taille+1)*TAILLE/2)+ 400, 'sur la fenêtre')
		x, y, ev = attente_clic_ou_touche()

		while y != 'r':
			attente_clic_ou_touche()
		if y== 'r':
			efface_tout()
			jouer(ancien_p,taille)
	
		
	elif res == 0:
		texte(((2*taille+1)*TAILLE/2) - 150,((2*taille+1)*TAILLE/2)-150,'VICTOIRE !', couleur='black', police="Fixedsys", taille=50)
		texte(((2*taille+1)*TAILLE/2) + 500,((2*taille+1)*TAILLE/2)+100, 'Cliquez pour revenir sur')
		texte(((2*taille+1)*TAILLE/2) + 500,((2*taille+1)*TAILLE/2)+ 150, 'le choix du labyrinthe')



def comment_jouer():
	efface_tout()
	texte(540,200,"Comment jouer ?", police='Fixedys', taille=40)
	texte(120,490,"Pour jouer il suffit d'utiliser les touches : 'Haut', 'Bas', 'Droite'")
	texte(320,520,"et 'Gauche', pour pouvoir ce diriger vers la porte !")
	texte(1090,900,'Retour')
	rectangle(1070,890,1210,950)

	x, y, clic = attente_clic()

	if 1070 <= x <= 1210 and 890 <= y <= 950:
		menu()
	else:
		comment_jouer()


def regle_du_jeu():
	efface_tout()
	texte(540,200,"Règle du jeu", police='Fixedys', taille=40)
	texte(40,450,"Ariane doit se déplacer de case en case pour récupérer Thésée qui lui la rejoint s'il est à une case d'elle pour ensuite", taille = 15)
	texte(40,480,"la porte ensemble. Cependant les minotaures verticaux (déplacement de haut en bas/bas en haut puis s'il se trouve sur la ", taille = 15)
	texte(40,510,"même ligne de gauche à droite/droite à gauche) et horizontaux (de gauche à droite/droite à gauche puis lorsqu'il se ", taille = 15)
	texte(40,540,	"trouvent sur la même colonne de haut en bas/ bas en haut) ne vous rendrons pas la tâche facile : ", taille = 15)
	texte(40,570," si vous ếtes aligné sur la même ligne que le minotaures verticale et qu'il doit jouer, il ", taille = 15)
	texte(40,600,"vous rejoindra sur votre case pour que vous perdiez sauf s'il rencontre un obstacle sur sa trajectoire. ",taille = 15)
	texte(40,630,"Vous devez impérativement ammené à la porte Ariane accompagner de Thésée sans qu'aucun minotaure ne vous attrape !",taille = 15)

	texte(1090,900,'Retour')
	rectangle(1070,890,1210,950)

	x, y, clic = attente_clic()

	if 1070 <= x <= 1210 and 890 <= y <= 950:
		menu()
	else:
		comment_jouer()


def Maps12_choix():
	"""Permet de faire un choix sur le labyrinthe de taille 12x12 en cliquant sur un des rectangles :
		on prend les coordonnées du clic et on vérifie s'ils appartiennent à un encadrement indiquer
	  et commencer à y jouer"""
	efface_tout()

	texte(630,50,'12x12', taille =40, police='Fixedsys')

	texte(440,300, 'Labyrinthe 1')
	texte(740,400, 'Labyrinthe 2')
	texte(1090,900,'Retour')


	rectangle(730,400,970,450)
	rectangle(430,300,660,350)
	rectangle(1070,890,1210,950)


	Maps12 = ['maps/big/big1.txt', 'maps/big/big2.txt']

	x, y, clic = attente_clic()


	if 730 <= x <= 970 and 400 <= y <= 450:
		efface_tout()
		taille, plateau = niveau(Maps12[0])
		jouer(plateau, taille)

	if 430 <= x <= 660 and 300 <= y <= 350:
		efface_tout()
		taille, plateau = niveau(Maps12[1])
		jouer(plateau, taille)
	
	if 1070 <= x <= 1210 and 890 <= y <= 950:
		niveaux()

	else:
		Maps12_choix()



def Maps10_choix():
	"""Permet de faire un choix sur le labyrinthe de taille 10x10 en cliquant sur un des rectangles :
		on prend les coordonnées du clic et on vérifie s'ils appartiennent à un encadrement indiquer
	  et commencer à y jouer"""
	efface_tout()

	texte(630,50,'10x10', taille =40,  police='Fixedsys')
	texte(740,200, 'Sandbox')
	texte(440,300, 'Labyrinthe 1')
	texte(740,400, 'Labyrinthe 2')
	texte(440,500, 'Labyrinthe 3')
	texte(740,600, 'Labyrinthe 4')
	texte(440,700, 'Labyrinthe 5')
	texte(1090,900,'Retour')


	rectangle(730,200,900,250)
	rectangle(430,300,660,350)
	rectangle(730,400,970,450)
	rectangle(430,500,660,550)
	rectangle(730,600,970,650)
	rectangle(430,700,660,750)
	rectangle(1070,890,1210,950)

	Maps10 = ['maps/sandbox.txt', 'maps/labyrinthe1.txt', 'maps/labyrinthe2.txt', 'maps/labyrinthe3.txt', 'maps/labyrinthe4.txt', 'maps/labyrinthe5.txt']

	x, y, clic = attente_clic()


	if 730 <= x <= 900 and 200 <= y <= 250:
		efface_tout()
		taille, plateau = niveau(Maps10[0])
		jouer(plateau, taille)

	if 430 <= x <= 660 and 300 <= y <= 350:
		efface_tout()
		taille, plateau = niveau(Maps10[1])
		jouer(plateau, taille)
	
	if 730 <= x <= 970 and 400 <= y <= 450:
		efface_tout()
		taille, plateau = niveau(Maps10[2])
		jouer(plateau, taille)

	if 430 <=  x <= 660 and 500 <= y <= 550:
		efface_tout()
		taille, plateau = niveau(Maps10[3])
		jouer(plateau, taille)

	if 730 <= x <= 970 and 600 <= y <= 650:
		efface_tout()
		taille, plateau = niveau(Maps10[4])
		jouer(plateau, taille)

	if 430 <= x <= 660 and 700 <= y <= 750:
		efface_tout()
		taille, plateau = niveau(Maps10[5])
		jouer(plateau, taille)

	if 1090 <= x <= 1210 and 890 <= y <= 950:
		niveaux()

	else:
		Maps10_choix()

def Maps8_choix():
	"""Permet de faire un choix sur le labyrinthe de taille 8x8 en cliquant sur un des rectangles :
		on prend les coordonnées du clic et on vérifie s'ils appartiennent à un encadrement indiquer
	  et commencer à y jouer"""
	efface_tout()
	texte(650,50,'8x8', taille =40, police='Fixedsys')
	texte(440,300, 'Labyrinthe 1')
	texte(740,400, 'Labyrinthe 2')
	texte(440,500, 'Labyrinthe 3')
	texte(740,600, 'Labyrinthe 4')
	texte(1090,900,'Retour')

	rectangle(430,300,660,350)
	rectangle(730,400,970,450)
	rectangle(430,500,660,550)
	rectangle(730,600,970,650)
	rectangle(1070,890,1210,950)

	Maps8 = ['maps/small/small1.txt', 'maps/small/small2.txt', 'maps/small/small3.txt', 'maps/small/small4.txt'] 

	x, y, clic = attente_clic()

	if 430 <= x <= 660 and 300 <= y <= 350:
		efface_tout()
		taille, plateau = niveau(Maps8[0])
		jouer(plateau, taille)
	
	if 730 <= x <= 970 and 400 <= y <= 450:
		efface_tout()
		taille, plateau = niveau(Maps8[1])
		jouer(plateau, taille)

	if 430 <= x <= 660 and 500 <= y <= 550:
		efface_tout()
		taille, plateau = niveau(Maps8[2])
		jouer(plateau, taille)

	if 730 <= x <= 970 and 600 <= y <= 650:
		efface_tout()
		taille, plateau = niveau(Maps8[3])
		jouer(plateau, taille)

	if 1080 <= x <= 1210 and 890 <= y <= 950:
		niveaux()
	

	else:
		Maps8_choix()

def Defi_choix():
	efface_tout()

	texte(630,50,'Défi', taille =40,  police='Fixedsys')

	texte(490,300, 'Défi 1')
	texte(790,400, 'Défi 2')
	texte(490,500, 'Défi 3')
	texte(790,600, 'Défi 4')

	texte(1090,900,'Retour')



	rectangle(430,300,660,350)
	rectangle(730,400,970,450)
	rectangle(430,500,660,550)
	rectangle(730,600,970,650)
	rectangle(1070,890,1210,950)

	Defi = ['maps/defi/defi0.txt', 'maps/defi/defi1.txt', 'maps/defi/defi2.txt', 'maps/defi/defi3.txt']

	x, y, clic = attente_clic()


	if 430 <= x <= 660 and 300 <= y <= 350:
		efface_tout()
		taille, plateau = niveau(Defi[1])
		jouer(plateau, taille)
	
	if 730 <= x <= 970 and 400 <= y <= 450:
		efface_tout()
		taille, plateau = niveau(Defi[2])
		jouer(plateau, taille)

	if 430 <=  x <= 660 and 500 <= y <= 550:
		efface_tout()
		taille, plateau = niveau(Defi[3])
		jouer(plateau, taille)

	if 1090 <= x <= 1210 and 890 <= y <= 950:
		niveaux()

	else:
		Defi_choix()


def niveaux():
	"""Regroupe les trois différents groupes de labyrinthes"""
	efface_tout()
	
	texte(520,50,'Choisir un niveaux', taille =40, police='Fixedsys')
	texte(620,200,'Labyrinthe 8x8')
	texte(620,400,'Labyrinthe 10x10')
	texte(620,600,'Labyrinthe 12x12')
	texte(710,800,'Défi')
	texte(1090,900,'Retour')

	rectangle(580,190,920,250)
	rectangle(580,390,920,450)
	rectangle(580,590,920,650)
	rectangle(580,790,920,850)
	rectangle(1070,890,1210,950)

	x, y, clic = attente_clic()


	if 580 <= x <= 920 and 190 <= y <= 250:
		Maps8_choix()
	
	if 580 <= x <= 920 and 390 <= y <= 450:
		Maps10_choix()

	if 580 <= x <= 920 and 590 <= y <= 650:
		Maps12_choix()

	if 580 <= x <= 920 and 790 <= y <= 850:
		Defi_choix()


	if 1070 <= x <= 1210 and 890 <= y <= 950:
		menu()

	else: 
		niveaux()

def aleatoire():
	"""Permet de lancer un des labyrinthes au hasard"""
	maps = ['maps/small/small1.txt', 'maps/small/small2.txt', 'maps/small/small3.txt', 'maps/small/small4.txt', 'maps/big/big1.txt', 'maps/big/big2.txt', 'maps/sandbox.txt', 'maps/labyrinthe1.txt', 'maps/labyrinthe2.txt', 'maps/labyrinthe3.txt', 'maps/labyrinthe4.txt', 'maps/labyrinthe5.txt']
	tab = random.randint(0,12)

	efface_tout()
	taille, plateau = niveau(maps[tab])
	jouer(plateau, taille)


def menu():
	"""C'est à cet endroit que l'on choisi quoi faire : lire les règle du jeu ou encore choisir un niveaux""" 
	efface_tout()
	texte(680,100,'Menu', taille =40, police='Fixedsys')
	texte(340,250, 'Règle du jeu')
	texte(340,600,'Comment jouer ?')
	texte(900,250, 'Niveaux')
	texte(900,600,'Mode Aléatoire')
	texte(700,850,'Quitter')

	rectangle(330,250,580,300)
	rectangle(330,600,660,650)
	rectangle(890,250,1040,300)
	rectangle(890,600,1180,650)
	rectangle(690,850,830,900)

	x, y, clic = attente_clic()


	if 330 <= x <= 580 and 250 <= y <= 300:
		regle_du_jeu()
	
	if 330 <= x <= 660 and 600 <= y <= 650:
		comment_jouer()
	
	if 890 <= x <= 1040 and 250 <= y <= 300:
		niveaux()

	if 890 <= x <= 1180 and 600 <= y <= 650:
		aleatoire()

	if 690 <= x <= 830 and 850 <= y <= 900:
		quit()

	else:
		menu()
	




def jouer(plateau, taille):
	"""Reçois un plateau de jeu ainsi que sa taille, et commence une partie. C'est ici que les déplacements des personnages sont générés"""
	#On sauvegarde la maps actuelle
	ancien_p = copy.deepcopy(plateau)
	# On récupère les coordonnées des personnages.
	posA, posT, posP, posV, posH = recuperer_personnages(plateau)

	ancienne_posA = copy.deepcopy(posA)
	deplacement_A = [ancienne_posA]

	ancienne_posV = copy.deepcopy(posV)
	deplacement_V = [ancienne_posV]

	ancienne_posH = copy.deepcopy(posH)
	deplacement_H = [ancienne_posH]

	ancienne_posT = copy.deepcopy(posT)
	deplacement_T = [ancienne_posT]
	# Tant que la partie n'est pas terminée.
	while ( True ):
		efface_tout()

		
		dessiner_plateau(plateau, posA, posT, posV, posH, posP)
		mise_a_jour()

		# On attend que l'utilisateur fasse quelque chose.
		a_bouge = 0
		event = donne_evenement()
		if type_evenement(event) == 'Touche': # Si l'utilisateur a appuyé sur une touche du clavier.
			if touche(event) == 'r' :
				efface_tout()
				jouer(ancien_p,taille)
				
			if touche(event) == 'b':
				niveaux()
			if touche(event) == 'm':
				menu()

			if touche(event) == 'a':
				if len(deplacement_A) > 1:
					deplacement_A.pop()
					posA = deplacement_A[len(deplacement_A)-1]
					print(posA,'nouv')
					
				if len(deplacement_T) > 1:
					deplacement_T.pop()
					posT = deplacement_T[len(deplacement_T)-1]

				if len(deplacement_H) > 1:
					deplacement_H.pop()
					posH = deplacement_H[len(deplacement_H)-1]

				if len(deplacement_V) > 1:
					deplacement_V.pop()
					posV = deplacement_V[len(deplacement_V)-1]
				
				efface_tout()
				dessiner_plateau(plateau, posA, posT, posV, posH, posP)


			if touche(event) == 'q':
				quit()
			if touche(event) in DIRECTIONS: # Si la touche qui a été appuyée est dans le dictionnaire de directions (cad si c'est haut, droit, bas ou gauche).
				if est_permis(plateau, posA, touche(event)): # Si le joueur a le droit de se déplacer dans cette direction.

					deplacer_perso(plateau, posA, touche(event))
					print(posA)
					ancienne_posA = copy.deepcopy(posA)
					deplacement_A.append(ancienne_posA)
					a_bouge = 1

		# Si le joueur a bougé, c'est au tour de l'ordinateur de jouer.
			if a_bouge:
				deplacement = est_a_une_case(plateau, posT, posA)
				if deplacement != None:
					deplacer_perso(plateau, posT, deplacement)
					ancienne_posT = copy.deepcopy(posT)
					deplacement_T.append(ancienne_posT)
				deplacer_minotaure_V(plateau, posV, posA, taille)
				ancienne_posV = copy.deepcopy(posV)
				deplacement_V.append(ancienne_posV)	
				deplacer_minotaure_H(plateau, posH, posA, taille)
				ancienne_posH = copy.deepcopy(posH)
				deplacement_H.append(ancienne_posH)

			print('dep',deplacement_A)
			if posV == posA or posH == posA:
				res = 1
				break
			elif posA == posP and posT == posP:
				res = 0
				break


	efface_tout()
	dessiner_plateau(plateau, posA, posT, posV, posH, posP)

	#Vérifie si la position d'Ariane n'est pas identique à celle d'un des minotaures
	if posV == posA or posH == posA:
		afficher_fin(1, taille, ancien_p)	

	#Vérifie si la position d'Ariane et de  Thésée est sur la porte
	elif posA == posP and posT == posP:
		afficher_fin(0, taille, ancien_p)

	
	attente_clic()



if __name__ == "__main__" :
	"""Cela regroupe tout ce dont on a besoin pour l'ordre des 
	fonctions pour la mise en marche du jeu"""


	cree_fenetre(1500, 1000)
	image(750, 500, "media/l1.gif")




#TITRE JEU
	texte(750, 250, 'Arianne', couleur="black", ancrage='center',taille=60,police='Fixedsys')
	texte(750, 460, ' & ', couleur='black', ancrage='center',taille=60,police='Fixedsys')
	texte(750, 670, 'Le Minotaure ', couleur="black", ancrage='center',taille=60,police='Fixedsys')

	attente_clic()

	efface_tout()

	menu()



	ferme_fenetre()


