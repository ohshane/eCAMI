import threading

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
            for i in shape[family]['_elements']:
                for w in iter(self.X[i](self.k)):
                    print(family, i, w)

        for family in self.families:
            t = threading.Thread(target=family_fit, args=(family,))
            t.start()