# Esercizio 1 — Centralino telefonico

Un call center riceve chiamate da clienti e le smista agli operatori. Ogni chiamata viene messa in una coda (buffer circolare); gli operatori la prelevano e la gestiscono.

## Parametri

| Parametro | Valore |
|---|---|
| `DIM_BUFFER` | 6 |
| `N_PRODUTTORI` (linee in entrata) | 3 |
| `N_CONSUMATORI` (operatori) | 2 |
| Chiamate per linea | 5 |

Ogni chiamata è una stringa con numero cliente generato casualmente, ad esempio `"333-4827163"`. La funzione `genera_numero()` è già fornita nel codice base.

## Cosa devi implementare

Il file di partenza contiene già il `main` completo e la funzione `genera_numero()`. Devi implementare solo le due classi thread.

### `ProduttoreThread`

Ogni linea (produttore) deve:

1. Generare esattamente `N_CHIAMATE` chiamate, poi terminare.
2. Per ogni chiamata, usare il protocollo con `vuoto`, `mutexP`, `i_metti`, `pieno` che hai studiato.
3. Stampare `[LINEA-N] ricevuta chiamata <numero>` dopo aver scritto nel buffer.

### `ConsumatoreThread`

Ogni operatore (consumatore) deve:

1. Girare in loop indefinito, prelevando una chiamata alla volta con il protocollo `pieno`, `mutexC`, `i_togli`, `vuoto`.
2. Se la chiamata prelevata è `None`, uscire dal loop (è il segnale di terminazione inviato dal `main`).
3. Stampare `[OP-N] risponde a <numero>`.

## Codice di partenza

```python
import threading
import random

DIM_BUFFER = 6
N_PRODUTTORI = 3
N_CONSUMATORI = 2
N_CHIAMATE = 5

buffer = [None] * DIM_BUFFER
metti = 0
togli = 0

vuoto = threading.Semaphore(DIM_BUFFER)
pieno = threading.Semaphore(0)
mutexP = threading.Semaphore(1)
mutexC = threading.Semaphore(1)


def genera_numero():
    return f"333-{random.randint(1000000, 9999999)}"


class ProduttoreThread(threading.Thread):
    # DA IMPLEMENTARE
    pass


class ConsumatoreThread(threading.Thread):
    # DA IMPLEMENTARE
    pass


def main():
    global metti # global anche in ProduttoreThread...

    produttori = [ProduttoreThread(i + 1) for i in range(N_PRODUTTORI)]
    consumatori = [ConsumatoreThread(i + 1) for i in range(N_CONSUMATORI)]

    # Avvia prima i consumatori, così sono pronti a ricevere chiamate
    # non appena le linee iniziano a produrre.
    for c in consumatori:
        c.start()
    for p in produttori:
        p.start()

    # Aspetta che tutte le linee abbiano terminato (ognuna ha prodotto
    # N_CHIAMATE messaggi ed è uscita dal loop).
    for p in produttori:
        p.join()

    print("Tutte le linee hanno terminato. Chiusura operatori...")

    # Invia una sentinella None per ogni operatore. Quando un operatore
    # preleva None, sa che deve terminare. Il main è l'unico thread
    # ancora attivo a scrivere nel buffer, quindi non serve mutexP.
    for _ in range(N_CONSUMATORI):
        vuoto.acquire()
        buffer[metti] = None
        metti = (metti + 1) % DIM_BUFFER
        pieno.release()

    # Aspetta che tutti gli operatori abbiano terminato prima di uscire.
    for c in consumatori:
        c.join()

    print("Centralino chiuso.")


if __name__ == "__main__":
    main()
```
