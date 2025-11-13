# Projet Bataille Navale – Python

Ce projet implémente une version simplifiée du jeu **Bataille Navale** en Python. Il inclut une grille, des bateaux, une interface console simple et des tests automatisés.

## Structure du projet

```
grille.py          # gestion de la grille
bateau.py          # classes Bateau et sous-classes
main.py            # boucle de jeu principale
test_grille.py     # tests de la grille
test_bateau.py     # tests des bateaux
test_game_flow.py  # test global
```

## Installation

Créer un environnement virtuel (optionnel) :

```bash
python -m venv venv
```

Activer :

* Windows : `./venv/Scripts/Activate.ps1`
* macOS/Linux : `source venv/bin/activate`

Installer la dépendance :

```bash
pip install pytest
```

## Lancer les tests

```bash
pytest -q
```

## Lancer le jeu

```bash
python main.py
```

## Règles du jeu

* Grille : **8 × 10**
* Bateaux placés aléatoirement sans chevauchement :

  * Porte-avion (P, 4)
  * Croiseur (C, 3)
  * Torpilleur (T, 2)
  * Sous-marin (S, 2)

### Symboles

| Symbole   | Signification                      |
| --------- | ---------------------------------- |
| `.`       | case vide                          |
| `x`       | tir effectué                       |
| `P/C/T/S` | bateaux (révélés en fin de partie) |

## Objectif

Tirer jusqu'à couler tous les bateaux. Le programme affiche :

* touché
* coulé
* déjà tiré
* nombre total de tirs à la fin.
