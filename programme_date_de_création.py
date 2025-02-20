from pathlib import Path
from datetime import datetime
from typing import List, Union, Dict
import logging

class PhotoScanner:
    def __init__(self, chemins: Union[str, List[str]]):
        """
        Initialise le scanner de photos avec un ou plusieurs chemins.
        
        Args:
            chemins: Peut être une chaîne de caractères (un seul chemin) 
                    ou une liste de chaînes (plusieurs chemins)
        """
        self.chemins = [chemins] if isinstance(chemins, str) else chemins
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Configure le logger pour le suivi des opérations."""
        logger = logging.getLogger("PhotoScanner")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def scanner_dossiers(self) -> Dict[str, List[Path]]:
        """
        Scanne tous les dossiers spécifiés et retourne les fichiers trouvés.
        
        Returns:
            Un dictionnaire avec les chemins comme clés et les listes de fichiers comme valeurs
        """
        resultats = {}
        
        for chemin in self.chemins:
            dossier = Path(chemin)
            if not dossier.exists():
                self.logger.warning(f"Le dossier '{chemin}' n'existe pas")
                continue
                
            if not dossier.is_dir():
                self.logger.warning(f"'{chemin}' n'est pas un dossier")
                continue
                
            try:
                fichiers = [f for f in dossier.iterdir() if f.is_file()]
                fichiers_tries = sorted(fichiers, key=lambda f: (f.stat().st_mtime, f.name))
                resultats[str(dossier)] = fichiers_tries
                self.logger.info(f"Trouvé {len(fichiers_tries)} fichiers dans '{chemin}'")
            except PermissionError:
                self.logger.error(f"Erreur de permission pour accéder à '{chemin}'")
            except Exception as e:
                self.logger.error(f"Erreur lors du scan de '{chemin}': {str(e)}")
                
        return resultats

    def afficher_resultats(self, resultats: Dict[str, List[Path]]) -> None:
        """
        Affiche les résultats du scan de manière formatée.
        
        Args:
            resultats: Dictionnaire contenant les résultats du scan
        """
        for dossier, fichiers in resultats.items():
            print(f"\nDossier: {dossier}")
            print("-" * 50)
            
            if not fichiers:
                print("Aucun fichier trouvé")
                continue
                
            for fichier in fichiers:
                date_modif = datetime.fromtimestamp(fichier.stat().st_mtime)
                taille = fichier.stat().st_size / 1024  # Taille en Ko
                print(f"{fichier.name:<30} - "
                      f"Date: {date_modif.strftime('%Y-%m-%d %H:%M:%S')} - "
                      f"Taille: {taille:.2f} Ko")

def main():
    # Exemple d'utilisation avec plusieurs chemins
    chemins = [
        "chemin/vers/dossier1",
        "chemin/vers/dossier2",
        "chemin/vers/dossier3"
    ]
    
    scanner = PhotoScanner(chemins)
    resultats = scanner.scanner_dossiers()
    scanner.afficher_resultats(resultats)

if __name__ == "__main__":
    main()