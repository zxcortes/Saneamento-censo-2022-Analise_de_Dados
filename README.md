# 📊 Análise de Dados da Infraestrutura Sanitária Municipal no Brasil (Censo IBGE 2022)

Este repositório contém a pipeline completa de Engenharia e Análise de Dados desenvolvida para mapear a situação do saneamento básico nos **5.570 municípios brasileiros**, utilizando dados oficiais do Censo Demográfico 2022 do IBGE.

---

## 🎯 Objetivo do Trabalho
Mapear a infraestrutura sanitária municipal através de processos de ETL em Python, integração em banco de dados SQLite e consultas SQL, gerando indicadores para apoio à tomada de decisão e priorização de investimentos no **Marco Legal do Saneamento**.

---

## 🔄 Fluxo e Metodologia da Pipeline

1. **Coleta de Dados:** Extração das tabelas brutas de Água, Esgotamento e Lixo no portal SIDRA/IBGE (`bruto_agua_municipios.csv`, `bruto_esgoto_municipios.csv`, `bruto_lixo_municipios.csv`).
2. **Higienização & ETL (`código_etl.py`):**
   - Isolamento do código IBGE de 7 dígitos (`cod`) como Chave Primária única.
   - Tratamento de valores nulos e padronização de tipos de dados.
   - Geração das bases higienizadas (`t_Agua_Municipio.csv`, `t_Esgoto_Municipio.csv`, `t_Lixo_Municipio.csv`).
3. **Integração no SQLite:** Importação das bases tratadas para o ambiente de banco de dados relacional.
4. **Modelagem & Análise SQL (`consultas_saneamento.sql`):**
   - Criação da **VIEW consolidada** `vw_saneamento_consolidado` unindo as três tabelas via `INNER JOIN` pela Chave Primária (`cod`).
   - Cálculo de **12 indicadores individuais** percentuais utilizando `CAST AS FLOAT` para garantir precisão decimal.
   - Criação de **2 índices integrados**:
     - **IAP (Índice de Atendimento Pleno):** Média da cobertura adequada nos 3 serviços.
     - **IVST (Índice de Vulnerabilidade Sanitária Total):** Média dos déficits acumulados.
4. **Apresentação da Apresentação dos resultados das Analises (`Apresentacao_Resultados_Censo_2022.pptx`)**

---

## 🧮 Fórmulas dos Índices Integrados

```sql
-- Índice de Atendimento Pleno (IAP)
IAP = (p_cobertura_agua + p_cobertura_esgoto + p_coleta_lixo) / 3.0

-- Índice de Vulnerabilidade Sanitária Total (IVST)
IVST = (p_vulnerabilidade_hidrica + p_esgotamento_inadequado + p_descarte_inadequado) / 3.0
