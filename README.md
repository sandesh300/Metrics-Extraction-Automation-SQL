# Metrics Extraction and Automation from SQL

## Objective
Use PostgreSQL to analyze and extract insights from search and clicks data, then automate the process.

## Database Schema

```sql
CREATE TABLE search_clicks (
    search_id SERIAL PRIMARY KEY,
    search_query VARCHAR(255),
    clicks INT DEFAULT 0,
    impressions INT DEFAULT 0,
    click_through_rate FLOAT,
    search_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE search_insights (
    id SERIAL PRIMARY KEY,
    insight_date DATE,
    average_ctr FLOAT,
    top_queries JSONB,
    low_performance_queries JSONB
);
```

## Requirements

### Metrics Analysis
Write SQL queries to:
1. **Calculate the average click-through rate (CTR) for each day.**

   **Query:**
   ```sql
   SELECT
       search_date,
       AVG(click_through_rate) AS average_ctr
   FROM
       search_clicks
   GROUP BY
       search_date;
   ```

   **Sample Output:**
   ```json
   | search_date | average_ctr        |
   | ----------- | ------------------ |
   | 2024-11-11  | 0.0800128540305011 |
   | 2024-11-04  | 0.0808993520518358 |
   | 2024-11-22  | 0.0813024774774774 |
   | 2024-11-13  | 0.0786556521739131 |
   | 2024-11-16  | 0.0789735807860262 |
   | 2024-10-31  | 0.0784418859649122 |
   | 2024-11-25  | 0.0781114035087719 |
   | 2024-11-18  | 0.0790831168831169 |
   | 2024-11-02  | 0.0772150214592275 |
   | 2024-11-27  | 0.0777504566210046 |
   | 2024-11-26  | 0.0767496659242761 |
   | 2024-11-01  | 0.0790427601809954 |
   | 2024-11-17  | 0.0774195011337869 |
   | 2024-11-10  | 0.080802277904328  |
   | 2024-11-20  | 0.0778314893617021 |
   | 2024-11-15  | 0.0789424628450107 |
   | 2024-11-24  | 0.0807866090712742 |
   | 2024-11-09  | 0.0776652360515022 |
   | 2024-11-12  | 0.0784299776286353 |
   | 2024-11-23  | 0.0767668903803131 |
   | 2024-11-21  | 0.0784713963963964 |
   | 2024-11-05  | 0.0782538461538461 |
   | 2024-11-08  | 0.0804749464668094 |
   | 2024-11-29  | 0.0780660550458716 |
   | 2024-10-30  | 0.0797660550458716 |
   | 2024-11-19  | 0.0798498929336188 |
   | 2024-11-03  | 0.079837339055794  |
   | 2024-11-14  | 0.0763444685466377 |
   | 2024-11-28  | 0.0769561926605504 |
   | 2024-11-06  | 0.0772013186813186 |
   | 2024-11-07  | 0.0774540540540541 |
   ```

2. **Identify the top 5 search queries with the highest CTR over a given period.**

   **Query:**
   ```sql
   SELECT
       search_query,
       click_through_rate
   FROM
       search_clicks
   WHERE
       search_date BETWEEN '2024-10-30' AND '2024-11-11'
   ORDER BY
       click_through_rate DESC
   LIMIT
       5;
   ```

   **Sample Output:**
   ```json
   | search_query      | click_through_rate |
   | ----------------- | ------------------ |
   | javascript basics | 0.15               |
   | sql commands      | 0.1499             |
   | node.js express   | 0.1499             |
   | vue.js components | 0.1499             |
   | javascript basics | 0.1498             |
   ```

