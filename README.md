# 🎧 Big Data Project — Análise da Popularidade de Artistas com Base em Concertos

Este projeto analisa se os concertos realizados por artistas têm impacto na sua popularidade, usando dados da API Setlist.fm (concertos) e dados de streams públicos do Spotify (Spotify Charts).

---

## 📁 Estrutura Atual do Projeto

```
📁 BIGDATA/
├── .gitattributes
├── artist_analysis.csv           # Ficheiro completo com todos os concertos detalhados + resumo
├── artist_popularity_analysis.py # Script para extrair dados da API Setlist.fm
├── transformaCSV.py              # Script para processar os dados do Spotify
├── streams_spotify.csv           # Ficheiro de output com streams agregados por artista e semana
├── requirements.txt              # Lista de dependências
└── README.md                     # Descrição do projeto
```

---

## 🧠 Objetivo

Estudar se há um aumento de popularidade (medido por streams no Spotify) após a realização de concertos, para artistas específicos.

---

## 🧰 Tecnologias Utilizadas

- Python 3.x
- Pandas
- Requests
- Matplotlib
- MongoDB (via Compass)
- Setlist.fm API
- Spotify Charts (dataset CSV)

---

## ⚙️ Como Usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Extrair dados de concertos
```bash
python artist_popularity_analysis.py
```
Grava os dados em `artist_analysis.csv`.

### 3. Processar dados do Spotify Charts
```bash
python transformaCSV.py
```
Gera o ficheiro `streams_spotify.csv` com streams agregados por semana e artista.

---

## 🗃️ Integração com MongoDB

- Base de dados: `bigdata_project`
- Coleções:
  - `concerts` → Dados do `artist_analysis.csv`
  - `streams`  → Dados do `streams_spotify.csv`


## 📊 Análises Planeadas

- Evolução semanal de streams.
- Streams antes e depois de concertos.
- Correlação entre número de concertos e streams por semana.
- Gráficos com Matplotlib/Seaborn.

---

## 📘 Relatório

Inclui:
- Introdução e objetivos
- Metodologia e fontes de dados
- Resultados e visualizações
- Arquitetura do sistema (MongoDB, scripts Python)
- Conclusões

---

## 👥 Autores

- João Mendes, Duarte Chambas e Milan Geiantilal
- Licenciatura em Tecnologias Digitais - TDMA, TDSI
- Projeto final de Big Data — 2025
