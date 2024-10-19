import hashlib
import shutil
from pathlib import Path

# Fonction pour calculer le hash MD5 d'un fichier
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Fonction principale pour détecter et déplacer les doublons
def detect_and_move_duplicates(folder_path, destination_folder):
    # Convertir en objets pathlib
    folder = Path(folder_path)
    destination = Path(destination_folder)

    # Créer le dossier de destination s'il n'existe pas
    destination.mkdir(parents=True, exist_ok=True)

    # Dictionnaire pour stocker les hash et chemins de fichiers
    seen_files = {}
    duplicate_count = 0

    # Parcourir le dossier et les sous-dossiers
    for file_path in folder.rglob("*.*"):
        if file_path.is_file():
            # Calculer le hash du fichier
            file_hash = calculate_md5(file_path)

            if file_hash in seen_files:
                # Déplacer les doublons vers le dossier de destination
                duplicate_count += 1
                shutil.move(str(file_path), destination / file_path.name)
                print(f"Doublon trouvé : {file_path}, déplacé vers {destination}")
            else:
                # Stocker le hash du fichier
                seen_files[file_hash] = file_path

    # Afficher le nombre de doublons détectés
    print(f"Nombre de photos en doublon détectées : {duplicate_count}")

# Exemple d'utilisation
if __name__ == "__main__":
    dossier_photos = "E:\\sauvegarde photos"
    dossier_doublons = "E:\\sauvegarde photos\\Photos doublons"
    detect_and_move_duplicates(dossier_photos, dossier_doublons)