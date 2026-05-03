# Implementazione con buffer circolare e semafori generalizzati

import threading

DIM_BUFFER = 3

# Buffer circolare con DIM_BUFFER celle.
buffer = [None] * DIM_BUFFER

# Indici (puntatori) sul buffer circolare.
metti = 0  # prossima posizione libera (dove inserire)
togli = 0  # prossima posizione piena (da cui prelevare)

# Semafori generalizzati (counting):
# - 'vuoto' = DIM_BUFFER: all'inizio tutte le celle sono libere.
# - 'pieno' = 0: nessun dato ancora prodotto.
vuoto = threading.Semaphore(DIM_BUFFER)
pieno = threading.Semaphore(0)


class ProduttoreThread(threading.Thread):

	def __init__(self):
		super().__init__()
		self.dato = 1

	def run(self):
		global metti

		while True:
			vuoto.acquire()  # P(vuoto): attendi una cella libera
			buffer[metti] = self.dato
			print(f"[PROD] prodotto {self.dato} in buffer[{metti}]")
			metti = (metti + 1) % DIM_BUFFER
			self.dato += 1
			pieno.release()  # V(pieno): segnala una cella piena


class ConsumatoreThread(threading.Thread):

	def __init__(self):
		super().__init__()

	def run(self):
		global togli

		while True:
			pieno.acquire()  # P(pieno): attendi una cella piena
			dato = buffer[togli]
			print(f"[CONS] consumato {dato} da buffer[{togli}]")
			togli = (togli + 1) % DIM_BUFFER
			vuoto.release()  # V(vuoto): segnala una cella libera


def main() -> None:
	t_prod = ProduttoreThread()
	t_cons = ConsumatoreThread()

	t_prod.start()
	t_cons.start()

	print(f"In esecuzione infinita (DIM_BUFFER={DIM_BUFFER}). Premi Ctrl+C per fermare.")


if __name__ == "__main__":
	main()
