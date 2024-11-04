import time
import pandas as pd
import glob

# Definir os códigos de família de CBO e grupo de CNAE para o filtro
cbo_familia = ('1236', '1425', '2122', '2124', '3171', '3172', '2123')
cnae_grupo = ('620', '631')

print("###################################\n")
print("Separação de dados RAIS - Filtrando para Sorocaba\n")

sum_dados = 0
processar = False

# Loop para escolha do ano e do filtro de TI
while not processar:
    ano = str(input("Escolha o ano: 2012 ou 2013 ou 2014 ou 2015 ou 2016 ou 2017 ou 2018 ou 2019 ou 2020 ou 2021 ou 2022: "))
    filtro_setor = input("Realizar filtro por setores de TI (S)/(N): ")

    # Anos de 2012 a 2017
    if ano in ('2012', '2013', '2014', '2015', '2016', '2017'):
        processar = True
        colunas_remover = [
            'Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Causa Afastamento 1', 'Causa Afastamento 2', 'Causa Afastamento 3',
            'Motivo Desligamento', 'CNAE 95 Classe', 'Distritos SP', 'Faixa Etária', 'Faixa Hora Contrat', 'Faixa Remun Dezem (SM)',
            'Faixa Remun Média (SM)', 'Faixa Tempo Emprego', 'Qtd Hora Contr', 'Ind CEI Vinculado', 'Ind Simples', 'Mês Admissão',
            'Mês Desligamento', 'Mun Trab', 'Município', 'Nacionalidade', 'Natureza Jurídica', 'Ind Portador Defic', 'Qtd Dias Afastamento',
            'Regiões Adm DF', 'Vl Remun Dezembro (SM)', 'Vl Remun Média Nom', 'Vl Remun Média (SM)', 'CNAE 2.0 Subclasse',
            'Tamanho Estabelecimento', 'Tempo Emprego', 'Tipo Admissão', 'Tipo Estab', 'Tipo Estab.1', 'Tipo Defic', 'Tipo Vínculo'
        ]
    # Anos de 2018 a 2022
    elif ano in ('2018', '2019', '2020', '2021', '2022'):
        processar = True
        colunas_remover = [
            'Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Causa Afastamento 1', 'Causa Afastamento 2', 'Causa Afastamento 3',
            'Motivo Desligamento', 'CNAE 95 Classe', 'Distritos SP', 'Faixa Etária', 'Faixa Hora Contrat', 'Faixa Remun Dezem (SM)',
            'Faixa Remun Média (SM)', 'Faixa Tempo Emprego', 'Qtd Hora Contr', 'Ind CEI Vinculado', 'Ind Simples', 'Mês Admissão',
            'Mês Desligamento', 'Mun Trab', 'Nacionalidade', 'Natureza Jurídica', 'Ind Portador Defic', 'Qtd Dias Afastamento',
            'Regiões Adm DF', 'Vl Remun Dezembro (SM)', 'Vl Remun Média Nom', 'Vl Remun Média (SM)', 'CNAE 2.0 Subclasse',
            'Tamanho Estabelecimento', 'Tempo Emprego', 'Tipo Admissão', 'Tipo Estab', 'Tipo Estab.1', 'Tipo Defic', 'Tipo Vínculo',
            'IBGE Subsetor', 'Vl Rem Janeiro CC', 'Vl Rem Fevereiro CC', 'Vl Rem Março CC', 'Vl Rem Abril CC', 'Vl Rem Maio CC',
            'Vl Rem Junho CC', 'Vl Rem Julho CC', 'Vl Rem Agosto CC', 'Vl Rem Setembro CC', 'Vl Rem Outubro CC',
            'Vl Rem Novembro CC', 'Ano Chegada Brasil', 'Ind Trab Intermitente', 'Ind Trab Parcial'
        ]

        uf = {
            '11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO', '21': 'MA',
            '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL', '28': 'SE', '29': 'BA',
            '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP', '41': 'PR', '42': 'SC', '43': 'RS', '50': 'MS',
            '51': 'MT', '52': 'GO', '53': 'DF'
        }
    else:
        print("Ano inválido!")

