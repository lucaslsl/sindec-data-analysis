import pandas as pd
import pandasql as pdsql

df = pd.DataFrame()

pysql = lambda q: pdsql.sqldf(q, globals())

df_1 = pd.read_csv('boletim_sindec_atendimento_2015_1o_trimestre.csv', delimiter=';')
df_2 = pd.read_csv('boletim_sindec_atendimento_2015_2o_trimestre.csv', delimiter=';')
df_3 = pd.read_csv('boletim_sindec_atendimento_2015_3o_trimestre.csv', delimiter=';')
df_4 = pd.read_csv('boletim_sindec_atendimento_2015_4o_trimestre.csv', delimiter=';')

df_list = []
df_list.append(df_1)
df_list.append(df_2)
df_list.append(df_3)
df_list.append(df_4)

df = pd.concat(df_list)

for month in range(1,13):
    with open('estado_sexo_idade_2015_%s.json' % str(month).zfill(2),'w') as json_file:
        query = 'select "UF","SexoConsumidor","FaixaEtariaConsumidor",count("DataAtendimento") as "Quantidade" from df where strftime("%%m", "DataAtendimento") = "%s" group by "UF","SexoConsumidor","FaixaEtariaConsumidor";' % str(month).zfill(2)
        df_result = pysql(query)
        json_file.write(df_result.reset_index().to_json(orient='records'))
