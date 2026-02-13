import numpy as np
import random

class AviatorPredictor:
    def analyze(self, history, platform):
        data = np.array(history)
        
        # Ajustement des algorithmes selon le bookmaker (simulation de latence serveur)
        offsets = {
            "1xBet": 0.32,
            "Melbet": 0.28,
            "Betclic": 0.45,
            "Betwinner": 0.30,
            "PremierBet": 0.35
        }
        
        margin = offsets.get(platform, 0.3)
        w_avg = np.average(data, weights=np.arange(1, len(data) + 1))
        volatility = np.std(data)
        
        # Prédiction de la cote
        prediction = w_avg - (volatility * margin)
        prediction = max(prediction, 1.20)
        
        # Calcul du signal temporel (Délai en secondes avant le prochain vol)
        # Basé sur la volatilité : plus c'est instable, plus le délai est court
        base_delay = random.randint(45, 90) # Temps moyen entre deux tours
        signal_delay = base_delay + int(volatility * 5)
        
        # Score de confiance
        confidence = 100 - (volatility * 12)
        confidence = max(min(int(confidence), 97), 35)
        
        return round(prediction, 2), confidence, signal_delay
