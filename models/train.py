import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os
from kick_generator import KickGenerator
import soundfile as sf

class KickDataset(Dataset):
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.kicks = []
        self.labels = []
        
        # Charger les kicks et leurs labels
        for style_idx, style in enumerate(['hard_tech', 'frenchcore', 'psy_trance']):
            style_dir = os.path.join(data_dir, style)
            if os.path.exists(style_dir):
                for file in os.listdir(style_dir):
                    if file.endswith('.wav'):
                        audio, _ = sf.read(os.path.join(style_dir, file))
                        self.kicks.append(audio)
                        self.labels.append(style_idx)
    
    def __len__(self):
        return len(self.kicks)
    
    def __getitem__(self, idx):
        return torch.tensor(self.kicks[idx], dtype=torch.float32), self.labels[idx]

def train_model(model, train_loader, num_epochs=100, learning_rate=0.001):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs, labels)
            loss = criterion(outputs, inputs)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(train_loader):.4f}')

def main():
    # Créer le modèle
    model = KickGenerator()
    
    # Créer le dataset et le dataloader
    dataset = KickDataset('data')
    train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Entraîner le modèle
    train_model(model, train_loader)
    
    # Sauvegarder le modèle
    torch.save(model.state_dict(), 'models/kick_generator.pth')

if __name__ == '__main__':
    main() 