"""
Simulations Monte Carlo pour la validation statistique
"""

import numpy as np
from scipy import stats
from typing import Dict
from .model import YusufCounterCycle


def run_monte_carlo(
    n_simulations: int = 100,
    years: int = 100,
    need: float = 0.06,
    interest_rate: float = 0.22
) -> Dict:
    """
    Exécute des simulations Monte Carlo pour comparer les deux systèmes.
    
    Args:
        n_simulations: Nombre de simulations
        years: Durée de la simulation
        need: Besoin minimal
        interest_rate: Taux d'intérêt du système capitaliste
        
    Returns:
        Dictionnaire des résultats statistiques
    """
    yusuf_final_stocks = []
    cap_final_stocks = []
    yusuf_collapse_years = []
    cap_collapse_years = []
    
    for _ in range(n_simulations):
        # Choc aléatoire
        shock_year = np.random.randint(20, 80)
        shock_magnitude = np.random.uniform(0.2, 0.7)
        
        model = YusufCounterCycle(years=years, need=need)
        
        # Simulation Yusuf
        df_y, years_y = model.simulate_yusuf(
            shock_year=shock_year,
            shock_magnitude=shock_magnitude
        )
        
        # Simulation capitaliste
        df_c, years_c = model.simulate_capitalist(
            interest_rate=interest_rate,
            shock_year=shock_year,
            shock_magnitude=shock_magnitude
        )
        
        yusuf_final_stocks.append(df_y['Stock'].iloc[-1])
        cap_final_stocks.append(df_c['Stock'].iloc[-1])
        yusuf_collapse_years.append(years_y)
        cap_collapse_years.append(years_c)
    
    # Tests statistiques
    t_stat, p_value = stats.ttest_ind(yusuf_final_stocks, cap_final_stocks)
    u_stat, p_mw = stats.mannwhitneyu(yusuf_final_stocks, cap_final_stocks)
    
    return {
        'yusuf_mean': np.mean(yusuf_final_stocks),
        'cap_mean': np.mean(cap_final_stocks),
        'yusuf_std': np.std(yusuf_final_stocks),
        'cap_std': np.std(cap_final_stocks),
        't_stat': t_stat,
        'p_value': p_value,
        'p_mw': p_mw,
        'yusuf_solvency': sum(1 for y in yusuf_collapse_years if y == years) / n_simulations,
        'cap_solvency': sum(1 for y in cap_collapse_years if y == years) / n_simulations,
        'yusuf_collapse_years': yusuf_collapse_years,
        'cap_collapse_years': cap_collapse_years,
        'yusuf_final_stocks': yusuf_final_stocks,
        'cap_final_stocks': cap_final_stocks
    }
