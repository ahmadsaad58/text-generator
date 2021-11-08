from torch import nn
import torch


class LSTM_Model(nn.module):
    def __init__(self, dataset):
        super().__init__()
        self.lstm_size = 128
        self.embedding_dim = 128
        self.num_layers = 3

        n_vocab = len(dataset.unique_words)
        self.embeddings = nn.Embedding(
            num_embeddings=n_vocab, embedding_dim=self.embedding_dim
        )
