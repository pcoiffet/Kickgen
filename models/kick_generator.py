import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class KickGenerator(nn.Module):
    def __init__(self, input_size=128, hidden_size=256, output_size=44100):
        super(KickGenerator, self).__init__()
        
        # Paramètres du modèle
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Couches du réseau
        self.encoder = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )
        
        self.style_embedding = nn.Embedding(3, hidden_size)  # 3 styles: hard tech, frenchcore, psy trance
        
        self.decoder = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),  # *2 car on concatène avec l'embedding de style
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Tanh()  # Pour normaliser la sortie entre -1 et 1
        )
        
    def forward(self, x, style_idx):
        # x: paramètres du kick (pitch, tail_length, punch, saturation, compression)
        # style_idx: indice du style (0: hard tech, 1: frenchcore, 2: psy trance)
        
        # Encodage des paramètres
        encoded = self.encoder(x)
        
        # Embedding du style
        style_emb = self.style_embedding(style_idx)
        
        # Concaténation des paramètres encodés et du style
        combined = torch.cat([encoded, style_emb], dim=1)
        
        # Décodage pour générer le kick
        output = self.decoder(combined)
        
        return output

    def generate_kick(self, style_idx, pitch=1.0, tail_length=0.5, punch=0.7, saturation=0.5, compression=0.3):
        # Préparation des paramètres
        params = torch.tensor([pitch, tail_length, punch, saturation, compression], dtype=torch.float32)
        
        # Génération du kick
        with torch.no_grad():
            kick = self.forward(params, torch.tensor([style_idx]))
        
        return kick.numpy()

# Fonction utilitaire pour sauvegarder le kick en WAV
def save_kick_to_wav(kick, filename, sample_rate=44100):
    import soundfile as sf
    sf.write(filename, kick, sample_rate) 