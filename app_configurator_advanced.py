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
        "1_ID": "1",
        "2_NAME": "ROBBY",
        "3_GENDER": "MALE",
        "4_CHANNEL_WHATSAPP": "OK",
        "5_CHANNEL_CLICK2CALL": "OK",
        "6_CHANNEL_PHONE_INBOUND": "OK",
        "7_CHANNEL_PHONE_OUTBOUND": "KO",
        "8_PERSONALITA": "EMPATHETIC",
        "9_DISCUSSION_MGM": "",
        "10_VOICE": "XXXX",
        "11_ETA_VOCALE_DEL_BOT": "Adult",
        "12_LINGUE": "IT",
        "13_VELOCITA_DEL_PARLATO": "Media",
        "14_MEMORIA_SESSIONE": "numero di cellulare",
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

# Definizione avanzata delle funzionalità disponibili
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

# --- HEADER (LOGHI E TITOLI) ---
try:
    # Mostra il logo se è stato caricato su GitHub
    st.image("logo_roar.png", width=150)
except:
    pass 

st.markdown("## 🤖 Configuratore Voicebot Avanzato")
st.markdown("---")

# --- 1. IMPOSTAZIONI GENERALI (I 13 PARAMETRI SPECIFICI) ---
st.header("1. Parametri di Base del Voicebot")

# Definizione delle opzioni per le dropdown list
OPTIONS_GENDER = ["MALE", "FEMALE", "NEUTRAL", "CUSTOM"]
OPTIONS_STATUS = ["OK", "KO"]
OPTIONS_PERSONALITA = ["Friendly", "Professional", "Empathetic", "Playful", "Formal"]
OPTIONS_ETA = ["Young", "Adult", "Senior"]
OPTIONS_VELOCITA = ["Lenta", "Media", "Veloce"]
OPTIONS_MEMORIA = ["numero di cellulare", "id specifico", "nome", "altra chiave identificativa"]


# Funzione per ottenere il valore corrente
def get_current_value(key):
    return st.session_state.config["general_params"].get(key, DEFAULT_CONFIG["general_params"].get(key, ""))


# --- PARAMETRI DI BASE ---
st.subheader("Configurazione Vocale e Identità")
cols1 = st.columns(3)

with cols1[0]:
    st.text_input("ID (1)", value=get_current_value("1_ID"), key="ID")

with cols1[1]:
    st.text_input("NAME (2)", value=get_current_value("2_NAME"), key="NAME")

with cols1[2]:
    st.selectbox("GENDER (3)", options=OPTIONS_GENDER, index=OPTIONS_GENDER.index(get_current_value("3_GENDER")), key="GENDER")


cols_voce = st.columns(3)

with cols_voce[0]:
    st.selectbox("PERSONALITA (8)", options=OPTIONS_PERSONALITA, index=OPTIONS_PERSONALITA.index(get_current_value("8_PERSONALITA")), key="PERSONALITA")

with cols_voce[1]:
    st.text_input("VOICE (9)", value=get_current_value("10_VOICE"), key="VOICE")
    
with cols_voce[2]:
    st.selectbox("ETA VOCALE DEL BOT (10)", options=OPTIONS_ETA, index=OPTIONS_ETA.index(get_current_value("11_ETA_VOCALE_DEL_BOT")), key="ETA")


cols_lingua = st.columns(3)

with cols_lingua[0]:
    st.text_input("LINGUE (11)", value=get_current_value("12_LINGUE"), key="LINGUE")

with cols_lingua[1]:
    st.selectbox("VELOCITA DEL PARLATO (12)", options=OPTIONS_VELOCITA, index=OPTIONS_VELOCITA.index(get_current_value("13_VELOCITA_DEL_PARLATO")), key="VELOCITA")

with cols_lingua[2]:
    st.selectbox("MEMORIA SESSIONE (13)", options=OPTIONS_MEMORIA, index=OPTIONS_MEMORIA.index(get_current_value("14_MEMORIA_SESSIONE")), key="MEMORIA")

st.text_input("DISCUSSION MGM (8)", value=get_current_value("9_DISCUSSION_MGM"), key="DISCUSSION")
st.markdown("---")

# --- PARAMETRI CANALI ---
st.subheader("Abilitazione Canali (Status OK/KO)")
cols_channel = st.columns(4)

with cols_channel[0]:
    st.selectbox("CHANNEL (WhatsApp) (4)", options=OPTIONS_STATUS, index=OPTIONS_STATUS.index(get_current_value("4_CHANNEL_WHATSAPP")), key="WHATSAPP")

with cols_channel[1]:
    st.selectbox("CHANNEL (Click2Call) (5)", options=OPTIONS_STATUS, index=OPTIONS_STATUS.index(get_current_value("5_CHANNEL_CLICK2CALL")), key="CLICK2CALL")

with cols_channel[2]:
    st.selectbox("CHANNEL (Phone Inbound) (6)", options=OPTIONS_STATUS, index=OPTIONS_STATUS.index(get_current_value("6_CHANNEL_PHONE_INBOUND")), key="INBOUND")

with cols_channel[3]:
    st.selectbox("CHANNEL (Phone Outbound) (7)", options=OPTIONS_STATUS, index=OPTIONS_STATUS.index(get_current_value("7_CHANNEL_PHONE_OUTBOUND")), key="OUTBOUND")

