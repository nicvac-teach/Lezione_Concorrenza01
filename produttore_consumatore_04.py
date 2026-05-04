# Implementazione con N produttori e M consumatori

import threading

DIM_BUFFER = 5
N_PRODUTTORI = 2
N_CONSUMATORI = 2

# Buffer circolare con DIM_BUFFER celle.
buffer = [None] * DIM_BUFFER

# Indici (puntatori) sul buffer circolare: ora condivisi da piu' produttori
# (metti) e da piu' consumatori (togli).
metti = 0
togli = 0

# Semafori generalizzati per il numero di celle libere/piene.
vuoto = threading.Semaphore(DIM_BUFFER)
pieno = threading.Semaphore(0)

# Mutex per serializzare l'accesso a 'metti' tra produttori e a 'togli' tra
# consumatori.
mutexP = threading.Semaphore(1)
mutexC = threading.Semaphore(1)


class ProduttoreThread(threading.Thread):

	def __init__(self, idx):
		super().__init__()
		self.idx = idx
		# Ogni produttore parte da un valore distinto, cosi' nei log si vede
		# subito chi ha prodotto cosa: P1 -> 1,2,3..., P2 -> 101,102,103...
		self.dato = idx * 100 + 1

	def run(self):
		global metti

		while True:
			vuoto.acquire()        # P(vuoto): attendi una cella libera
			mutexP.acquire()       # P(mutexP): mutua esclusione tra produttori
			i_metti = metti
			metti = (metti + 1) % DIM_BUFFER
			mutexP.release()       # V(mutexP): rilascia la regione critica

			# Scrittura nel buffer FUORI dalla regione critica:
			# altri produttori possono "depositare" in parallelo nelle loro celle.
			buffer[i_metti] = self.dato
			print(f"[PROD-{self.idx}] prodotto {self.dato} in buffer[{i_metti}]")
			self.dato += 1

			pieno.release()        # V(pieno): segnala una cella piena


class ConsumatoreThread(threading.Thread):

	def __init__(self, idx):
		super().__init__()
		self.idx = idx

	def run(self):
		global togli

		while True:
			pieno.acquire()        # P(pieno): attendi una cella piena
			mutexC.acquire()       # P(mutexC): mutua esclusione tra consumatori
			i_togli = togli
			togli = (togli + 1) % DIM_BUFFER
			mutexC.release()       # V(mutexC): rilascia la regione critica

			# Lettura dal buffer FUORI dalla regione critica.
			dato = buffer[i_togli]
			print(f"[CONS-{self.idx}] consumato {dato} da buffer[{i_togli}]")

			vuoto.release()        # V(vuoto): segnala una cella libera


def main() -> None:
	produttori = [ProduttoreThread(i + 1) for i in range(N_PRODUTTORI)]
	consumatori = [ConsumatoreThread(i + 1) for i in range(N_CONSUMATORI)]

	for p in produttori:
		p.start()
	for c in consumatori:
		c.start()

	print(
		f"In esecuzione infinita ({N_PRODUTTORI} produttori, "
		f"{N_CONSUMATORI} consumatori, DIM_BUFFER={DIM_BUFFER}). "
		"Premi Ctrl+C per fermare."
	)


if __name__ == "__main__":
	main()
