import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client
import time

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def generate_realistic_search_queries():
    """Generate a list of realistic search queries with categories."""
    return {
        'programming': [
            'python tutorial', 'javascript basics', 'react hooks tutorial',
            'sql commands', 'django rest framework', 'node.js express',
            'vue.js components', 'typescript basics', 'golang tutorial'
        ],
        'tools': [
            'vs code extensions', 'git commands', 'docker compose example',
            'kubernetes tutorial', 'jenkins pipeline', 'nginx configuration',
            'postman api testing', 'aws cli commands', 'terraform basics'
        ],
        'concepts': [
            'microservices architecture', 'ci/cd pipeline', 'test driven development',
            'agile methodology', 'design patterns', 'clean code principles',
            'system design basics', 'database indexing', 'caching strategies'
        ]
    }

def generate_time_based_activity(hour):
    """Generate activity multiplier based on time of day."""
    # Simulate higher activity during work hours
    if 9 <= hour <= 17:  # 9 AM to 5 PM
        return random.uniform(1.5, 2.5)
    elif 6 <= hour <= 8 or 18 <= hour <= 22:  # Early morning and evening
        return random.uniform(0.8, 1.5)
    else:  # Night time
        return random.uniform(0.3, 0.8)

def generate_realistic_metrics(query_type, activity_multiplier):
    """Generate realistic metrics based on query type and activity."""
    base_impressions = {
        'programming': (100, 500),
        'tools': (50, 300),
        'concepts': (30, 200)
    }

    min_imp, max_imp = base_impressions[query_type]
    impressions = int(random.randint(min_imp, max_imp) * activity_multiplier)
    
    # CTR varies by query type
    ctr_ranges = {
        'programming': (0.05, 0.15),
        'tools': (0.03, 0.12),
        'concepts': (0.02, 0.10)
    }
    
    min_ctr, max_ctr = ctr_ranges[query_type]
    ctr = random.uniform(min_ctr, max_ctr)
    
    clicks = int(impressions * ctr)
    return impressions, clicks, ctr

def generate_dummy_data(days=30, batch_size=100):
    """Generate dummy data for the specified number of days."""
    queries_by_category = generate_realistic_search_queries()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    total_records = 0
    print(f"Starting data generation for {days} days...")
    
    current_date = start_date
    while current_date <= end_date:
        batch_data = []
        
        # Generate data for each hour of the day
        for hour in range(24):
            activity_multiplier = generate_time_based_activity(hour)
            
            # Generate data for each category and its queries
            for category, queries in queries_by_category.items():
                for query in queries:
                    # Add some randomness to avoid generating data for every query every hour
                    if random.random() < 0.7:  # 70% chance of generating data for each query
                        impressions, clicks, ctr = generate_realistic_metrics(category, activity_multiplier)
                        
                        timestamp = current_date.replace(hour=hour)
                        
                        batch_data.append({
                            "search_query": query,
                            "clicks": clicks,
                            "impressions": impressions,
                            "click_through_rate": round(ctr, 4),
                            "search_date": timestamp.strftime("%Y-%m-%d")
                        })
                        
                        if len(batch_data) >= batch_size:
                            try:
                                supabase.table('search_clicks').insert(batch_data).execute()
                                total_records += len(batch_data)
                                print(f"Inserted {len(batch_data)} records. Total: {total_records}")
                                batch_data = []
                            except Exception as e:
                                print(f"Error inserting batch: {e}")
                                return
        
        # Insert any remaining records in the batch
        if batch_data:
            try:
                supabase.table('search_clicks').insert(batch_data).execute()
                total_records += len(batch_data)
                print(f"Inserted {len(batch_data)} records. Total: {total_records}")
            except Exception as e:
                print(f"Error inserting final batch: {e}")
                return
        
        current_date += timedelta(days=1)
        time.sleep(1)  # Add small delay to avoid hitting rate limits
    
    print(f"Data generation complete. Total records inserted: {total_records}")

if __name__ == "__main__":
    # Generate 30 days of dummy data
    generate_dummy_data(days=30)