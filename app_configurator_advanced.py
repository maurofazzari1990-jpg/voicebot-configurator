import streamlit as st
import json
import os
from collections import OrderedDict

# --- CONFIGURAZIONE E STRUTTURA DATI ---

CONFIG_FILE = "voicebot_config.json"
DEFAULT_CONFIG = {
    "bot_name": "Nuovo Voicebot",
    "general_params": {}, 
    "enabled_features": {}
}

# Funzioni di caricamento/salvataggio (Gestiscono gli errori se il file è corrotto)
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
            st.warning("⚠️ Errore: Il file di configurazione è corrotto. Ritorno alla configurazione di default.")
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

st.set_page_config(layout="wide", page_title="Voicebot Configurator Avanzato")
st.title("🤖 Configuratore Voicebot Avanzato")

# Inizializza o carica lo stato di sessione
if 'config' not in st.session_state:
    st.session_state.config = load_config()

# --- 1. IMPOSTAZIONI GENERALI + 10 CAMPI ---
st.header("1. Impostazioni Generali")

new_name = st.text_input(
    "Nome del Voicebot:", 
    st.session_state.config.get('bot_name', DEFAULT_CONFIG['bot_name'])
)
st.session_state.config['bot_name'] = new_name

# Area per i 10 campi aggiuntivi
if 'general_params' not in st.session_state.config:
    st.session_state.config['general_params'] = {}

st.subheader("Parametri Aggiuntivi Personalizzati (10 Campi)")
st.caption("Usa questi campi per impostazioni globali specifiche del tuo bot.")

# Ciclo for per creare 10 campi di testo facilmente
cols_general = st.columns(2)
for i in range(1, 11):
    param_key = f'parametro_{i}'
    
    current_value = st.session_state.config['general_params'].get(param_key, "")

    with cols_general[(i-1) % 2]:
        new_value = st.text_input(
            f"Campo di Configurazione {i}:", 
            value=current_value,
            key=f"general_{param_key}"
        )
    
    st.session_state.config['general_params'][param_key] = new_value

st.markdown("---")

# --- 2. ABILITAZIONE E CONFIGURAZIONE FUNZIONALITÀ ---
st.header("2. Abilitazione e Parametri Funzionalità")
st.info("Seleziona una funzionalità per abilitarla e vedi apparire i suoi parametri specifici qui sotto.")

# Contenitore per le checkbox
enabled_features = {}
cols_features = st.columns(2)
i = 0

st.subheader("Seleziona Funzionalità:")
with st.container(border=True):
    for feature_name, feature_data in AVAILABLE_FEATURES.items():
        
        is_checked_init = feature_name in st.session_state.config['enabled_features']
        
        is_checked = cols_features[i % 2].checkbox(
            feature_name, 
            value=is_checked_init,
            help=feature_data['description'],
            key=f"check_{feature_name}"
        )
        
        if is_checked:
            current_params_data = st.session_state.config['enabled_features'].get(feature_name, {"params": {}})
            enabled_features[feature_name] = {"enabled": True, "params": current_params_data.get("params", {})}
            
        i += 1

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
            
            for param_key, param_info in feature_def['params'].items():
                label = param_info['label']
                param_type = param_info['type']
                default_value = param_info['default']
                
                current_value = enabled_features[feature_name]["params"].get(param_key, default_value)

                new_value = None
                
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

# Aggiorna la configurazione finale nello stato di sessione
st.session_state.config['enabled_features'] = enabled_features

st.markdown("---")

# --- 4. RIEPILOGO E SALVATAGGIO CON DOWNLOAD ---
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
st.info(f"Clicca 'Salva configurazione su server' per rendere persistenti le modifiche online, oppure 'Scarica file configurazione' per ottenere il file JSON sul tuo computer.")
