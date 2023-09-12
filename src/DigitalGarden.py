

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

