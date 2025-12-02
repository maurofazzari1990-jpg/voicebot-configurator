import streamlit as st
import json
import os
import urllib.parse
from collections import OrderedDict

# --- DEFINIZIONE GLOBALE DELLO SCHEMA E OPZIONI ---

CONFIG_FILE = "voicebot_config.json"

# --- OPZIONI DEFINITE DALLO SCHEMA JSON ---
BOT_GENDERS = ["male", "female", "neutral"]
BOT_VOICES = [
    "f-Achernar", "m-Achird", "m-Algenib", "m-Algieba", "m-Alnilam", "f-Aoede", "f-Autonoe", "f-Callirrhoe", 
    "m-Caronte", "f-Despina", "m-Encelado", "f-Erinome", "m-Fenrir", "f-Gacrux", "m-Giapeto", "f-Kore", 
    "f-Laomedeia", "f-Leda", "m-Orus", "f-Pulcherrima", "m-Puck", "m-Rasalgethi", "m-Sadachbia", 
    "m-Sadaltager", "m-Schedar", "f-Sulafat", "m-Umbriel", "f-Vindemiatrix", "f-Zephyr", "m-Zubenelgenubi"
]
AVAILABLE_LANGUAGES = [
    "german", "english", "spanish", "french", "italian", "japanese", "dutch", "polish", 
    "portuguese", "russian", "turkish", "catalan", "croatian", "danish", "finnish", 
    "greek", "hindi", "korean", "romanian", "swedish", "ukrainian", "vietnamese"
]
LINGUISTIC_FORMS = ["formale", "informale", "neutrale", "tecnico", "burocratico", "persuasivo", "semplificato"]
INTERACTION_STYLES = [
    "conversazionale", "amichevole", "professionale", "rassicurante", "divertente", 
    "empatico", "servizievole", "curioso", "assertivo", "accogliente", "paziente", 
    "inclusivo", "affidabile"
]
VERBOSITY_LEVELS = ["conciso", "dettagliato", "esaustivo ma conciso", "esaustivo", "contestuale"]
KNOWLEDGE_LEVELS = [
    "none", "low", "low + open questions", "moderate", "moderate + open questions", 
    "high", "high + open questions"
]
LLM_MODELS = ["gpt-4.1", "gemini-2.5-flash", "o4-mini", "gpt-oss-120b"]


# Struttura dei valori di default basata sullo schema JSON
DEFAULT_CONFIG = {
    "botParams": {
        "botName": "ROBBY",
        "botGender": "male",
        "botVoice": BOT_VOICES[0],
        "serviceDescription": "Assistente virtuale per il supporto vendite.",
        "serviceIntroduction": True,
        "availableLanguages": ["italian"], 
        "startLanguage": "italian", 
        "linguisticForm": ["neutrale"],
        "interactionStyle": ["professionale", "amichevole"],
        "verbosity": "esaustivo ma conciso",
        "useOfGeneralKnowledge": "low",
        "llmModel": "gemini-2.5-flash",
        "allowedSessionHistory": True,
        "email": "mauro.fazzari@roarinc.com"
    },
    "tools": {
        "allowedContactAgent": True,
        "allowedSendDocuments": True,
        "allowedSendEmail": True,
        "allowedScheduleMeeting": False,
        "allowedRequestCallback": True,
        "allowedHangup": True,
        "allowedSendSMS": True 
    },
    "business": {
        "ragioneSociale": "ROAR S.p.A.",
        "partitaIva": "12345678901",
        "sedeLegale": "Via Fittizia 1, 00100 Roma",
        "sitoWeb": "https://www.roarinc.com"
    }
}

# --- FUNZIONI UTILI ---

