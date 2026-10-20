import os
import pandas as pd


PASTA_DESTINO = r"C:\Users\Arão Côrtes\OneDrive\1.Meu_One_Drive\6.Faculdade_Senac\1° Semestre\5.4 - Mineracao de Dados\projeto_saneamento_2022\Arquivos_Tratados"

def extrair_uf_e_limpar_municipio(df, col_municipio):
    """Extrai a UF para uma nova coluna e remove a indicação (UF) do nome do município."""
    df['uf'] = df[col_municipio].str.extract(r'\(([A-Z]{2})\)')
    df['municipio'] = df[col_municipio].str.replace(r'\s*\([A-Z]{2}\)', '', regex=True)
    return df

# EXTRAÇÃO

try:
    print('--- ⚠️ Iniciando ETL dos DataSets ⚠️ --- \n')

    print(' 🚽 Lendo DataSet Esgoto_Municipios')
    df_esgoto_bruto = pd.read_csv('esgoto_municipios.csv', sep=';', header=4, encoding='utf-8-sig')

    print(' 💧 Lendo DataSet Agua_Municipios')
    df_agua_bruto = pd.read_csv('agua_municipios.csv', sep=';', header=None, names=list(range(21)), encoding='utf-8-sig')

    print(' 🗑️ Lendo DataSet Lixo_Municipios')
    df_lixo_bruto = pd.read_csv('lixo_municipios.csv', sep=';', header=4, encoding='utf-8-sig')

    print(' ✅ Arquivos carregados com sucesso!\n')

except Exception as e:
    print(f' ❌ Erro no carregamento dos dados: {e} ❌')
    raise SystemExit(e)

# ==========================================
# TRATAMENTO: ESGOTO
# ==========================================
print(' ⚙️  Tratando dados de Esgoto...')

df_esgoto = df_esgoto_bruto.iloc[:5570].copy().reset_index(drop=True)

col_cod_esgoto = df_esgoto.columns[0]
col_mun_esgoto = df_esgoto.columns[1]

df_esgoto = df_esgoto.rename(columns={
    col_cod_esgoto: 'cod',
    col_mun_esgoto: 'municipio_esgoto',
    'Total': 'total_esgoto',
    'Rede geral ou pluvial': 'rede_geral_ou_pluvial_esgoto',
    'Fossa séptica ou fossa filtro não ligada à rede': 'fossa_septica_ou_fossa_filtro_nao_ligada_a_rede_esgoto',
    'Fossa rudimentar ou buraco': 'fossa_rudimentar_ou_buraco_esgoto',
    'Vala': 'vala_esgoto',
    'Rio, lago, córrego ou mar': 'rio_lago_corrego_ou_mar_esgoto',
    'Não tinham banheiro nem sanitário': 'nao_tinham_banheiro_nem_sanitario_esgoto'
})

# Extrai UF e cria 'municipio' limpo
df_esgoto = extrair_uf_e_limpar_municipio(df_esgoto, 'municipio_esgoto')

# Remove coluna redundante e reordena (cod, municipio, uf)
df_esgoto = df_esgoto.drop(columns=['municipio_esgoto'])
col_mun_esg = df_esgoto.pop('municipio')
col_uf_esg = df_esgoto.pop('uf')
df_esgoto.insert(1, 'municipio', col_mun_esg)
df_esgoto.insert(2, 'uf', col_uf_esg)

# ==========================================
# TRATAMENTO: ÁGUA
# ==========================================
print(' ⚙️  Tratando dados de Água...')

df_agua = df_agua_bruto.drop(index=[0, 1, 2, 3]).reset_index(drop=True)
df_agua.columns = df_agua.iloc[0]

