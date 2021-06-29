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

def shape(elements):
    def append_key(family_dict, family_levels, desc):
        total_levels = len(family_levels)
        
        cw_dict = family_dict
        
        for i in range(total_levels):
            if family_levels[i] not in cw_dict:
                cw_dict[family_levels[i]] = {
                    '_ex_count' : 0,
                    '_count' : 1,
                    '_elements' : [],
                }
                
            else:
                cw_dict[family_levels[i]]['_count'] += 1
            
            if desc not in cw_dict[family_levels[i]]['_elements']:
                cw_dict[family_levels[i]]['_elements'].append(desc)
            cw_dict = cw_dict[family_levels[i]]
            
            if i == total_levels-1 :
                cw_dict['_ex_count'] += 1
                # cw_dict['_elements'].append(desc)

    family_dict = {}
    for i, element in enumerate(elements):
        for family_levels in element.families:
            append_key(family_dict, family_levels, i)

    data = {
        'family' : family_dict.keys(),
        'count' : [family_dict[key]['_count'] for key in family_dict.keys()],
        'subfamily ratio' : [100 - family_dict[key]['_ex_count']*100/family_dict[key]['_count'] for key in family_dict.keys()],
    }
    df = pd.DataFrame(data)
    print(df.sort_values(by=['subfamily ratio', 'count'], ascending=False).reset_index(drop=True))

    return family_dict