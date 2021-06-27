import pandas as pd
from proteinIO.protein import Protein


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
        families = [family for family in protein_df.loc[i, 'families'].split('|')]
        families = [family for family in sorted(list(set(families)))]

        hierarchy_duplicates = []
        for family in families:
            excluded_families = families.copy()
            excluded_families.remove(family)

            for child_family in excluded_families:
                if family in child_family:
                    hierarchy_duplicates.append(family)
                    break

        for duplicate in hierarchy_duplicates:
            families.remove(duplicate)

        families_string = ''
        for family in families:
            families_string += family
            families_string += '|'
        families_string = families_string[:-1]

        protein_df.loc[i, 'families'] = families_string

    print(f'Manipulated unmatched family protein (keep=\"{keep}\") DF shape: {protein_df.shape}')

    return protein_df

def series2object(df):
    elements = []
    for _, row in df.iterrows():
        elements.append(Protein(id=row['id'],
                                families=[family.split('_') for family in row['families'].split('|')],
                                sequence=row['sequence']))
    return elements