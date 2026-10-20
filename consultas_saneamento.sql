-- ============================================================
-- PROJETO: Análise de Dados de Saneamento Básico (Censo 2022)
-- AUTOR: Arão de Almeida Côrtes
-- BANCO DE DADOS: SQLite
-- ============================================================

-- 1. CONSULTAS DE INDICADORES INDIVIDUAIS POR TABELA

-- 1.1. Indicadores de Água (t_Agua_Municipio)
SELECT 
    cod,
    municipio,
    uf,
    ROUND(CAST(rede_geral_principal_agua AS FLOAT) / total_agua * 100, 2) AS p_cobertura_agua,
    ROUND(CAST(sem_rede_geral_total_agua AS FLOAT) / total_agua * 100, 2) AS p_vulnerabilidade_hidrica,
    ROUND(CAST(carro_pipa_agua AS FLOAT) / total_agua * 100, 2) AS p_dependencia_carro_pipa,
    ROUND(CAST(pocos_nascentes_agua AS FLOAT) / total_agua * 100, 2) AS p_pocos_nascentes
FROM t_Agua_Municipio;

-- 1.2. Indicadores de Esgoto (t_Esgoto_Municipio)
SELECT 
    cod,
    municipio,
    uf,
    ROUND(CAST(rede_geral_ou_pluvial_esgoto AS FLOAT) / total_esgoto * 100, 2) AS p_cobertura_esgoto,
    ROUND(CAST((fossa_rudimentar_ou_buraco_esgoto + vala_esgoto + rio_lago_corrego_ou_mar_esgoto + nao_tinham_banheiro_nem_sanitario_esgoto) AS FLOAT) / total_esgoto * 100, 2) AS p_esgotamento_inadequado,
    ROUND(CAST(fossa_septica_esgoto AS FLOAT) / total_esgoto * 100, 2) AS p_fossa_septica,
    ROUND(CAST(nao_tinham_banheiro_nem_sanitario_esgoto AS FLOAT) / total_esgoto * 100, 2) AS p_sem_banheiro
FROM t_Esgoto_Municipio;

-- 1.3. Indicadores de Lixo (t_Lixo_Municipio)
SELECT 
    cod,
    municipio,
    uf,
    ROUND(CAST(coletado_lixo AS FLOAT) / total_lixo * 100, 2) AS p_coleta_lixo,
    ROUND(CAST((queimado_na_propriedade_lixo + enterrado_na_propriedade_lixo + jogado_em_terreno_baldio_encosta_ou_area_publica_lixo + outro_destino_lixo) AS FLOAT) / total_lixo * 100, 2) AS p_descarte_inadequado,
    ROUND(CAST(queimado_na_propriedade_lixo AS FLOAT) / total_lixo * 100, 2) AS p_lixo_queimado,
    ROUND(CAST(jogado_em_terreno_baldio_encosta_ou_area_publica_lixo AS FLOAT) / total_lixo * 100, 2) AS p_lixo_terreno_baldio
FROM t_Lixo_Municipio;


-- 2. CRIAÇÃO DA VIEW CONSOLIDADA

CREATE VIEW IF NOT EXISTS vw_saneamento_consolidado AS
SELECT 
    a.cod,
    a.municipio,
    a.uf,
    a.total_agua,
    a.rede_geral_principal_agua,
    a.sem_rede_geral_total_agua,
    a.carro_pipa_agua,
    a.pocos_nascentes_agua,
    e.total_esgoto,
    e.rede_geral_ou_pluvial_esgoto,
    e.fossa_septica_esgoto,
    e.fossa_rudimentar_ou_buraco_esgoto,
    e.vala_esgoto,
    e.rio_lago_corrego_ou_mar_esgoto,
    e.nao_tinham_banheiro_nem_sanitario_esgoto,
    l.total_lixo,
    l.coletado_lixo,
    l.queimado_na_propriedade_lixo,
    l.enterrado_na_propriedade_lixo,
    l.jogado_em_terreno_baldio_encosta_ou_area_publica_lixo,
    l.outro_destino_lixo
FROM t_Agua_Municipio a
INNER JOIN t_Esgoto_Municipio e ON a.cod = e.cod
INNER JOIN t_Lixo_Municipio l ON a.cod = l.cod;


-- 3. CONSULTA CONSOLIDADA DOS ÍNDICES INTEGRADOS (IAP E IVST)

WITH IndicadoresBase AS (
    SELECT 
        cod,
        municipio,
        uf,
        ROUND(CAST(rede_geral_principal_agua AS FLOAT) / total_agua * 100, 2) AS p_cobertura_agua,
        ROUND(CAST(sem_rede_geral_total_agua AS FLOAT) / total_agua * 100, 2) AS p_vulnerabilidade_hidrica,
        ROUND(CAST(carro_pipa_agua AS FLOAT) / total_agua * 100, 2) AS p_dependencia_carro_pipa,
        ROUND(CAST(pocos_nascentes_agua AS FLOAT) / total_agua * 100, 2) AS p_pocos_nascentes,
        ROUND(CAST(rede_geral_ou_pluvial_esgoto AS FLOAT) / total_esgoto * 100, 2) AS p_cobertura_esgoto,
        ROUND(CAST((fossa_rudimentar_ou_buraco_esgoto + vala_esgoto + rio_lago_corrego_ou_mar_esgoto + nao_tinham_banheiro_nem_sanitario_esgoto) AS FLOAT) / total_esgoto * 100, 2) AS p_esgotamento_inadequado,
        ROUND(CAST(fossa_septica_esgoto AS FLOAT) / total_esgoto * 100, 2) AS p_fossa_septica,
        ROUND(CAST(nao_tinham_banheiro_nem_sanitario_esgoto AS FLOAT) / total_esgoto * 100, 2) AS p_sem_banheiro,
        ROUND(CAST(coletado_lixo AS FLOAT) / total_lixo * 100, 2) AS p_coleta_lixo,
        ROUND(CAST((queimado_na_propriedade_lixo + enterrado_na_propriedade_lixo + jogado_em_terreno_baldio_encosta_ou_area_publica_lixo + outro_destino_lixo) AS FLOAT) / total_lixo * 100, 2) AS p_descarte_inadequado,
        ROUND(CAST(queimado_na_propriedade_lixo AS FLOAT) / total_lixo * 100, 2) AS p_lixo_queimado,
        ROUND(CAST(jogado_em_terreno_baldio_encosta_ou_area_publica_lixo AS FLOAT) / total_lixo * 100, 2) AS p_lixo_terreno_baldio
    FROM vw_saneamento_consolidado
)
SELECT 
    *,
    ROUND((p_cobertura_agua + p_cobertura_esgoto + p_coleta_lixo) / 3.0, 2) AS iap_atendimento_pleno,
    ROUND((p_vulnerabilidade_hidrica + p_esgotamento_inadequado + p_descarte_inadequado) / 3.0, 2) AS ivst_vulnerabilidade_total
FROM IndicadoresBase;
