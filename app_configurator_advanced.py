import streamlit as st
import json
import os
from collections import OrderedDict

# --- CONFIGURAZIONE E STRUTTURA DATI ---
# ... (tutto il resto del codice che segue)

# --- 1. IMPOSTAZIONI GENERALI ---
st.header("1. Impostazioni Generali")

new_name = st.text_input(
    "Nome del Voicebot:", 
    st.session_state.config.get('bot_name', DEFAULT_CONFIG['bot_name'])
)
st.session_state.config['bot_name'] = new_name

# Aggiungi un nuovo dizionario nella configurazione per questi campi generali
if 'general_params' not in st.session_state.config:
    st.session_state.config['general_params'] = {}

st.subheader("Parametri Aggiuntivi del Voicebot")

# Ciclo for per creare 10 campi di testo facilmente
for i in range(1, 11):
    param_key = f'parametro_{i}'
    
    # Recupera il valore corrente o imposta una stringa vuota come default
    current_value = st.session_state.config['general_params'].get(param_key, "")

    new_value = st.text_input(
        f"Campo di Configurazione {i}:", 
        value=current_value,
        key=f"general_{param_key}"
    )
    
    # Salva il nuovo valore nella configurazione di sessione
    st.session_state.config['general_params'][param_key] = new_value

st.markdown("---")
