def drop_duplicates(protein_df, keep=False):
    protein_df = protein_df.drop_duplicates(subset=['sequence', 'families'], keep='first')
    print(f'Unique protein DF shape: {protein_df.shape}')

    protein_df = protein_df.drop_duplicates(subset=['sequence'], keep=keep)
    print(f'Dropped unmatched family protein DF shape: {protein_df.shape}')

    return protein_df