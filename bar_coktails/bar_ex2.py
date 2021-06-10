import sys
import asyncio

class Accessoire(list):
    pass

class Pic(Accessoire):
    """ Un pic peut embrocher un post-it par-dessus les post-it déjà présents
        et libérer le dernier embroché. """

    async def embrocher(self,commande):
        print(f'[Pic] postit {commande} embroché')
        self.append(commande)

    async def liberer(self, postit):
        print(f'[Pic] postit {postit} libéré')

class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """
    async def recevoir(self,plateau):
        print(f'[Bar] {plateau} reçu')
        self.append(plateau)

    async def evacuer(self,commande):
        print(f'[Bar] {commande} évacuée')


class Serveur:

    def __init__(self,pic,bar,commandes):
        self.pic = pic
        self.bar = bar
        self.commandes = commandes
        print('[Serveur] Prêt pour le service')

    
    async def prendre_commande(self):
        """ Prend une commande et embroche un post-it. """
        for commande in self.commandes:
            print(f'[Serveur] Je prends commande de {commande}')
            await self.pic.embrocher(commande) # on enchaîne les coroutines - pic embroché
            await asyncio.sleep(0) # le temps min pour que le serveur ait au moins 1 commande - donc liste du pic pas vide.
        print("[Serveur] Il n'y a plus de commandes à prendre")
       

    # Cette coroutine s'active à la fin, lorsqu'au moins une commande est prête 
    # Sleep au début: si on entre dans la coroutine, elle ne s'active pas jusqu'au moment où toutes les commandes sont fabriquées.
    async def servir(self):
        """ Prend un plateau sur le bar. """
        await asyncio.sleep(0.2) 
        plateaux = self.bar     
        for plateau in plateaux:
            await self.bar.evacuer(plateau) #enchaîne coroutine
            print(f'[Serveur] Je sers {plateau}')


class Barman:

    def __init__(self,pic,bar):
        self.pic = pic
        self.bar = bar
        print('[Barman] prêt pour le service !')


    async def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """
        commandes = self.pic  
        # On chaîne les coroutines pic.libérer, bar.recevoir            
        for commande in commandes:
            await self.pic.liberer(commande) # on enchaîne coroutine pic.liberer - pic libérer
            print(f'[Barman] Je commence la fabrication de {commande}')
            await asyncio.sleep(0) # pendant que le barman fabrique on laisse un temps >0.8s pour laisser le temps au serveur de prendre une nouvelle commande + pic embroché et pic parle
            print(f'[Barman] Je termine la fabrication de {commande}')
            await self.bar.recevoir(commande) # bar recoit les commandes par table (append liste) : le bar parle

  
#Programme principal
# On peut jongler parmi les 3 coroutines
async def main_prog():
    await asyncio.gather(
    serveur.prendre_commande(),
    barman.preparer(),
    serveur.servir()
    )
        


if __name__ == '__main__':

    pic = Pic()
    bar = Bar()
    commandes = sys.argv[1:] #les commandes doivent être écrites en ligne de commande (strings)
    serveur = Serveur(pic,bar,commandes)
    barman = Barman(pic,bar)
    asyncio.run(main_prog())