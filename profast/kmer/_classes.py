import threading
import multiprocessing
import copy

class KMerClassifier():
    def __init__(self, *, alpha=2, beta=0.9):
        self.alpha = alpha
        self.beta = beta

    def fit(self, X, *, shape, families=[], k=8):
        self.X = X
        self.shape = shape
        self.families = families
        self.k = k

        if '*' in families:
            self.families = shape.keys()

        else:
            temp_families = []
            for family in families:
                if family in shape.keys():
                    temp_families.append(family)

            self.families = temp_families

        print(f'fitting families:\n{sorted(self.families)}')

        def family_fit(family):
            def word_to_matrix(matrix, protein_no):
                protein = copy.deepcopy(self.X[protein_no])
                for pointer, word in iter(protein(self.k)):
                    pass

            matrix = {}
            for i in shape[family]['_elements']:
                t = threading.Thread(target=word_to_matrix, args=(matrix, i,))

        family_fit_processes = []
        for family in self.families:
            p = multiprocessing.Process(target=family_fit, args=(family,))
            p.name = family
            p.daemon = False
            family_fit_processes.append(p)
            p.start()