3. **Detect queries with high impressions but low clicks (possible optimization candidates).**

   **Query:**
   ```sql
   SELECT
       search_query,
       impressions,
       clicks
   FROM
       search_clicks
   WHERE
       impressions > 50 AND clicks < 10;
   ```

   **Sample Output:**
   ```json
   | search_query               | impressions | clicks |
   | -------------------------- | ----------- | ------ |
   | javascript basics          | 149         | 8      |
   | vue.js components          | 79          | 7      |
   | golang tutorial            | 102         | 8      |
   | git commands               | 104         | 6      |
   | jenkins pipeline           | 157         | 6      |
   | nginx configuration        | 81          | 7      |
   | microservices architecture | 94          | 9      |
   | design patterns            | 76          | 6      |
   | django rest framework      | 78          | 4      |
   | node.js express            | 85          | 8      |
   | git commands               | 70          | 2      |
   | kubernetes tutorial        | 83          | 4      |
   | jenkins pipeline           | 61          | 7      |
   | postman api testing        | 82          | 6      |
   | aws cli commands           | 60          | 4      |
   | ci/cd pipeline             | 76          | 6      |
   | test driven development    | 70          | 4      |
   | design patterns            | 88          | 6      |
   | clean code principles      | 68          | 1      |
   | system design basics       | 52          | 3      |
   | database indexing          | 73          | 1      |
   | node.js express            | 86          | 8      |
   | golang tutorial            | 69          | 6      |
   | vs code extensions         | 64          | 5      |
   | nginx configuration        | 104         | 8      |
   | postman api testing        | 153         | 7      |
   | microservices architecture | 77          | 2      |
   | ci/cd pipeline             | 77          | 3      |
   | test driven development    | 91          | 8      |
   | agile methodology          | 99          | 9      |
   | design patterns            | 80          | 3      |
   | database indexing          | 81          | 3      |
   | node.js express            | 70          | 7      |
   | jenkins pipeline           | 150         | 5      |
   | terraform basics           | 199         | 7      |
   | microservices architecture | 63          | 5      |
   | ci/cd pipeline             | 71          | 1      |
   | test driven development    | 92          | 3      |
   | agile methodology          | 84          | 5      |
   | react hooks tutorial       | 57          | 7      |
   | sql commands               | 103         | 9      |
   | git commands               | 80          | 7      |
   ```

### Pipeline Automation
Develop a Python script to execute these SQL queries and store the results in a summary table. Automate the script to run daily using a scheduler like Celery.

## Deliverables

1. Use Supabase free tier to complete the assignments.
2. Make a dummy dataset for all the above tasks.
3. Provide SQL queries and the summary table structure.
4. Develop a Python script for pipeline automation.
5. Provide sample output of the pipeline with mock data.

## Setup

### Prerequisites
- Python 3.x
- PostgreSQL
- Supabase account
- Redis (for Celery)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sandesh300/Metrics-Extraction-Automation-SQL
   cd metrics-extraction-automation-sql
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root with the following content:
   ```env
   SUPABASE_URL=<your_supabase_url>
   SUPABASE_KEY=<your_supabase_key>
   ```

4. **Start Redis Server**:
   Ensure Redis is running on your local machine.

## Usage

### Generate Dummy Data
Run the `generate_dummy_data.py` script to generate mock data for testing:
```bash
python generate_dummy_data.py
```
### Python script for Pipeline automation
```python
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
```

### Run the Pipeline Manually
Run the `metrics_script.py` script to execute the analytics pipeline manually:
```bash
python metrics_script.py
```

### Automate the Pipeline with Celery
1. **Start Celery Worker**:
   ```bash
   celery -A metrics_script worker --loglevel=info
   ```

2. **Start Celery Beat Scheduler**:
   ```bash
   celery -A metrics_script beat --loglevel=info
   ```

## Sample Output

After running the pipeline, you can query the `search_insights` table to see the generated insights:

```sql
SELECT * FROM search_insights;
```

