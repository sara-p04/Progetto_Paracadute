import numpy as np
import matplotlib.pyplot as plt
from paracadute1 import Paracadute
# Funzione che esegue la simulazione di Montecarlo
def simulazione(num_lanci, parametri):
    """
    Funzione che esegue la simulazione di Montecarlo per un numero N di lanci di un paracadutista

    Parametri:
    -----------------------------
    num_lanci : numero di lanci da simulare
    parametri : dizionario con i parametri del paracadutista

    Restituisce:
    -----------------------------
    posizione: array delle posizioni di atterraggio in x
    tempo_lancio: array contenente gli istanti di tempo di lancio
    sesso: array contenente il sesso dei paracadutisti ('M' o 'F')
    gittate: array delle gittate dei paracadutisti
    masse: array delle masse dei paracadutisti

    """
    posizione = []
    gittate=[]
    
    # Generazione casuale dei tempi di lancio, masse 
    dt = np.random.exponential(scale=20.0, size=num_lanci)
    tempo_lancio=np.cumsum(dt)

    masse = np.zeros(num_lanci)
    sesso=np.empty(num_lanci, dtype='<U1')

    num_maschi = (num_lanci +1) // 2
    num_femmine = num_lanci // 2

    masse[::2] = np.random.normal(loc=75.0, scale=3.0, size=num_maschi)
    sesso[::2] = 'M'

    masse[1::2] = np.random.normal(loc=60.0, scale=2.0, size=num_femmine)
    sesso[1::2] = 'F'

    # Ciclo sui lanci
    for i in range(num_lanci):
        
        p = Paracadute(masse[i], parametri['h0'], parametri['v0'], parametri['ka'], parametri['kc'], parametri['ht'])
        t, sol = p.soluzione()

        gitt = sol[-1,0]
        gittate.append(gitt)

        x_atterraggio = parametri['v0']*tempo_lancio[i] + gitt
        posizione.append(x_atterraggio)
    
    return np.array(posizione), np.array(tempo_lancio), np.array(sesso), np.array(gittate), np.array(masse)
# Funzione che crea i grafici della distribuzione delle posizioni di atterraggio
def grafici_distribuzione(posizione, tempo_lancio, sesso, gittate, masse):
    """
    Funzione che crea i grafici della distribuzione delle posizioni di atterraggio 

    Parametri:
    -----------------------------
    posizione : array delle posizioni di atterraggio in x
    tempo_lancio : array contenente gli istanti di tempo di lancio
    sesso : array contenente il sesso dei paracadutisti ('M' o 'F')
    gittate : array delle gittate dei paracadutisti
    masse: array delle masse dei paracadutisti

    """
    fig, axes = plt.subplots(2,2, figsize=(12,7))
    fig.suptitle('Distribuzione delle posizioni di atterraggio', fontsize=16)
    # Primo grafico: posizione di atterraggio vs tempo di lancio
    axes[0,0].scatter(tempo_lancio[sesso=='M'], posizione[sesso=='M'], color='blue', alpha=0.5, label='Maschi')
    axes[0,0].scatter(tempo_lancio[sesso=='F'], posizione[sesso=='F'], color='red', alpha=0.2, label='Femmine')
    axes[0,0].set_title('Posizione di atterraggio vs Tempo di lancio')
    axes[0,0].set_xlabel('Tempo di lancio (s)')
    axes[0,0].set_ylabel('Posizione di atterraggio (m)')
    axes[0,0].legend()
    axes[0,0].grid(True, linestyle='--', alpha=0.6)

    # Secondo grafico: istogramma delle gittate

    axes[0,1].hist(gittate[sesso=='M'], bins=30, alpha=0.7, color='blue', label='Maschi')
    axes[0,1].hist(gittate[sesso=='F'], bins=30, alpha=0.5, color='red', label='Femmine')
    axes[0,1].set_title('Istogramma delle Gittate')
    axes[0,1].set_xlabel('Gittate (m)')
    axes[0,1].set_ylabel('Frequenza')
    axes[0,1].legend()
    axes[0,1].grid(True, linestyle='--', alpha=0.6)

    # Terzo grafico: gittata vs massa del paracadutista
    axes[1,0].scatter(masse[sesso=='M'], gittate[sesso=='M'], color='blue', alpha=0.5, label='Maschi')
    axes[1,0].scatter(masse[sesso=='F'], gittate[sesso=='F'], color='red', alpha=0.2, label='Femmine')
    axes[1,0].set_title('Gittata vs Massa del paracadutista')
    axes[1,0].set_xlabel('Massa (kg)')  
    axes[1,0].set_ylabel('Gittata (m)')
    axes[1,0].legend()
    axes[1,0].grid(True, linestyle='--', alpha=0.6)

    # Quarto grafico: statistiche delle gittate
    mu_m = np.mean(gittate[sesso=='M'])
    sigma_m = np.std(gittate[sesso=='M'])
    mu_f = np.mean(gittate[sesso=='F'])
    sigma_f=np.std(gittate[sesso=='F'])
    
    axes[1,1].axis('off')
    testo_statistiche = (
        '{:<10s} {:>8s} {:>8s}\n' + 
        ('-'*28) + '\n' +
        '{:<10s} {:>8.1f} {:>8.1f}\n'
        '{:<10s} {:>8.1f} {:>8.1f}'
    )
    axes[1,1].text(0.5, 0.5, testo_statistiche.format('Sesso', 'Media', 'Dev.Std', 'Maschi', mu_m, sigma_m, 'Femmine', mu_f, sigma_f),
                    horizontalalignment='center',
                    verticalalignment='center',
                    family='monospace',
                    fontsize=12
                   )

   
    plt.tight_layout()
    plt.savefig('distribuzione_atterraggio1.png')
    plt.show()

# Funzione principale
def main():
    parametri = {
        'h0': 4000.0,
        'v0': 50.0,
        'ka': 60.0,
        'kc': 15.0,
        'ht': 1000.0
    }
    print('Parametri della simulazione: \n ----------------------')
    for chiave, valore in parametri.items():
        print('{:s}: {:g}'.format(chiave, valore))
    
    num_lanci = 500
    
    posizione, tempo_lancio, sesso, gittate, masse = simulazione(num_lanci, parametri)
    grafici_distribuzione(posizione, tempo_lancio, sesso, gittate, masse)
    

if __name__ == "__main__":
    main()