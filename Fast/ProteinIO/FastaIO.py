from tqdm import tqdm
import pandas as pd
import os

from Fast.ProteinIO.Protein import Protein


def read(*paths):
    if len(paths) < 1:
        raise Exception('too short')
    elif len(paths) == 1:
        if isinstance(paths[0], (list, tuple)):
            paths = paths[0]
        else:
            raise Exception('not iterable')

    proteins = []
    temp_protein = None

    for path in paths:
        file = open(path, 'r')

        for line in file:
            line = line.strip().upper()

            if line[-1] == '|':
                line = line[:-1]
            
            if line[0] == '>':
                if temp_protein is not None:
                    proteins.append(temp_protein.to_list())
                
                temp_protein = Protein()

                try:
                    id, families = line.split('|', 1)
                except:
                    print(f'\n[ERROR] format error: {line}')
                    id = line
                    families = ''
                
                id = id[1:]
                
                temp_protein.id = id

                temp_families = []
                for family in families.split('|'):
                    if family[0].isalpha():
                        temp_families.append(family)

                families = ''
                for family in sorted(temp_families):
                    families += family
                    families += '|'
                
                families = families[:-1]
                
                temp_protein.families = families
                
            else:
                temp_protein.sequence += line


    columns = ['id', 'families', 'sequence']
    protein_df = pd.DataFrame(proteins, columns=columns)
    print(f'Protein DF shape: {protein_df.shape}')

    return protein_df

def write(protein_df):
    if os.path.exists('out.fa'):
        os.remove('out.fa')
    
    f = open('out.fa', 'w')
    for _, protein in tqdm(protein_df.iterrows()):
        id = protein['id']
        families = protein['families']
        sequence = protein['sequence']
        
        f.write(f'>{id}|{families}\n')
        f.write(f'{sequence}\n')
    
    f.close()
    print('exported out.fa')

def manipulate_duplicates(protein_df, keep=False):
    protein_df = protein_df.drop_duplicates(subset=['sequence', 'families'], keep='first')
    print(f'Unique protein DF shape: {protein_df.shape}')

    if keep == 'union':
        temp_df = pd.DataFrame()
        for sequence in protein_df.loc[protein_df.duplicated(subset=['sequence'])]['sequence']:
            duplicated_set_df = protein_df.loc[protein_df['sequence'] == sequence]
            temp_row = duplicated_set_df.head(1)

            temp_family = ''
            for _, row in duplicated_set_df.iterrows():
                temp_family += row['families']
                temp_family += '|'

            temp_family = temp_family[:-1]
            temp_row['families'] = temp_family

            temp_df = temp_df.append(temp_row)

        protein_df = protein_df.drop_duplicates(subset=['sequence'], keep=False)
        protein_df = protein_df.append(temp_df)

    else:
        protein_df = protein_df.drop_duplicates(subset=['sequence'], keep=keep)

    protein_df = protein_df.reset_index(drop=True)

    for i in range(len(protein_df)):
        families = protein_df.loc[i, 'families']

        protein_df.loc[i, 'families'] = ''

    print(f'Manipulated unmatched family protein (keep=\"{keep}\") DF shape: {protein_df.shape}')

    return protein_df