def load_config():
    """Carica la configurazione esistente o quella di default (con protezione da vecchia struttura)."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
            
            # --- CORREZIONE CRITICA PER KEY ERROR ---
            if not all(key in data for key in ['botParams', 'business', 'tools']):
                return DEFAULT_CONFIG
            
            return data
        except json.JSONDecodeError:
            st.warning("Errore di decodifica JSON. Carico i valori di default.")
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

# Funzione per estrarre il codice voce dal nome completo
def extract_voice_code(full_name):
    return full_name.split(' ')[0]

# --- INTERFACCIA STREAMLIT ---

st.set_page_config(layout="wide", page_title="Configuratore JSON Schema Voicebot")

if 'config' not in st.session_state:
    st.session_state.config = load_config()

# --- CORREZIONE AGGIUNTIVA: Garantire l'esistenza delle chiavi principali nella sessione ---
# Inizializza le chiavi mancanti con il default se la cache Streamlit ha caricato una struttura parziale.
st.session_state.config['business'] = st.session_state.config.get('business', DEFAULT_CONFIG['business'])
st.session_state.config['botParams'] = st.session_state.config.get('botParams', DEFAULT_CONFIG['botParams'])
st.session_state.config['tools'] = st.session_state.config.get('tools', DEFAULT_CONFIG['tools'])


# --- HEADER ---
try:
    st.image("ROAR LOGO.png", width=200) # Assicurati che il nome del file del logo sia corretto
except:
    pass 

st.markdown("## 🤖 Configuratore JSON Schema Voicebot")
st.caption("Configura i parametri secondo lo schema JSON richiesto.")
st.markdown("---")


# --- 1. SEZIONE BUSINESS ---
st.header("1. 🏢 Informazioni Aziendali (Business)")
current_business = st.session_state.config['business']

cols_b1 = st.columns(2)
with cols_b1[0]:
    current_business['ragioneSociale'] = st.text_input(
        "Ragione Sociale (NOME SOCIETA)", 
        value=current_business.get('ragioneSociale'), 
        key="BUSINESS_RAGIONE"
    )

with cols_b1[1]:
    current_business['partitaIva'] = st.text_input(
        "Partita IVA", 
        value=current_business.get('partitaIva'), 
        key="BUSINESS_P_IVA",
        help="Deve contenere 11 o 12 cifre numeriche (secondo lo schema)."
    )
    
current_business['sedeLegale'] = st.text_area("Sede Legale", value=current_business.get('sedeLegale'), key="BUSINESS_SEDE")
current_business['sitoWeb'] = st.text_input("Sito Web (URL)", value=current_business.get('sitoWeb'), key="BUSINESS_SITO")
st.markdown("---")


# --- 2. SEZIONE PARAMETRI BOT (botParams) ---
st.header("2. ⚙️ Parametri di Configurazione del Bot")
current_params = st.session_state.config['botParams']

# --- RIGA 1: Identità e Contatti ---
st.subheader("Identità e Contatti")
cols_p1 = st.columns(3)
with cols_p1[0]:
    current_params['botName'] = st.text_input(
        "Nome del Bot (botName)", 
        value=current_params.get('botName'), 
        key="PARAM_BOTNAME"
    )
with cols_p1[1]:
    current_params['botGender'] = st.selectbox(
        "Genere del Bot (botGender)", 
        options=BOT_GENDERS, 
        index=BOT_GENDERS.index(current_params.get('botGender')),
        key="PARAM_GENDER"
    )
with cols_p1[2]:
    current_params['email'] = st.text_input(
        "Email (Per ricezione file)", 
        value=current_params.get('email', DEFAULT_CONFIG['botParams']['email']),
        key="PARAM_EMAIL"
    )
st.text_input("Numero di Telefono (phoneNumber)", value=current_params.get('phoneNumber', 'non definito'), disabled=True, help="Campo di sola lettura come da schema.")
st.markdown("---")

# --- RIGA 2: Lingue e Voice ---
st.subheader("Lingue e Voce")
cols_p2 = st.columns(2)

with cols_p2[0]:
    # availableLanguages (Multi-Select)
    current_params['availableLanguages'] = st.multiselect(
        "Lingue disponibili (availableLanguages)", 
        options=AVAILABLE_LANGUAGES, 
        default=current_params.get('availableLanguages'),
        key="PARAM_LANG_AVAIL",
        help="Seleziona tutte le lingue supportate."
    )

with cols_p2[1]:
    # startLanguage (Selectbox, DEVE essere una lingua selezionata in 'availableLanguages')
    start_lang_options = current_params.get('availableLanguages', [])
    
    start_lang_value = current_params.get('startLanguage', 'italian')
    start_index = 0
    if start_lang_options:
        try:
            start_index = start_lang_options.index(start_lang_value)
        except ValueError:
            start_lang_value = start_lang_options[0]
            start_index = 0
            
    current_params['startLanguage'] = st.selectbox(
        "Lingua di Avvio (startLanguage)",
        options=start_lang_options,
        index=start_index,
        key="PARAM_LANG_START",
        help="DEVE essere una delle lingue scelte sopra."
    )

current_params['botVoice'] = st.selectbox(
    "Personalità Vocale (botVoice)",
    options=BOT_VOICES,
    index=BOT_VOICES.index(current_params.get('botVoice')),
    key="PARAM_VOICE",
    help="Seleziona la voce desiderata (m=maschile, f=femminile)."
)
st.markdown("---")

# --- RIGA 3: Stili e Comportamento ---
st.subheader("Stili di Conversazione e Conoscenza")
cols_p3 = st.columns(2)

with cols_p3[0]:
    # interactionStyle (Multi-Select)
    current_params['interactionStyle'] = st.multiselect(
        "Stile di Interazione (interactionStyle)",
        options=INTERACTION_STYLES,
        default=current_params.get('interactionStyle'),
        key="PARAM_INTERACTION",
        help="Seleziona lo stile prevalente (es. professionale, amichevole, empatico)."
    )

with cols_p3[1]:
    # linguisticForm (Multi-Select)
    current_params['linguisticForm'] = st.multiselect(
        "Forma Linguistica (linguisticForm)",
        options=LINGUISTIC_FORMS,
        default=current_params.get('linguisticForm'),
        key="PARAM_LINGUISTIC",
        help="Seleziona la forma linguistica utilizzata dal bot."
    )

current_params['verbosity'] = st.selectbox(
    "Livello di Verbosità (verbosity)",
    options=VERBOSITY_LEVELS,
    index=VERBOSITY_LEVELS.index(current_params.get('verbosity')),
    key="PARAM_VERBOSITY"
)

current_params['useOfGeneralKnowledge'] = st.selectbox(
    "Uso della Knowledge Base Esterna (useOfGeneralKnowledge)",
    options=KNOWLEDGE_LEVELS,
    index=KNOWLEDGE_LEVELS.index(current_params.get('useOfGeneralKnowledge')),
    key="PARAM_KB_USE"
)
st.markdown("---")

# --- RIGA 4: Servizio e Tecnica ---
st.subheader("Dettagli del Servizio e Tecnici")

current_params['serviceDescription'] = st.text_area(
    "Descrizione del Servizio (serviceDescription)",
    value=current_params.get('serviceDescription'),
    key="PARAM_SERVICE_DESC"
)

cols_tech = st.columns(3)
with cols_tech[0]:
    current_params['serviceIntroduction'] = st.checkbox(
        "Introduzione al Servizio (serviceIntroduction)",
        value=current_params.get('serviceIntroduction'),
        key="PARAM_SERVICE_INTRO"
    )
with cols_tech[1]:
    current_params['allowedSessionHistory'] = st.checkbox(
        "Storia della Sessione Consentita (allowedSessionHistory)",
        value=current_params.get('allowedSessionHistory'),
        key="PARAM_SESSION_HISTORY"
    )
with cols_tech[2]:
    current_params['llmModel'] = st.selectbox(
        "Modello LLM (llmModel)",
        options=LLM_MODELS,
        index=LLM_MODELS.index(current_params.get('llmModel')),
        key="PARAM_LLM"
    )
st.markdown("---")


# --- 3. SEZIONE CANALI e TOOLS ---
st.header("3. 🛠️ Strumenti e Canali Abilitati (Tools)")
current_tools = st.session_state.config['tools']

st.caption("Usa questa sezione per abilitare/disabilitare i canali di comunicazione e gli strumenti del bot.")

# --- CHECKLIST CANALI ---
st.subheader("Checklist Canali di Comunicazione")

cols_canali = st.columns(3)

with cols_canali[0]:
    # Telefono inbound (Mappato a allowedHangup)
    current_tools['allowedHangup'] = st.checkbox(
        "✅ Telefono Inbound",
        value=current_tools.get('allowedHangup'),
        key="TOOL_PHONE_INBOUND"
    )
    # WhatsApp (Mappato a allowedContactAgent - per contatto non-email)
    current_tools['allowedContactAgent'] = st.checkbox(
        "✅ WhatsApp",
        value=current_tools.get('allowedContactAgent'),
        key="TOOL_WHATSAPP"
    )
    # SMS (Mappato a allowedSendSMS)
    current_tools['allowedSendSMS'] = st.checkbox(
        "✅ SMS",
        value=current_tools.get('allowedSendSMS'),
        key="TOOL_SMS"
    )

with cols_canali[1]:
    # Telefono Outbound (Mappato a allowedRequestCallback)
    current_tools['allowedRequestCallback'] = st.checkbox(
        "✅ Telefono Outbound (Recall)",
        value=current_tools.get('allowedRequestCallback'),
        key="TOOL_PHONE_OUTBOUND"
    )
    # Click2Call (Mappato a allowedScheduleMeeting)
    current_tools['allowedScheduleMeeting'] = st.checkbox(
        "✅ Click2Call / Programma Riunioni",
        value=current_tools.get('allowedScheduleMeeting'),
        key="TOOL_CLICK2CALL"
    )
    # Email (Mappato a allowedSendEmail)
    current_tools['allowedSendEmail'] = st.checkbox(
        "✅ Email",
        value=current_tools.get('allowedSendEmail'),
        key="TOOL_EMAIL"
    )

st.markdown("---")

st.subheader("Strumenti e Funzionalità Aggiuntive")

cols_tools = st.columns(2)

with cols_tools[0]:
    current_tools['allowedSendDocuments'] = st.checkbox(
        "Inviare Documenti",
        value=current_tools.get('allowedSendDocuments'),
        key="TOOL_SEND_DOCS"
    )

st.markdown("---")

# --- 4. SALVATAGGIO E DOWNLOAD ---
st.header("4. 💾 Riepilogo e Download")

st.subheader("Anteprima Configurazione JSON")

# Sostituiamo i dati nella sessione con i dati modificati
st.session_state.config['business'] = current_business
st.session_state.config['botParams'] = current_params
st.session_state.config['tools'] = current_tools

st.json(st.session_state.config)

# Creo il file JSON per il download
json_data = json.dumps(st.session_state.config, indent=4)

# Ottengo i dati per l'email
destinatario = st.session_state.config['botParams']['email']
nome_societa = st.session_state.config['business']['ragioneSociale']

# Costruisco il corpo dell'email
email_subject = urllib.parse.quote(f"Configurazione Bot: {nome_societa} - Riepilogo")
email_body_text = f"""Ciao,

