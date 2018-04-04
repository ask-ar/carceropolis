import pandas as pd

'''
Gera um arquivo R que preenche os campos "id_unidade" das unidades
prisionais de um ano.
'''

input_filename = 'df2015_unidades.csv'
output_filename = 'coorrel.R'
ID_COL = 'id_unidade'
ORIG_COL = 'ordem original'
UF_COL = 'UF.'

# read CSV
df = pd.read_csv(input_filename, sep=';')

# remove " - União" from UF names
df[UF_COL] = df[UF_COL].apply(lambda x: x[0:2])

with open(output_filename, 'w') as f:
    for uf, rows in df.groupby(UF_COL):
        # block header
        lines = ['# Adicionando o id_unidade para {uf} [{n} unidades]'.format(
            uf=uf, n=len(rows))]
        # block lines
        for _, row in rows.sort_values(ORIG_COL).iterrows():
            lines.append('df2015$id_unidade[{orig}]<-{id}'.format(
                orig=row[ORIG_COL],
                id=int(row[ID_COL]) if pd.notnull(row[ID_COL]) else ''))
        f.write('\n'.join(lines) + '\n\n')
