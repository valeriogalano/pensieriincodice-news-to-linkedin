<div align="center">
  <img src="https://cdn.pensieriincodice.it/images/pensieriincodice-locandina.png" alt="Logo Progetto" width="150"/>
  <h1>Pensieri in codice — News to LinkedIn</h1>
  <p>Pubblica automaticamente le news di PIC sull'account LinkedIn del podcast, prelevandole da Readwise.</p>
  <p>
    <img src="https://img.shields.io/github/stars/valeriogalano/pensieriincodice-news-to-linkedin?style=for-the-badge" alt="GitHub Stars"/>
    <img src="https://img.shields.io/github/forks/valeriogalano/pensieriincodice-news-to-linkedin?style=for-the-badge" alt="GitHub Forks"/>
    <img src="https://img.shields.io/github/last-commit/valeriogalano/pensieriincodice-news-to-linkedin?style=for-the-badge" alt="Last Commit"/>
    <a href="https://pensieriincodice.it/sostieni" target="_blank" rel="noopener noreferrer">
      <img src="https://img.shields.io/badge/sostieni-Pensieri_in_codice-fb6400?style=for-the-badge" alt="Sostieni Pensieri in codice"/>
    </a>
  </p>
</div>

---

## Come funziona

Lo script interroga l'API di Readwise per recuperare le ultime news salvate, le formatta tramite un template configurabile e le pubblica sull'account LinkedIn del podcast tramite le API ufficiali.

> **Nota sull'autenticazione:** Le API di LinkedIn non restituiscono un `refresh_token`, quindi per ottenere un nuovo `access_token` è necessaria ogni volta l'interazione manuale dell'utente. L'`access_token` ha validità di 60 giorni.

### Flusso di autenticazione

1. Avvia lo script `auth.py` — viene stampato l'URL di autorizzazione LinkedIn.
2. Apri l'URL nel browser, effettua il login e autorizza l'applicazione.
3. Dopo il redirect, copia l'URL completo dalla barra del browser e incollalo nel terminale.
4. Viene salvato un file `{data_odierna}.json` con `access_token` e `personal_urn`.
5. Lo script aggiorna automaticamente i secrets e la variabile `TOKEN_CREATED_AT` su GitHub (se `GH_CSV` è configurato).

### Monitoraggio scadenza token

Il workflow controlla ad ogni esecuzione la variabile `TOKEN_CREATED_AT` per verificare la scadenza del token (60 giorni):

- **≤10 giorni alla scadenza** → warning nel log della build
- **≤5 giorni alla scadenza** → errore, la build fallisce con messaggio chiaro

Quando si rinnova il token tramite `auth.py`, `TOKEN_CREATED_AT` viene aggiornato automaticamente su tutti i repository configurati in `GH_CSV`.

---

## Requisiti

- Python 3.11+
- Un account LinkedIn con applicazione OAuth configurata
- Un account Readwise con access token

---

## Variabili di ambiente

### Necessarie per l'autenticazione

```
CLIENT_ID="<LinkedIn client ID>"
CLIENT_SECRET="<LinkedIn client secret>"
READWISE_ACCESS_TOKEN="<token di accesso Readwise>"
```

### Opzionali (hanno valori di default)

```
CALLBACK_URL_PORT="8000"
CALLBACK_URL_PROTOCOL="http"
CALLBACK_URL="localhost"
SCOPE="w_member_social openid profile"
```

### Necessarie per la pubblicazione (da impostare nei secrets GitHub)

```
ACCESS_TOKEN="<access token LinkedIn>"
PERSONAL_URN="<personal URN LinkedIn>"
LINKEDIN_MESSAGE_TEMPLATE="{title}\n{notes}\n\n{link}"
```

### Sincronizzazione automatica dei secrets (opzionale)

Imposta `GH_CSV` per sincronizzare automaticamente `ACCESS_TOKEN`, `PERSONAL_URN` e la variabile `TOKEN_CREATED_AT` via API GitHub su tutti i repository configurati. Il formato è CSV con separatore `\n` tra repository:

```
GH_CSV="<owner>,<repo_name>,<github_token>\n<owner>,<repo_name>,<github_token>"
```

### Template del messaggio

La variabile `LINKEDIN_MESSAGE_TEMPLATE` supporta i seguenti placeholder:

| Placeholder | Descrizione |
|---|---|
| `{title}` | Titolo dell'articolo |
| `{notes}` | Note dell'articolo |
| `{link}` | Link all'articolo |

---

## Installazione e avvio

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Avvia il processo di autenticazione
python auth.py
```

Lo script stampa l'URL di autorizzazione LinkedIn. Aprilo nel browser, effettua il login, poi copia l'URL di redirect dalla barra del browser e incollalo nel terminale quando richiesto.

---

## Contributi

Se noti qualche problema o hai suggerimenti, sentiti libero di aprire una **Issue** e successivamente una **Pull Request**. Ogni contributo è ben accetto!

---

## Importante

Vorremmo mantenere questo repository aperto e gratuito per tutti, ma lo scraping del contenuto di questo repository **NON È CONSENTITO**. Se ritieni che questo lavoro ti sia utile e vuoi utilizzare qualche risorsa, ti preghiamo di citare come fonte il podcast e/o questo repository.
