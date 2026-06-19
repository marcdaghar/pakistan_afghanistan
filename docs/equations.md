# Équations du modèle Yusuf Counter-Cycle

## 1. Variables d'état

| Variable | Description | Unité |
|----------|-------------|-------|
| S(t) | Stock collectif de biens essentiels | UM (Unités Monétaires) |
| P(t) | Production | UM/an |
| C(t) | Consommation | UM/an |
| D(t) | Dette totale | UM |

## 2. Production cyclique

La production suit un cycle sinusoïdal de période 14 ans (référence aux 7 années d'abondance et 7 de disette) :
P(t) = P_mean + P_amp × sin(2πt/T) + ε(t)

Où :
- P_mean = 1,0 (production moyenne)
- P_amp = 0,5 (amplitude)
- T = 14 (période en années)
- ε(t) ~ N(0, 0.05) (bruit aléatoire)

## 3. Système Yusuf (contre-cycle)

### Règle de basculement par seuil

Le système alterne entre deux phases selon le stock disponible :
γ(t) = γ_high si S(t) > θ × max(S)
γ(t) = γ_low si S(t) ≤ θ × max(S)

Où :
- γ_high = 0,5 (taux d'épargne en abondance)
- γ_low = 0,85 (taux de puisage en rareté)
- θ = 0,25 (seuil de basculement)

### Consommation
C(t) = B × γ(t)

Où B = 0,06 est le besoin minimal annuel.

### Dynamique du stock
dS/dt = P(t) - C(t)

### Évolution discrète
S(t+1) = max(0, S(t) + P(t) - C(t))

## 4. Système capitaliste (référence)

### Dette avec intérêt composé
D(t+1) = D(t) × (1 + r)

Où r = 0,22 est le taux d'intérêt annuel (Pakistan 2025).

### Service de la dette
Service(t) = D(t) × r

### Consommation limitée
C_cap(t) = min(P(t) - Service(t), B)

### Dynamique du stock
dS_cap/dt = P(t) - C_cap(t) - Service(t)

### Évolution discrète
S_cap(t+1) = max(0, S_cap(t) + P(t) - C_cap(t) - Service(t))

## 5. Module de gamification

### Score de conformité
Score(t) ∈ [0, 1]

### Besoin modulé
B_mod(t) = B_base × (1 - α × Score(t))

Où :
- B_base = 0,05 (besoin de base)
- α = 0,5 (impact de la conformité)

### Conformité avec clipping
B_mod(t) = clip(B_mod(t), B_min, B_max)

Où :
- B_min = 0,01
- B_max = 0,10

## 6. Métriques de validation

### Solvabilité
Solvabilité = P(S(t) > 0 pour tout t)

### Volatilité de la consommation
σ_C = √(Var(C(t)))

### Intervalle de confiance (95%)
IC_95% = μ ± 1.96 × σ/√n

### Test t de Student
t = (μ_Y - μ_C) / √(σ_Y²/n_Y + σ_C²/n_C)

### Test U de Mann-Whitney

Test non-paramétrique de comparaison des distributions.
