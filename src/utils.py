"""
Fonctions utilitaires pour le modèle Yusuf Counter-Cycle
"""

import json
import numpy as np
from typing import Dict, Any, Optional
from pathlib import Path


def load_parameters(country: str, data_dir: str = "data") -> Dict[str, Any]:
    """
    Charge les paramètres pour un pays donné.
    
    Args:
        country: Nom du pays ('pakistan' ou 'afghanistan')
        data_dir: Répertoire des données
    
    Returns:
        Dictionnaire des paramètres
    """
    file_path = Path(data_dir) / f"{country.lower()}_parameters.json"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier de paramètres introuvable : {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_results(results: Dict[str, Any], filename: str, output_dir: str = "results"):
    """
    Sauvegarde les résultats au format JSON.
    
    Args:
        results: Dictionnaire des résultats
        filename: Nom du fichier
        output_dir: Répertoire de sortie
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(output_dir) / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)


def validate_parameters(params: Dict[str, Any]) -> bool:
    """
    Valide les paramètres du modèle.
    
    Args:
        params: Dictionnaire des paramètres
    
    Returns:
        True si valide, False sinon
    """
    required_keys = [
        'need_minimal',
        'interest_rate',
        'gamma_high',
        'gamma_low',
        'threshold_ratio'
    ]
    
    for key in required_keys:
        if key not in params:
            print(f"Paramètre manquant : {key}")
            return False
        
        value = params[key]
        if not isinstance(value, (int, float)):
            print(f"Paramètre {key} doit être numérique, reçu {type(value)}")
            return False
        
        if key == 'threshold_ratio' and not (0 < value < 1):
            print(f"threshold_ratio doit être entre 0 et 1, reçu {value}")
            return False
    
    return True


def compute_confidence_interval(data: np.ndarray, confidence: float = 0.95) -> tuple:
    """
    Calcule l'intervalle de confiance pour un ensemble de données.
    
    Args:
        data: Tableau de données
        confidence: Niveau de confiance (défaut : 0.95)
    
    Returns:
        Tuple (moyenne, borne_inf, borne_sup)
    """
    mean = np.mean(data)
    std = np.std(data)
    n = len(data)
    
    # Intervalle de confiance (approche normale)
    z_score = 1.96  # pour 95%
    if confidence == 0.99:
        z_score = 2.576
    
    margin = z_score * std / np.sqrt(n)
    
    return mean, mean - margin, mean + margin


def format_metric(value: float, uncertainty: float, decimals: int = 2) -> str:
    """
    Formate une métrique avec son incertitude.
    
    Args:
        value: Valeur
        uncertainty: Incertitude
        decimals: Nombre de décimales
    
    Returns:
        Chaîne formatée "valeur ± incertitude"
    """
    return f"{value:.{decimals}f} ± {uncertainty:.{decimals}f}"
