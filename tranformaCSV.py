import pandas as pd

# 1. Lê o CSV dos Spotify Charts
charts_df = pd.read_csv("spotify_charts.csv")

# Converte explicitamente a coluna "date" para datetime
charts_df["date"] = pd.to_datetime(charts_df["date"], errors="coerce")

# Remove linhas com datas inválidas
charts_df = charts_df.dropna(subset=["date"])

# 2. Adiciona coluna 'week' para agregação
charts_df["week"] = charts_df["date"].dt.to_period("W").dt.start_time

# 3. Agrupa por artista + semana
weekly_streams = (
    charts_df.groupby(["artists", "week"])["streams"]
    .sum()
    .reset_index()
    .rename(columns={"artists": "artist_name"})
)

# 4. Guarda para MongoDB
weekly_streams.to_csv("streams_spotify.csv", index=False)
print("✅ Ficheiro 'streams_for_mongo.csv' criado com sucesso.")
