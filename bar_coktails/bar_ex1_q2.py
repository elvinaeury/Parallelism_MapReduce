import sys

class Accessoire(list):
    pass

class Pic(Accessoire):
    """ Un pic peut embrocher un post-it par-dessus les post-it déjà présents
        et libérer le dernier embroché. """
    def embrocher(self,commande):
        print(f'[Pic] postit {commande} embroché')
        self.append(commande)

    def liberer(self, postit):
        print(f'[Pic] postit {postit} libéré')
        

class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """
    def recevoir(self,plateau):
        print(f'[Bar] {plateau} reçu')
        self.append(plateau)

    def evacuer(self,commande):
        print(f'[Bar] {commande} évacuée')

class Barman:

    def __init__(self,pic,bar):
        self.pic = pic
        self.bar = bar
        print('[Barman] Prêt pour le service !')

    def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """
        commandes = [self.pic[k] for k in range(len(self.pic)-1,-1,-1)]
        for commande in commandes :
            self.pic.liberer(commande)
            print(f'[Barman] Je commence la fabrication de {commande}')
            print(f'[Barman] Je termine la fabrication de {commande}')
            self.bar.recevoir(commande)
            
        

class Serveur:

    def __init__(self,pic,bar,commandes):
        self.pic = pic
        self.bar = bar
        self.commandes = commandes
        print('[Serveur] Prêt pour le service')

    
    def prendre_commande(self):
        """ Prend une commande et embroche un post-it. """
        for commande in self.commandes:
            print(f'[Serveur] Je prends commande de {commande}') 
            self.pic.embrocher(commande)
        print("[Serveur] Il n'y a plus de commandes à prendre")
       


    def servir(self):
        """ Prend un plateau sur le bar. """
        plateaux = [self.bar[k] for k in range(len(self.bar)-1,-1,-1)]
        for plateau in plateaux:
            self.bar.evacuer(plateau)
            print(f'[Serveur] Je sers {plateau}')

  
#Programme principal

def main():
    try:
        serveur.prendre_commande()
    except Cocktail_Error as e:
        log(1,e)
    print('Plus de commande à prendre')
    try:
        barman.preparer()
    except Cocktail_Error as e:
        log(1,e)
    print('Le pic est vide')
    try:
        serveur.servir()
    except Cocktail_Error as e:
        log(1,e)
    print('Le bar est vide')


if __name__ == '__main__':

    pic = Pic()
    bar = Bar()
    commandes = sys.argv[1:]
    barman = Barman(pic,bar)
    serveur = Serveur(pic,bar,commandes)
    main()
