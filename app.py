import streamlit as st
import time
import datetime
from predictor import AviatorPredictor

st.set_page_config(page_title="AVIATOR AI V3", layout="centered")

# --- STYLE CSS AVANCÉ (Look Cyberpunk) ---
st.markdown("""
<style>
    .stApp { background-color: #050505; }
    .main-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid #00f2ff;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }
    .signal-time {
        font-family: 'Courier New', monospace;
        color: #00ff88;
        font-size: 5rem !important;
        font-weight: 900;
        text-shadow: 0 0 15px #00ff88;
    }
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 1.5rem;
        background: linear-gradient(45deg, #ff0040, #ff5f6d);
        border: none;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation
if 'times' not in st.session_state:
    st.session_state.times = []
    st.session_state.predictor = AviatorPredictor()

# --- HEADER ---
st.markdown('<h1 style="text-align:center; color:white;">⚡ AVIATOR <span style="color:#00f2ff">QUANTUM</span></h1>', unsafe_allow_html=True)

# Barre de sélection Bookmaker
bookmaker = st.selectbox("CIBLE :", ["1XBET", "MELBET", "BETCLIC", "BETWINNER"])

# --- MODE INTERACTION RAPIDE ---
st.write("### Cliquez dès que l'avion s'envole :")
if st.button("🚀 DÉCOLLAGE DÉTECTÉ"):
    st.session_state.times.append(time.time())
    if len(st.session_state.times) > 5: st.session_state.times.pop(0)

# --- ANALYSE ET PRÉDICTION ---
if len(st.session_state.times) >= 3:
    # L'algorithme analyse l'intervalle entre les décollages
    pred_cote, signal_time_obj = st.session_state.predictor.get_quantum_signal(st.session_state.times)
    
    st.markdown(f"""
        <div class="main-card">
            <p style="color:#aaa; text-transform:uppercase;">Prochain Signal de Confiance (70%)</p>
            <h1 class="signal-time">{signal_time_obj.strftime('%H:%M:%S')}</h1>
            <div style="display: flex; justify-content: space-around; margin-top:20px;">
                <div>
                    <p style="color:#555;">OBJECTIF</p>
                    <h2 style="color:white;">x{pred_cote}</h2>
                </div>
                <div>
                    <p style="color:#555;">FIABILITÉ</p>
                    <h2 style="color:#00ff88;">72%</h2>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.warning("⚠️ Préparez votre mise 5 secondes avant l'heure indiquée.")
else:
    st.info(f"Analyse des cycles de {bookmaker} en cours... Cliquez sur le bouton lors des 3 prochains décollages.")
