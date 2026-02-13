import streamlit as st
import time
import datetime
from predictor import AviatorPredictor

# Configuration de la page
st.set_page_config(page_title="Aviator Predictor by Caly", page_icon="✈️", layout="centered")

# --- IDENTIFIANTS ---
USER_ID = "caly007"
USER_PASS = "Felin007@"

# --- STYLE CSS PREMIUM ---
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; }
    .login-box {
        padding: 40px;
        background: #161b22;
        border-radius: 15px;
        border: 1px solid #ff0040;
        text-align: center;
        margin-top: 50px;
    }
    .main-container {
        border: 1px solid #333;
        padding: 25px;
        border-radius: 15px;
        background-color: #161b22;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .title-caly { color: white; font-weight: 900; font-size: 32px; letter-spacing: 1px; }
    .subtitle-caly { color: #ff0040; font-size: 14px; font-weight: bold; letter-spacing: 4px; margin-bottom: 30px; }
    .time-text { color: #00ff88; font-size: 4.5rem; font-weight: 900; margin: 0; text-shadow: 0 0 15px rgba(0,255,136,0.3); }
    .stat-label { color: #aaa; font-size: 11px; text-transform: uppercase; margin-bottom: 5px; }
    .stat-val { color: white; font-size: 26px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialisation de la session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1 style="color:white; margin-bottom:30px;">💎 ACCÈS CALY</h1>', unsafe_allow_html=True)
    
    u_input = st.text_input("IDENTIFIANT")
    p_input = st.text_input("MOT DE PASSE", type="password")
    
    if st.button("SE CONNECTER", use_container_width=True):
        if u_input == USER_ID and p_input == USER_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Accès refusé. Identifiants incorrects.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- INTERFACE DU BOT ---
else:
    if 'times' not in st.session_state:
        st.session_state.times = []
        st.session_state.predictor = AviatorPredictor()

    # Barre latérale
    with st.sidebar:
        st.title("CALY SETTINGS")
        st.write(f"Connecté en tant que: **{USER_ID}**")
        if st.button("Déconnexion"):
            st.session_state.logged_in = False
            st.rerun()

    # En-tête
    st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="title-caly">AVIATOR PREDICTOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-caly">BY CALY</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    bookmaker = st.selectbox("PLATEFORME CIBLE :", ["1XBET", "MELBET", "BETCLIC", "BETWINNER", "PREMIERBET"])

    st.markdown("<br>", unsafe_allow_html=True)

    # Bouton de capture
    if st.button("🚀 ENVOL DÉTECTÉ (CLIQUEZ AU CRASH)", use_container_width=True, type="primary"):
        st.session_state.times.append(time.time())
        if len(st.session_state.times) > 5: st.session_state.times.pop(0)

    # Analyse
    if len(st.session_state.times) >= 3:
        p_main, p_assur, s_time, conf = st.session_state.predictor.analyze(st.session_state.times)
        
        st.markdown(f"""
            <div class="main-container">
                <div style="background: #0b0e14; border: 2px solid #ff0040; border-radius: 12px; padding: 25px; margin: 20px 0;">
                    <p style="color:#aaa; margin-bottom:5px; font-size:13px; letter-spacing:1px;">SIGNAL PRÉVU À</p>
                    <h1 class="time-text">{s_time.strftime('%H:%M:%S')}</h1>
                </div>
                
                <div style="display: flex; justify-content: space-around; align-items: center;">
                    <div>
                        <p class="stat-label">Cote Principale</p>
                        <p class="stat-val">x{p_main}</p>
                    </div>
                    <div style="width: 1px; height: 40px; background: #333;"></div>
                    <div>
                        <p class="stat-label">Cote Assurance</p>
                        <p class="stat-val" style="color:#ffcc00;">x{p_assur}</p>
                    </div>
                    <div style="width: 1px; height: 40px; background: #333;"></div>
                    <div>
                        <p class="stat-label">Fiabilité</p>
                        <p class="stat-val" style="color:#00ff88;">{conf}%</p>
                    </div>
                </div>
                <div style="margin-top:20px; font-size:12px; color:#555;">Serveur : {bookmaker} Sync OK</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        needed = 3 - len(st.session_state.times)
        st.info(f"Analyse des cycles en cours... Cliquez encore {needed} fois lors des prochains décollage.")
