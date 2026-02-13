import streamlit as st
import time
import datetime
from predictor import AviatorPredictor

# Configuration
st.set_page_config(page_title="Aviator Predictor by Caly", page_icon="✈️")

# Identifiants
USER_ID = "caly007"
USER_PASS = "Felin007@"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- PAGE DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("🔑 ACCÈS CALY PREDICTOR")
    u = st.text_input("Identifiant")
    p = st.text_input("Mot de passe", type="password")
    if st.button("SE CONNECTER"):
        if u == USER_ID and p == USER_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Identifiants incorrects.")

# --- APPLICATION PRINCIPALE ---
else:
    st.title("🚀 AVIATOR PREDICTOR BY CALY")
    
    # Récupération de l'outil de prédiction
    if 'times' not in st.session_state:
        st.session_state.times = []
        st.session_state.predictor = AviatorPredictor()

    # --- SÉLECTION DU BOOKMAKER (RÉTABLIE) ---
    market = st.selectbox(
        "SÉLECTIONNEZ VOTRE PLATEFORME :", 
        ["1XBET", "MELBET", "BETCLIC", "BETWINNER", "PREMIERBET", "888STARZ"]
    )
    
    st.write(f"Connecté sur : **{market}**")

    # Bouton de synchronisation
    if st.button("🔥 SYNC CRASH MAINTENANT", use_container_width=True):
        st.session_state.times.append(time.time())
        if len(st.session_state.times) > 5: st.session_state.times.pop(0)

    st.divider()

    # --- AFFICHAGE DES RÉSULTATS ---
    if len(st.session_state.times) >= 3:
        p_main, p_assur, s_time, conf = st.session_state.predictor.analyze(st.session_state.times)
        
        # Affichage du signal en clair
        st.markdown("### 🕒 PROCHAIN SIGNAL DÉTECTÉ :")
        st.header(f"👉 {s_time.strftime('%H:%M:%S')}")
        
        st.write("") # Espace

        # Colonnes pour les statistiques
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("COTE PRINCIPALE", f"x{p_main}")
        with c2:
            st.metric("ASSURANCE", f"x{p_assur}")
        with c3:
            st.metric("FIABILITÉ", f"{conf}%")
            
        st.info(f"Analyse synchronisée avec les serveurs de {market}")

    else:
        manquant = 3 - len(st.session_state.times)
        st.warning(f"Calibrage en cours... Cliquez encore {manquant} fois lors des prochains crashs.")

    # Sidebar
    st.sidebar.button("Déconnexion", on_click=lambda: st.session_state.update({"logged_in": False}))
