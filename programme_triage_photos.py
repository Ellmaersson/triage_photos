import hashlib
import shutil
from pathlib import Path
from typing import List, Dict

def calculate_md5(file_path: Path) -> str:
    """Calcule le hash MD5 d'un fichier."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def detect_and_move_duplicates(source_folders: List[str], destination_folder: str) -> Dict[str, int]:
    """
    Détecte et déplace les doublons depuis plusieurs dossiers source.
    
    Args:
        source_folders: Liste des chemins des dossiers source
        destination_folder: Chemin du dossier de destination pour les doublons
    
    Returns:
        Dict contenant les statistiques des opérations
    """
    # Convertir le dossier de destination en objet Path
    destination = Path(destination_folder)
    destination.mkdir(parents=True, exist_ok=True)

    # Dictionnaire pour stocker les hash et chemins de fichiers
    seen_files: Dict[str, Path] = {}
    
    # Statistiques
    stats = {
        "total_files": 0,
        "duplicates": 0,
        "errors": 0
    }

    # Traiter chaque dossier source
    for source_folder in source_folders:
        folder = Path(source_folder)
        if not folder.exists():
            print(f"Attention: Le dossier {folder} n'existe pas")
            continue

        print(f"Analyse du dossier : {folder}")
        
        # Parcourir le dossier et les sous-dossiers
        for file_path in folder.rglob("*.*"):
            if not file_path.is_file():
                continue

            stats["total_files"] += 1
            
            try:
                # Calculer le hash du fichier
                file_hash = calculate_md5(file_path)
                
                if file_hash in seen_files:
                    # Gérer le doublon
                    stats["duplicates"] += 1
                    original_path = seen_files[file_hash]
                    
                    # Créer un nom unique pour le fichier
                    new_name = f"{file_path.stem}_doublon_{stats['duplicates']}{file_path.suffix}"
                    destination_path = destination / new_name
                    
                    # Déplacer le fichier
                    shutil.move(str(file_path), str(destination_path))
                    print(f"Doublon trouvé :")
                    print(f"  Original : {original_path}")
                    print(f"  Doublon  : {file_path}")
                    print(f"  Déplacé vers : {destination_path}")
                else:
                    # Stocker le hash du fichier
                    seen_files[file_hash] = file_path
                    
            except Exception as e:
                stats["errors"] += 1
                print(f"Erreur lors du traitement de {file_path}: {str(e)}")

    return stats

if __name__ == "__main__":
    # Liste des dossiers à analyser
    dossiers_source = [
        "chemin/vers/dossier1",
        "chemin/vers/dossier2",
        "chermin/vers/dossier3"
    ]
    
    dossier_doublons = "chemin/vers/dossier/Photos doublons"
    
    # Exécuter la détection
    stats = detect_and_move_duplicates(dossiers_source, dossier_doublons)
    
    # Afficher les statistiques
    print("\nRésumé des opérations:")
    print(f"Fichiers analysés : {stats['total_files']}")
    print(f"Doublons trouvés : {stats['duplicates']}")
    print(f"Erreurs rencontrées : {stats['errors']}")