print("\nProcessando...")

tempo_inicial = time.time()

# Definindo o caminho dos arquivos de acordo com o ano
if ano in ('2012', '2013', '2014', '2015', '2016', '2017','2018','2019','2020','2021','2022'):
    list_files = glob.glob("C:/Users/Mikael Lenartevitz/Downloads/Cris projeto de pesquisa/Cris estagio/RAIS" + ano + "/*.txt")
else:
    list_files = glob.glob("C:/Users/Mikael Lenartevitz/Downloads/Cris projeto de pesquisa/Cris estagio/RAIS" + ano + "/*.txt")
for file in list_files:
    # Leitura do CSV do estado ou região atual:
    df = pd.read_csv(file, sep=";", encoding='latin-1', dtype=object)

    # Elimina as colunas na lista colunas_remover:
    df.drop(colunas_remover, inplace=True, axis=1)

    # Filtra somente com vínculo ativo 31/12:
    df = df[df["Vínculo Ativo 31/12"] == '1']

    # Retira a coluna anterior do vínculo, que não é mais necessária:
    df.drop("Vínculo Ativo 31/12", inplace=True, axis=1)
    
    # Retira salários zerados:
    df = df[df["Vl Remun Dezembro Nom"] != '0000000000,00']

    # Transforma as remunerações em flutuante:
    df['Vl Remun Dezembro Nom'] = df['Vl Remun Dezembro Nom'].str.lstrip('0')       # Tira zero à esquerda
    df['Vl Remun Dezembro Nom'] = df['Vl Remun Dezembro Nom'].str.replace(',', '.')  # Substitui a vírgula por ponto

    # Realiza o filtro pelas famílias de CBOs:
    df = df[df["CBO Ocupação 2002"].str.startswith(cbo_familia)]

    # Realiza o filtro dos setores de TI, caso escolhido a opção:
    if filtro_setor == 'S':
        df = df[df["CNAE 2.0 Classe"].str.startswith(cnae_grupo)]

    # Filtro para o município de Sorocaba (código IBGE: 3552205)
    df = df[df["Mun Trab"] == '3552205']

    # Exibe o total de dados separados para o arquivo atual:
    sum_dados += len(df)
    print("\nTotal de casos separados: " + str(len(df)) + "\npara o arquivo: " + file)

    # Salva em um novo csv para o estado atual:
    df.to_csv("C:/Users/Mikael Lenartevitz/Downloads/Cris projeto de pesquisa/Cris estagio/sorocaba/" + file[-10:-4] + ".csv", index=False, sep=';', encoding='utf-8')


# Realiza a leitura de cada arquivo CSV e junta em um só
print("\nSalvando o arquivo final...\n")

list_files = glob.glob("C:/Users/Mikael Lenartevitz/Downloads/Cris projeto de pesquisa/Cris estagio/sorocaba/*.csv")

df_final = pd.read_csv(list_files[0], sep=";", encoding='utf-8', dtype=object)
del list_files[0]

for file in list_files:
    df = pd.read_csv(file, sep=";", encoding='utf-8', dtype=object)
    df_final = pd.concat([df_final, df], ignore_index=True, sort=False)

if filtro_setor == 'S':
    df_final.to_csv("./data/raw/DATA_RAIS_SETORTI_SOROCABA_" + ano + ".csv", index=False, sep=";", encoding='utf-8')
else:
    df_final.to_csv("./data/raw/DATA_RAIS_GERAL_SOROCABA_" + ano + ".csv", index=False, sep=";", encoding='utf-8')

tempo_final = time.time()
print("\nTotal de itens: " + str(sum_dados))
print("\n{:.1f} segundos".format(tempo_final - tempo_inicial))

print("\n###################################")
