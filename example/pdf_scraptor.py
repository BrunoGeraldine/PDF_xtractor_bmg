import numpy  as np
import pandas as pd

from pdferli            import get_pdfdf
from PrettyColorPrinter import add_printer

path = r'modelo_de_nota_de_envio_de_amostra.pdf'

#add_printer(1)
df = get_pdfdf(path, normalize_content=False)

togi=[]
for r in np.split(df, df.loc[df.aa_element_type == 'LTAnno'].index):
    df2=r.dropna(subset='aa_size') #eliminando os nan
    if not df2.empty:
        # agora vamos organizar toda a info pelo aa_x0
        df3 = df2.sort_values(by='aa_x0')
        togi.append(df3.iloc[:1].copy())

df4 = pd.concat(togi).copy()
df4.loc[:,'x0round'] = df4.aa_x0.round(2)

# resultado 
resultado = []
for name,group in df4.groupby('x0round'):
    # separnado por uma determinado detalhe da info (nesse caso palavras em negritO)
    if len(group) > 1:
        group2 = group.reset_index(drop=True)
        group3 = np.split(group2, group2.loc[group2.aa_fontname == 'Helvetica-Bold'].index)
        for group4 in group3:
            if len(group4) > 1:
                group5 = (group4.sort_values(by='bb_hierachy_page'))
                t1 = group5.aa_text_line.iloc[0]
                t2 = '\n'.join(group5.aa_text_line.iloc[1:].to_list())
                # teste abaixo
                #print(f'\nXXXXXXXXXXXXXXXXXX\n{t1}\n---------\n{t2}\n')
                resultado.append((t1,t2))
                #print(resultado)

df_r = pd.DataFrame(resultado).set_index(0).T
#print(df_r)
df_r.to_excel('resultado.xlsx')

