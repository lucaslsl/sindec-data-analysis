import pandas as pd
import pandasql as pdsql

df = pd.DataFrame()

pysql = lambda q: pdsql.sqldf(q, globals())

columns_names = [
	'AnoAtendimento',
	'TrimestreAtendimento',
	'MesAtendimento',
	'DataAtendimento',
	'CodigoRegiao',
	'Regiao',
	'UF',
	'CodigoTipoAtendimento',
	'DescricaoTipoAtendimento',
	'CodigoAssunto',
	'DescricaoAssunto',
	'GrupoAssunto',
	'CodigoProblema',
	'DescricaoProblema',
	'GrupoProblema',
	'SexoConsumidor',
	'FaixaEtariaConsumidor',
	'CEPConsumidor']

df_1 = pd.read_csv('data/Boletim_Sindec_Atendimento_1o_Trimestre_2014.csv', delimiter=';', names=columns_names)
df_2 = pd.read_csv('data/Boletim_Sindec_Atendimento_2o_Trimestre_2014.csv', delimiter=';', names=columns_names)
df_3 = pd.read_csv('data/Boletim_Sindec_Atendimento_3o_Trimestre_2014.csv', delimiter=';', names=columns_names)
df_4 = pd.read_csv('data/Boletim_Sindec_Atendimento_4o_Trimestre_2014.csv', delimiter=';', names=columns_names)

df_list = []
df_list.append(df_1)
df_list.append(df_2)
df_list.append(df_3)
df_list.append(df_4)

df = pd.concat(df_list)

for month in range(1,13):
    with open('data/estado_sexo_idade_2014_%s.json' % str(month).zfill(2),'w') as json_file:
        query = 'select "UF","SexoConsumidor","FaixaEtariaConsumidor",count("DataAtendimento") as "Quantidade" from df where strftime("%%m", "DataAtendimento") = "%s" group by "UF","SexoConsumidor","FaixaEtariaConsumidor";' % str(month).zfill(2)
        df_result = pysql(query)
        json_file.write(df_result.reset_index().to_json(orient='records'))