df_agua = df_agua.drop(index=0).iloc[:5570].reset_index(drop=True).rename(columns={
    'Cód.': 'cod',
    'Município': 'municipio_agua',
    'Total': 'total_agua',
    'Possui ligação à rede geral e a utiliza como forma principal': 'rede_geral_principal_agua',
    'Possui ligação à rede geral, mas utiliza principalmente outra forma': 'rede_geral_outra_forma_agua',
    'Possui ligação à rede geral, mas utiliza principalmente outra forma - Poço profundo ou artesiano': 'rede_geral_poco_profundo_artesiano_agua',
    'Possui ligação à rede geral, mas utiliza principalmente outra forma - Poço raso, freático ou cacimba': 'rede_geral_poco_raso_cacimba_agua',
    'Possui ligação à rede geral, mas utiliza principalmente outra forma - Fonte, nascente ou mina': 'rede_geral_fonte_nascente_mina_agua',
    'Possui ligação à rede geral, mas utiliza principalmente outra forma - Carro-pipa': 'rede_geral_carro_pipa_agua',
    'Possui ligação à rede geral, mas utiliza principalmente outra forma - Água da chuva armazenada': 'rede_geral_agua_chuva_agua',
    'Possui ligação à rede geral, mas utiliza principalmente outra forma - Rios, açudes, córregos, lagos e igarapés': 'rede_geral_rios_lacos_corregos_agua',
    'Possui ligação à rede geral, mas utiliza principalmente outra forma - Outra': 'rede_geral_outra_agua',
    'Não possui ligação com a rede geral': 'sem_rede_geral_total_agua',
    'Não possui ligação com a rede geral - Poço profundo ou artesiano': 'sem_rede_geral_poco_profundo_artesiano_agua',
    'Não possui ligação com a rede geral - Poço raso, freático ou cacimba': 'sem_rede_geral_poco_raso_cacimba_agua',
    'Não possui ligação com a rede geral - Fonte, nascente ou mina': 'sem_rede_geral_fonte_nascente_mina_agua',
    'Não possui ligação com a rede geral - Carro-pipa': 'sem_rede_geral_carro_pipa_agua',
    'Não possui ligação com a rede geral - Água da chuva armazenada': 'sem_rede_geral_agua_chuva_agua',
    'Não possui ligação com a rede geral - Rios, açudes, córregos, lagos e igarapés': 'sem_rede_geral_rios_lagos_corregos_agua',
    'Não possui ligação com a rede geral - Outra': 'sem_rede_geral_outra_agua'
})

df_agua = extrair_uf_e_limpar_municipio(df_agua, 'municipio_agua')

# Remove coluna redundante e reordena (cod, municipio, uf)
df_agua = df_agua.drop(columns=['municipio_agua'])
col_mun_ag = df_agua.pop('municipio')
col_uf_ag = df_agua.pop('uf')
df_agua.insert(1, 'municipio', col_mun_ag)
df_agua.insert(2, 'uf', col_uf_ag)

# ==========================================
# TRATAMENTO: LIXO
# ==========================================
print(' ⚙️  Tratando dados de Lixo...')

df_lixo = df_lixo_bruto.iloc[:5570].copy().reset_index(drop=True)

col_cod_lixo = df_lixo.columns[0]
col_mun_lixo = df_lixo.columns[1]

df_lixo = df_lixo.rename(columns={
    col_cod_lixo: 'cod',
    col_mun_lixo: 'municipio_lixo',
    'Total': 'total_lixo',
    'Coletado': 'coletado_lixo',
    'Coletado no domicílio por serviço de limpeza': 'coletado_no_domicilio_por_servico_de_limpeza_lixo',
    'Depositado em caçamba de serviço de limpeza': 'depositado_em_cacamba_de_servico_de_limpeza_lixo',
    'Queimado na propriedade': 'queimado_na_propriedade_lixo',
    'Enterrado na propriedade': 'enterrado_na_propriedade_lixo',
    'Jogado em terreno baldio, encosta ou área pública': 'jogado_em_terreno_baldio_encosta_ou_area_publica_lixo',
    'Outro destino': 'outro_destino_lixo'
})

# Extrai UF e cria 'municipio' limpo
df_lixo = extrair_uf_e_limpar_municipio(df_lixo, 'municipio_lixo')

# Remove coluna redundante e reordena (cod, municipio, uf)
df_lixo = df_lixo.drop(columns=['municipio_lixo'])
col_mun_lx = df_lixo.pop('municipio')
col_uf_lx = df_lixo.pop('uf')
df_lixo.insert(1, 'municipio', col_mun_lx)
df_lixo.insert(2, 'uf', col_uf_lx)

# ==========================================
# EXPORTAÇÃO DOS DADOS
# ==========================================
try:
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    print('\n💾 Salvando arquivos...')

    df_esgoto.to_csv(os.path.join(PASTA_DESTINO, 't_Esgoto_Municipio.csv'), index=False, encoding='utf-8-sig')
    print('  ✅ t_Esgoto_Municipio.csv')

    df_agua.to_csv(os.path.join(PASTA_DESTINO, 't_Agua_Municipio.csv'), index=False, encoding='utf-8-sig')
    print('  ✅ t_Agua_Municipio.csv')

    df_lixo.to_csv(os.path.join(PASTA_DESTINO, 't_Lixo_Municipio.csv'), index=False, encoding='utf-8-sig')
    print('  ✅ t_Lixo_Municipio.csv')

    print('\n  ✅ ETL Finalizado com Sucesso! ✅')

except Exception as e:
    print(f'-- 🚫 -- Falha ao salvar os arquivos tratados! Erro: {e}')