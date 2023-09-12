

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



