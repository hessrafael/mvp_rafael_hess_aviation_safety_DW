# Pós-Graduação Ciência de Dados e Analytics - PUCRio - Sprint 2 - Engenharia de Dados

## Autor: Rafael Hess Almaleh
## Data: 12/07/2024

Projeto MVP da disciplina de Engenharia de Dados para criação de pipeline de dados e construção de Datawarehouse na nuvem (Databricks) para análise de dados históricos de acidentes aéreos

> [!IMPORTANT]
>  O **relatório do projeto** está presente na **Wiki** deste projeto disponível para avaliação (https://github.com/hessrafael/mvp_rafael_hess_aviation_safety_DW/wiki)


- Na pasta **"Notebooks Databricks"** está presente a estrutura de pastas utilizadas no Databricks e todos os notebooks utilizados na execução do projeto com seus outputs

  
- Na pasta **"data"** estão presentes os 3 arquivos csv resultantes do código de webscraping. Esses arquivos estão presentes em modo público no Google Drive:
    - accidents_data: https://drive.google.com/file/d/1GiY52XA1ZWqZArdZF4GEBAah9JVp-yp9/view?usp=sharing
    - countries_data: https://drive.google.com/file/d/1p9mhGiq_MpRTQjr-J2hTJW7UHgz8cq35/view?usp=sharing
    - aircrafts_data: https://drive.google.com/file/d/1SVPyBi0bUfXBlbm2C4AofmEgTqppfhq4/view?usp=sharing


- Na pasta **"Scraper"** está presente o código que realiza o webscraping e cria os csvs
    - Recomenda-se o uso de ambientes virtuais para execução do código com o comando

      ```python -m venv env```
      
    - Ativação do ambiente com o comando ```.\env\Scripts\activate ```
    - Instalar os requirements.txt com o comando ```pip install -r .\requirements.txt```
    - Rodar o código accidents_scrapper.py com o comando ``` py .\accidents_scraper.py  ```
