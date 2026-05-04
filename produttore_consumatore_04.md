# Produttori-Consumatori — N produttori e M consumatori

Riferimento: libro, pagine **168-169**.

## Limite della soluzione precedente

Le [soluzioni precedenti](produttore_consumatore_03.md) considerano un solo produttore e un solo consumatore. Estendendo lo schema al caso generale di **n produttori** e **m consumatori** emergono nuove problematiche di sincronizzazione.

I semafori `vuoto` e `pieno` continuano a sincronizzare correttamente la coppia produttori-consumatori (un produttore si sospende se non c'è una cella libera, un consumatore se non c'è un dato pronto). Ma c'è un secondo livello di sincronizzazione che prima non esisteva: i puntatori `metti` e `togli` non sono più variabili "private" del singolo produttore o consumatore — diventano **risorse condivise** rispettivamente tra tutti i produttori e tra tutti i consumatori.

Se due produttori entrano contemporaneamente nella sezione critica per aggiornare `metti`:

```
metti = (metti + 1) % DIM_BUFFER;
```

molto probabilmente:

- scriveranno nella **stessa cella** (entrambi hanno letto lo stesso valore di `metti`);
- aggiorneranno `metti` in modo errato (race condition sull'incremento).

Lo stesso problema si presenta per `togli` tra più consumatori, che potrebbero leggere lo stesso dato due volte.

## La soluzione: mutex sui puntatori

Si introduce un nuovo semaforo binario per ciascun gruppo:

- `mutexP = 1`: serializza l'accesso a `metti` tra i produttori;
- `mutexC = 1`: serializza l'accesso a `togli` tra i consumatori.

L'idea chiave è **separare** la sezione critica (lettura+aggiornamento dell'indice) dalla scrittura/lettura effettiva sul buffer:

- la sezione critica protetta da `mutexP`/`mutexC` contiene solo l'aggiornamento dell'indice;
- la scrittura/lettura del buffer avviene **fuori** dalla regione critica, su una cella ormai "prenotata" tramite la variabile locale `tempo`.

In questo modo più produttori (e più consumatori) possono lavorare **in parallelo** sul buffer, ognuno sulla propria cella.

## Pseudocodice

```
semaphore vuoto  = DIM_BUFFER     // posti liberi nel buffer
semaphore pieno  = 0              // dati pronti nel buffer
semaphore mutexP = 1              // mutex tra produttori
semaphore mutexC = 1              // mutex tra consumatori
buffer array[DIM_BUFFER]

Processo produci(int dato)
int i_metti;
inizio
  P(vuoto)                        // attendi una cella libera
    P(mutexP)                     // entra nella RC dei produttori
      i_metti = metti             // "prenota" la cella
      metti = (metti + 1) % DIM_BUFFER;
    V(mutexP)                     // esci dalla RC
    buffer[i_metti] = dato        // deposito (fuori dalla RC)
  V(pieno)                        // segnala dato pronto
fine

Processo consuma()
int i_togli;
inizio
  P(pieno)                        // attendi un dato pronto
    P(mutexC)                     // entra nella RC dei consumatori
      i_togli = togli             // "prenota" la cella
      togli = (togli + 1) % DIM_BUFFER;
    V(mutexC)                     // esci dalla RC
    <consuma buffer[i_togli]>     // prelievo (fuori dalla RC)
  V(vuoto)                        // segnala cella libera
fine
```

## Perché il deposito è fuori dalla regione critica

È fondamentale **non** racchiudere l'operazione di scrittura/lettura del buffer dentro al mutex. Se lo facessimo, e la scrittura nel buffer fosse lenta (ad esempio per dati grandi o operazioni di I/O):

- tutti gli altri produttori rimarrebbero bloccati su `P(mutexP)` anche in presenza di posti liberi nel buffer;
- di conseguenza i consumatori si fermerebbero, non avendo nulla da consumare;
- si distruggerebbe il **parallelismo** che il buffer circolare aveva appena introdotto.

La regione critica si limita quindi all'**unica** operazione che richiede esclusività: l'aggiornamento atomico di `metti` (o `togli`). Una volta "prenotato" l'indice salvandolo in `i_metti` (o `i_togli`), ogni produttore può scrivere nella propria cella in parallelo agli altri.

## File del progetto

- `produttore_consumatore_04.html`: animazione passo-passo con 2 produttori e 2 consumatori.
- `produttore_consumatore_04.py`: implementazione Python con `N_PRODUTTORI` e `N_CONSUMATORI` thread.