Sample output:
```json
| id | insight_date | average_ctr | top_queries                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | low_performance_queries                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -- | ------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 9  | 2024-11-29   | 0.0781      | [{"search_query": "django rest framework", "clicks": 38, "impressions": 256, "click_through_rate": 0.1496}, {"search_query": "golang tutorial", "clicks": 39, "impressions": 264, "click_through_rate": 0.149}, {"search_query": "django rest framework", "clicks": 98, "impressions": 669, "click_through_rate": 0.1478}, {"search_query": "vue.js components", "clicks": 14, "impressions": 97, "click_through_rate": 0.147}, {"search_query": "golang tutorial", "clicks": 63, "impressions": 431, "click_through_rate": 0.1469}] | [{"search_query": "jenkins pipeline", "clicks": 19, "impressions": 439, "click_through_rate": 0.0441}, {"search_query": "jenkins pipeline", "clicks": 16, "impressions": 424, "click_through_rate": 0.0398}, {"search_query": "postman api testing", "clicks": 13, "impressions": 422, "click_through_rate": 0.0323}, {"search_query": "microservices architecture", "clicks": 9, "impressions": 409, "click_through_rate": 0.0233}, {"search_query": "caching strategies", "clicks": 10, "impressions": 405, "click_through_rate": 0.0261}, {"search_query": "kubernetes tutorial", "clicks": 19, "impressions": 391, "click_through_rate": 0.0493}, {"search_query": "aws cli commands", "clicks": 12, "impressions": 363, "click_through_rate": 0.0345}, {"search_query": "git commands", "clicks": 12, "impressions": 357, "click_through_rate": 0.0344}, {"search_query": "ci/cd pipeline", "clicks": 8, "impressions": 355, "click_through_rate": 0.0236}, {"search_query": "docker compose example", "clicks": 16, "impressions": 341, "click_through_rate": 0.0493}, {"search_query": "agile methodology", "clicks": 15, "impressions": 337, "click_through_rate": 0.0457}, {"search_query": "nginx configuration", "clicks": 10, "impressions": 337, "click_through_rate": 0.0302}, {"search_query": "postman api testing", "clicks": 14, "impressions": 334, "click_through_rate": 0.0428}, {"search_query": "database indexing", "clicks": 11, "impressions": 324, "click_through_rate": 0.0363}, {"search_query": "test driven development", "clicks": 13, "impressions": 323, "click_through_rate": 0.0428}, {"search_query": "terraform basics", "clicks": 15, "impressions": 306, "click_through_rate": 0.0494}, {"search_query": "aws cli commands", "clicks": 9, "impressions": 291, "click_through_rate": 0.0332}, {"search_query": "caching strategies", "clicks": 11, "impressions": 284, "click_through_rate": 0.0407}, {"search_query": "design patterns", "clicks": 11, "impressions": 259, "click_through_rate": 0.0441}, {"search_query": "test driven development", "clicks": 7, "impressions": 259, "click_through_rate": 0.0289}, {"search_query": "kubernetes tutorial", "clicks": 12, "impressions": 257, "click_through_rate": 0.0481}, {"search_query": "aws cli commands", "clicks": 10, "impressions": 253, "click_through_rate": 0.0423}, {"search_query": "design patterns", "clicks": 10, "impressions": 246, "click_through_rate": 0.0418}, {"search_query": "clean code principles", "clicks": 11, "impressions": 234, "click_through_rate": 0.0493}, {"search_query": "vs code extensions", "clicks": 9, "impressions": 230, "click_through_rate": 0.0395}, {"search_query": "ci/cd pipeline", "clicks": 7, "impressions": 230, "click_through_rate": 0.0329}, {"search_query": "git commands", "clicks": 11, "impressions": 228, "click_through_rate": 0.0493}, {"search_query": "microservices architecture", "clicks": 8, "impressions": 227, "click_through_rate": 0.0383}, {"search_query": "database indexing", "clicks": 10, "impressions": 227, "click_through_rate": 0.0459}, {"search_query": "ci/cd pipeline", "clicks": 10, "impressions": 220, "click_through_rate": 0.0457}, {"search_query": "system design basics", "clicks": 6, "impressions": 213, "click_through_rate": 0.0302}, {"search_query": "caching strategies", "clicks": 5, "impressions": 213, "click_through_rate": 0.0236}, {"search_query": "caching strategies", "clicks": 7, "impressions": 205, "click_through_rate": 0.0385}, {"search_query": "git commands", "clicks": 8, "impressions": 202, "click_through_rate": 0.044}, {"search_query": "microservices architecture", "clicks": 6, "impressions": 188, "click_through_rate": 0.035}, {"search_query": "kubernetes tutorial", "clicks": 6, "impressions": 184, "click_through_rate": 0.035}, {"search_query": "agile methodology", "clicks": 3, "impressions": 169, "click_through_rate": 0.0213}, {"search_query": "agile methodology", "clicks": 4, "impressions": 169, "click_through_rate": 0.0262}, {"search_query": "microservices architecture", "clicks": 7, "impressions": 159, "click_through_rate": 0.048}, {"search_query": "postman api testing", "clicks": 5, "impressions": 155, "click_through_rate": 0.0358}, {"search_query": "vs code extensions", "clicks": 6, "impressions": 154, "click_through_rate": 0.0395}, {"search_query": "jenkins pipeline", "clicks": 6, "impressions": 153, "click_through_rate": 0.0425}, {"search_query": "vs code extensions", "clicks": 6, "impressions": 153, "click_through_rate": 0.0442}, {"search_query": "design patterns", "clicks": 3, "impressions": 143, "click_through_rate": 0.0227}, {"search_query": "caching strategies", "clicks": 5, "impressions": 142, "click_through_rate": 0.036}, {"search_query": "vs code extensions", "clicks": 6, "impressions": 133, "click_through_rate": 0.0457}, {"search_query": "ci/cd pipeline", "clicks": 5, "impressions": 133, "click_through_rate": 0.0424}, {"search_query": "postman api testing", "clicks": 5, "impressions": 130, "click_through_rate": 0.0412}, {"search_query": "caching strategies", "clicks": 3, "impressions": 128, "click_through_rate": 0.0265}, {"search_query": "test driven development", "clicks": 2, "impressions": 126, "click_through_rate": 0.0219}, {"search_query": "postman api testing", "clicks": 5, "impressions": 126, "click_through_rate": 0.0427}, {"search_query": "microservices architecture", "clicks": 4, "impressions": 124, "click_through_rate": 0.0326}, {"search_query": "agile methodology", "clicks": 4, "impressions": 122, "click_through_rate": 0.0391}, {"search_query": "git commands", "clicks": 4, "impressions": 117, "click_through_rate": 0.0417}, {"search_query": "git commands", "clicks": 3, "impressions": 112, "click_through_rate": 0.0347}, {"search_query": "system design basics", "clicks": 4, "impressions": 110, "click_through_rate": 0.0439}, {"search_query": "clean code principles", "clicks": 3, "impressions": 106, "click_through_rate": 0.0293}, {"search_query": "system design basics", "clicks": 4, "impressions": 104, "click_through_rate": 0.0419}, {"search_query": "system design basics", "clicks": 4, "impressions": 103, "click_through_rate": 0.0401}, {"search_query": "microservices architecture", "clicks": 2, "impressions": 102, "click_through_rate": 0.0253}, {"search_query": "clean code principles", "clicks": 4, "impressions": 102, "click_through_rate": 0.0404}, {"search_query": "jenkins pipeline", "clicks": 4, "impressions": 100, "click_through_rate": 0.0462}, {"search_query": "vs code extensions", "clicks": 4, "impressions": 100, "click_through_rate": 0.0481}] |
```

## Conclusion

This project demonstrates how to use PostgreSQL to analyze and extract insights from search and clicks data, and automate the process using Python and Celery. The application meets the specified requirements and deliverables, including the generation of dummy data, SQL queries, pipeline automation, and sample output.
                                                                                                                                                                                                                                                                                                                                                   
