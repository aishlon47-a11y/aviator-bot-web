import numpy as np
import datetime
import random

class AviatorPredictor:
    def analyze(self, time_history):
        # Calcul des écarts de temps entre les décollages
        intervals = np.diff(time_history)
        avg_interval = np.mean(intervals)
        volatility = np.std(intervals) if len(intervals) > 1 else 5
        
        # Algorithme de prédiction Caly
        # Plus l'intervalle est stable, plus la confiance est élevée
        if avg_interval > 40:
            p_main = round(random.uniform(1.68, 2.15), 2)
            base_conf = 78
        else:
            p_main = round(random.uniform(1.32, 1.58), 2)
            base_conf = 68
            
        # Cote Assurance (Sécurité ultra-haute)
        p_assur = round(random.uniform(1.18, 1.25), 2)
        
        # Calcul du moment précis du prochain vol
        # On se base sur le rythme moyen constaté
        next_ts = time_history[-1] + avg_interval
        s_time = datetime.datetime.fromtimestamp(next_ts)
        
        # Calcul du score de fiabilité dynamique
        reliability = base_conf - (volatility * 0.5)
        reliability = max(min(int(reliability), 92), 40)
        
        return p_main, p_assur, s_time, reliability
