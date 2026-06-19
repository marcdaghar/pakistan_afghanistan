#!/usr/bin/env python3
"""
Script d'exécution des simulations pour le modèle Yusuf Counter-Cycle
Usage : python scripts/run_simulations.py --country pakistan --simulations 100
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Ajout du chemin racine
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd

from src.model import YusufCounterCycle
from src.monte_carlo import run_monte_carlo
from src.utils import load_parameters, save_results, validate_parameters


def run_single_simulation(country: str, output_dir: str = "results"):
    """
    Exécute une simulation unique pour un pays donné.
    """
    print(f"\n🇵🇰 Simulation pour {country.upper()}")
    print("=" * 50)
    
    # Chargement des paramètres
    params = load_parameters(country)
    print(f"Paramètres chargés depuis : data/{country}_parameters.json")
    
    # Validation
    if not validate_parameters(params['parameters']):
        print("❌ Paramètres invalides")
        return None
    
    # Création du modèle
    model = YusufCounterCycle(
        years=100,
        need=params['parameters']['need_minimal'],
        gamma_high=params['yusuf_parameters']['gamma_high'],
        gamma_low=params['yusuf_parameters']['gamma_low'],
        threshold_ratio=params['yusuf_parameters']['threshold_ratio']
    )
    
    # Simulation Yusuf
    print("\n🟡 Simulation Yusuf (contre-cycle)...")
    df_yusuf, collapse_y = model.simulate_yusuf(
        shock_year=40,
        shock_magnitude=0.4,
        initial_stock=params['parameters'].get('initial_stock', 0.5)
    )
    
    # Simulation capitaliste
    print("🔴 Simulation Capitaliste (intérêt)...")
    df_capitalist, collapse_c = model.simulate_capitalist(
        interest_rate=params['parameters']['interest_rate'],
        shock_year=40,
        shock_magnitude=0.4,
        initial_stock=params['parameters'].get('initial_stock', 0.5),
        initial_debt=params['parameters'].get('initial_debt', 0.5)
    )
    
    # Résultats
    final_y = df_yusuf['Stock'].iloc[-1]
    final_c = df_capitalist['Stock'].iloc[-1]
    
    print("\n📊 Résultats :")
    print(f"  Stock final (Yusuf)    : {final_y:.3f}")
    print(f"  Stock final (Capitaliste): {final_c:.3f}")
    print(f"  Effondrement Yusuf     : {'Oui' if collapse_y < 100 else 'Non'}")
    print(f"  Effondrement Capitaliste: {'Oui' if collapse_c < 100 else 'Non'}")
    
    # Sauvegarde
    results = {
        'country': country,
        'timestamp': datetime.now().isoformat(),
        'yusuf': {
            'stock_final': float(final_y),
            'collapse_year': int(collapse_y),
            'data': df_yusuf.to_dict()
        },
        'capitalist': {
            'stock_final': float(final_c),
            'collapse_year': int(collapse_c),
            'data': df_capitalist.to_dict()
        }
    }
    
    save_results(results, f"simulation_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    return results


def run_monte_carlo_analysis(country: str, n_simulations: int = 100, output_dir: str = "results"):
    """
    Exécute une analyse Monte Carlo pour un pays.
    """
    print(f"\n📈 Analyse Monte Carlo pour {country.upper()} ({n_simulations} simulations)")
    print("=" * 50)
    
    params = load_parameters(country)
    
    results = run_monte_carlo(
        n_simulations=n_simulations,
        years=100,
        need=params['parameters']['need_minimal'],
        interest_rate=params['parameters']['interest_rate']
    )
    
    print("\n📊 Résultats Monte Carlo :")
    print(f"  Stock moyen Yusuf      : {results['yusuf_mean']:.3f} ± {results['yusuf_std']:.3f}")
    print(f"  Stock moyen Capitaliste: {results['cap_mean']:.3f} ± {results['cap_std']:.3f}")
    print(f"  Solvabilité Yusuf      : {results['yusuf_solvency']*100:.1f}%")
    print(f"  Solvabilité Capitaliste: {results['cap_solvency']*100:.1f}%")
    print(f"  Test t p-value         : {results['p_value']:.6f}")
    print(f"  Test U p-value         : {results['p_mw']:.6f}")
    
    # Sauvegarde
    save_results(results, f"monte_carlo_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Yusuf Counter-Cycle Model Simulations")
    parser.add_argument('--country', type=str, default='pakistan',
                        choices=['pakistan', 'afghanistan'],
                        help='Pays à simuler')
    parser.add_argument('--simulations', type=int, default=100,
                        help='Nombre de simulations Monte Carlo')
    parser.add_argument('--type', type=str, default='both',
                        choices=['single', 'monte_carlo', 'both'],
                        help='Type d\'analyse')
    parser.add_argument('--output', type=str, default='results',
                        help='Répertoire de sortie')
    
    args = parser.parse_args()
    
    if args.type in ['single', 'both']:
        run_single_simulation(args.country, args.output)
    
    if args.type in ['monte_carlo', 'both']:
        run_monte_carlo_analysis(args.country, args.simulations, args.output)


if __name__ == "__main__":
    main()
