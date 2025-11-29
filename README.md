<div align="center">
  <img src="https://cdn.pensieriincodice.it/images/pensieriincodice-locandina.png" alt="Logo Progetto" width="150"/>
  <h1>Pensieri In Codice - News to LinkedIn</h1>
  <p>
    Il progetto ha lo scopo di pubblicare le news di PIC sull'account Linkedin del podcast.
  </p><p>    
    Le news vengono prelevate da Readwise.
  </p>
  
  <p>
    <img src="https://img.shields.io/github/stars/valeriogalano/pensieriincodice-news-to-linkedin?style=for-the-badge" alt="GitHub Stars"/>
    <img src="https://img.shields.io/github/forks/valeriogalano/pensieriincodice-news-to-linkedin?style=for-the-badge" alt="GitHub Forks"/>
    <img src="https://img.shields.io/github/last-commit/valeriogalano/pensieriincodice-news-to-linkedin?style=for-the-badge" alt="Last Commit"/>
    <a href="https://pensieriincodice.it/sostieni" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/sostieni-Pensieri_in_codice-fb6400?style=for-the-badge" alt="Sostieni Pensieri in codice"></a>
 </p>
</div>

---

## Flusso di funzionamento

## Autenticazione

Purtroppo le API di Linkedin non restituiscono un `refresh_token` e per ottenere ogni volta un `access_token`
c'è bisogno dell'interazione utente che inserisca manualmente i dati di accesso.

L'`access_token` ha validità 60 giorni.


### Flusso

![flusso di autenticazione](assets/sequence_auth.jpg)

Per l'autenticazione è necessario avviare lo script `auth.py`.

Verrà aperta una finestra del browser dove chiederà all'utente di inserire username e password dell'account Linkedin.

Una volta che l'utente ha effettuato il login, il browser si chiuderà automaticamente
e verrà memorizzato in un file json denominato `{today_date}.json` 
(ad es. `2024-10-04.json`) l'`access_token` e il `personal_urn` (id) dell'utente.

Queste informazioni dovranno essere aggiornate nei secrets di github per poter far funzionare l'automazione.


## Installazione in locale


### Variabili di ambiente

Nel file `.env.example` ci sono le variabili di ambiente che devi compilare per completare l'autenticazione,
puoi impostarle nel tuo IDE o nel sistema operativo in esecuzione.

Le variabili necessarie l'autenticazione sono 3:

```
CLIENT_ID="<LINKEDIN_CLIENT_ID_HERE>"
CLIENT_SECRET="<LINKEDIN_CLIENT_SECRET_HERE>"
READWISE_ACCESS_TOKEN="<READWISE_ACCESS_TOKEN_HERE>"
```

Le seguenti variabili sono opzionali perchè hanno nel codice un valore di default: 

```
CALLBACK_URL_PORT="8000"
CALLBACK_URL_PROTOCOL="http"
CALLBACK_URL="localhost"
SCOPE="w_member_social openid profile"
```

Mentre le seguenti variabili:

```
ACCESS_TOKEN=<ACCESS_TOKEN_HERE>
PERSONAL_URN=<PERSONAL_URN_HERE>
LINKEDIN_MESSAGE_TEMPLATE="{title}\n{notes}\n\n{link}"
```

sono da inserire solo sul repo per consentire alla action di github di eseguire la pubblicazione.

Infine se vuoi che lo script di autenticazione sincronizzi automaticamente via API il 
tuo `access_token` ed il tuo `personal_urn` senza che tu debba farlo manualmente ti basta inserire la 
variabile di ambiente `GH_CSV`.

Nella variabile `GH_CSV` devi inserire sotto forma di CSV le seguenti informazioni:
- proprietario del repository
- nome del repository
- token (puoi generare un token di GitHub seguendo questa procedura: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

Puoi inserire più repository inserendo il separatore `\n` dopo ogni repository, ad es.

```
GH_CSV="<owner>,<repo_name>,<token>\n<owner>,<repo_name>,<token>"
```


### Installazione dei requirements

Per installare le dipendenze di progetto lancia il seguente comando:

```bash
pip install -r requirements.txt
```


### Avvia il processo di autenticazione

Per avviare il processo di autenticazione:

```bash
python auth.py
```

Inserisci le credenziali Linkedin nel browser che ti apparirà e attendi la chiusura del browser.

---

## Contributi

Se noti qualche problema o hai suggerimenti per migliorare l'organizzazione, sentiti libero di aprire una **Issue**
e successivamente una **Pull Request**. Ogni contributo è ben accetto!

---

## Importante

Vorremmo mantenere questo repository aperto e gratuito per tutti,
ma lo scraping del contenuto di questo repository NON È CONSENTITO.
Se ritieni che questo lavoro ti sia utile e vuoi utilizzare qualche risorsa,
ti preghiamo di citare come fonte il podcast e/o questo repository.

---

<div align="center">
  <p>
    Realizzato con ❤️ da <strong>Valerio Galano</strong>
  </p>
  <p>
    <a href="https://valeriogalano.it/">Sito Web</a> | 
    <a href="https://daredevel.com/">Blog</a> | 
    <a href="https://pensieriincodice.it/">Podcast</a>
  </p>
</div>