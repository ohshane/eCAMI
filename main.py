from pathlib import Path
import os

from proteinIO import fastaIO
from profast.kmer import KMerClassifier

__file__ = os.getcwd()
paths = [Path(__file__) / 'data' / 'dbCAN2' / 'CAZyDB.mini.fa']

proteins = fastaIO.read(paths)
proteins = fastaIO.drop_duplicates(proteins)

fastaIO.write(proteins)

kmc = KMerClassifier()