In allegato trovi il file JSON di configurazione completo per il tuo Voicebot "{current_params['botName']}" di {nome_societa}.

Il file JSON è scaricabile tramite l'app o allegabile separatamente.

RIEPILOGO PARAMETRI CHIAVE:
Nome Bot: {current_params['botName']}
Voce: {current_params['botVoice']}
Lingue Disponibili: {', '.join(current_params['availableLanguages'])}
Stile: {', '.join(current_params['interactionStyle'])}
"""
email_body = urllib.parse.quote(email_body_text)


col_save, col_download, col_email = st.columns(3)

if col_save.button("💾 SALVA CONFIGURAZIONE SU SERVER", type="primary"):
    save_config(st.session_state.config)

filename = f"{st.session_state.config['business']['ragioneSociale'].replace(' ', '_')}_config.json"

col_download.download_button(
    label="⬇️ SCARICA FILE CONFIGURAZIONE (.json)",
    data=json_data,
    file_name=filename,
    mime="application/json"
)

# Pulsante Email (usa st.markdown per il link mailto)
col_email.markdown(
    f"""
    <a href="mailto:{destinatario}?cc={DEFAULT_CONFIG['botParams']['email']}&subject={email_subject}&body={email_body}" target="_blank">
        <button style="background-color: #f63366; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">
            📧 INVIA RIEPILOGO EMAIL
        </button>
    </a>
    """,
    unsafe_allow_html=True
)
