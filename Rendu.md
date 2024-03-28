# Rendu du Projet d'Algo 2024, Capiomont Théo, Edery Sacha



## Déroulé du projet

- Réflexion sur les algorithmes de résolution

- Analyse des fichiers fournis

- Génération de tests

- Implémentation de l'algorithme Point In Polygon

- Implémentation de l'algorithme Polygon Inclusion



## Algorithmes envisagés pour le problème de point dans un polygone

Entrée : ensemble des points d'un polygone et un point à traiter

Sortie : vrai ou faux si le point est à l'intérieur ou à l'extérieur du polygone

### Algorithme classique

- Pour un polygone donné, on vérifie si un point appartient au polygone grâce à la méthode de tracé d'une demi-droite partant du point. Si le nombre d'intersections avec le polygone est impair, le point est à l'intérieur, sinon à l'extérieur. On fait attention aux cas particuliers (demi-droite qui croise un sommet, demi-droite qui contient un segment du polygone, etc)


### Algorithme de triangulation

- On triangule le polynome

- Pour un triangle donné, on vérifie si un point appartient au triangle selon une des méthodes suivantes : intersection demi-droite / polygone, calcul d'aires, calcul d'orientation


### Algorithme de grille

- On grille le plan

- On distingue les cases vides et les cases de la grille qui contiennent au moins un segment de polygones

- ...


## Algorithmes envisagés pour le problèmes d'inclusion des polygones

Entrée : coordonnées des points de tous les polygones dans l'ordre de numérotation

Outils : Algorithme Point in Polygon

Sortie : liste des inclusions de polygones

### Algorithme naïf

- On vérifie pour un polygone "fils" si tous ses sommets appartiennent à un même polygone "père". Si c'est le cas, alors le polygone "fils" est inclus dans le polygone "père". On itère cette vérification pour l'ensemble des couples fils-père possibles.



## Conditions d'entrée pour les algorithmes



## Générateurs d'entrées envisagés



## Partie expérimentale



### Mesure de performances et traçage de courbes

### Comparaison expérimentale des différents algorithmes


