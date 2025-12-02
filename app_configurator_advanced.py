import streamlit as st
import json
import os
import urllib.parse
from collections import OrderedDict

# --- DEFINIZIONE GLOBALE DELLO SCHEMA E OPZIONI (omesse per brevità, sono le stesse di prima) ---

CONFIG_FILE = "voicebot_config.json"

# --- OPZIONI DEFINITE DALLO SCHEMA JSON ---
BOT_GENDERS = ["male", "female", "neutral"]
# ... (altre liste di opzioni) ...
LLM_MODELS = ["gpt-4.1", "gemini-2.5-flash", "o4-mini", "gpt-oss-120b"]

# Struttura dei valori di default basata sullo schema JSON
DEFAULT_CONFIG = {
    "botParams": {
        "botName": "ROBBY",
        "botGender": "male",
        "botVoice": "f-Achernar",
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
        "email": "mauro.fazzari@roarinc.com" # L'indirizzo da cui l'utente vuole inviare
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
# (Le funzioni load_config, save_config, get_current_value, extract_voice_code rimangono le stesse)

# ... (Il resto del codice fino alla Sezione 4) ...

# --- 4. SALVATAGGIO E DOWNLOAD (AGGIORNATO CON INVIO EMAIL) ---
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
mittente_desiderato = "mauro.fazzari@roarinc.com"
destinatario = st.session_state.config['botParams']['email']
nome_societa = st.session_state.config['business']['ragioneSociale']

# Costruisco il corpo dell'email
email_subject = urllib.parse.quote(f"Configurazione Bot: {nome_societa} - Riepilogo JSON")
email_body_text = f"""Ciao,

In allegato trovi il file JSON di configurazione completo per il tuo Voicebot "{current_params['botName']}" di {nome_societa}, basato sullo schema richiesto.

----------------------------------------------------
RIEPILOGO PARAMETRI CHIAVE:
Nome Bot: {current_params['botName']}
Voce: {current_params['botVoice']}
Lingue Disponibili: {', '.join(current_params['availableLanguages'])}
Stile: {', '.join(current_params['interactionStyle'])}
----------------------------------------------------

Il file JSON completo è contenuto di seguito. Puoi incollarlo nel corpo dell'email prima di inviare.

"""
email_body = urllib.parse.quote(email_body_text) + urllib.parse.quote(json_data)

# Creo il link mailto:
mailto_link = f"mailto:{destinatario}?cc={mittente_desiderato}&subject={email_subject}&body={email_body}"

# --- BOTTONI ---

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
    <a href="{mailto_link}" target="_blank">
        <button style="background-color: #f63366; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">
            📧 INVIA RIEPILOGO EMAIL (Tramite Mailer Locale)
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

st.warning("⚠️ AVVISO: L'invio dell'email aprirà il tuo client di posta locale con i campi precompilati. **È necessario che tu incolli il contenuto del file JSON (mostrato sotto l'anteprima) come allegato o nel corpo dell'email prima di inviare.**")
