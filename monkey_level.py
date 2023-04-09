import random

def monkey_choice(plateau:list)->int:
    """
    Prend en paramètre un plateau de puissance 4
    et renvoie une colonne aléatoire dans laquelle 
    mettre un pion.
    """
    choixMonkey = random.randint(0, 6)
    while plateau[0][choixMonkey] != 0:
        choixMonkey = random.randint(0, 6)
    return choixMonkey

test = [ [1, 0, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1, 1] ]
assert monkey_choice(test) == 1

    
