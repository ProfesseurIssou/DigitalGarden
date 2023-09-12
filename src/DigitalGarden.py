import pygame, random, math

pygame.init()
clock = pygame.time.Clock()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
BLUE = 0, 0, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

WINDOW_SIZE = (1024, 1024)
FPS = 20

class Gene:
    """
        Gene permettant de définir les règles de génération d'une cellule
    """
    # Longueur d'un segment
    length: int                                 # Nombre de cellule avant la prochaine mutation
    lengthDeviation: int                        # Nombre de cellule avant la prochaine mutation (aleatoire, entre -lengthDeviation et lengthDeviation puis on additionne a length)

    # Taille des cellules du segment
    radius: float                               # Rayon de la cellule
    radiusDeviation: float                      # Changement de rayon par rapport au segment parent (Aleatoire, entre -radiusDeviation et radiusDeviation puis on additionne a radius)
    radiusChange: float                         # Changement de rayon de la cellule
    radiusChangeDeviation: float                # Changement de changement de rayon de la cellule (Aleatoire, entre -radiusChangeDeviation et radiusChangeDeviation puis on additionne a radiusChange)

    # Couleur des cellules au fur et a mesure du segment
    color: tuple[int, int, int]                 # Couleur de la cellule
    colorDeviation: float                       # Changement de couleur par rapport au segment precedent (Aleatoire, entre -colorDeviation et colorDeviation puis on additionne a color)
    colorChange: tuple[int, int, int]           # Changement de couleur de la cellule
    colorChangeDeviation: float                 # Changement de changement de couleur de la cellule (Aleatoire, entre -colorChangeDeviation et colorChangeDeviation puis on additionne a colorChange)

    # Passage d'un segment a un autre
    nbBranche: int                              # Nombre de branche de la cellule (si elle ce duplique)
    nbBrancheDeviation: int                     # Nombre de branche de la cellule (si elle ce duplique) (aleatoire, entre -nbBrancheDeviation et nbBrancheDeviation puis on additionne a nbBranche)
    angleBranche: float                         # Angle entre les branches de la cellule (si 180, alors elles partent de 90 degres l'une de l'autre)
    angleDeviation: float                       # Angle entre les branches de la cellule (si 180, alors elles partent de 90 degres l'une de l'autre) (aleatoire, entre 0 et angleDeviation puis on additionne a angleBranche)

    # Rotation de chaque cellules du segment
    turn: float                                 # Angle de rotation de la cellule (si 0, alors elle ne tourne pas)
    turnRandom: float                           # Angle de rotation aleatoire de la cellule (si 0, alors elle ne tourne pas, si 1, alors elle tourne de 0 a 360 degres)
    downUp: float                               # Valeur negatif ou positive, plus le LENGTH est grand, plus la cellule descend/monte au fur et a mesure du segment

    def __init__(self, ancestorGene: 'Gene' = None) -> None:
        """
            Initialise un gene (en passant d'un segment a un autre)
            Si ancestorGene est None, alors un gene aleatoire est crée
            Sinon, le gene est un gene enfant du gene ancestorGene
        """
        if ancestorGene is None:
            self.length = 10
            self.lengthDeviation = 3

            self.radius = 10
            self.radiusDeviation = -1
            self.radiusChange = 0
            self.radiusChangeDeviation = -1

            self.color = RED
            self.colorDeviation = 10
            self.colorChange = (0, 0, 0)
            self.colorChangeDeviation = 10

            self.nbBranche = 2
            self.nbBrancheDeviation = 1
            
            self.angleBranche = 90
            self.angleDeviation = 5

            self.turn = 0
            self.turnRandom = 0.5
            self.downUp = 0.5
        else:
            self.length = ancestorGene.length + random.randint(-ancestorGene.lengthDeviation, ancestorGene.lengthDeviation)
            self.lengthDeviation = int(ancestorGene.lengthDeviation * (random.random() * 4))    # Valeur entre 0 et 2 qu'on multiplie par 2 pour avoir un nombre entre 0 et 2, puis on multiplie par lengthDeviation pour avoir un nombre entre -lengthDeviation et lengthDeviation

            self.radius = ancestorGene.radius + (((random.random() * 2)-1) * ancestorGene.radiusDeviation)  # Valeur entre -1 et 1 qu'on multiplie par radiusDeviation pour avoir un nombre entre -radiusDeviation et radiusDeviation, puis on additionne a radius 
            self.radiusDeviation = ancestorGene.radiusDeviation * (((random.random() * 2)-1)*2)    # Valeur entre -1 et 1 qu'on multiplie par 2 pour avoir un nombre entre -2 et 2, puis on multiplie par radiusDeviation pour avoir un nombre entre -radiusDeviantion et radiusDeviantion
            self.radiusChange = ancestorGene.radiusChange + (((random.random() * 2)-1) * ancestorGene.radiusChangeDeviation)  # Valeur entre -1 et 1 qu'on multiplie par radiusChangeDeviation pour avoir un nombre entre -radiusChangeDeviation et radiusChangeDeviation, puis on additionne a radiusChange
            self.radiusChangeDeviation = ancestorGene.radiusChangeDeviation * (((random.random() * 2)-1)*2)    # Valeur entre -1 et 1 qu'on multiplie par 2 pour avoir un nombre entre -2 et 2, puis on multiplie par radiusChangeDeviation pour avoir un nombre entre -radiusChangeDeviantion et radiusChangeDeviantion

            colorR = int(ancestorGene.color[0] + ancestorGene.colorChange[0] * ancestorGene.colorDeviation)
            if colorR > 255: colorR = 255
            elif colorR < 0: colorR = 0
            colorG = int(ancestorGene.color[1] + ancestorGene.colorChange[1] * ancestorGene.colorDeviation)
            if colorG > 255: colorG = 255
            elif colorG < 0: colorG = 0
            colorB = int(ancestorGene.color[2] + ancestorGene.colorChange[2] * ancestorGene.colorDeviation)
            if colorB > 255: colorB = 255
            elif colorB < 0: colorB = 0
            self.color = (
                colorR,
                colorG,
                colorB
            )  # Valeur entre -1 et 1 qu'on multiplie par colorChange pour avoir un nombre entre -colorChange et colorChange, puis on additionne a color
            self.colorDeviation = ancestorGene.colorDeviation * (((random.random() * 2)-1)*2)    # Valeur entre -1 et 1 qu'on multiplie par 2 pour avoir un nombre entre -2 et 2, puis on multiplie par colorDeviation pour avoir un nombre entre -colorDeviantion et colorDeviantion
            self.colorChange = (
                ancestorGene.colorChange[0] + (((random.random() * 2)-1) * ancestorGene.colorChangeDeviation),
                ancestorGene.colorChange[1] + (((random.random() * 2)-1) * ancestorGene.colorChangeDeviation), 
                ancestorGene.colorChange[2] + (((random.random() * 2)-1) * ancestorGene.colorChangeDeviation)
            ) # Valeur entre -1 et 1 qu'on multiplie par colorChangeDeviation pour avoir un nombre entre -colorChangeDeviation et colorChangeDeviation, puis on additionne a colorChange
            self.colorChangeDeviation = ancestorGene.colorChangeDeviation * (((random.random() * 2)-1)*2)    # Valeur entre -1 et 1 qu'on multiplie par 2 pour avoir un nombre entre -2 et 2, puis on multiplie par colorChangeDeviation pour avoir un nombre entre -colorChangeDeviantion et colorChangeDeviantion

            self.nbBranche = ancestorGene.nbBranche + random.randint(-ancestorGene.nbBrancheDeviation, ancestorGene.nbBrancheDeviation)
            self.nbBrancheDeviation = int(ancestorGene.nbBrancheDeviation * (((random.random() * 2)-1)*2))    # Valeur entre -1 et 1 qu'on multiplie par 2 pour avoir un nombre entre -2 et 2, puis on multiplie par nbBrancheDeviation pour avoir un nombre entre -nbBrancheDeviation et nbBrancheDeviation
            if self.nbBranche < 1:
                self.nbBranche = 1
            
            self.angleBranche = ancestorGene.angleBranche + (((random.random() * 2)-1) * ancestorGene.angleDeviation)  # Valeur entre -1 et 1 qu'on multiplie par angleDeviation pour avoir un nombre entre -angleDeviation et angleDeviation, puis on additionne a angleBranche
            self.angleDeviation = ancestorGene.angleDeviation * (((random.random() * 2)-1)*2)    # Valeur entre -1 et 1 qu'on multiplie par 2 pour avoir un nombre entre -2 et 2, puis on multiplie par angleDeviation pour avoir un nombre entre -angleDeviantion et angleDeviantion

            self.turn = ancestorGene.turn + (((random.random() * 2)-1) * ancestorGene.turnRandom)  # Valeur entre -1 et 1 qu'on multiplie par turnRandom pour avoir un nombre entre -turnRandom et turnRandom, puis on additionne a turn
            self.turnRandom = ancestorGene.turnRandom * (((random.random() * 2)-1)*2)    # Valeur entre -1 et 1 qu'on multiplie par 2 pour avoir un nombre entre -2 et 2, puis on multiplie par turnRandom pour avoir un nombre entre -turnRandom et turnRandom
            self.downUp = ancestorGene.downUp + ((((random.random() * 2)-1)*2) * ancestorGene.downUp)  # Valeur entre -2 et 2 qu'on multiplie par downUp pour avoir un nombre entre -downUp et downUp, puis on additionne a downUp
        return


