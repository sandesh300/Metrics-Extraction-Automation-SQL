import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def calculate_daily_insights(date):
    """Calculate insights for a specific date."""
    try:
        # Calculate average CTR for the day
        daily_ctr_response = supabase.table('search_clicks')\
            .select('click_through_rate')\
            .eq('search_date', date)\
            .execute()
        
        daily_ctr = 0
        if daily_ctr_response.data:
            ctrs = [record['click_through_rate'] for record in daily_ctr_response.data]
            daily_ctr = sum(ctrs) / len(ctrs) if ctrs else 0

        # Get top performing queries
        top_queries_response = supabase.table('search_clicks')\
            .select('search_query, clicks, impressions, click_through_rate')\
            .eq('search_date', date)\
            .order('click_through_rate', desc=True)\
            .limit(5)\
            .execute()

        # Get low performing queries
        low_performing_response = supabase.table('search_clicks')\
            .select('search_query, clicks, impressions, click_through_rate')\
            .eq('search_date', date)\
            .lt('click_through_rate', 0.05)\
            .gte('impressions', 100)\
            .order('impressions', desc=True)\
            .execute()

        # Prepare data for insertion
        insight_data = {
            "insight_date": date,
            "average_ctr": round(daily_ctr, 4),
            "top_queries": json.dumps(top_queries_response.data),
            "low_performance_queries": json.dumps(low_performing_response.data)
        }

        # Check if insight for this date already exists
        existing_insight = supabase.table('search_insights')\
            .select('id')\
            .eq('insight_date', date)\
            .execute()

        if existing_insight.data:
            # Update existing record
            supabase.table('search_insights')\
                .update(insight_data)\
                .eq('insight_date', date)\
                .execute()
            print(f"Updated insights for {date}")
        else:
            # Insert new record
            supabase.table('search_insights')\
                .insert(insight_data)\
                .execute()
            print(f"Inserted new insights for {date}")

    except Exception as e:
        print(f"Error processing insights for {date}: {e}")

def populate_historical_insights(days=30):
    """Populate insights for the last specified number of days."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        calculate_daily_insights(date_str)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    # Check if we have any existing insights
    existing_insights = supabase.table('search_insights').select('count').execute()
    count = len(existing_insights.data)

    if count == 0:
        print("No insights found. Populating historical insights...")
        populate_historical_insights()
    else:
        print(f"Found {count} existing insights.")
        # Calculate only for the most recent day
        calculate_daily_insights(datetime.now().strftime("%Y-%m-%d"))
    
    print("Insights population complete!")