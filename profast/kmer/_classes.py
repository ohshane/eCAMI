import threading
import multiprocessing
import copy
import numpy as np

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
                if family in shape:
                    temp_families.append(family)

            self.families = temp_families

        print(f'fitting families:\n{sorted(self.families)}')

        def family_fit(family, return_dict):
            def word_to_matrix(matrix, protein_no):
                protein = copy.deepcopy(self.X[protein_no])

                words = {}
                for _, word in iter(protein(self.k)):
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1

                del protein

                for word in words.keys():
                    if word in matrix:
                        matrix[word][protein_no] = words[word]
                    else:
                        matrix[word] = {protein_no : None}
                        matrix[word][protein_no] = words[word]


            matrix = {}
            threads = []
            for i in shape[family]['_elements']:
                t = threading.Thread(target=word_to_matrix, args=(matrix, i,))
                t.daemon = False
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()

            return_dict[family] = matrix

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        family_fit_processes = []
        for family in self.families:
            p = multiprocessing.Process(target=family_fit, args=(family, return_dict))
            p.name = family
            p.daemon = False
            family_fit_processes.append(p)
            p.start()
        
        for p in family_fit_processes:
            p.join()

        self.matrix_group = return_dict
        print(return_dict)