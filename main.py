import pygame, time, sys
from copy import deepcopy
import ordinateur_level
import monkey_level

winner = -1
grille = [[0] * 7 for _ in range(6)] # création d'un tableau de jeu
JAUNE = pygame.image.load('ressources/PionJaune.png')
ROUGE = pygame.image.load('ressources/PionRouge.png')

#set-up de pygame
pygame.init()
pygame.display.set_caption("Wish Blast")
screen = pygame.display.set_mode((700, 600))
winner_song = pygame.mixer.Sound("ressources/win_sound.ogg")
bouton_pause = pygame.image.load('ressources/bouton pause.png')
bouton_pause = pygame.transform.scale(bouton_pause, (100, 24))
nom_jeu = pygame.image.load('ressources/titre jeu.png')
nom_jeu = pygame.transform.scale(nom_jeu, (100, 24))
niveau1 = pygame.image.load('ressources/niveau1.png')
niveau2 = pygame.image.load('ressources/niveau2.png')
niveau3 = pygame.image.load('ressources/niveau3.png')
monkey = pygame.image.load('ressources/monkey.png')


def case_libre_la_plus_basse(grille:list,num_colonne:int)->int:
    """
    Fonction qui prend en paramètres une matrice représentant un plateau de puissance 4
    ainsi qu'un numéro de colonne et renvoie la case libre la plus basse dans cette colonne
    """
    fin = 5
    while grille[fin][num_colonne] != 0 and fin != -1:
        fin-=1
    return fin






def animation_pion(x:int, y:int, img):
    """
    Fonction qui prend en paramètres des coordonnées de la matrice d'un plateau de jeu de puissance 4
    et simule une animation d'un jeton qui tombe du haut du plateau jusqu'a sa coordonnée y
    """
    for co in range(y+1):
        screen.blit( pygame.image.load('ressources/trou.png'), ((x*100, (co-1)*100)))
        pygame.display.flip()
        screen.blit( img, (x*100, co*100) )
        pygame.display.flip()
        time.sleep(0.1)
    pygame.event.clear()

def afficher(j_coup:int, x:int, y:int):
    """
    Fonction qui prend en paramètre le numéro du joueur qui joue (1 ou 2) et les coordonnées
    de l'endroit ou il souhaite jouer, et affiche grace à la fonction animation le jeton à sa bonne place
    """
    if j_coup == 1:
        pion = JAUNE
    else: #j_coup == 2
        pion = ROUGE
    animation_pion(x, y, pion)
    grille[y][x] = j_coup
    #recharge le bouton pause et le nom à chaque passage pour éviter que quelque chose soit blit dessus
    screen.blit( bouton_pause, (600, 0))
    screen.blit( nom_jeu, (300, 0) )
    pygame.display.flip()

def afficher_plateau(plateau:list):
    """
    Fonction qui prend en paramètre une matrice représentant un plateau de puissance 4
    et affiche le plateau avec les jetons
    """
    for y in range(6):
        for x in range(7):
            if grille[y][x] == 1:
                pion = JAUNE
                screen.blit(pion, (x*100, y*100))
            elif grille[y][x] == 2:
                pion = ROUGE
                screen.blit(pion, (x*100, y*100))





"""
Fonctions qui vérifient si la partie est finit et actualise la varibale global winner
"""
def alignement_horizontal(grille:list):
    global winner
    for li in range(6):
        for co in range(4):
            if grille[li][co] != 0 and grille[li][co] == grille[li][co+1] == grille[li][co+2] == grille[li][co+3]:
                winner = grille[li][co]
                return True
    return False

def alignement_vertical(grille:list):
    global winner
    for li in range(3):
        for co in range(7):
            if grille[li][co] != 0 and grille[li][co] == grille[li+1][co] == grille[li+2][co] == grille[li+3][co]:
                winner = grille[li][co]
                return True
    return False

def alignement_oblique_montant(grille:list):
    global winner
    for li in range(3, 6):
        for co in range(0, 4):
            if grille[li][co] != 0 and grille[li][co] == grille[li-1][co+1] == grille[li-2][co+2] == grille[li-3][co+3]:
                winner = grille[li][co]
                return True
    return False

def alignement_oblique_descendant(grille:list):
    global winner
    for li in range(0, 3):
        for co in range(0, 4):
            if grille[li][co] != 0 and grille[li][co] == grille[li+1][co+1] == grille[li+2][co+2] == grille[li+3][co+3]:
                winner = grille[li][co]
                return True
    return False

def match_nul(grille:list):
    for c in range(7):
        if grille[0][c] == 0:
            winner = 0
            return False
    return True

