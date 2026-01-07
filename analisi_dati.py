import numpy as np
import matplotlib.pyplot as plt
from paracadute1 import Paracadute
import argparse 
# Funzione neccessaria per passare e gestire gli argomenti da terminale
def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulazione della caduta di un paracadutista')
    parser.add_argument('-m', '--massa', type=float, default=75.0, help='Massa del paracadutista in kg (default: 80 kg)')
    parser.add_argument('-h0', '--quotainizi', type=float, default=4000.0, help='Quota iniziale di lancio in metri (default: 4000 m)')
    parser.add_argument('-v0', '--velocitainiz', type=float, default=50.0, help='Velocità orizzontale iniziale in m/s (default: 50 m/s)')
    parser.add_argument('-ka', '--kaperto', type=float, default=60.0, help='Coefficiente di attrito a paracadute aperto in kg/s (default: 60 kg/s)')
    parser.add_argument('-kc', '--kchiuso', type=float, default=None, help='Coefficiente di attrito a paracadute chiuso in kg/s (default: None, uguale a ka)')
    parser.add_argument('-ht', '--quotaapertura', type=float, default=1000.0, help='Quota di apertura del paracadute in metri (default: 1000 m)')

    parser.add_argument('-var', '--variare', required=True, choices=['m', 'h0', 'v0', 'ka', 'kc', 'ht'], help='Variabile da variare (massa, quotaapertura, velocità iniziale, coeffattrito1, coeffattrito2, quotaapertura)')
    parser.add_argument('-start', '--valinizzio', type=float, required=True, help='Valore iniziale della variabile da variare')
    parser.add_argument('-stop', '--valfine', type=float, required=True, help='Valore finale della variabile da variare')
    parser.add_argument('-step', '--passo', type=float, default=5, help='Passo di variazione della variabile da variare')
    return parser.parse_args()
# Funzione principale di analisi dati
def analisi_dati(parametro_variabile, valori_parametro, parametri_fissi):
    """
    Funzione che crea grafici al variare dei parametri analizzando: 
    1. La traiettoria y(x)
    2. L'evoluzione della velocità verticale in funzione del tempo v_y(t)
    3. La distanza di atterraggio in funzione del parametro variabile
    4. La velocità di atterraggio in funzione del parametro variabile
    5. La velocità massima raggiunta in funzione del parametro variabile

    Parametri:
    -----------------------------
    parametro_variabile : stringa che indica quale parametro variare
    valori_parametro : array dei valori del parametro variabile
    parametri_fissi : dizionario con i parametri fissi del paracadutista

    """
    distanze_atterraggio = []
    velocita_atterraggio = []
    velocita_massima = []

    fig, axes = plt.subplots(2, 3, figsize=(12,6))
    fig.suptitle('Analisi al variare di {:s} da {:g} a {:g}'.format(parametro_variabile, valori_parametro[0], valori_parametro[-1]), fontsize=16)
    # Ciclo sui valori del parametro variabile
    for val in valori_parametro:
        params = parametri_fissi.copy()
        params[parametro_variabile] = val

        paracadutista = Paracadute(params['m'], params['h0'], params['v0'], params['ka'], params['kc'], params['ht'])
        t, sol = paracadutista.soluzione()

        x = sol[:,0]
        y = sol[:,1]
        vx= sol[:,2]
        vy = sol[:,3]

        distanze_atterraggio.append(x[-1])
        velocita_atterraggio.append(np.sqrt(vx[-1]**2 + vy[-1]**2))
        velocita_massima.append(np.max(np.sqrt(vx**2 + vy**2)))
        # 1. Traiettoria y(x) e 2. Velocità verticale v_y(t) per ogni valore del parametro variabile
        axes[0,0].plot(x, y, label='{}={:.1f}'.format(parametro_variabile, val))
        axes[0,1].plot(t, np.abs(vy), label='{}={:.1f}'.format(parametro_variabile, val))
    
    #1. Traiettoria y(x)
    axes[0,0].set_title('Traiettoria y(x)')
    axes[0,0].set_xlabel('x (m)')
    axes[0,0].set_ylabel('y (m)')
    axes[0,0].legend(title=parametro_variabile, fontsize='x-small', framealpha=0.5)
    axes[0,0].grid(True, linestyle='--', alpha=0.6)
    
    #2. Velocità verticale v_y(t)
    axes[0,1].set_title('Velocità verticale v_y(t)')
    axes[0,1].set_xlabel('t (s)')
    axes[0,1].set_ylabel('v_y (m/s)')
    axes[0,1].legend(title=parametro_variabile, fontsize='x-small', framealpha=0.5)
    axes[0,1].grid(True, linestyle='--', alpha=0.6)
    
    #3. Distanza di atterraggio in funzione del parametro variabile
    axes[1,0].plot(valori_parametro, distanze_atterraggio, 'o-', color='green')
    axes[1,0].set_title('Distanza di atterraggio vs {:s}'.format(parametro_variabile))
    axes[1,0].set_xlabel(parametro_variabile)
    axes[1,0].set_ylabel('Distanza di atterraggio (m)')
    axes[1,0].grid(True)
    
    #4. Velocità di atterraggio in funzione del parametro variabile
    axes[1,1].plot(valori_parametro, velocita_atterraggio, 'o-', color='red')
    axes[1,1].set_title('Velocità di atterraggio vs {:s}'.format(parametro_variabile))
    axes[1,1].set_xlabel(parametro_variabile)
    axes[1,1].set_ylabel('Velocità di atterraggio (m/s)')
    axes[1,1].grid(True)
    
    #5. Velocità massima raggiunta in funzione del parametro variabile
    axes[0,2].plot(valori_parametro, velocita_massima, 'o-', color='purple')
    axes[0,2].set_title('Velocità massima raggiunta vs {:s}'.format(parametro_variabile))
    axes[0,2].set_xlabel(parametro_variabile)
    axes[0,2].set_ylabel('Velocità massima (m/s)')
    axes[0,2].grid(True)

    axes[1,2].axis('off')
    testo_fissi = "PARAMETRI FISSI:\n----------------\n"
    
    for chiave, valore in parametri_fissi.items():
        if chiave != parametro_variabile: 
            if valore == None: 
                testo_fissi = testo_fissi + '{:s} = {:g} \n'.format(chiave, parametri_fissi['ka'])
            else:
                testo_fissi = testo_fissi + '{:s} = {:g}\n'.format(chiave, valore)

    axes[1,2].text(0.5, 0.5, testo_fissi, 
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=12,
                   family='monospace') 


    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    plt.tight_layout()
    plt.savefig('analisi_{:s}_da{:g}_a{:g}.png'.format(parametro_variabile, valori_parametro[0], valori_parametro[-1]), dpi=300)
    plt.show()

def main():
    args = parse_arguments()

    parametri_fissi = {
        'm': args.massa,
        'h0': args.quotainizi,
        'v0': args.velocitainiz,
        'ka': args.kaperto,
        'kc': args.kchiuso,
        'ht': args.quotaapertura
    }

    valori_parametro = np.arange(args.valinizzio, args.valfine + args.passo, args.passo)

    analisi_dati(args.variare, valori_parametro, parametri_fissi)

if __name__ == "__main__":
    main()


