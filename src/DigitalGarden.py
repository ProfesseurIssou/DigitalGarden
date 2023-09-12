import pygame

pygame.init()
clock = pygame.time.Clock()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
BLUE = 0, 0, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

WINDOW_SIZE = (1024, 1024)
FPS = 20


class Cell:
    """
        Permet a une cellule de ce dupliquer selon des regles dans les gène
    """
    pos: tuple[int, int]    # X, Y
    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos
        return
    
    def Generate(self) -> list['Cell']:
        """
            Genere une cellule a partir de la cellule actuelle
        """
        return [Cell((self.pos[0], self.pos[1] - 1))]



class Tree:
    """
        Agent faisant evoluer des cellules
    """
    oldCells: list[Cell]                    # Liste des ancienes cellules (qui ne genere pas de cellule)
    cells: list[Cell]                       # Liste des cellules qui vont généré des cellules (ensuite elle seront ajouté a la liste des ancienes cellules)


    def __init__(self, initPos: tuple[int, int]) -> None:
        self.cells = [Cell(initPos)]
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
            pygame.draw.circle(screen, color, cell.pos, size)


        pygame.display.update()
        screen.fill(BLACK)
        clock.tick(FPS)
        ##############

if __name__ == '__main__':
    main()