class Cell:
    """
        Permet a une cellule de ce dupliquer selon des regles dans les gène
    """
    pos: tuple[int, int]    # X, Y
    angle: float            # Angle de la cellule
    posInBranch: int        # Position de la cellule dans la branche (segment) (0=premiere cellule, 1=deuxieme cellule, etc...), Passage a un autre segment quand LENGTH est atteint
    gene: Gene              # Gene de la cellule
    def __init__(self, pos: tuple[int, int], angle: float, posInBranch: int ,gene: Gene) -> None:
        self.pos = pos
        self.angle = angle
        self.posInBranch = posInBranch
        self.gene = gene
        return
    
    def Generate(self) -> list['Cell']:
        """
            Genere une cellule a partir de la cellule actuelle
        """
        newCells: list['Cell'] = []

        if self.posInBranch == self.gene.length:                            # Si la cellule est a la fin de son segment
            self.gene = Gene(self.gene)                                         # On crée un nouveau gene

            angleBetweenBranch: float = self.gene.angleBranche / self.gene.nbBranche
            startAngle: float = self.angle - (self.gene.angleBranche / 2)

            for i in range(self.gene.nbBranche):                                 # On crée les cellules filles
                newCells.append(Cell(
                    (
                        self.pos[0],
                        self.pos[1]
                    ),
                    startAngle + (angleBetweenBranch * i),                              # Nouvel angle
                    0,                                                                  # Nouvelle branche
                    self.gene                                                           # Nouveau gene
                ))
        else:
            colorR = int(self.gene.color[0] + self.gene.colorChange[0])
            if colorR > 255: colorR = 255
            elif colorR < 0: colorR = 0
            colorG = int(self.gene.color[1] + self.gene.colorChange[1])
            if colorG > 255: colorG = 255
            elif colorG < 0: colorG = 0
            colorB = int(self.gene.color[2] + self.gene.colorChange[2])
            if colorB > 255: colorB = 255
            elif colorB < 0: colorB = 0
            self.gene.color = (
                colorR,
                colorG,
                colorB
            )  # Valeur entre -1 et 1 qu'on multiplie par colorChange pour avoir un nombre entre -colorChange et colorChange, puis on additionne a color
            self.gene.radius += self.gene.radiusChange
            newCells.append(Cell(
                (
                    self.pos[0] + (self.gene.radius * math.cos(self.angle)), 
                    self.pos[1] + (self.gene.radius * math.sin(self.angle))
                ),
                self.angle + self.gene.turn + (random.random() * self.gene.turnRandom), 
                self.posInBranch + 1, 
                self.gene
            ))                

        return newCells

