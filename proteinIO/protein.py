class Protein:
    def __init__(self, id='', families='', sequence=''):
        self.id = id
        self.families = families
        self.sequence = sequence
        self.sequence_len = len(sequence)
        
    def to_list(self):
        return [self.id, self.families, self.sequence]

    def get_word(self, at, k):
        if self._check_k(k):
            word = None

            if at + k < self.sequence_len:
                word = self.sequence[self.pointer : self.pointer+k]
            return word
            
        raise Exception('[ERROR] Set k for k-mer')

    def get_index(self, word):
        if not isinstance(word, str):
            raise Exception('[ERROR] word error')
        word = word.strip().upper()
        k = len(word)
        index = -1
        for i, w in iter(self(k)):
            if w == word:
                index = i
                break
        return index

    def get_indexes(self, word):
        if not isinstance(word, str):
            raise Exception('[ERROR] word error')
        word = word.strip().upper()
        k = len(word)
        indexes = []
        for i, w in iter(self(k)):
            if w == word:
                indexes.append(i)
        return indexes

    def _check_k(self, k):
        if isinstance(k, int) and k > 0:
            return True
        return False

    def __call__(self, k):
        if self._check_k(k):
            self.k = k
            return self
        raise Exception('[ERROR] Invalid k value')

    def __iter__(self):
        self.pointer = -1

        if not self.sequence:
            protein_name = None
            if self.id:
                protein_name = self.id
            raise Exception(f'[ERROR] No sequence in protein ({protein_name})')

        if self.k < 1:
            raise Exception('[ERROR] Set k for k-mer')

        return self

    def __next__(self):
        if self.pointer + self.k > self.sequence_len - 1:
            delattr(self, 'k')
            raise StopIteration

        self.pointer += 1
        
        return self.pointer, self.sequence[self.pointer : self.pointer+self.k]

        
    def __repr__(self):
        return f'''\r{self.id}
        \r{self.families}
        \r{self.sequence[:20]}...{len(self.sequence)}...{self.sequence[-5:]}\n'''