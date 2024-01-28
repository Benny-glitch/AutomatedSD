
# ANALISI STATICA DI CASSANDRA CON SPOTBUGS

Questo script in Python viene utilizzato per analizzare, attraverso SPOTBUGS, una repo di un tool di Apache chiamato CASSANDRA, questo strumento di analisi statica analizza il codice Java in cerca di bug.
 
## Requisiti
-   Sistema operativo: GNU/Linux/MAC necessario per eseguire la build.
-   Python 3.x.x installato nel sistema
-   Installare le librerie attraverso il file ```requirements.txt```
Puoi installare le librerie necessarie attraverso:
```bash
  pip install requirements.txt
```
    
## Utilizzo 
1. Eseguire lo script attraverso:


```bash
  python menu.py
```

2.  Segui le istruzioni che ti vengono date nello script



## Note

This project is used by the following companies:

- I commit che non presentano una build valida vengono automaticamente scartati
- I risultati vengono scitti nella cartella ```results``` in un file ```.csv``` che conterrà:  
   -   Hash del commit per esteso
   -   Autore che ha effettutato il commit
   -   Nome della classe dove è stato individuato un bug
