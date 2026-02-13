import streamlit as st
import time
import datetime
from predictor import AviatorPredictor

# Config de la page
st.set_page_config(page_title="Aviator Predictor by Caly", layout="centered")

# Identifiants
USER_ID = "caly007"
USER_PASS = "Felin007@"

# --- GESTION CONNEXION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.header("🔑 CONNEXION")
    u = st.text_input("Identifiant")
    p = st.text_input("Mot de passe", type="password")
    if st.button("SE CONNECTER"):
        if u == USER_ID and p == USER_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Accès refusé")

# --- INTERFACE PRINCIPALE ---
else:
    st.title("✈️ AVIATOR PREDICTOR")
    st.write("Compte : **CALY Premium**")
    
    if 'times' not in st.session_state:
        st.session_state.times = []
        st.session_state.predictor = AviatorPredictor()

    # Bouton d'action
    if st.button("🚀 SYNC CRASH MAINTENANT", use_container_width=True):
        st.session_state.times.append(time.time())
        if len(st.session_state.times) > 5: st.session_state.times.pop(0)

    st.divider() # Petite ligne de séparation propre

    # AFFICHAGE DES RÉSULTATS LISIBLES
    if len(st.session_state.times) >= 3:
        p_main, p_assur, s_time, conf = st.session_state.predictor.analyze(st.session_state.times)
        
        # 1. L'heure de décollage en gros
        st.subheader("🕒 PROCHAIN SIGNAL À :")
        st.header(f"👉 {s_time.strftime('%H:%M:%S')}")
        
        st.write("") # Espace

        # 2. Les chiffres clés sous forme de colonnes propres (sans code HTML visible)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="COTE PRINCIPALE", value=f"x{p_main}")
            
        with col2:
            st.metric(label="ASSURANCE", value=f"x{p_assur}")
            
        with col3:
            st.metric(label="FIABILITÉ", value=f"{conf}%")

        st.success("Analyse terminée. Préparez votre mise.")

    else:
        # Message d'attente s'il manque des données
        manquant = 3 - len(st.session_state.times)
        st.warning(f"Patientez... Cliquez encore {manquant} fois lors des prochains crashs pour calibrer le bot.")

    # Bouton déconnexion en bas
    st.sidebar.button("Quitter", on_click=lambda: st.session_state.update({"logged_in": False}))
