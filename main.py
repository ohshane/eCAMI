from Fast.ProteinIO import FastaIO
from pathlib import Path
import os

from Fast.ProteinIO import FastaIO

__file__ = os.getcwd()
paths = [Path(__file__) / 'data' / 'dbCAN2' / 'CAZyDB.mini.fa']

proteins = FastaIO.read(paths)
proteins = FastaIO.drop_duplicates(proteins)

FastaIO.write(proteins)