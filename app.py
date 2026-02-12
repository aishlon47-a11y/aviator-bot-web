import streamlit as st
import pandas as pd
import os
from predictor import AviatorPredictor

# Configuration de la page
st.set_page_config(
    page_title="Aviator Bot Pro",
    page_icon="✈️",
    layout="centered"
)

# Chargement du CSS personnalisé
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("static/style.css")

# Initialisation du prédicteur
if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.predictor = AviatorPredictor()

# Header
st.markdown('<div class="header"><h1>✈️ AVIATOR <span style="color:#ff2b2b">PRO</span></h1></div>', unsafe_allow_html=True)

# Zone de saisie
with st.container():
    col1, col2 = st.columns([2,1])
    with col1:
        val = st.number_input("Entrez le dernier crash :", min_value=1.0, step=0.01, format="%.2f")
    with col2:
        st.write("##") # Espacement
        if st.button("AJOUTER"):
            st.session_state.history.append(val)
            if len(st.session_state.history) > 30:
                st.session_state.history.pop(0)

# Dashboard de résultat
if len(st.session_state.history) >= 3:
    prediction, confidence = st.session_state.predictor.analyze(st.session_state.history)
    
    st.markdown(f"""
    <div class="card">
        <p style="margin:0; color:#aaa; text-transform:uppercase; font-size:12px;">Prochain crash estimé</p>
        <h1 style="color:#00ff88; font-size:4rem; margin:10px 0;">x {prediction:.2f}</h1>
        <div style="background:#333; height:8px; border-radius:5px;">
            <div style="background:#00ff88; width:{confidence}%; height:100%; border-radius:5px;"></div>
        </div>
        <p style="margin-top:10px; font-size:14px;">Indice de confiance : {confidence}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Graphique de tendance
    st.subheader("📈 Historique")
    st.line_chart(st.session_state.history[-15:])
else:
    st.info("💡 Ajoutez au moins 3 valeurs pour lancer l'algorithme d'IA.")

# Bouton réinitialiser
if st.sidebar.button("Effacer l'historique"):
    st.session_state.history = []
    st.rerun()