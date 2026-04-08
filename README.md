<div align="center">
  <img src="https://cdn.pensieriincodice.it/images/pensieriincodice-locandina.png" alt="Logo Progetto" width="150"/>
  <h1>Pensieri In Codice — News to LinkedIn</h1>
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

1. Avvia lo script `auth.py` — verrà aperto un browser per il login LinkedIn.
2. Dopo il login, il browser si chiude automaticamente e viene salvato un file `{data_odierna}.json` con `access_token` e `personal_urn`.
3. Aggiorna i secrets di GitHub con i valori ottenuti.

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

Imposta `GH_CSV` per sincronizzare automaticamente `access_token` e `personal_urn` via API GitHub senza intervento manuale. Il formato è CSV con separatore `\n` tra repository:

```
GH_CSV="<owner>,<repo_name>,<token>\n<owner>,<repo_name>,<token>"
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
pip install -r requirements.txt

# Avvia il processo di autenticazione
python auth.py
```

Inserisci le credenziali LinkedIn nel browser che apparirà e attendi la chiusura automatica.

---

## Contributi

Se noti qualche problema o hai suggerimenti, sentiti libero di aprire una **Issue** e successivamente una **Pull Request**. Ogni contributo è ben accetto!

---

## Importante

Vorremmo mantenere questo repository aperto e gratuito per tutti, ma lo scraping del contenuto di questo repository **NON È CONSENTITO**. Se ritieni che questo lavoro ti sia utile e vuoi utilizzare qualche risorsa, ti preghiamo di citare come fonte il podcast e/o questo repository.