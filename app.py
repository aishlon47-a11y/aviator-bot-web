import streamlit as st
import time
import datetime
from predictor import AviatorPredictor

# Configuration
st.set_page_config(page_title="Aviator Predictor", page_icon="✈️")

# Identifiants Caly
USER_ID = "caly007"
USER_PASS = "Felin007@"

# --- STYLE VISUEL ---
st.markdown("""
<style>
    .result-box {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ff0040;
        text-align: center;
        margin-top: 20px;
    }
    .time-display {
        color: #00ff88;
        font-size: 50px;
        font-weight: bold;
        margin: 10px 0;
    }
    .prediction-text {
        color: white;
        font-size: 20px;
        margin-bottom: 5px;
    }
    .values-row {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
        border-top: 1px solid #333;
        padding-top: 15px;
    }
    .stat-card {
        text-align: center;
    }
    .label { color: #888; font-size: 14px; }
    .value { color: white; font-size: 24px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- CONNEXION ---
if not st.session_state.logged_in:
    st.title("🔑 ACCÈS CALY")
    u = st.text_input("Utilisateur")
    p = st.text_input("Mot de passe", type="password")
    if st.button("ENTRER"):
        if u == USER_ID and p == USER_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Erreur d'accès")

# --- APP PRINCIPALE ---
else:
    st.markdown("<h1 style='text-align:center;'>AVIATOR PREDICTOR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ff0040;'>SYSTÈME DE SYNCHRONISATION CALY</p>", unsafe_allow_html=True)

    if 'times' not in st.session_state:
        st.session_state.times = []
        st.session_state.predictor = AviatorPredictor()

    # Bouton de synchronisation
    if st.button("🚀 CLIQUEZ LORS DU CRASH", use_container_width=True):
        st.session_state.times.append(time.time())
        if len(st.session_state.times) > 5: st.session_state.times.pop(0)
        st.success("Crash enregistré !")

    # Affichage des résultats en langage clair
    if len(st.session_state.times) >= 3:
        p_main, p_assur, s_time, conf = st.session_state.predictor.analyze(st.session_state.times)
        
        # Le bloc de résultat propre et lisible
        st.markdown(f"""
            <div class="result-box">
                <p class="prediction-text">PROCHAIN DÉCOLLAGE À :</p>
                <div class="time-display">{s_time.strftime('%H:%M:%S')}</div>
                
                <div class="values-row">
                    <div class="stat-card">
                        <div class="label">OBJECTIF</div>
                        <div class="value">x{p_main}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">ASSURANCE</div>
                        <div class="value" style="color:#ffcc00;">x{p_assur}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">CONFIANCE</div>
                        <div class="value" style="color:#00ff88;">{conf}%</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Message d'attente lisible
        st.info(f"Analyse en cours... (Besoin de {3 - len(st.session_state.times)} crashs supplémentaires)")

    if st.sidebar.button("Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()
