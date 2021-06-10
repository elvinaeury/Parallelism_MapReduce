import sys

class Accessoire(list):
    #Toutes les classes héritant de la classe Accessoire seront des objets de type list
    pass

class Pic(Accessoire):
    """ Un pic peut embrocher un post-it (un post-it = 1 commande) par-dessus les post-it déjà présents
    et libérer le dernier embroché. """
    def embrocher(self,commande):
    #L'objet Pic est une liste vide par défaut, on peut donc lui ajouter les commandes (1 commande = 1 post-it)
        self.append(commande)

    def liberer(self, postit):
        #on retire le dernier postit embroché
        return(postit)
        

class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """
    def recevoir(self,plateau):
        #L'objet Bar est une liste vide par défaut, on peut donc lui ajouter les plateaux (contenant les boissons d'un post-it)
        self.append(plateau)

    def evacuer(self,commande):
        #on évacue le dernier plateau posé
        return(commande)

class Barman:

    def __init__(self,pic,bar):
        #Le Barman et le Serveur partagent le même pic et le même bar
        self.pic = pic
        self.bar = bar
        print('[Barman] Prêt pour le service !')

    def preparer(self):
        """ Prend le dernier post-it embroché, prépare la commande et la dépose sur le bar. """
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
        self.commandes = commandes #obtenues en ligne de commande
        print('[Serveur] Prêt pour le service')

    
    def prendre_commande(self):
        """ Prend une commande et embroche un post-it. """
        #self.commandes est une liste de string, un string représentant une commande
        for commande in self.commandes:
            print(f'[Serveur] Je prends commande de {commande}') 
            self.pic.embrocher(commande)
        print("[Serveur] Il n'y a plus de commandes à prendre")
       


    def servir(self):
        """ Prend le dernier plateau déposé sur le bar et le sert. """
        plateaux = [self.bar[k] for k in range(len(self.bar)-1,-1,-1)]
        #plateaux est une liste contenant toutes les commandes préparées par le Barman
        for plateau in plateaux:
            self.bar.evacuer(plateau)
            print(f'[Serveur] Je sers {plateau}')

  
#Programme principal

def main():
    try:
        serveur.prendre_commande()
    except Cocktail_Error as e:
        log(1,e)
    try:
        barman.preparer()
    except Cocktail_Error as e:
        log(1,e)
    try:
        serveur.servir()
    except Cocktail_Error as e:
        log(1,e)


if __name__ == '__main__':

    pic = Pic()
    bar = Bar()
    commandes = sys.argv[1:]
    barman = Barman(pic,bar)
    serveur = Serveur(pic,bar,commandes)
    main()
