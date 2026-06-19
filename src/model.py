"""
Yusuf Counter-Cycle Model
Module principal contenant les classes de simulation
"""

import numpy as np
import pandas as pd
from typing import Optional, Tuple


class YusufCounterCycle:
    """
    Simulation du système économique basé sur le contre-cycle de Yusuf.
    
    Attributs:
        years (int): Nombre d'années de simulation
        need (float): Besoin minimal annuel
        gamma_high (float): Taux d'épargne en abondance
        gamma_low (float): Taux de puisage en rareté
        threshold_ratio (float): Seuil de basculement (0-1)
    """
    
    def __init__(
        self,
        years: int = 100,
        need: float = 0.06,
        gamma_high: float = 0.5,
        gamma_low: float = 0.85,
        threshold_ratio: float = 0.25,
        cycle_period: int = 14
    ):
        self.years = years
        self.need = need
        self.gamma_high = gamma_high
        self.gamma_low = gamma_low
        self.threshold_ratio = threshold_ratio
        self.cycle_period = cycle_period

    def production_cycle(self, t: int, amplitude: float = 0.5, mean: float = 1.0) -> float:
        """Cycle de production sinusoïdal (période de 14 ans)"""
        return mean + amplitude * np.sin(2 * np.pi * t / self.cycle_period)

    def simulate_yusuf(
        self,
        shock_year: Optional[int] = None,
        shock_magnitude: float = 0.4,
        initial_stock: float = 0.5
    ) -> Tuple[pd.DataFrame, int]:
        """
        Simule le système Yusuf sur la période donnée.
        
        Args:
            shock_year: Année du choc (None pour aucun choc)
            shock_magnitude: Amplitude du choc (0-1)
            initial_stock: Stock initial
            
        Returns:
            DataFrame des résultats, année d'effondrement (years si pas d'effondrement)
        """
        S = np.zeros(self.years + 1)
        C = np.zeros(self.years + 1)
        P = np.zeros(self.years + 1)
        Phase = np.zeros(self.years + 1)
        
        S[0] = initial_stock
        max_stock = S[0]
        
        for t in range(self.years):
            # Production
            P[t] = self.production_cycle(t)
            
            # Choc éventuel
            if shock_year and t >= shock_year:
                P[t] *= (1 - shock_magnitude)
            
            # Règle de basculement
            if S[t] > self.threshold_ratio * max_stock:
                gamma = self.gamma_high
                Phase[t] = 1  # Abondance
            else:
                gamma = self.gamma_low
                Phase[t] = 0  # Rareté
            
            # Consommation et mise à jour du stock
            C[t] = self.need * gamma
            dS = P[t] - C[t]
            S[t + 1] = max(0, S[t] + dS)
            
            if S[t + 1] > max_stock:
                max_stock = S[t + 1]
            
            # Effondrement
            if S[t + 1] == 0:
                return pd.DataFrame({
                    'Stock': S[:t + 2],
                    'Consumption': C[:t + 2],
                    'Production': P[:t + 2],
                    'Phase': Phase[:t + 2]
                }), t + 1
        
        return pd.DataFrame({
            'Stock': S,
            'Consumption': C,
            'Production': P,
            'Phase': Phase
        }), self.years

    def simulate_capitalist(
        self,
        interest_rate: float = 0.22,
        debt_ratio: float = 0.75,
        shock_year: Optional[int] = None,
        shock_magnitude: float = 0.4,
        initial_stock: float = 0.5,
        initial_debt: float = 0.5
    ) -> Tuple[pd.DataFrame, int]:
        """
        Simule le système capitaliste avec intérêt composé.
        
        Args:
            interest_rate: Taux d'intérêt annuel
            debt_ratio: Ratio dette/PIB
            shock_year: Année du choc
            shock_magnitude: Amplitude du choc
            
        Returns:
            DataFrame des résultats, année d'effondrement
        """
        S = np.zeros(self.years + 1)
        D = np.zeros(self.years + 1)
        C = np.zeros(self.years + 1)
        P = np.zeros(self.years + 1)
        
        S[0] = initial_stock
        D[0] = initial_debt
        
        for t in range(self.years):
            P[t] = self.production_cycle(t)
            
            if shock_year and t >= shock_year:
                P[t] *= (1 - shock_magnitude)
            
            # Accumulation de la dette
            D[t + 1] = D[t] * (1 + interest_rate)
            debt_service = D[t] * interest_rate
            
            # Consommation limitée par la disponibilité
            available = max(0, P[t] - debt_service)
            C[t] = min(available, self.need)
            
            # Mise à jour du stock
            dS = P[t] - C[t] - debt_service
            S[t + 1] = max(0, S[t] + dS)
            
            # Effondrement
            if S[t + 1] == 0:
                return pd.DataFrame({
                    'Stock': S[:t + 2],
                    'Debt': D[:t + 2],
                    'Consumption': C[:t + 2],
                    'Production': P[:t + 2]
                }), t + 1
        
        return pd.DataFrame({
            'Stock': S,
            'Debt': D,
            'Consumption': C,
            'Production': P
        }), self.years
