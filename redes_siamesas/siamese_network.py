# notebook code1
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import random

# Configurações
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

# ============================================
# 1. PRÉ-PROCESSAMENTO DOS DADOS
# ============================================

class SequenceProcessor:
    """Processa as sequências comportamentais do CSV"""

    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.vocab = self._build_vocab()
        self.species_names = self.df.columns.tolist()

    def _build_vocab(self):
        """Constrói vocabulário de todos os comportamentos"""
        all_behaviors = set()
        for col in self.df.columns:
            sequences = self.df[col].dropna().astype(str)
            for seq in sequences:
                all_behaviors.update(seq.split())

        vocab = {beh: idx + 1 for idx, beh in enumerate(sorted(all_behaviors))}
        vocab['<PAD>'] = 0  # Padding token
        return vocab

    def encode_sequence(self, sequence_str, max_length=100):
        """Converte string de comportamentos em tensor de índices"""
        behaviors = sequence_str.split()
        indices = [self.vocab.get(b, 0) for b in behaviors]

        # Padding ou truncamento
        if len(indices) < max_length:
            indices = indices + [0] * (max_length - len(indices))
        else:
            indices = indices[:max_length]

        return torch.tensor(indices, dtype=torch.long)

    def get_all_sequences(self, max_length=100):
        """Retorna todas as sequências codificadas"""
        sequences = []
        species_labels = []

        for col in self.df.columns:
            for seq in self.df[col].dropna().astype(str):
                sequences.append(self.encode_sequence(seq, max_length))
                species_labels.append(col)

        return sequences, species_labels


# ============================================
# 2. DATASET PARA PARES DE SEQUÊNCIAS
# ============================================

class SiameseSequenceDataset(Dataset):
    """Dataset que gera pares de sequências para treinamento"""

    def __init__(self, sequences, labels, num_pairs=1000):
        self.sequences = sequences
        self.labels = labels
        self.num_pairs = num_pairs

        # Agrupa por espécie
        self.species_indices = {}
        for idx, label in enumerate(labels):
            if label not in self.species_indices:
                self.species_indices[label] = []
            self.species_indices[label].append(idx)

        self.pairs = self._generate_pairs()

    def _generate_pairs(self):
        """Gera pares positivos (mesma espécie) e negativos (espécies diferentes)"""
        pairs = []
        species_list = list(self.species_indices.keys())

        for _ in range(self.num_pairs):
            if random.random() < 0.5:  # Par positivo (mesma espécie)
                species = random.choice(species_list)
                indices = self.species_indices[species]
                if len(indices) >= 2:
                    idx1, idx2 = random.sample(indices, 2)
                    pairs.append((idx1, idx2, 1))  # Label 1 = similar
            else:  # Par negativo (espécies diferentes)
                species1, species2 = random.sample(species_list, 2)
                idx1 = random.choice(self.species_indices[species1])
                idx2 = random.choice(self.species_indices[species2])
                pairs.append((idx1, idx2, 0))  # Label 0 = dissimilar

        return pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        idx1, idx2, label = self.pairs[idx]
        return self.sequences[idx1], self.sequences[idx2], torch.tensor(label, dtype=torch.float32)

# ============================================
# 3. ARQUITETURA DA REDE SIAMESA
# ============================================

class SequenceEncoder(nn.Module):
    """Encoder de sequências com Embedding + LSTM"""

    def __init__(self, vocab_size, embedding_dim=64, hidden_dim=128, num_layers=2):
        super(SequenceEncoder, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.3
        )

    def forward(self, x):
        # x: (batch_size, seq_length)
        embedded = self.embedding(x)  # (batch, seq_len, embedding_dim)

        # LSTM
        lstm_out, (hidden, cell) = self.lstm(embedded)

        # Usa a concatenação dos últimos estados hidden de ambas as direções
        hidden_fwd = hidden[-2]  # Última camada forward
        hidden_bwd = hidden[-1]  # Última camada backward
        encoding = torch.cat([hidden_fwd, hidden_bwd], dim=1)

        return encoding


class SiameseNetwork(nn.Module):
    """Rede Siamesa completa"""

    def __init__(self, vocab_size, embedding_dim=64, hidden_dim=128):
        super(SiameseNetwork, self).__init__()

        self.encoder = SequenceEncoder(vocab_size, embedding_dim, hidden_dim)

    def forward(self, seq1, seq2):
        # Codifica ambas as sequências
        encoding1 = self.encoder(seq1)
        encoding2 = self.encoder(seq2)

        return encoding1, encoding2

# ============================================
# 4. FUNÇÃO DE PERDA
# ============================================

class ContrastiveLoss(nn.Module):
    """Contrastive Loss para redes siamesas"""

    def __init__(self, margin=2.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, encoding1, encoding2, label):
        # Distância euclidiana
        distance = torch.nn.functional.pairwise_distance(encoding1, encoding2)

        # Loss: para pares similares (label=1), minimiza distância
        #       para pares dissimilares (label=0), maximiza distância (até margin)
        loss = (label * distance.pow(2) +
                (1 - label) * torch.clamp(self.margin - distance, min=0.0).pow(2))

        return loss.mean()

# ============================================
# 5. TREINAMENTO
# ============================================

def train_model(model, train_loader, criterion, optimizer, num_epochs=20, device='cpu'):
    """Treina a rede siamesa"""

    model = model.to(device)
    model.train()

    for epoch in range(num_epochs):
        total_loss = 0

        for seq1, seq2, labels in train_loader:
            seq1, seq2, labels = seq1.to(device), seq2.to(device), labels.to(device)

            optimizer.zero_grad()

            # Forward pass
            encoding1, encoding2 = model(seq1, seq2)
            loss = criterion(encoding1, encoding2, labels)

            # Backward pass
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}')

    return model

