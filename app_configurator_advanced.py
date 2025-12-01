import streamlit as st
import json
import os
from collections import OrderedDict

# --- CONFIGURAZIONE GLOBALE ---

# Imposta il layout wide e il titolo
st.set_page_config(layout="wide", page_title="Voicebot Configurator Avanzato")

CONFIG_FILE = "voicebot_config.json"
# Struttura dei 13 parametri generali
DEFAULT_CONFIG = {
    "bot_name": "Nuovo Voicebot",
    "general_params": {
        "1_NOME AZIENDA": "",
        "2_NAME": "",
        "3_GENDER": "",
        "4_CHANNEL_WHATSAPP": "",
        "5_CHANNEL_CLICK2CALL": "",
        "6_CHANNEL_PHONE_INBOUND": "",
        "7_CHANNEL_PHONE_OUTBOUND": "",
        "8_PERSONALITA": "",
        "9_DISCUSSION_MGM": "",
        "10_VOICE": "",
        "11_ETA_VOCALE_DEL_BOT": "",
        "12_LINGUE": "",
        "13_VELOCITA_DEL_PARLATO": "",
        "14_MEMORIA_SESSIONE": "",
    },
    "enabled_features": {}
}

# Funzioni di caricamento/salvataggio
def load_config():
    """Carica la configurazione esistente o quella di default."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                return {
                    "bot_name": data.get("bot_name", DEFAULT_CONFIG["bot_name"]),
                    "general_params": data.get("general_params", DEFAULT_CONFIG["general_params"]),
                    "enabled_features": data.get("enabled_features", DEFAULT_CONFIG["enabled_features"])
                }
        except json.JSONDecodeError:
            # Ritorna DEFAULT_CONFIG in caso di corruzione del file
            return DEFAULT_CONFIG 
    return DEFAULT_CONFIG

def save_config(config_data):
    """Salva la configurazione corrente in un file JSON sul server."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
        st.success(f"✅ Configurazione salvata con successo in '{CONFIG_FILE}'")
    except Exception as e:
        st.error(f"❌ Errore durante il salvataggio: {e}")

# Definizione avanzata delle funzionalità disponibili (Sezione 2 e 3)
AVAILABLE_FEATURES = OrderedDict([
    ("FAQ & Risposte Standard", {
        "description": "Risponde a domande predefinite e frequenti.",
        "params": {
            "knowledge_base_url": {"label": "URL della Knowledge Base", "type": "text", "default": "http://example.com/faqs.json"},
            "max_attempts": {"label": "Max tentativi prima di fallire", "type": "number", "default": 3}
        }
    }),
    ("Reindirizzamento Operatore", {
        "description": "Trasferisce la conversazione ad un agente umano.",
        "params": {
            "target_number": {"label": "Numero di Telefono Agente", "type": "text", "default": "+3906123456"},
            "queue_priority": {"label": "Priorità in Coda (1=Alta)", "type": "number", "default": 5}
        }
    }),
    ("Autenticazione Utente", {
        "description": "Verifica l'identità dell'utente (es. tramite PIN).",
        "params": {
            "auth_service_api": {"label": "Endpoint API di Autenticazione", "type": "text", "default": "https://auth.service/verify"},
            "token_expiration_minutes": {"label": "Durata Token (minuti)", "type": "number", "default": 30}
        }
    }),
    ("Invio Riepilogo (SMS/Email)", {
        "description": "Invia un riepilogo dell'interazione al cliente.",
        "params": {
            "default_channel": {"label": "Canale di Invio Predefinito", "type": "select", "options": ["Email", "SMS"], "default": "Email"}
        }
    })
])

# --- INTERFACCIA STREAMLIT ---

# Inizializza o carica lo stato di sessione
if 'config' not in st.session_state:
    st.session_state.config = load_config()

# CORREZIONE CRITICA: Assicurarsi che le chiavi principali esistano (risolve Attribute/Value Error)
# Forza l'uso dei default se la sessione non è completa (es. dopo l'eliminazione di voicebot_config.json)
if 'general_params' not in st.session_state.config or not st.session_state.config['general_params']:
    st.session_state.config['general_params'] = DEFAULT_CONFIG['general_params']

if 'enabled_features' not in st.session_state.config:
    st.session_state.config['enabled_features'] = DEFAULT_CONFIG['enabled_features']


# --- DEFINIZIONE VARIABILI E OPZIONI PER IL FRONTEND ---

# Definizione delle opzioni per le dropdown list
OPTIONS_GENDER = ["MALE", "FEMALE", "NEUTRAL", "CUSTOM"]
OPTIONS_STATUS = ["OK", "KO"]
OPTIONS_PERSONALITA = ["Friendly", "Professional", "EMPATHETIC", "Playful", "Formal"] # ATTENZIONE: deve corrispondere al default!
OPTIONS_ETA = ["Young", "Adult", "Senior"]
OPTIONS_VELOCITA = ["Lenta", "Media", "Veloce"]
OPTIONS_MEMORIA = ["numero di cellulare", "id specifico", "nome", "altra chiave identificativa"]

