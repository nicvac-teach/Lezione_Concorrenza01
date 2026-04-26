# Implementazione con due semafori (pieno / vuoto)

import threading

# Buffer a singola cella.
buffer = None

# All'inizio il buffer e' vuoto:
# - 'vuoto' = 1 (verde): il produttore puo' scrivere subito.
# - 'pieno' = 0 (rosso): il consumatore deve aspettare.
vuoto = threading.Semaphore(1)
pieno = threading.Semaphore(0)


class ProduttoreThread(threading.Thread):

	def __init__(self):
		super().__init__()
		self.dato = 1

	def run(self):
		global buffer

		while True:
			vuoto.acquire()  # P(vuoto): attendi una cella libera
			buffer = self.dato
			print(f"[PROD] prodotto {self.dato}")
			self.dato += 1
			pieno.release()  # V(pieno): segnala una cella piena


class ConsumatoreThread(threading.Thread):

	def __init__(self):
		super().__init__()

	def run(self):
		global buffer

		while True:
			pieno.acquire()  # P(pieno): attendi una cella piena
			dato = buffer
			buffer = None
			print(f"[CONS] consumato {dato}")
			vuoto.release()  # V(vuoto): segnala una cella libera


def main() -> None:
	t_prod = ProduttoreThread()
	t_cons = ConsumatoreThread()

	t_prod.start()
	t_cons.start()

	print("In esecuzione infinita. Premi Ctrl+C per fermare.")


if __name__ == "__main__":
	main()
