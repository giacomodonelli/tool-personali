# tool-personali

Piccoli strumenti web, pensati per l'iPhone: nessuna installazione da App Store, si aprono in Safari e si possono aggiungere alla schermata Home.

## Livella (`livella/`)

Una livella a bolla che usa i sensori di movimento del telefono.

- **Piano** – bolla circolare per superfici orizzontali (tavoli, mensole, elettrodomestici), con gli scarti sinistra/destra e avanti/indietro in gradi.
- **Muro** – appoggiando il telefono di taglio o contro una parete misura lo scostamento dalla verticale e indica di quanto ruotare (utile per quadri e mensole).
- **Auto** – passa da una modalità all'altra da sola, in base a come tieni il telefono.
- **Azzera** – imposta la posizione attuale come zero, per compensare un piano non perfetto o l'imprecisione del sensore. La calibrazione resta salvata; un secondo tocco la rimuove.
- **Blocca** – congela la lettura quando non riesci a vedere lo schermo (ad esempio sotto un pensile).
- **Suono** – bip quando arriva in bolla.
- Lo schermo resta acceso mentre l'app è aperta, e dopo la prima apertura funziona anche **offline**.

Tolleranza "in bolla": 0,5°. Fondo scala della bolla: 10°.

### Come usarla sull'iPhone

1. Pubblica la cartella su **GitHub Pages**: nel repository → *Settings* → *Pages* → *Source: Deploy from a branch*, scegli il branch e la cartella `/ (root)`, poi *Save*.
2. Dopo un minuto la pagina è su `https://<tuo-utente>.github.io/tool-personali/livella/`.
3. Apri quel link **in Safari sull'iPhone** e tocca *Attiva sensori* (iOS chiede il permesso "Movimento e orientamento": è obbligatorio e va concesso con un tocco).
4. Menu Condividi → **Aggiungi a Home**: da lì in poi si apre a tutto schermo come una normale app.

> L'accesso ai sensori funziona solo su **HTTPS** (GitHub Pages va bene) o su `localhost`; aprendo il file con `file://` iOS non fornisce i dati.
> Se il permesso è stato negato per errore: *Impostazioni → App → Safari → Movimento e orientamento*, attiva e ricarica.

### Precisione

I sensori dell'iPhone hanno un piccolo errore di zero che varia da esemplare a esemplare. Per una misura seria:
appoggia il telefono sulla superficie, premi **Azzera**, poi ruotalo di 180° e rileggi: il valore dovrebbe essere
speculare. Metà della differenza è l'errore residuo. Per lavori di precisione resta meglio una livella vera.

### Provarla dal computer

```bash
python3 -m http.server 8000
# poi apri http://localhost:8000/livella/
```

Da desktop i sensori non esistono, quindi la bolla resta ferma al centro: serve solo a controllare la grafica.
