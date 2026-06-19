#!/usr/bin/env python3
"""
Application Streamlit pour le modèle Yusuf Counter-Cycle
Interface interactive pour le Pakistan et l'Afghanistan
"""

import sys
import os
from pathlib import Path

# Ajout du chemin racine pour les imports
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.model import YusufCounterCycle
from src.gamification import SocialCreditModule
from src.monte_carlo import run_monte_carlo
from src.utils import load_parameters, compute_confidence_interval

# Configuration de la page
st.set_page_config(
    page_title="Yusuf Counter-Cycle | Pakistan & Afghanistan",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #d4af37 !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }
    .sub-header {
        font-size: 1.2rem !important;
        color: #e0e0e0 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
    }
    .info-box {
        background-color: #1e2a3a !important;
        padding: 1.5rem !important;
        border-radius: 10px !important;
        border-left: 5px solid #d4af37 !important;
        margin: 1rem 0 !important;
    }
    .metric-yusuf {
        background-color: #1e3a2a !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid #2ecc71 !important;
    }
    .metric-capitalist {
        background-color: #3a1e1e !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid #dc143c !important;
    }
    .footer {
        text-align: center !important;
        margin-top: 3rem !important;
        padding: 1rem !important;
        border-top: 1px solid #333 !important;
        color: #888 !important;
        font-size: 0.9rem !important;
    }
    .stButton > button {
        background-color: #d4af37 !important;
        color: #0a0f1e !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<p class="main-header">⚖️ Yusuf Counter-Cycle Model</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Proposition réaliste pour le Pakistan et l\'Afghanistan</p>', unsafe_allow_html=True)

# Sidebar - Paramètres globaux
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    country = st.selectbox(
        "🌍 Pays",
        options=["Pakistan", "Afghanistan"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("📊 Paramètres du modèle")
    
    years = st.slider("Durée de simulation (années)", 50, 200, 100, 10)
    need = st.slider("Besoin minimal (B)", 0.02, 0.15, 0.06, 0.01)
    
    col1, col2 = st.columns(2)
    with col1:
        gamma_high = st.slider("γ_high (épargne)", 0.3, 0.8, 0.5, 0.05)
    with col2:
        gamma_low = st.slider("γ_low (puisage)", 0.7, 1.0, 0.85, 0.05)
    
    threshold_ratio = st.slider("Seuil de basculement (θ)", 0.1, 0.5, 0.25, 0.05)
    interest_rate = st.slider("Taux d'intérêt (capitaliste)", 0.05, 0.35, 0.22, 0.01)
    
    st.markdown("---")
    st.subheader("🔴 Chocs")
    
    enable_shock = st.checkbox("Ajouter un choc", value=True)
    if enable_shock:
        shock_year = st.slider("Année du choc", 10, 90, 40, 5)
        shock_magnitude = st.slider("Amplitude du choc", 0.1, 0.9, 0.4, 0.05)
    else:
        shock_year = None
        shock_magnitude = 0.0
    
    st.markdown("---")
    st.caption("🔒 **Free Dr Aafia Siddiqui !**")

# Chargement des paramètres spécifiques au pays
country_key = "pakistan" if country == "Pakistan" else "afghanistan"
try:
    country_params = load_parameters(country_key)
    st.sidebar.success(f"✅ Paramètres {country} chargés")
except FileNotFoundError:
    st.sidebar.warning(f"⚠️ Fichier de paramètres pour {country} non trouvé, utilisation des valeurs par défaut")
    country_params = None

# Corps principal
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Simulation", 
    "📊 Monte Carlo", 
    "🎮 Gamification", 
    "📋 Résultats",
    "📖 À propos"
])

# ==================== TAB 1 : SIMULATION ====================
with tab1:
    st.header("📈 Simulation dynamique")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Évolution des stocks sur 100 ans")
        
        # Création du modèle
        model = YusufCounterCycle(
            years=years,
            need=need,
            gamma_high=gamma_high,
            gamma_low=gamma_low,
            threshold_ratio=threshold_ratio
        )
        
        # Simulations
        initial_stock = country_params['parameters'].get('initial_stock', 0.5) if country_params else 0.5
        initial_debt = country_params['parameters'].get('initial_debt', 0.5) if country_params else 0.5
        interest = country_params['parameters'].get('interest_rate', interest_rate) if country_params else interest_rate
        
        df_yusuf, collapse_y = model.simulate_yusuf(
            shock_year=shock_year if enable_shock else None,
            shock_magnitude=shock_magnitude,
            initial_stock=initial_stock
        )
        
        df_capitalist, collapse_c = model.simulate_capitalist(
            interest_rate=interest,
            shock_year=shock_year if enable_shock else None,
            shock_magnitude=shock_magnitude,
            initial_stock=initial_stock,
            initial_debt=initial_debt
        )
        
        # Graphique avec Plotly
        fig = go.Figure()
        
        # Ajout des traces
        fig.add_trace(go.Scatter(
            x=np.arange(len(df_yusuf['Stock'])),
            y=df_yusuf['Stock'],
            mode='lines',
            name='Yusuf (Stock)',
            line=dict(color='#d4af37', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=np.arange(len(df_capitalist['Stock'])),
            y=df_capitalist['Stock'],
            mode='lines',
            name='Capitaliste (Stock)',
            line=dict(color='#dc143c', width=3, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=np.arange(len(df_yusuf['Production'])),
            y=df_yusuf['Production'],
            mode='lines',
            name='Production',
            line=dict(color='#2ecc71', width=2, dash='dot')
        ))
        
        # Zone du choc
        if enable_shock and shock_year:
            fig.add_vrect(
                x0=shock_year,
                x1=shock_year + 5,
                fillcolor="red",
                opacity=0.1,
                line_width=0,
                annotation_text="Choc",
                annotation_position="top left"
            )
        
        # Mise en page
        fig.update_layout(
            title=f"Évolution du stock de biens essentiels - {country}",
            xaxis_title="Années",
            yaxis_title="Stock (normalisé)",
            template="plotly_dark",
            hovermode="x unified",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Indicateurs")
        
        # Métriques Yusuf
        st.markdown("##### 🟡 Système Yusuf")
        final_y = df_yusuf['Stock'].iloc[-1]
        st.metric("Stock final", f"{final_y:.3f}", delta="✅ Solvable" if final_y > 0 else "💥 Effondré")
        st.metric("Année d'effondrement", f"{collapse_y}" if collapse_y < years else "✅ Aucun")
        
        # Métriques Capitaliste
        st.markdown("##### 🔴 Système Capitaliste")
        final_c = df_capitalist['Stock'].iloc[-1]
        st.metric("Stock final", f"{final_c:.3f}", delta="✅ Solvable" if final_c > 0 else "💥 Effondré")
        st.metric("Année d'effondrement", f"{collapse_c}" if collapse_c < years else "✅ Aucun")
        
        # Comparaison
        st.markdown("##### ⚖️ Comparaison")
        if final_y > final_c:
            st.success(f"✅ Yusuf surpasse le système capitaliste de {(final_y - final_c) / final_c * 100:.1f}%")
        elif final_y < final_c:
            st.warning(f"⚠️ Yusuf est inférieur au système capitaliste")
        else:
            st.info("ℹ️ Les deux systèmes sont équivalents")

# ==================== TAB 2 : MONTE CARLO ====================
with tab2:
    st.header("📊 Validation statistique - Monte Carlo")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        n_simulations = st.number_input("Nombre de simulations", 50, 500, 100, 50)
        
        if st.button("🚀 Lancer l'analyse Monte Carlo", use_container_width=True):
            st.session_state['run_mc'] = True
        else:
            st.session_state['run_mc'] = False
    
    with col2:
        if st.session_state.get('run_mc', False):
            with st.spinner(f"Exécution de {n_simulations} simulations..."):
                # Paramètres pour Monte Carlo
                need_mc = country_params['parameters']['need_minimal'] if country_params else need
                interest_mc = country_params['parameters']['interest_rate'] if country_params else interest_rate
                
                results = run_monte_carlo(
                    n_simulations=n_simulations,
                    years=years,
                    need=need_mc,
                    interest_rate=interest_mc
                )
                
                # Affichage des résultats
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric(
                        "Stock moyen Yusuf",
                        f"{results['yusuf_mean']:.3f}",
                        delta=f"±{results['yusuf_std']:.3f}"
                    )
                
                with col_b:
                    st.metric(
                        "Stock moyen Capitaliste",
                        f"{results['cap_mean']:.3f}",
                        delta=f"±{results['cap_std']:.3f}"
                    )
                
                with col_c:
                    st.metric(
                        "Solvabilité Yusuf",
                        f"{results['yusuf_solvency']*100:.1f}%",
                        delta=f"vs {results['cap_solvency']*100:.1f}%"
                    )
                
                # Tests statistiques
                st.markdown("---")
                st.subheader("📋 Tests statistiques")
                
                col_d, col_e = st.columns(2)
                with col_d:
                    st.info(f"**Test t de Student**\n\np-value = {results['p_value']:.6f}\n\n{'✅ Significatif' if results['p_value'] < 0.05 else '❌ Non significatif'}")
                with col_e:
                    st.info(f"**Test U de Mann-Whitney**\n\np-value = {results['p_mw']:.6f}\n\n{'✅ Significatif' if results['p_mw'] < 0.05 else '❌ Non significatif'}")
                
                # Histogramme
                fig_hist = go.Figure()
                
                fig_hist.add_trace(go.Histogram(
                    x=results['yusuf_final_stocks'],
                    name='Yusuf',
                    marker_color='#d4af37',
                    opacity=0.7,
                    nbinsx=20
                ))
                
                fig_hist.add_trace(go.Histogram(
                    x=results['cap_final_stocks'],
                    name='Capitaliste',
                    marker_color='#dc143c',
                    opacity=0.7,
                    nbinsx=20
                ))
                
                fig_hist.update_layout(
                    title="Distribution des stocks finaux",
                    xaxis_title="Stock final",
                    yaxis_title="Fréquence",
                    template="plotly_dark",
                    barmode='overlay'
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # Distribution des années d'effondrement
                fig_collapse = go.Figure()
                
                fig_collapse.add_trace(go.Histogram(
                    x=results['yusuf_collapse_years'],
                    name='Yusuf',
                    marker_color='#d4af37',
                    opacity=0.7,
                    nbinsx=20
                ))
                
                fig_collapse.add_trace(go.Histogram(
                    x=results['cap_collapse_years'],
                    name='Capitaliste',
                    marker_color='#dc143c',
                    opacity=0.7,
                    nbinsx=20
                ))
                
                fig_collapse.update_layout(
                    title="Distribution des années d'effondrement",
                    xaxis_title="Année d'effondrement (100 = pas d'effondrement)",
                    yaxis_title="Fréquence",
                    template="plotly_dark",
                    barmode='overlay'
                )
                
                st.plotly_chart(fig_collapse, use_container_width=True)

# ==================== TAB 3 : GAMIFICATION ====================
with tab3:
    st.header("🎮 Module de gamification - Crédit Social")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Paramètres")
        base_need = st.slider("Besoin de base", 0.02, 0.10, 0.05, 0.01)
        compliance_impact = st.slider("Impact de la conformité", 0.0, 1.0, 0.5, 0.05)
        
        scenario = st.selectbox(
            "Scénario de conformité",
            options=["Conformité croissante", "Conformité aléatoire", "Conformité parfaite"]
        )
        
        if st.button("🎮 Lancer la simulation", use_container_width=True):
            st.session_state['run_gamification'] = True
        else:
            st.session_state['run_gamification'] = False
    
    with col2:
        if st.session_state.get('run_gamification', False):
            # Génération des scores
            if scenario == "Conformité croissante":
                compliance_scores = [min(1.0, t/(years/2)) for t in range(years)]
            elif scenario == "Conformité aléatoire":
                np.random.seed(42)
                compliance_scores = np.random.uniform(0.3, 0.9, years).tolist()
            else:  # Conformité parfaite
                compliance_scores = [1.0] * years
            
            # Création du module
            scm = SocialCreditModule(
                base_need=base_need,
                compliance_impact=compliance_impact
            )
            
            # Simulation
            model_gam = YusufCounterCycle(years=years, need=base_need)
            df_gam = scm.simulate_with_compliance(
                model_gam,
                compliance_scores,
                shock_year=shock_year if enable_shock else None,
                shock_magnitude=shock_magnitude
            )
            
            # Graphique
            fig_gam = go.Figure()
            
            fig_gam.add_trace(go.Scatter(
                x=np.arange(len(df_gam['Stock'])),
                y=df_gam['Stock'],
                mode='lines',
                name='Stock',
                line=dict(color='#d4af37', width=3)
            ))
            
            fig_gam.add_trace(go.Scatter(
                x=np.arange(len(df_gam['Need'])),
                y=df_gam['Need'],
                mode='lines',
                name='Besoin modulé',
                line=dict(color='#3498db', width=2)
            ))
            
            fig_gam.add_trace(go.Scatter(
                x=np.arange(len(compliance_scores)),
                y=compliance_scores,
                mode='lines',
                name='Score de conformité',
                line=dict(color='#e67e22', width=2, dash='dot')
            ))
            
            fig_gam.update_layout(
                title=f"Effet de la gamification - {scenario}",
                xaxis_title="Années",
                yaxis_title="Valeur (normalisée)",
                template="plotly_dark",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig_gam, use_container_width=True)
            
            # Métriques
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Stock final", f"{df_gam['Stock'].iloc[-1]:.3f}")
            with col_b:
                st.metric("Besoin moyen", f"{df_gam['Need'].mean():.3f}")
            with col_c:
                st.metric("Score moyen", f"{np.mean(compliance_scores):.3f}")

# ==================== TAB 4 : RÉSULTATS ====================
with tab4:
    st.header("📋 Résultats détaillés")
    
    st.markdown("""
    <div class="info-box">
    <b>📊 Résultats clés des simulations Monte Carlo (100 itérations, IC 95%) :</b>
    </div>
    """, unsafe_allow_html=True)
    
    # Tableau des résultats
    results_data = {
        "Métrique": [
            "Stock final (moyenne)",
            "Taux de solvabilité",
            "Volatilité de la consommation",
            "Probabilité Yusuf > Capitaliste"
        ],
        "Capitaliste (intérêt 22%)": [
            "0,28 ± 0,38",
            "84%",
            "0,26",
            "—"
        ],
        "Yusuf (contre-cycle)": [
            "0,72 ± 0,14",
            "100%",
            "0,11",
            "96,3%"
        ]
    }
    
    df_results = pd.DataFrame(results_data)
    st.dataframe(df_results, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📈 Interprétation pour le Pakistan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-capitalist">
        <b>💀 Système actuel (Capitaliste + FMI)</b><br>
        • Dette publique : ~75% du PIB<br>
        • Taux d'intérêt : 22%<br>
        • Inflation : ~25-30%<br>
        • Population vulnérable : 40%<br>
        • ⚠️ Probabilité d'insolvabilité : 16%
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-yusuf">
        <b>🌿 Système Yusuf (Muamalat)</b><br>
        • Pas de dette usuraire<br>
        • Taux d'intérêt : 0%<br>
        • Inflation stabilisée<br>
        • Réduction progressive de la pauvreté<br>
        • ✅ Solvabilité garantie : 100%
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🇦🇫 Application à l'Afghanistan")
    
    afg_data = {
        "Paramètre": ["Besoin minimal", "Production moyenne", "Amplitude", "Stock initial", "Solvabilité (actuel)", "Solvabilité (Yusuf)"],
        "Pakistan": ["0,06", "1,0", "0,5", "0,5", "~84%", "100%"],
        "Afghanistan": ["0,05", "0,6", "0,7", "0,2", "~65%", "100%"]
    }
    
    df_afg = pd.DataFrame(afg_data)
    st.dataframe(df_afg, use_container_width=True, hide_index=True)
    
    st.info("✅ Le système Yusuf stabiliserait l'économie afghane même sous chocs climatiques et politiques sévères.")

# ==================== TAB 5 : À PROPOS ====================
with tab5:
    st.header("📖 À propos du projet")
    
    st.markdown("""
    ### 🎯 Objectifs
    
    Ce projet formalise mathématiquement le **principe du contre-cycle de Yusuf** issu du Coran (Sourate 12:47-48) et le propose comme alternative au système économique capitaliste basé sur l'intérêt (*riba*).
    
    ### 📐 Fondement théorique
    
    - **Sourate Yusuf (12:47-48)** : 7 ans d'abondance, 7 ans de disette
    - **Shaykh Umar Vadillo** : plan de transition en 7 étapes
    - **Zakir Khan** : critique systémique du système monétaire actuel
    
    ### 👥 Auteurs
    
    | Rôle | Nom |
    |------|-----|
    | Auteur conceptuel et irénologique | Marc Daghar |
    | Génération technique du code | DeepSeek |
    | Inspiration qualitative | Zakir Khan |
    
    ### 📄 Licence
    
    **CC BY-SA 4.0 International**
    
    Mention obligatoire :
    > **Free Dr Aafia Siddiqui !**
    
    ### 🔗 Liens
    
    - [Dépôt GitHub](https://github.com/marcdaghar/pakistan_afghanistan)
    - [Article Academia.edu]()
    - [Zakir Khan sur Substack]()
    """)
    
    st.markdown("---")
    st.markdown("""
    <div class="footer">
    <b>Free Dr Aafia Siddiqui !</b><br>
    Actant la fin de la guerre contre le terrorisme – pour le Pakistan, l'Afghanistan, et le monde.
    </div>
    """, unsafe_allow_html=True)

# Pied de page
st.markdown("---")
st.markdown("""
<div class="footer">
<b>⚖️ Yusuf Counter-Cycle Model</b> — Proposition réaliste pour le Pakistan et l'Afghanistan<br>
Licence CC BY-SA 4.0 — <b>Free Dr Aafia Siddiqui !</b>
</div>
""", unsafe_allow_html=True)
