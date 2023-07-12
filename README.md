# Anleitung zur Prüfungsaufgabe

## Abhängigkeiten
Damit das Projekt lauffähig ist müssen folgende Abhängigkeiten installiert sein:  
- python3 `sudo apt install python3`
- mpirun `sudo apt install mpich`

Damit MPI mit Python verwendet werden kann muss mpi4py installiert werden, dies geht so: 
- `python3 -m pip install -r requirements.txt` (traditionelle Art)
- `sudo apt install python3-mpi4py` (ab Ubuntu 23.04 nötig)

```bash
mpirun --use-hwthread-cpus -np 8 python3 test_tree_mpi.py
```