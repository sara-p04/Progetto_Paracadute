import numpy as np 
from scipy import integrate

class Paracadute: 
    """
    Classe che descrive la dinamica del paracadutista, simulando la caduta 
    sotto l'effetto della gravità e della resistenza aerodinamica,
    inclusa la fase di apertura del paracadute.

    Attributi:
    -----------------------------
    m : Massa del sistema paracadutista (kg).
    h0 : Quota iniziale di lancio rispetto al suolo (m).
    v0 : Velocità orizzontale iniziale fornita dall'aereo (m/s).
    k_aperto : Coefficiente di attrito viscoso a paracadute APERTO (kg/s).
    k_chiuso : Coefficiente di attrito viscoso a paracadute CHIUSO (kg/s).
    ht : Quota a cui avviene l'apertura del paracadute (m).
    """
    # Costruttore
    def __init__(self, m, h0, v0, ka, kc=None, ht=1000):
        self.m = m
        self.h0 = h0
        self.v0 = v0
        self.ka = ka
        if kc==None:
            self.kc = ka
        else:
            self.kc = kc
        self.ht = ht
    # Equazioni del moto
    def moto_paracadute(self, s, t):
        """
        Funzione che calcola dx/dy, dy/dt, dvx/dt, dvy/dt 
        
        Parametri:
        -----------------------------
        self: oggetto paracadute con attributi m, k1, k2, ht
        s = [ r, v ] : vettore con r = [x, y] e v = [vx, vy]
        t : array dei tempi

        Restituisce:
        -----------------------------
        dx/dt, dy/dt, dvx/dt, dvy/dt
        """
        g = 9.81 
        dxdt = s[2]
        dydt = s[3]
        
        if s[1] > self.ht:
            k = self.kc
        else:   
            k = self.ka
        
        dvxdt = - (k/self.m)*s[2]
        dvydt = - (k/self.m)*s[3] - g

        return (dxdt, dydt, dvxdt, dvydt)
    # Soluzione dell'equazione del moto
    def soluzione(self):
        """
        Funzione che risolve l'equazione del moto del paracadutista

        Parametri:
        -----------------------------
        self: oggetto paracadute con attributi m, k_aperto, k_chiuso, ht

        Restituisce:
        -----------------------------
        t: array dei tempi
        sol: matrice Nx4 con N: numero di istanti di tempo, 1 colonna: x(t), 2 colonna: y(t), 3 colonna: vx(t), 4 colonna: vy(t)

        """
        g = 9.81
        
        k_max = self.ka
        # costruiamo l'array dei tempi in base ai parametri del problema
        v_limite = (self.m * g) / k_max
        t_stimato = self.h0 / v_limite
        t_finale = t_stimato * 1.5
        num_punti = int(t_finale * 50) 
        
        t = np.linspace(0, t_finale, num_punti)
        
        # condizioni iniziali: [x0, y0, vx0, vy0]
        s_iniz = np.array([0, self.h0, self.v0, 0]) 
        
        # troviamo la soluzione numerica
        sol = integrate.odeint(self.moto_paracadute, s_iniz, t)
        
        # filtriamo i dati per mantenere solo y >= 0
        masksol = sol[:,1] >= 0
        sol = sol[masksol]
        t = t[masksol]
        
        return t, sol