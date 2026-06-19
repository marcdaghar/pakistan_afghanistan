"""
Yusuf Counter-Cycle Model - Package principal
Proposition réaliste pour le Pakistan et l'Afghanistan
"""

from .model import YusufCounterCycle
from .gamification import SocialCreditModule
from .monte_carlo import run_monte_carlo
from .utils import load_parameters, save_results, validate_parameters

__version__ = "1.0.0"
__author__ = "Marc Daghar"
__license__ = "CC BY-SA 4.0"

__all__ = [
    "YusufCounterCycle",
    "SocialCreditModule",
    "run_monte_carlo",
    "load_parameters",
    "save_results",
    "validate_parameters"
]
