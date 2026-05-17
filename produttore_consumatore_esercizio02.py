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
        self.dato = ""

    def run(self):
        global metti

        while self.dato != "X":

            print(f"[PROD-{self.idx}] digita messaggio: ")
            self.dato = input()
            if self.dato == "X": 
                print(f"[PROD-{self.idx}] Ricevuto messaggio di terminazione.")
                continue

            vuoto.acquire()
            mutexP.acquire()
            i_metti = metti
            metti = (metti + 1) % DIM_BUFFER
            mutexP.release()

            buffer[i_metti] = self.dato
            print(f"[PROD-{self.idx}] prodotto [{self.dato}] in buffer[{i_metti}]")

            pieno.release()


class ConsumatoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    def run(self):
        global togli

        esci = False
        while not esci:
            pieno.acquire()
            mutexC.acquire()
            i_togli = togli
            togli = (togli + 1) % DIM_BUFFER
            mutexC.release()

            dato = buffer[i_togli]

            if dato != None:
                print(f"[CONS-{self.idx}] consumato [{dato}] da buffer[{i_togli}]")
            else:
                print(f"[CONS-{self.idx}] Ricevuto messaggio di uscita da buffer[{i_togli}]")
                esci = True

            vuoto.release()


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
