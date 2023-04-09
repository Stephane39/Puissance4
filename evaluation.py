"""
Barème d'évaluation des points:
    -plus un pion se situe vers le milieu selon l'abscisse, plus le score augmente
    -plus un pion se situe vers le milieu selon l'ordonnée, plus le score augmente
    -si sur 4 cases alignées il y a 2 pions et 2 cases vides, alors le score augmente de 50
    -si sur 4 cases alignées il y a 3 pions et 1 cases vides, alors le score augmente de 100
    -si sur 4 case alignées il y a 4 pions alors on renvoit 10 000 directement
"""


def controle_centre(plateau:list, coup:int):
    """
    Fonction qui prend en paramètre un plateau de jeu de puissance 4 et évalue la position en fonction du controle du centre
    """
    score = 0
    for ligne in range(6):

        if plateau[ligne][2] == coup:
            score=+5
        elif plateau[ligne][2] == coup%2 + 1:
            score=-5

        if plateau[ligne][3] == coup:
            score=+10
        elif plateau[ligne][3] == coup%2 + 1:
            score=-10

        if plateau[ligne][4] == coup:
            score=+5
        elif plateau[ligne][4] == coup%2 + 1:
            score=-5
    return score

def controle_hauteur(plateau:list, coup:int):
    """
    Fonction qui prend en paramètre un plateau de jeu de puissance 4 et évalue la position en fonction du controle de la hauteur
    """
    score = 0
    for ligne in range(6):
        for case in range(7):
            if plateau[ligne][case] == coup:
                if ligne == 2 or ligne == 3:
                    score+=6
                elif ligne == 1 or ligne == 4:
                    score+=4
                else:
                    score+=2
            if plateau[ligne][case] == coup%2 + 1:
                if ligne == 2 or ligne == 3:
                    score-=6
                elif ligne == 1 or ligne == 4:
                    score-=4
                else:
                    score-=2
    return score


def alignements(plateau:list, nbPions:int, coup:int):
    """
    Fonction qui prend en paramètre un plateau de jeu de puissance 4 et évalue la position en fonction des possibles alignements
    """
    score = 0
    #horizontal
    for ligne in range(6):
        for case in range(4):
            seq = plateau[ligne][case:case+nbPions]
            if seq.count(coup) == nbPions:
                if nbPions == 4:
                    return 10000
                if nbPions == 3 and seq.count(0) == 1:
                    score+=100
                if nbPions == 2 and seq.count(0) == 2:
                    score+=50

            elif seq.count(coup%2 + 1) == nbPions:
                if nbPions == 4 :
                    return -10000
                elif nbPions == 3 and seq.count(0) == 1:
                    score-=100
                elif nbPions == 2 and seq.count(0) == 2:
                    score-=50
    #vertical
    for colonne in range(7):
        for case in range(3):
            seq = [plateau[i][colonne] for i in range(case, case+4)]
            if seq.count(coup) == nbPions:
                if nbPions == 4:
                    return 10000
                if nbPions == 3 and seq.count(0) == 1:
                    score+=100
                if nbPions == 2 and seq.count(0) == 2:
                    score+=50

            elif seq.count(coup%2 + 1) == nbPions:
                if nbPions == 4:
                    return -10000
                elif nbPions == 3 and seq.count(0) == 1:
                    score-=100
                elif nbPions == 2 and seq.count(0) == 2:
                    score-=50
    #oblique montant
    for i in range(4):
        for j in range(3, 6):
            seq = [plateau[j-k][i+k] for k in range(4)]
            if seq.count(coup) == nbPions:
                if nbPions == 4:
                    return 10000
                if nbPions == 3 and seq.count(0) == 1:
                    score+=100
                if nbPions == 2 and seq.count(0) == 2:
                    score+=50

            elif seq.count(coup%2 + 1) == nbPions:
                if nbPions == 4:
                    return -10000
                elif nbPions == 3 and seq.count(0) == 1:
                    score-=100
                elif nbPions == 2 and seq.count(0) == 2:
                    score-=50
    #oblique descendant
    for i in range(4):
        for j in range(3):
            seq = [plateau[j+k][i+k] for k in range(4)]
            if seq.count(coup) == nbPions:
                if nbPions == 4:
                    return 10000
                if nbPions == 3 and seq.count(0) == 1:
                    score+=100
                if nbPions == 2 and seq.count(0) == 2:
                    score+=50

            elif seq.count(coup%2 + 1) == nbPions:
                if nbPions == 4:
                    return -10000
                elif nbPions == 3 and seq.count(0) == 1:
                    score-=100
                elif nbPions == 2 and seq.count(0) == 2:
                    score-=50
    return score

def evaluation(plateau:list, coup:int):
    """
    Fonction faisant la synthèse des fonctions précedentes afin de renvoyer un score global de la position actuelle
    """
    score = 0
    score += controle_centre(plateau, coup)
    score += controle_hauteur(plateau, coup)
    for nbPions in range(2, 5):
        score += alignements(plateau, nbPions, coup)
    return score



