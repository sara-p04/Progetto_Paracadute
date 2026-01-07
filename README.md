# Progetto\_Paracadute

Progetto\_Paracadute

\# Simulazione Moto Paracadutista

Questo repository contiene il progetto d'esame per la simulazione della dinamica di caduta di un paracadutista. Il modello fisico include la forza di gravità e l'attrito viscoso dell'aria (regime lineare), gestendo la fase di apertura del paracadute a una quota prestabilita.



Il progetto si compone di tre parti principali:



1. Modulo per la risoluzione dell'equazione differenziale del moto

2\. Analisi parametrica della fisica del moto.

3\. Simulazione Montecarlo di lanci multipli.



\*Descrizione dei File\*



\* paracadute1.py: Modulo contenente la classe Paracadute. Definisce le equazioni differenziali del moto e utilizza la funzione odeint della libreria scipy per risolverle.

\* analisi\_dati.py: Script per generare grafici comparativi al variare dei parametri fisici 

\* simulazione.py: Script per la simulazione Montecarlo. Genera una popolazione di lanci con distribuzione casuale (tempi di Poisson, masse Gaussiane) e produce statistiche sugli atterraggi.



\*Istruzioni per l'Esecuzione\*



1\. Analisi Dati

Questo script analizza come cambiano la traiettoria e le velocità al variare di un parametro fisico.



Per visualizzare l'elenco completo dei comandi e dei parametri disponibili, eseguire:

python analisi\_dati.py --help



Personalizzazione e Default:

Lo script utilizza dei valori di default per tutti i parametri non specificati, in particolare: Massa=75kg, 

Quota=4000m, 

v0(velocità dell'aereo)=50m/s, 

kaperto(coefficiente di attrito a paracadute APERTO)= 60 kg/s, 

kchiuso(coefficiente di attrito a paracadute CHIUSO)=None, 

Quota apertura = 1000 m



È comunque possibile personalizzare tutti i parametri della simulazione (massa, velocità, coefficienti, quote) utilizzando le apposite opzioni (-m, -h0, -v0, -ka, -kc, -ht) contemporaneamente alle opzioni del parametro scelto per l'analisi.



Sintassi di base:

python analisi\_dati.py -var \[VARIABILE\_DA\_ANALIZZARE] -start \[INIZIO] -stop \[FINE] \[PERSONALIZZAZIONE\_PARAMETRI]



Esempi di utilizzo:

\* Variare la massa (m) da 60 a 100 kg (lasciando gli altri parametri di default):

python analisi\_dati.py -var m -start 60 -stop 100 -step 5

\* Variare il coefficiente d'attrito (k1) specificando una massa personalizzata di 95kg:

python analisi\_dati.py -var k1 -start 10 -stop 25 -step 2 -m 95

\* Variare la quota di apertura (ht) da 200m a 1000m:

python analisi\_dati.py -var ht -start 200 -stop 1000 -step 100



2\. Simulazione Montecarlo

Esegue la simulazione statistica su 500 lanci (con distribuzione gaussiana di masse e poissoniana dei lanci) e mostra i grafici di distribuzione (tempi, posizioni, gittate). In questo caso tutti gli altri parametri sono impostati di Default e stampati nel momento in cui lo script viene eseguito. 

python simulazione.py



