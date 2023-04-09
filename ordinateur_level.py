import evaluation


def case_la_plus_basse(plateau:list, i:int)->int:
    """
    Fonction qui prend en paramètres un plateau de de puissance 4 et le numéro d'une colonne
    et renvoie la case vide la plus basse de la colonne.
    """
    fin = 5
    while plateau[fin][i] != 0 and fin >= 0:
        fin-=1
    return fin

def minimax(plateau:list, profondeur:int, joueur:bool, coup:int)->int:
    """
    Fonction récursive qui prend en paramètres un plateau et une profondeur et qui retourne
    le meilleur coup possible en simulant le meilleur coup jouer pour l'ordinateur et le meilleur 
    coup que pourrait jouer le joueur à chaque passage dans la fonction.
    """
    if profondeur == 0:
        return evaluation.evaluation(plateau, coup)
    iswin = evaluation.alignements(plateau, 4, coup)
    if iswin == 10000:
        return 10000-profondeur
    elif iswin == -10000:
        return -10000-profondeur
    else:
        if joueur: #coup d'ordinateur
            meilleur_score = -10000
            for co in range(7):
                x, y = case_la_plus_basse(plateau, co), co
                if plateau[x][y] == 0:
                    plateau[x][y] = coup
                    score = minimax(plateau, profondeur-1, False, coup)
                    plateau[x][y] = 0
                    if score > meilleur_score:
                        meilleur_score = score
            return meilleur_score
        else: #coup du joueur
            meilleur_score = 10000
            for co in range(7):
                x, y = case_la_plus_basse(plateau, co), co
                print(x, y)
                if plateau[x][y] == 0:
                    plateau[x][y] = coup%2 + 1
                    score = minimax(plateau, profondeur-1, True, coup)
                    plateau[x][y] = 0
                    if score < meilleur_score:
                        meilleur_score = score
            return meilleur_score

def coup_ordinateur(plateau:list, profondeur:int, coup:int)->tuple:
    """
    Fonction qui prend en paramètres un plateau de puissance 4 
    et le nombre de coup à l'avance à calculer.
    La fonction renvoie le coup optimal à jouer.
    """
    meilleur_score = -10000
    y = plateau[0].index(0)
    x = case_la_plus_basse(plateau, y)
    meilleur_coup = (x, y)

    for co in range(7):
        x, y = case_la_plus_basse(plateau, co), co
        if plateau[x][y] == 0:
            plateau[x][y] = coup
            score = minimax(plateau, profondeur, False, coup)
            plateau[x][y] = 0
            if score >= meilleur_score:
                meilleur_score = score
                meilleur_coup = (x, y)
    return meilleur_coup