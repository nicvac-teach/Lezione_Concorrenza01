# Esercizio 2 — Bacheca messaggi

Un sistema di messaggistica interna permette agli utenti di inviare messaggi testuali a una bacheca condivisa. Dei thread "ricevitori" leggono i messaggi digitati dall'utente dalla tastiera e li inserisce in un buffer circolare; Altri thread "visualizzatori" prelevano i messaggi dal buffer e li stampano a schermo con l'ora corrente. 
Ogni ricevitore termina quando riceve il messaggio `X` (maiuscolo). 
Ogni visualizzatore termina il suo lavoro quando riceve il messaggio None.
Dopo che tutti i ricevitori hanno terminato il loro lavoro, il main invia un messaggio sentinella (None) per ogni consumatore attivo, in modo che possano terminare ordinatamente.

## Parametri

| Parametro | Valore |
|---|---|
| `DIM_BUFFER` | 4 |
| `N_PRODUTTORI` (thread di input) | 3 |
| `N_CONSUMATORI` (visualizzatori) | 4 |

## Cosa devi implementare

Il file di partenza contiene già il `main` completo e la funzione `timestamp()`. Devi implementare solo le due classi thread.

### `ProduttoreThread`

Ogni thread di input deve:

1. Leggere un messaggio dalla tastiera con `input()` in un loop.
2. Se il messaggio è `"X"`, uscire dal loop (senza inserirlo nel buffer).
3. Per ogni messaggio valido, usare il protocollo con `vuoto`, `mutexP`, `i_metti`, `pieno`.
4. Stampare `[INPUT-N] inserito: <messaggio>` dopo aver scritto nel buffer.

### `ConsumatoreThread`

Ogni visualizzatore deve:

1. Girare in loop indefinito, prelevando un messaggio alla volta con il protocollo `pieno`, `mutexC`, `i_togli`, `vuoto`.
2. Se il messaggio prelevato è `None`, uscire dal loop (sentinella di terminazione).
3. Stampare `[VIEWER-N] <timestamp> >> <messaggio>`.

## Codice di partenza

```python
import threading
import datetime

DIM_BUFFER = 4
N_PRODUTTORI = 3
N_CONSUMATORI = 4

buffer = [None] * DIM_BUFFER
metti = 0
togli = 0

vuoto = threading.Semaphore(DIM_BUFFER)
pieno = threading.Semaphore(0)
mutexP = threading.Semaphore(1)
mutexC = threading.Semaphore(1)


def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")


class ProduttoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    # DA IMPLEMENTARE (run)


class ConsumatoreThread(threading.Thread):
    # DA IMPLEMENTARE
    pass


def main():
    global metti

    consumatori = [ConsumatoreThread(i + 1) for i in range(N_CONSUMATORI)]
    produttori = [ProduttoreThread(i + 1) for i in range(N_PRODUTTORI)]

    for c in consumatori:
        c.start()
    for p in produttori:
        p.start()

    # Aspetta che tutti i produttori abbiano terminato (ogni utente ha digitato X).
    for p in produttori:
        p.join()

    print("Input terminato. Chiusura visualizzatori...")

    # Invia una sentinella None per ogni visualizzatore.
    for _ in range(N_CONSUMATORI):
        vuoto.acquire()
        buffer[metti] = None
        metti = (metti + 1) % DIM_BUFFER
        pieno.release()

    for c in consumatori:
        c.join()

    print("Bacheca chiusa.")


if __name__ == "__main__":
    main()
```
