import requests
import redis
import matplotlib.pyplot as plt
import json

class DataHandler:
    """Class to handle Redis operations."""
    
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initializes the Redis connection.
        
        :param host: Redis host
        :param port: Redis port
        :param db: Redis database
        """
        self.redis = redis.Redis(host=host, port=port, db=db)

    def insert_data(self, key, data):
        """
        Inserts data into Redis.
        
        :param key: Redis key
        :param data: Data to insert, expected in JSON format
        """
        self.redis.set(key, json.dumps(data))

    def fetch_data(self, key):
        """
        Fetches data from Redis.
        
        :param key: Redis key to fetch the data
        :return: Data associated with the key in JSON format
        """
        data = self.redis.get(key)
        return json.loads(data) if data else None

class DataProcessor:
    """Class to process data."""
    
    def __init__(self, data):
        """
        Initializes the DataProcessor with data.
        
        :param data: Data to process
        """
        self.data = data

    def generate_charts(self):
        """Generates and saves two charts based on Ditto's stats."""
        stats = [stat['base_stat'] for stat in self.data['stats']]
        stat_names = [stat['stat']['name'] for stat in self.data['stats']]

        # Chart 1: Base Stats of Ditto
        plt.figure(figsize=(8, 4))
        plt.bar(stat_names, stats, color='purple')
        plt.title('Base Stats of Ditto')
        plt.xlabel('Stat')
        plt.ylabel('Base Stat Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('ditto_base_stats.png')

       # Chart 2: Visualization of Ditto's Ability Count
        abilities = [ability['ability']['name'] for ability in self.data['abilities']]
        ability_counts = [1] * len(abilities)  # Simplified for illustration; each ability counts as one

        plt.figure()
        plt.bar(abilities, ability_counts, color='green')
        plt.title('Abilities of Ditto')
        plt.xlabel('Ability')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('ditto_abilities.png')

    def aggregate_data(self):
        """Aggregates the base stats for Ditto."""
        return sum(stat['base_stat'] for stat in self.data['stats'])

    def search_data(self, stat_name):
        """Finds a specific stat value for Ditto."""
        for stat in self.data['stats']:
            if stat['stat']['name'] == stat_name:
                return stat['base_stat']
        return None

# Main execution flow
api_url = 'https://pokeapi.co/api/v2/pokemon/ditto'
response = requests.get(api_url)
api_data = response.json()

# Handling data with Redis
redis_handler = DataHandler()
redis_key = 'ditto_data'
redis_handler.insert_data(redis_key, api_data)
retrieved_data = redis_handler.fetch_data(redis_key)

# Generate charts
data_processor = DataProcessor(retrieved_data)
data_processor.generate_charts()

# Aggregate data
total_base_stats = data_processor.aggregate_data()

# Search for a specific stat
stat_to_search = 'speed'
stat_value = data_processor.search_data(stat_to_search)

print(f"Total Base Stats: {total_base_stats}")
print(f"Value of {stat_to_search} stat: {stat_value}")
