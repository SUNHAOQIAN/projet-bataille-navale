# grille.py
from typing import List, Tuple

class Grille:
    def __init__(self, lignes: int, colonnes: int, vide: str = "."):
        if lignes <= 0 or colonnes <= 0:
            raise ValueError("lignes et colonnes doivent être > 0")
        self.lignes = lignes
        self.colonnes = colonnes
        self.vide = vide
        self.matrice: List[str] = [self.vide for _ in range(lignes * colonnes)]

    def _idx(self, ligne: int, colonne: int) -> int:
        if not (0 <= ligne < self.lignes and 0 <= colonne < self.colonnes):
            raise ValueError("Coordonnées hors de la grille")
        return ligne * self.colonnes + colonne

    def __str__(self) -> str:
        rows = []
        for r in range(self.lignes):
            start = r * self.colonnes
            rows.append("".join(self.matrice[start:start + self.colonnes]))
        return "\n".join(rows)

    def get(self, ligne: int, colonne: int) -> str:
        return self.matrice[self._idx(ligne, colonne)]

    def set(self, ligne: int, colonne: int, val: str) -> None:
        self.matrice[self._idx(ligne, colonne)] = val

    def tirer(self, ligne: int, colonne: int, touche: str = "x") -> str:
        idx = self._idx(ligne, colonne)
        current = self.matrice[idx]
        if current == touche:
            return "already"
        if current == self.vide:
            self.matrice[idx] = touche
            return "miss"
        self.matrice[idx] = touche
        return "hit"

    def ajoute(self, bateau) -> None:
        positions = bateau.positions
        idxs = []
        for (l, c) in positions:
            if not (0 <= l < self.lignes and 0 <= c < self.colonnes):
                raise ValueError("Le bateau ne rentre pas dans la grille")
            idx = self._idx(l, c)
            idxs.append(idx)
            cur = self.matrice[idx]
            if cur != self.vide and cur != "x":
                raise ValueError("Chevauchement de bateaux")
        for idx in idxs:
            self.matrice[idx] = bateau.marker

    def positions_with_marker(self, marker: str):
        res = []
        for i, v in enumerate(self.matrice):
            if v == marker:
                res.append((i // self.colonnes, i % self.colonnes))
        return res
