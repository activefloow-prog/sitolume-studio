# Luca — Riferimenti Reels esistenti di Sito Lume

Data verifica: 2026-11-11. Fonte: account Instagram collegato via Windsor.ai, profilo **@sitolume_studio** (ID 17841470620093368). L'indirizzo **@sito_lume** non risultava disponibile al momento della verifica, quindi non sono stati attribuiti contenuti a quel diverso handle.

## Reel del profilo da prendere come riferimento

1. Reel [DfYEkb5t3Mq](https://www.instagram.com/reel/DfYEkb5t3Mq/), pubblicato il 5 novembre 2026 ore 22:09 UTC. Titolo dal testo del post: *«Seguimi dietro le quinte: un'idea diventa un sito, un passo alla volta.»* Tema: backstage, sviluppo di un'idea in prodotto web e racconto dei processi.
2. Reel [DfZqXATocv0](https://www.instagram.com/reel/DfZqXATocv0/), pubblicato il 6 novembre 2026 ore 12:59 UTC. Caption non presente nei dati API. Video presente e URL Instagram verificato.

Questi sono riferimenti editoriali della stessa attività, **non una prova di avere analizzato ogni fotogramma dei video**. Non copiarli in modo seriale: mantenere brand, contenuto originale e coerenza narrativa; evitare di spacciarli per portfolio esterno o testimonianze.

## Requisiti non negoziabili

- **Presenter**: avatar realistico sintetico con movimenti espressivi e bocca che pronunci le parole della voce, non statico e non un'immagine con zoom.
- **Voci**: Ryan maschile e Serena femminile Qwen3-TTS italiano, già renderizzate nel cloud.
- **Motore lipsync**: MuseTalk 1.5 reale, con audio condizionato; test della coppia video+voce e verifica visiva prima di promozione/Instagram. La qualità non può essere dichiarata conclusa solo con ffprobe.
- **Movimento del corpo**: generato/ripreso da un video sorgente realmente animato e autorizzato, o mediante un ulteriore modello di motion synthesis realmente funzionante. MuseTalk modifica la bocca, NON genera da solo la gestualità dell'intero corpo.
- **Montaggio**: ritmo dinamico coerente con i Reel Sito Lume, nero-oro, titoli leggibili, stacchi, sottotitoli sincronizzati, invito a visitare il sito; senza promesse di performance/viralità.
- **Infrastruttura**: rendering su runner cloud gratuito, nessun modello o video di lavoro sul Mac; nessuna GPU a pagamento né nuovi account.
- **Pubblicazione**: NON consentita finché il Reel completo non è verificato e approvato. @sitolume_studio connesso a Windsor.ai per pubblicazioni; DM non disponibili.
- Se il test MuseTalk fallisce, segnare `lipsync_unverified` e non sostituirlo silenziosamente con slideshow/zoom.

## Stato

Pilota GitHub Actions: [Luca Real Lip Sync MuseTalk CPU Pilot](https://github.com/activefloow-prog/sitolume-studio/actions/workflows/luca-musetalk-cpu-pilot.yml). Le prove precedenti sono **soltanto motion editing**, non lipsync.
