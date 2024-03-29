# Scripts Utilitaires

## pst2poly
Convertit un (ou plusieurs !) fichier .txt au format psTricks (exportable depuis GeoGebra et facile à parser) en fichier .poly.
Le programme ne prend en compte que les polygones, tout le reste est ignoré.

Utilisation :
```bash
./pst2poly FILE [FILES...]
```

Sortie : fichier(s) .poly, avec le même préfixe et dans le même dossier.

## svg2poly

Programme python pour convertir les polygones au format .svg au format .poly.
Le programme ne prend en compte que les objets labellisés comme polygones dans le fichier .svg

Utilisation :
```bash
./svg2poly SVG_FILE [SVG_FILES...]
```

Sortie : fichier(s) .poly