def win(grille):
    """
    Fonction qui prend en paramètre la matrice représentant le plateau de jeu et qui fait une synthèse des
    des fonctions précedentes, renvoie True si le jeu prend fin.
    """
    return match_nul(grille) or alignement_oblique_descendant(grille) or alignement_oblique_montant(grille) or alignement_vertical(grille) or alignement_horizontal(grille)






#Fonctions principals
def menu():
    """
    Fonction qui affiche graphiquement les differentes possibilités du joueur:
    -lancer le jeu (3 niveaux + 1 bogo level)
    -quitter le jeu
    """
    #set-up
    background = pygame.image.load('ressources/ecran accueil.png')
    screen.blit( background, (0, 0) )

    #boutons jouer
    screen.blit( niveau1, (25, 120) )
    screen.blit( niveau2, (250, 120) )
    screen.blit( niveau3, (475, 120) )
    screen.blit( monkey, (0, 0))

    #bouton quitter
    bouton_quitter = pygame.image.load('ressources/bouton sortie.png')
    screen.blit( bouton_quitter, (95, 348) )

    #acutalisation
    pygame.display.flip()
    niveau = -1

    while True:
        keys=pygame.key.get_pressed()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                #bouton jouer cliqué
                if (25 <= x <= 25 + 200) and (120 <= y <= 120 + 200):
                    jouer(2)
                    break
                elif (250 <= x <= 250 + 200) and (120 <= y <= 120 + 200):
                    jouer(3)
                    break
                elif (475 <= x <= 475 + 200) and (120 <= y <= 120 + 200):
                    jouer(4)
                    break
                elif (0 <= x <= 100) and (0 <= y <= 100):
                    jouer(0)
                    break
                #bouton quitter cliqué
                elif (95 <= x <= 95 + 513) and (348 <= y <= 348 + 157):
                    pygame.quit()
                    sys.exit()
                    break


def jouer(niveau):
    """
    Fonction principal qui boucle tant que la partie n'est pas finit puis affiche le gagnant.
    """
    #good luck
    print("   __ _  ___   ___   __| | | |_   _  ___| | __")
    print("  / _` |/ _ \ / _ \ / _` | | | | | |/ __| |/ /")
    print(" | (_| | (_) | (_) | (_| | | | |_| | (__|   <")
    print("  \__, |\___/ \___/ \__,_| |_|\__,_|\___|_|\_\|")
    print("  |___/")

    #charge la nouvel page
    background = pygame.image.load('ressources/grille.png')
    screen.blit( background, (0, 0) )
    screen.blit( bouton_pause, (600, 0))
    screen.blit( nom_jeu, (300, 0) )
    afficher_plateau(grille)
    pygame.display.flip()


    tour = 0 #variable qui permet de déterminer quels joueur doit jouer
    #boucle jusqu'a ce qu'il y est un gagnant ou une égalité
    while not win(grille):

        keys=pygame.key.get_pressed()
        events = pygame.event.get()


        if tour%2 + 1 == 1: #coup joueur 2 (rouge)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if (700-100 <= x <= 700 ) and (0 <= y <= 24 ):
                        menu()
                        break
                    tour+=1
                    y = case_libre_la_plus_basse(grille, x//100)
                    afficher(tour%2 + 1, x//100, y)
            """
            if niveau != 0:
                x, y = ordinateur_level.coup_ordinateur(grille, niveau, 2)
                tour+=1
                afficher(tour%2 + 1, y, x)
            else: #si le niveau choisit est 0, alors le monkey se charge de nous renvoyer des coordonnées géneré aléatoirement
                x = monkey_level.monkey_choice(grille)
                y = case_libre_la_plus_basse(grille, x)
                tour+=1
                afficher(tour%2 + 1, x, y)
            """
        #coup joueur 1 (jaune)
        else:
            if niveau != 0:
                x, y = ordinateur_level.coup_ordinateur(grille, niveau, 1)
                tour+=1
                afficher(tour%2 + 1, y, x)
            else: #si le niveau choisit est 0, alors le monkey se charge de nous renvoyer des coordonnées géneré aléatoirement
                x = monkey_level.monkey_choice(grille)
                y = case_libre_la_plus_basse(grille, x)
                tour+=1
                afficher(tour%2 + 1, x, y)



    #Vérifie dans quels état est la fin de la partie
    if winner == 1:
        img = pygame.image.load('ressources/JauneGagne.png')
        winner_song.play()
    elif winner == 2:
        img = pygame.image.load('ressources/RougeGagne.png')
        winner_song.play()
    else:#Egalité
        img = pygame.image.load('ressources/MatchNul.png')

    #affiche l'image et ferme le programme
    screen.blit( img, (125, 200) )
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()


menu()





