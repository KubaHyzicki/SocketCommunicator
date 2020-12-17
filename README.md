Komunikator z szyfrowaniem bazujący na protokole Diffie-Hellman.

Komunikator tekstowy umożliwia jednoczesną obustronną komunikację serwer < - > klient. Obsługuje wielu klientów na danej kieszeni obsługiwanej przez moduł serwera
osługuje wielu klientów na danej kieszeni obsługiwanej przez moduł serwera i umożliwia jednoczesną obustronną komunikację serwer < - > klient.

Wybrany język: python3 - ze względu na własną znajomość języka, łatwość jego testowania oraz jego szerokie zastosowanie w poruszaniu się w systemach operacyjnych i korzystaniu z ich funkcji. Język ten świetnie nadaje się do prostych małych aplikacji, zachowując tym samym potencjał skalowalności
Wybrana biblioteka: socket - standardowa biblioteka pythonowa do obsługi socket'ów dostępna na większości obecnie rozpowszechnionych systemów(w tym Linux, Windows, MacOS)

Sposób uruchomienia:
	Serwer: python3 server.py
	Klient: python3 client.py start_chat
Dodatkowe argumenty opisane pod flagą --help

Projekt składa się z dwóch głównych interfejsów wiersza poleceń:
	server.py - Interfejs serweru w komunikatorze  
	clinet.py - Interfejs klienta w komunikatorze



Moduły:
	socketUI.py - Moduł bazowy do obsługi kieszeni
	serverUI.py - Moduł do obsługi serwera, dziedziczy po SocketUI
	clientUI.py - Moduł do obsługi klienta, dziedziczy po SocketUI
	diffiHellman.py - Moduł definiujący operacje protokołu Diffie'go-Hellman'a
	encrypter.py - Moduł definiujący metody szyfrowania/deszyfrowania wiadomości