# Funzione per ottenere il valore corrente (CORREZIONE FINALE)
# Questa versione è più robusta e usa il DEFAULT_CONFIG in caso di errore di indicizzazione.
def get_current_value(key):
    try:
        # Tenta di prendere il valore dalla sessione
        value = st.session_state.config["general_params"].get(key)
        if value is None:
            # Se non è in sessione, usa il valore di default
            return DEFAULT_CONFIG["general_params"].get(key, "")
        return value
    except:
        # In caso di qualsiasi altro errore di sessione, usa il valore di default
        return DEFAULT_CONFIG["general_params"].get(key, "")


# --- HEADER (LOGHI E TITOLI) ---
try:
    # Mostra il logo se è stato caricato su GitHub
    st.image("logo_roar.png", width=200) 
except:
    pass 

st.markdown("## 🤖 Configuratore Voicebot Avanzato")
st.markdown("---")


# --- 1. PARAMETRI DI BASE DEL VOICEBOT (I 13 PARAMETRI SPECIFICI) ---
st.header("1. Parametri di Base del Voicebot")

# --- Configurazione Vocale e Identità ---
st.subheader("Configurazione Vocale e Identità")
cols1 = st.columns(3)

# GESTIONE DEI CAMPI D'INPUT E SELECTBOX
with cols1[0]:
    # 1. ID
    st.text_input("ID (1)", value=get_current_value("1_ID"), key="ID")

with cols1[1]:
    # 2. NAME
    st.text_input("NAME (2)", value=get_current_value("2_NAME"), key="NAME")

with cols1[2]:
    # 3. GENDER (Dropdown)
    st.selectbox("GENDER (3)", options=OPTIONS_GENDER, index=OPTIONS_GENDER.index(get_current_value("3_GENDER")), key="GENDER")


cols_voce = st.columns(3)

with cols_voce[0]:
    # 8. PERSONALITA (Dropdown)
    st.selectbox("PERSONALITA (8)", options=OPTIONS_PERSONALITA, index=OPTIONS_PERSONALITA.index(get_current_value("8_PERSONALITA")), key="PERSONALITA")

with cols_voce[1]:
    # 9. VOICE
    st.text_input("VOICE (9)", value=get_current_value("10_VOICE"), key="VOICE")
    
with cols_voce[2]:
    # 10. ETA VOCALE DEL BOT (Dropdown)
    st.selectbox("ETA VOCALE DEL BOT (10)", options=OPTIONS_ETA, index=OPTIONS_ETA.index(get_current_value("11_ETA_VOCALE_DEL_BOT")), key="ETA")


cols_lingua = st.columns(3)

with cols_lingua[0]:
    # 11. LINGUE
    st.text_input("LINGUE (11)", value=get_current_value("12_LINGUE"), key="LINGUE")

with cols_lingua[1]:
    # 12. VELOCITA DEL PARLATO (Dropdown)
    st.selectbox("VELOCITA DEL PARLATO (12)", options=OPTIONS_VELOCITA, index=OPTIONS_VELOCITA.index(get_current_value("13_VELOCITA_DEL_PARLATO")), key="VELOCITA")

with cols_lingua[2]:
    # 13. MEMORIA SESSIONE (Dropdown)
    st.selectbox("MEMORIA SESSIONE (13)", options=OPTIONS_MEMORIA, index=OPTIONS_MEMORIA.index(get_current_value("14_MEMORIA_SESSIONE")), key="MEMORIA")

# 8. DISCUSSION MGM (Campo singolo che prende l'intera larghezza)
st.text_input("DISCUSSION MGM (9)", value=get_current_value("9_DISCUSSION_MGM"), key="DISCUSSION")
st.markdown("---")

# --- PARAMETRI CANALI ---
st.subheader("Abilitazione Canali (Status OK/KO)")
cols_channel = st.columns(4)

with cols_channel[0]:
    # 4. CHANNEL (WhatsApp) (Dropdown)
    st.selectbox("CHANNEL (WhatsApp) (4)", options=OPTIONS_STATUS, index=OPTIONS_STATUS.index(get_current_value("4_CHANNEL_WHATSAPP")), key="WHATSAPP")

with cols_channel[1]:
    # 5. CHANNEL (Click2Call) (Dropdown)
    st.selectbox("CHANNEL (Click2Call) (5)", options=OPTIONS_STATUS, index=OPTIONS_STATUS.index(get_current_value("5_CHANNEL_CLICK2CALL")), key="CLICK2CALL")

with cols_channel[2]:
    # 6. CHANNEL (Phone Inbound) (Dropdown)
    st.selectbox("CHANNEL (Phone Inbound) (6)", options=OPTIONS_STATUS, index=OPTIONS_STATUS.index(get_current_value("6_CHANNEL_PHONE_INBOUND")), key="INBOUND")

with cols_channel[3]:
    # 7. CHANNEL (Phone Outbound) (Dropdown)
st.markdown("---")
