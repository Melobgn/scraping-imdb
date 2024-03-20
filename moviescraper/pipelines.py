# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class MoviescraperPipeline:
    def convert_time(self, duration):
        print(f"Conversion de la durée: '{duration}'")  # Débogage
        parts = duration.split(' ')
        heures = 0
        minutes = 0
        for part in parts:
            if 'h' in part:
                heures = int(part.replace('h', '')) * 60
            elif 'm' in part:
                minutes = int(part.replace('m', ''))
        total_minutes = heures + minutes
        print(f"Total en minutes: {total_minutes}")  # Débogage
        return total_minutes
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        duration = self.convert_time(item.get('duration', '0'))
        adapter['duration'] = duration
        # Convertir le score en float si c'est une chaîne
        value_score = adapter.get('score')
        if value_score and isinstance(value_score, str):
            try:
                adapter['score'] = float(value_score)
            except ValueError:
                # Gérer le cas où la valeur ne peut pas être convertie en float
                pass

        # Convertir l'année en entier si c'est une chaîne
        value_year = adapter.get('year')
        if value_year and isinstance(value_year, str):
            try:
                adapter['year'] = int(value_year)
            except ValueError:
                # Gérer le cas où la valeur ne peut pas être convertie en int
                pass

        # Nettoyer la colonne "genre"
        genre_list = adapter.get('genre')
        if genre_list:
            # Vérifier si le dernier élément de la liste est "Back To Top"
            if genre_list[-1] == 'Back to top':
                # Supprimer le dernier élément de la liste
                adapter['genre'] = genre_list[:-1]

        
        return item
    
import sqlite3
from moviescraper.items import MovieItem, SerieItem

class SaveToSqlitePipeline:
    def __init__(self):
        self.con_movies = sqlite3.connect("movies.db")
        self.cur_movies = self.con_movies.cursor()
        self.cur_movies.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            score DECIMAL,
            genre TEXT,
            year INTEGER,
            duration INTEGER,
            description TEXT,
            top_cast TEXT,
            public TEXT,
            country TEXT,
            language TEXT
        )
        """)

        self.con_series = sqlite3.connect("series.db")
        self.cur_series = self.con_series.cursor()
        self.cur_series.execute("""
        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            score DECIMAL,
            genre TEXT,
            year INTEGER,
            duration INTEGER,
            description TEXT,
            top_cast TEXT,
            public TEXT,
            country TEXT,
            language TEXT
        )
        """)

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            cur = self.cur_movies
            table_name = "movies"
        elif isinstance(item, SerieItem):
            cur = self.cur_series
            table_name = "series"
        else:
            return item

        item["title"] = str(item["title"])
        item["description"] = str(item["description"])
        item["genre"] = str(item["genre"])
        item["top_cast"] = str(item["top_cast"])

        cur.execute(f"""
        INSERT INTO {table_name} (
            url,
            title,
            score,
            genre,
            year,
            duration,
            description,
            top_cast,
            public,
            country,
            language
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["url"],
            item["title"],
            item["score"],
            item["genre"],
            item["year"],
            item["duration"],
            item["description"],
            item["top_cast"],
            item["public"],
            item["country"],
            item["language"]
        ))

        if table_name == "movies":
            self.con_movies.commit()
        elif table_name == "series":
            self.con_series.commit()

        return item

    def close_spider(self, spider):
        self.cur_movies.close()
        self.con_movies.close()
        self.cur_series.close()
        self.con_series.close()
    
        
    

