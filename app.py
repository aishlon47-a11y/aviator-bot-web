import streamlit as st
import datetime
from predictor import AviatorPredictor

st.set_page_config(page_title="Aviator Signal Pro", layout="centered")

# --- BARRE LATÉRALE (Sélecteur de Bookmaker) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/732/732200.png", width=50)
bookmaker = st.sidebar.selectbox(
    "SÉLECTIONNER LE BOOKMAKER",
    ("1xBet", "Melbet", "Betclic", "Betwinner", "PremierBet")
)
st.sidebar.write(f"**Mode :** Synchronisation {bookmaker}")
st.sidebar.markdown("---")
st.sidebar.write("⚠️ *Attendez le signal exact.*")

# --- LOGIQUE DE SESSION ---
if 'predictor' not in st.session_state:
    st.session_state.predictor = AviatorPredictor()
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown(f'<h1 style="text-align:center;">{bookmaker.upper()} <span style="color:#ff0040">LIVE</span></h1>', unsafe_allow_html=True)

# Entrée des données
val = st.number_input("Dernier multiplicateur (ex: 1.85) :", min_value=1.0, step=0.01)
if st.button("CALCULER LE PROCHAIN SIGNAL"):
    st.session_state.history.append(val)
    if len(st.session_state.history) > 10: st.session_state.history.pop(0)

# --- AFFICHAGE DU SIGNAL HORAIRE ---
if len(st.session_state.history) >= 3:
    pred, conf, delay_sec = st.session_state.predictor.analyze(st.session_state.history, bookmaker)
    
    # Calcul de l'heure du signal (Heure actuelle + délai calculé)
    signal_time = datetime.datetime.now() + datetime.timedelta(seconds=delay_sec)
    time_str = signal_time.strftime("%H:%M:%S")

    st.markdown(f"""
        <div style="background:#1e1e26; padding:20px; border-radius:15px; border:2px solid #ff0040; text-align:center;">
            <h3 style="color:white; margin:0;">SIGNAL DÉTECTÉ</h3>
            <p style="color:#aaa;">Préparez votre mise pour :</p>
            <h1 style="color:#00ff88; font-size:3.5rem; margin:10px 0;">{time_str}</h1>
            <p style="color:white;">Cote estimée : <b>x {pred:.2f}</b></p>
            <small style="color:#555;">Confiance : {conf}%</small>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("Entrez les 3 derniers résultats pour générer le signal horaire.")
