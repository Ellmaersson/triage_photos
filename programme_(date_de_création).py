from pathlib import Path

# Chemin vers le dossier contenant les photos
dossier_photos = Path(r"E:\sauvegarde photos")

# Vérifie si le chemin existe et est un répertoire
if dossier_photos.exists() and dossier_photos.is_dir():
    # Liste des fichiers dans le dossier (seulement les fichiers)
    fichiers_photos = [f for f in dossier_photos.iterdir() if f.is_file()]

    # Tri des fichiers par date de création et par nom
    fichiers_photos_trie = sorted(fichiers_photos, key=lambda f: (f.stat(), f.name))

    # Affiche les fichiers triés
    for fichier in fichiers_photos_trie:
        print(f"{fichier.name} - Date de création: {fichier.stat()}")
else:
    print(f"Le dossier '{dossier_photos}' n'existe pas ou n'est pas un répertoire.")