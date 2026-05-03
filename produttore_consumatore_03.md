# Produttori-Consumatori — buffer circolare e semafori generalizzati

Riferimento: libro, pagine **167-168**.

## Limite della soluzione precedente

La [soluzione con due semafori binari](produttore_consumatore_02.md) usa un buffer di **una sola cella** e impone un'alternanza rigida 1↔1: il produttore scrive il secondo dato **solo dopo** che il consumatore ha prelevato il primo. Se i due processi lavorano a velocità diverse il più veloce è continuamente costretto ad aspettare il più lento — il buffer non riesce ad assorbire le differenze di ritmo.

Per disaccoppiare produttore e consumatore si introduce un **buffer circolare** di `DIM_BUFFER` celle, gestito come una coda FIFO.

## Buffer circolare

La memoria condivisa è un array di lunghezza `DIM_BUFFER` con due indici:

- `metti`: prossima posizione **libera** in cui il produttore inserirà;
- `togli`: prossima posizione **piena** da cui il consumatore preleverà.

Inizialmente `metti = togli = 0`. Entrambi gli indici si spostano in modo ciclico tramite l'operatore modulo (`%`), realizzando la coda circolare:

```
metti = (metti + 1) % DIM_BUFFER
togli = (togli + 1) % DIM_BUFFER
```

```
        ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
buffer  │  │  │XX│XX│XX│  │  │  │  │  │
        └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
              ↑        ↑
            togli    metti
```

## Semafori generalizzati

Con un buffer di più celle ogni cella diventa una **risorsa** a sé: siamo in presenza di **risorse a molteplicità > 1**. I semafori binari della soluzione precedente non sono più sufficienti — se li usassimo qui, il produttore potrebbe inserire il secondo dato solo dopo che il consumatore ha prelevato il primo, **rendendo di fatto inutile il buffer circolare**.

Servono allora **semafori generalizzati** (o *counting*), che tengono il conteggio del numero corrente di celle libere e di celle piene:

- `vuoto = DIM_BUFFER`: all'inizio tutte le celle sono libere;
- `pieno = 0`: nessun dato ancora prodotto.

Così:

- il produttore può inserire fino a `DIM_BUFFER` dati di seguito senza che nessuno venga consumato (se il consumatore è momentaneamente più lento);
- il semaforo `pieno` "ricorda" quanti nuovi dati attendono il consumatore.

## Pseudocodice

```
semaphore vuoto = DIM_BUFFER       // all'inizio il buffer ha posti liberi
semaphore pieno = 0                // dati da leggere presenti nel buffer
buffer array[DIM_BUFFER]

Processo produci(int dato)
inizio
  P(vuoto)                         // quando il buffer ha almeno una cella libera
  buffer[metti] = dato;
  metti = (metti + 1) % DIM_BUFFER;
  V(pieno)                         // segnala che c'è un nuovo dato
fine

Processo consuma()
inizio
  P(pieno)                         // quando il buffer ha almeno un dato
  <consuma il dato>
  togli = (togli + 1) % DIM_BUFFER;
  V(vuoto)                         // segnala una cella libera
fine
```

Il produttore si blocca solo se il buffer è completamente pieno (`vuoto = 0`); il consumatore si blocca solo se è completamente vuoto (`pieno = 0`). Tra questi due estremi i due processi procedono in parallelo, regolati esclusivamente dai contatori dei due semafori.

## File del progetto

- `produttore_consumatore_03.html`: animazione passo-passo del buffer circolare (con `DIM_BUFFER = 3`).
- `produttore_consumatore_03.py`: implementazione Python.
