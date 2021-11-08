from collections import Counter
import pandas as pd
import torch
from torch.utils.data import Dataset

PATH = "data/data.csv"


class Words_Dataset(Dataset):
    def __init__(self, args, dataset_path=PATH):
        self.args = args
        self.dataset_path = dataset_path

        # load all the words
        self.words = self.load_words()
        self.unique_words = self.get_unique_words()

        # create the mappings
        self.index_to_word = {
            index: word for index, word in enumerate(self.unique_words)
        }
        self.word_to_index = {
            word: index for index, word in enumerate(self.unique_words)
        }

        # write all the indexes
        self.word_indexes = [self.word_to_index[word] for word in self.words]

    def load_words(self):
        # converts data frame to list of words
        df = pd.read_csv(self.dataset_path)
        text = df["0"].str.cat(sep=" ")
        return text.split(" ")

    def get_unique_words(self):
        # sorts by most frequent word
        word_counts = Counter(self.words)
        return sorted(word_counts, key=word_counts.get, reverse=True)

    def __len__(self):
        return len(self.word_indexes) - self.args.sequence_length

    def __getitem__(self, index):
        first = torch.tensor(
            self.word_indexes[index : index + self.args.sequence_length]
        )
        second = torch.tensor(
            self.word_indexes[index + 1 : self.args.sequence_length + 1]
        )
        return first, second
