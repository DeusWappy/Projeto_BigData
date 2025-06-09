import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import csv

class SetlistFMAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.setlist.fm/rest/1.0"
        self.headers = {
            "x-api-key": api_key,
            "Accept": "application/json"
        }

    def search_artist(self, artist_name):
        print(f"\n🔍 Searching for artist: {artist_name}")
        url = f"{self.base_url}/search/artists"
        params = {
            "artistName": artist_name,
            "sort": "relevance"
        }

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("artist"):
                artist_data = data["artist"][0]
                print(f"✅ Found artist: {artist_data.get('name')} (MBID: {artist_data.get('mbid')})")
                return artist_data["mbid"]
            else:
                print("❌ No artist found with that name")
        else:
            print(f"❌ Error in API response: {response.status_code}")
        return None

    def get_artist_setlists(self, mbid, page=1):
        url = f"{self.base_url}/artist/{mbid}/setlists"
        params = {"p": page}

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error fetching setlists: {response.status_code}")
        return None

    def analyze_popularity(self, artist_name):
        print(f"\n🎵 Starting analysis for {artist_name}")
        mbid = self.search_artist(artist_name)
        if not mbid:
            return None, None

        all_setlists = []
        page = 1
        while True:
            data = self.get_artist_setlists(mbid, page)
            if not data or not data.get("setlist"):
                break

            all_setlists.extend(data["setlist"])
            if page >= data.get("total", 0):
                break
            page += 1
            time.sleep(1)

        if not all_setlists:
            print(f"❌ No setlists found for {artist_name}")
            return None, None

        concerts_data = []
        for i, setlist in enumerate(all_setlists, 1):
            try:
                date = datetime.strptime(setlist["eventDate"], "%d-%m-%Y")
                venue = setlist.get("venue", {})
                venue_name = venue.get("name", "Unknown Venue")
                city = venue.get("city", {}).get("name", "Unknown City")
                country = venue.get("city", {}).get("country", {}).get("name", "Unknown Country")

                concerts_data.append({
                    "date": date,
                    "venue": venue_name,
                    "city": city,
                    "country": country
                })
            except (ValueError, KeyError):
                continue

        df = pd.DataFrame(concerts_data)
        if df.empty:
            print("❌ No valid concert data found")
            return None, None

        df = df.sort_values("date")
        df = df[df['date'].dt.year >= 2006]  # filter from 2006 onward

        summary = {
            "artist_name": artist_name,
            "total_concerts": len(df),
            "first_concert": df["date"].min().date(),
            "last_concert": df["date"].max().date(),
            "countries_visited": df["country"].nunique(),
            "cities_visited": df["city"].nunique(),
            "venues_played": df["venue"].nunique(),
            "years_active": (df["date"].max() - df["date"].min()).days / 365.25
        }

        return summary, df


def save_to_csv(summary_data, detailed_df, filename="artist_analysis.csv"):
    print(f"\n💾 Saving combined data to {filename}")

    for key, value in summary_data.items():
        detailed_df[key] = value

    cols = [
        "artist_name", "date", "venue", "city", "country",
        "total_concerts", "first_concert", "last_concert",
        "countries_visited", "cities_visited", "venues_played", "years_active"
    ]
    detailed_df = detailed_df[cols]

    file_exists = False
    try:
        with open(filename, 'r') as f:
            file_exists = True
            print("   Appending to existing file")
    except FileNotFoundError:
        print("   Creating new file")

    detailed_df.to_csv(filename, mode='a', index=False, header=not file_exists)
    print("✅ Saved all detailed data to CSV")


def main():
    print("🎸 Setlist.fm Artist Analyzer")
    print("-----------------------------")

    API_KEY = "gyyHPxxEa_693ucEkE5yTjXj9m1SebkEvGJe"
    analyzer = SetlistFMAnalyzer(API_KEY)

    while True:
        artist_name = input("\n👉 Enter artist name to analyze (or 'quit' to exit): ")
        if artist_name.lower() == 'quit':
            print("\n👋 Goodbye!")
            break

        summary, df = analyzer.analyze_popularity(artist_name)
        if summary is not None and df is not None:
            save_to_csv(summary, df)

            print("\n📊 Analysis Summary:")
            print("------------------")
            print(f"Artist: {summary['artist_name']}")
            print(f"Total concerts: {summary['total_concerts']}")
            print(f"Date range: {summary['first_concert']} to {summary['last_concert']}")
            print(f"Years active: {summary['years_active']:.1f}")
            print(f"Countries visited: {summary['countries_visited']}")
            print(f"Cities visited: {summary['cities_visited']}")
            print(f"Venues played: {summary['venues_played']}")

if __name__ == "__main__":
    main()
