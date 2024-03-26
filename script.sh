#!/bin/bash

# Créer un répertoire pour les fichiers de sortie s'il n'existe pas
output_dir="output_files"
mkdir -p "$output_dir"

# Boucle pour exécuter le programme 100 fois
for ((i=1; i<=10; i++))
do
    # Nom du fichier de sortie
    output_file="$output_dir/output_$i.txt"
    
    # Exécution du programme avec redirection de la sortie vers le fichier
    ./entree.py > "$output_file"
    
    echo "Exécution $i terminée. Sortie dans $output_file"
done

