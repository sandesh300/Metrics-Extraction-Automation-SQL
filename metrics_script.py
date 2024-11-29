import os
import json
from datetime import datetime, timedelta
import random
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client
from celery import Celery
from celery.schedules import crontab

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Initialize Celery
celery_app = Celery('search_analytics',
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0')

# Configure Celery to run the task daily at midnight
celery_app.conf.beat_schedule = {
    'daily-analytics': {
        'task': 'search_analytics.process_daily_analytics',
        'schedule': crontab(hour=0, minute=0),
    },
}

def generate_mock_data():
    """Generate and insert mock search data for testing."""
    mock_queries = [
        "python tutorial", "javascript basics", "react hooks",
        "sql commands", "docker basics", "aws tutorial",
        "machine learning", "data science", "web development"
    ]
    
    data = []
    start_date = datetime.now() - timedelta(days=30)
    
    for day in range(31):
        for query in mock_queries:
            impressions = random.randint(50, 1000)
            clicks = random.randint(0, impressions)
            ctr = clicks / impressions if impressions > 0 else 0
            
            data.append({
                "search_query": query,
                "clicks": clicks,
                "impressions": impressions,
                "click_through_rate": ctr,
                "search_date": (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
            })
    
    # Insert mock data using Supabase
    supabase.table('search_clicks').insert(data).execute()

def get_daily_ctr():
    """Calculate average CTR for each day."""
    query = """
    SELECT 
        search_date,
        AVG(click_through_rate) as average_ctr
    FROM search_clicks
    GROUP BY search_date
    ORDER BY search_date DESC;
    """
    response = supabase.rpc('execute_query', {'query': query}).execute()
    return response.data

def get_top_queries():
    """Get top 5 search queries with highest CTR."""
    query = """
    SELECT 
        search_query,
        AVG(click_through_rate) as avg_ctr,
        SUM(impressions) as total_impressions
    FROM search_clicks
    WHERE search_date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY search_query
    HAVING SUM(impressions) >= 100
    ORDER BY avg_ctr DESC
    LIMIT 5;
    """
    response = supabase.rpc('execute_query', {'query': query}).execute()
    return response.data

def get_low_performing_queries():
    """Identify queries with high impressions but low clicks."""
    query = """
    SELECT 
        search_query,
        SUM(impressions) as total_impressions,
        AVG(click_through_rate) as avg_ctr
    FROM search_clicks
    WHERE search_date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY search_query
    HAVING SUM(impressions) >= 500 AND AVG(click_through_rate) < 0.01
    ORDER BY total_impressions DESC;
    """
    response = supabase.rpc('execute_query', {'query': query}).execute()
    return response.data

@celery_app.task
def process_daily_analytics():
    """Process daily analytics and store in summary table."""
    try:
        # Get all required metrics
        daily_ctr = get_daily_ctr()
        top_queries = get_top_queries()
        low_performing = get_low_performing_queries()
        
        # Prepare data for insertion
        insight_data = {
            "insight_date": datetime.now().strftime("%Y-%m-%d"),
            "average_ctr": daily_ctr[0]["average_ctr"] if daily_ctr else 0,
            "top_queries": json.dumps(top_queries),
            "low_performance_queries": json.dumps(low_performing)
        }
        
        # Insert into summary table
        supabase.table('search_insights').insert(insight_data).execute()
        
        return {"status": "success", "date": insight_data["insight_date"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Generate mock data if needed
    generate_mock_data()
    
    # Run analytics pipeline manually
    result = process_daily_analytics()
    print(f"Pipeline execution result: {result}")