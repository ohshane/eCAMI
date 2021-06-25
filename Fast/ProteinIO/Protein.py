class Protein:
    def __init__(self, id='', families='', sequence=''):
        self.id = id
        self.families = families
        self.sequence = sequence
        
    def to_list(self):
        return [self.id, self.families, self.sequence]
        
    def __repr__(self):
        return f'''\r{self.id}
        \r{self.families}
        \r{self.sequence[:20]}...{len(self.sequence)}...{self.sequence[-5:]}'''