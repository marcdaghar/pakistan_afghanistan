# pakistan_afghanistan

# Yusuf Counter-Cycle Model
## Proposition réaliste pour le Pakistan et l'Afghanistan

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)

---

### 📖 Présentation

Ce projet formalise mathématiquement le **principe du contre-cycle de Yusuf** issu du Coran (Sourate 12:47-48) et le propose comme alternative au système économique capitaliste basé sur l'intérêt (*riba*).

Le modèle compare deux systèmes économiques sur 100 ans :

1. **Système capitaliste** : basé sur l'intérêt composé (simulation du Pakistan avec un taux d'intérêt de 22%)
2. **Système Yusuf** : basé sur le stockage en période d'abondance et le puisage en période de rareté

#### Résultats clés des simulations Monte Carlo (100 itérations, IC 95%) :

| Métrique | Capitaliste (intérêt 22%) | Yusuf (contre-cycle) |
|----------|--------------------------|---------------------|
| Stock final (moyenne) | 0,28 ± 0,38 | **0,72 ± 0,14** |
| Taux de solvabilité | 84% | **100%** |
| Volatilité de la consommation | 0,26 | **0,11** |
| Probabilité Yusuf > Capitaliste | — | **96,3%** |

**Tests statistiques** : t-test et Mann-Whitney U (p < 0,001) — différence hautement significative.

---

### 🎯 Objectifs du projet

- ✅ Fournir un **modèle quantitatif** du contre-cycle de Yusuf
- ✅ Offrir une **simulation interactive** via Streamlit
- ✅ Proposer un **module de gamification** inspiré du crédit social
- ✅ Adapter le modèle aux **contextes du Pakistan et de l'Afghanistan**
- ✅ Acter symboliquement la **fin de la guerre contre le terrorisme** par l'irénologie

---

### 🚀 Installation et exécution

#### 1. Cloner le dépôt
```bash
git clone https://github.com/marcdaghar/pakistan_afghanistan.git