st.markdown("---")


# --- Aggiorna i valori di sessione dopo l'interazione ---
st.session_state.config["general_params"]["1_ID"] = st.session_state["ID"]
st.session_state.config["general_params"]["2_NAME"] = st.session_state["NAME"]
st.session_state.config["general_params"]["3_GENDER"] = st.session_state["GENDER"]
st.session_state.config["general_params"]["8_PERSONALITA"] = st.session_state["PERSONALITA"]
st.session_state.config["general_params"]["10_VOICE"] = st.session_state["VOICE"]
st.session_state.config["general_params"]["11_ETA_VOCALE_DEL_BOT"] = st.session_state["ETA"]
st.session_state.config["general_params"]["12_LINGUE"] = st.session_state["LINGUE"]
st.session_state.config["general_params"]["13_VELOCITA_DEL_PARLATO"] = st.session_state["VELOCITA"]
st.session_state.config["general_params"]["14_MEMORIA_SESSIONE"] = st.session_state["MEMORIA"]
st.session_state.config["general_params"]["9_DISCUSSION_MGM"] = st.session_state["DISCUSSION"]
st.session_state.config["general_params"]["4_CHANNEL_WHATSAPP"] = st.session_state["WHATSAPP"]
st.session_state.config["general_params"]["5_CHANNEL_CLICK2CALL"] = st.session_state["CLICK2CALL"]
st.session_state.config["general_params"]["6_CHANNEL_PHONE_INBOUND"] = st.session_state["INBOUND"]
st.session_state.config["general_params"]["7_CHANNEL_PHONE_OUTBOUND"] = st.session_state["OUTBOUND"]


# --- 2. ABILITAZIONE E CONFIGURAZIONE FUNZIONALITÀ ---
st.header("2. Abilitazione e Parametri Funzionalità")
st.info("Seleziona una funzionalità per abilitarla e vedi apparire i suoi parametri specifici qui sotto.")

# Contenitore per le checkbox
enabled_features = {}

st.subheader("Seleziona Funzionalità:")
with st.container(border=True):
    for feature_name, feature_data in AVAILABLE_FEATURES.items():
        
        is_checked_init = feature_name in st.session_state.config['enabled_features']
        
        is_checked = st.checkbox(
            feature_name, 
            value=is_checked_init,
            help=feature_data['description'],
            key=f"check_{feature_name}"
        )
        
        if is_checked:
            current_params_data = st.session_state.config['enabled_features'].get(feature_name, {"params": {}})
            enabled_features[feature_name] = {"enabled": True, "params": current_params_data.get("params", {})}
            
st.markdown("---")

# --- 3. CONFIGURAZIONE DEI PARAMETRI ---
st.subheader("3. Configura i Parametri Dettagliati:")

if not enabled_features:
    st.warning("Nessuna funzionalità selezionata per la configurazione dettagliata.")
else:
    # Usiamo un expander per ogni funzionalità abilitata
    for feature_name in enabled_features.keys():
        with st.expander(f"⚙️ Parametri: {feature_name}", expanded=True):
            feature_def = AVAILABLE_FEATURES[feature_name]
            
            param_cols = st.columns(2)
            param_i = 0

            for param_key, param_info in feature_def['params'].items():
                label = param_info['label']
                param_type = param_info['type']
                default_value = param_info['default']
                
                current_value = enabled_features[feature_name]["params"].get(param_key, default_value)
                new_value = None

                with param_cols[param_i % 2]:
                    if param_type == "text":
                        new_value = st.text_input(label, value=str(current_value), key=f"{feature_name}_{param_key}")
                    elif param_type == "number":
                        try:
                            step_value = 1 if isinstance(default_value, int) else 0.1
                            new_value = st.number_input(label, value=float(current_value), step=step_value, key=f"{feature_name}_{param_key}")
                        except ValueError:
                            new_value = st.number_input(label, value=float(default_value), key=f"{feature_name}_{param_key}")
                    elif param_type == "select":
                        options = param_info.get("options", [])
                        try:
                            index = options.index(current_value)
                        except ValueError:
                            index = 0
                        new_value = st.selectbox(label, options, index=index, key=f"{feature_name}_{param_key}")

                if new_value is not None:
                    enabled_features[feature_name]["params"][param_key] = new_value
                
                param_i += 1

# Aggiorna la configurazione finale nello stato di sessione
st.session_state.config['enabled_features'] = enabled_features

st.markdown("---")

# --- 4. RIEPILOGO E SALVATAGGIO (DOWNLOAD) ---
st.header("4. Riepilogo e Salvataggio (Download)")

st.subheader("Anteprima Configurazione Voicebot (JSON)")
st.json(st.session_state.config)

# Creo il file JSON per il download
json_data = json.dumps(st.session_state.config, indent=4)

col_save, col_download = st.columns(2)

# Bottone per salvare sul server
if col_save.button("💾 SALVA CONFIGURAZIONE SU SERVER", type="primary"):
    save_config(st.session_state.config)

# Bottone per scaricare il file JSON generato
col_download.download_button(
    label="⬇️ SCARICA FILE CONFIGURAZIONE (.json)",
    data=json_data,
    file_name=CONFIG_FILE,
    mime="application/json"
)

st.markdown("---")
