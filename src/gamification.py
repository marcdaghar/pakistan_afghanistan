"""
Module de gamification - Crédit Social et Conformité
Inspiré des principes de Muamalat
"""

import numpy as np
import pandas as pd
from typing import Union, Callable, Optional


class SocialCreditModule:
    """
    Module de gamification modulant le besoin de base en fonction de la conformité.
    
    Attributes:
        base_need (float): Besoin de base minimum
        max_need (float): Besoin maximum (conformité nulle)
        min_need (float): Besoin minimum (conformité parfaite)
        compliance_impact (float): Impact de la conformité sur le besoin (0-1)
    """
    
    def __init__(
        self,
        base_need: float = 0.05,
        max_need: float = 0.10,
        min_need: float = 0.01,
        compliance_impact: float = 0.5
    ):
        self.base_need = base_need
        self.max_need = max_need
        self.min_need = min_need
        self.compliance_impact = compliance_impact
    
    def calculate_need(self, compliance_score: float) -> float:
        """
        Calcule le besoin modulé en fonction du score de conformité.
        
        Args:
            compliance_score: Score de conformité entre 0 et 1
                              (1 = conformité parfaite)
        
        Returns:
            Besoin modulé (entre min_need et max_need)
        """
        need = self.base_need * (1 - self.compliance_impact * compliance_score)
        return np.clip(need, self.min_need, self.max_need)
    
    def simulate_with_compliance(
        self,
        model,
        compliance_scores: Union[list, Callable],
        shock_year: Optional[int] = None,
        shock_magnitude: float = 0.5
    ) -> pd.DataFrame:
        """
        Simule le système Yusuf avec modulation du besoin par la conformité.
        
        Args:
            model: Instance de YusufCounterCycle
            compliance_scores: Liste des scores ou fonction t -> score
            shock_year: Année du choc (None pour aucun choc)
            shock_magnitude: Amplitude du choc
            
        Returns:
            DataFrame des résultats
        """
        years = model.years
        S = np.zeros(years + 1)
        C = np.zeros(years + 1)
        P = np.zeros(years + 1)
        Need = np.zeros(years + 1)
        
        S[0] = 1.0
        max_stock = S[0]
        
        for t in range(years):
            # Production
            P[t] = model.production_cycle(t)
            
            # Choc éventuel
            if shock_year and t >= shock_year:
                P[t] *= (1 - shock_magnitude)
            
            # Score de conformité
            if callable(compliance_scores):
                score = compliance_scores(t)
            else:
                score = compliance_scores[t] if t < len(compliance_scores) else 0.5
            
            # Besoin modulé
            Need[t] = self.calculate_need(score)
            
            # Règle de basculement
            if S[t] > model.threshold_ratio * max_stock:
                gamma = model.gamma_high
            else:
                gamma = model.gamma_low
            
            # Consommation et stock
            C[t] = Need[t] * gamma
            dS = P[t] - C[t]
            S[t + 1] = max(0, S[t] + dS)
            
            if S[t + 1] > max_stock:
                max_stock = S[t + 1]
            
            if S[t + 1] == 0:
                return pd.DataFrame({
                    'Stock': S[:t + 2],
                    'Consumption': C[:t + 2],
                    'Production': P[:t + 2],
                    'Need': Need[:t + 2]
                })
        
        return pd.DataFrame({
            'Stock': S,
            'Consumption': C,
            'Production': P,
            'Need': Need
        })
    
    def generate_scenarios(self, years: int = 100) -> dict:
        """
        Génère trois scénarios de conformité.
        
        Returns:
            Dictionnaire avec trois scénarios
        """
        scenarios = {}
        
        # Scénario 1 : Conformité croissante
        scenarios['croissante'] = [min(1.0, t/50) for t in range(years)]
        
        # Scénario 2 : Conformité aléatoire
        np.random.seed(42)
        scenarios['aleatoire'] = np.random.uniform(0.3, 0.9, years).tolist()
        
        # Scénario 3 : Conformité parfaite
        scenarios['parfaite'] = [1.0] * years
        
        return scenarios
