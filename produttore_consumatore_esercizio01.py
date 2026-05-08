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
    def __init__(self, idx):
        super().__init__()
        self.idx = idx
        # Ogni produttore parte da un valore distinto, cosi' nei log si vede
        # subito chi ha prodotto cosa: P1 -> 1,2,3..., P2 -> 101,102,103...
        self.dato = genera_numero()

    def run(self):
        global metti

        #Termino quando genero N_CHIAMATE
        chiamateGenerate = 0

        while chiamateGenerate < N_CHIAMATE:
            vuoto.acquire()        # P(vuoto): attendi una cella libera
            mutexP.acquire()       # P(mutexP): mutua esclusione tra produttori
            i_metti = metti
            metti = (metti + 1) % DIM_BUFFER
            mutexP.release()       # V(mutexP): rilascia la regione critica

            # Scrittura nel buffer FUORI dalla regione critica:
            # altri produttori possono "depositare" in parallelo nelle loro celle.
            buffer[i_metti] = self.dato
            chiamateGenerate += 1
            print(f"[LINEA-{self.idx}] ricevuta chiamata {self.dato}, inserita in buffer[{i_metti}]")
            self.dato = genera_numero()

            pieno.release()        # V(pieno): segnala una cella piena


class ConsumatoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    def run(self):
        global togli

        #Rimango in esecuzione finchè non ricevo il messaggio 'None'
        termina = False
        while not(termina):
            pieno.acquire()        # P(pieno): attendi una cella piena
            mutexC.acquire()       # P(mutexC): mutua esclusione tra consumatori
            i_togli = togli
            togli = (togli + 1) % DIM_BUFFER
            mutexC.release()       # V(mutexC): rilascia la regione critica

            # Lettura dal buffer FUORI dalla regione critica.
            dato = buffer[i_togli]
            if dato == None:
                termina = True
            else:
                print(f"[OP-{self.idx}] risponde al numero {dato} da buffer[{i_togli}]")

            vuoto.release()        # V(vuoto): segnala una cella libera


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