class Tree:
    """
        Agent faisant evoluer des cellules
    """
    oldCells: list[Cell]                    # Liste des ancienes cellules (qui ne genere pas de cellule)
    cells: list[Cell]                       # Liste des cellules qui vont généré des cellules (ensuite elle seront ajouté a la liste des ancienes cellules)


    def __init__(self, initPos: tuple[int, int]) -> None:
        self.cells = [Cell(initPos, -90, 0, Gene())]
        self.oldCells = []
        return
    
    def Generate(self) -> list[Cell]:
        """
            Genère la prochaine génération de cellule et retourne la liste des cellules existantes
        """
        newCells: list[Cell] = []
        
        for cell in self.cells:
            newCells += cell.Generate()
        
        self.oldCells += self.cells
        self.cells = newCells
        return self.oldCells + self.cells







def main():
    screen = pygame.display.set_mode(WINDOW_SIZE)
    loop = True

    size = 20
    color = RED

    tree: Tree = Tree((512, 1000))

    while loop:
        ### Event ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        #############


        ### LOGIC ###
        #############


        ### RENDER ###
        for cell in tree.Generate():
            pygame.draw.circle(screen, cell.gene.color, cell.pos, cell.gene.radius)


        pygame.display.update()
        screen.fill(BLACK)
        clock.tick(FPS)
        ##############

if __name__ == '__main__':
    main()
