default_k = 8

class Protein:
    def __init__(self, id='', families='', sequence='', k=default_k):
        self.id = id
        self.families = families
        self.sequence = sequence
        self.sequence_len = len(sequence)
        self.k = int(k)
        
    def to_list(self):
        return [self.id, self.families, self.sequence]

    def get_word(self, k=default_k):
        pass

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
            raise StopIteration

        self.pointer += 1
        
        return self.pointer, self.sequence[self.pointer : self.pointer+self.k]

        
    def __repr__(self):
        return f'''\r{self.id}
        \r{self.families}
        \r{self.sequence[:20]}...{len(self.sequence)}...{self.sequence[-5:]}'''