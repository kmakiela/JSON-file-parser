Napisać program, który odczytuje plik w formacie JSON z opisem grafiki, wyświetla tę grafikę na ekranie i zapisuje w pliku PNG.

Plik może zawierać:

    punkty
    wielokąty (podana lista punktów)
    prostokąty (współrzędne środka, wysokość, szerokość) - równolegle do osi układu współrzędnych
    kwadraty (środek i długość boku)
    koła (środek i promień)

Każda figura może mieć określony kolor w postaci słownej (z zadanej palety, np. red), trójki liczb dziesiętnych (np. (255, 0, 0) lub notacji HTML (#ff0000).

Przykładowy plik zawierający wszystkie dopuszczalne elementy: http://home.agh.edu.pl/~zkaleta/python/sample.json

Program ma przyjmować nazwę pliku wejściowego z linii komend. Jeżeli zostanie podana flaga -o (lub --output) to po niej ma być nazwa pliku, do którego grafikę należy zapisać. Jeśli flaga -o nie zostanie podana, to należy tylko wyświetlić na ekranie.
