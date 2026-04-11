#Implementazione con un semaforo

import threading

# All'inizio il buffer e' vuoto: semaforo verde.
accedi = threading.Semaphore(1)

# Buffer a singola cella.
buffer = None

# Turno iniziale al produttore: "P" = produttore, "C" = consumatore.
aChiTocca = "P"

class ProduttoreThread(threading.Thread):
	
	def __init__(self):
		super().__init__()
		self.dato = 1

	def run(self):
		global buffer, aChiTocca

		while True:
			accedi.acquire()  # P(accedi)
			if aChiTocca == "P":
				buffer = self.dato
				aChiTocca = "C"
				print(f"[PROD] prodotto {self.dato}")
				self.dato += 1

			accedi.release()  # V(accedi)


class ConsumatoreThread(threading.Thread):
	def __init__(self):
		super().__init__()

	def run(self):
		global buffer, aChiTocca

		while True:
			accedi.acquire()  # P(accedi)

			if aChiTocca == "C":
				dato = buffer
				buffer = None
				aChiTocca = "P"
				print(f"[CONS] consumato {dato}")
				
			accedi.release()  # V(accedi)


def main() -> None:
	t_prod = ProduttoreThread()
	t_cons = ConsumatoreThread()

	t_prod.start()
	t_cons.start()

	print("In esecuzione infinita. Premi Ctrl+C per fermare.")


if __name__ == "__main__":
	main()
