import numpy as np

class AviatorPredictor:
    def analyze(self, history):
        if not history:
            return 1.0, 0
        
        data = np.array(history)
        
        # 1. Moyenne pondérée (donne plus de poids aux crashs récents)
        weights = np.arange(1, len(data) + 1)
        w_avg = np.average(data, weights=weights)
        
        # 2. Calcul de la volatilité (écart-type)
        volatility = np.std(data)
        
        # 3. Logique de prédiction (sécuritaire)
        # On retire un pourcentage de la volatilité pour être prudent
        prediction = w_avg - (volatility * 0.3)
        
        # On s'assure que ca ne descend pas sous 1.10
        prediction = max(prediction, 1.10)
        
        # 4. Score de confiance
        confidence = 100 - (volatility * 15)
        confidence = max(min(int(confidence), 98), 20)
        
        return round(prediction, 2), confidence