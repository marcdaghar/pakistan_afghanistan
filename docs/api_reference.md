# Référence API - Yusuf Counter-Cycle Model

## Package `src`

### Classe `YusufCounterCycle`

Modèle principal de simulation du contre-cycle de Yusuf.

#### Constructeur

```python
YusufCounterCycle(
    years: int = 100,
    need: float = 0.06,
    gamma_high: float = 0.5,
    gamma_low: float = 0.85,
    threshold_ratio: float = 0.25,
    cycle_period: int = 14
)
