# Anleitung zur Prüfungsaufgabe

## Abhängigkeiten
Damit das Projekt lauffähig ist müssen folgende Abhängigkeiten installiert sein:  
- python3 `sudo apt install python3`
- mpirun `sudo apt install mpich`

Damit MPI mit Python verwendet werden kann muss mpi4py installiert werden, dies geht so: 
- `python3 -m pip install -r requirements.txt` (traditionelle Art)
- `sudo apt install python3-mpi4py` (ab Ubuntu 23.04 nötig)

## Das Programm laufen lassen
Mithilfe folgenen Befehls kann das Programm ausgeführt werden: `mpirun -np NUMBER_PROCESSES python3 main.py ROWS COLUMNS`.  
Dabei müssen die groß geschriebenen Worte ersetzt werden durch:  
- `NUMBER_PROCESSES`: Anzahl der Prozesse, zB. 8
- `ROWS`: Anzahl der Zeilen der start-Matrix, zB. 1000
- `COLUMNS`: Anzahl der Spalten der start-Matrix. zB. 1000

Beispiel: `mpirun -np 8 python3 main.py 1000 1000`

## Allgemeine Dokumentation