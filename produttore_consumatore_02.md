# Produttori-Consumatori — soluzione con due semafori

Riferimento: libro, pagine **166-167**.

## Limiti della soluzione precedente

La [soluzione con un solo semaforo](produttore_consumatore_01.md) usa un semaforo unico più una variabile di turno (`aChiTocca`).
Garantisce la mutua esclusione, ma **non risolve il problema del buffer underflow**: il consumatore acquisisce comunque il semaforo e **tenta la lettura del buffer anche quando è vuoto**, scoprendo solo dopo (controllando `aChiTocca`) che non c'è nulla da consumare e dovendo riprovare. Specularmente, il produttore tenta la scrittura anche quando il buffer è ancora pieno.

Il risultato è un'attesa attiva (*busy-waiting*): tutti i processi vengono risvegliati per "controllare se tocca a loro", sprecando tempo di CPU e introducendo ritardi non necessari nell'accesso alla sezione critica. Questo viola il terzo requisito di Dijkstra: *un processo fuori dalla sezione critica non deve ritardare l'ingresso di un altro processo*.

## La soluzione: due semafori

Si usano **due semafori** che descrivono direttamente lo stato del buffer:

- `pieno` (inizialmente **0**, *rosso*): segnala la presenza di un dato pronto da consumare.
- `vuoto` (inizialmente **1**, *verde*): segnala la disponibilità di una cella libera da riempire.

Il produttore aspetta una cella vuota e poi segnala che è piena.
Il consumatore aspetta una cella piena e poi segnala che è vuota.

```
semaphore pieno = 0
semaphore vuoto = 1

int buffer;

Processo produci(int dato)        Processo consuma()
inizio                            inizio
  P(vuoto)                          P(pieno)
  buffer = dato                     <consuma il dato>
  V(pieno)                          V(vuoto)
fine                              fine
```

In questo modo:

- il produttore risveglia **solo il consumatore**;
- il consumatore risveglia **solo il produttore**.

Niente più busy-waiting né variabile di turno: l'alternanza tra produttore e consumatore è imposta direttamente dai due semafori, e ogni processo si blocca esattamente fino al momento in cui può effettivamente operare sul buffer.

## File del progetto

- `produttore_consumatore_02.html`: animazione passo-passo della soluzione.
- `produttore_consumatore_02.py`: implementazione Python.
