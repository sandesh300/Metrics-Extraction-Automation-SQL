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
1. Calculate the average click-through rate (CTR) for each day.
2. Identify the top 5 search queries with the highest CTR over a given period.
3. Detect queries with high impressions but low clicks (possible optimization candidates).

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
   git clone <repository_url>
   cd <repository_directory>
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
Run the `dummy_data.py` script to generate mock data for testing:
```bash
python dummy_data.py
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
[
  {
    "id": 9,
    "insight_date": "2024-11-29",
    "average_ctr": 0.0781,
    "top_queries": "[{\"search_query\": \"django rest framework\", \"clicks\": 38, \"impressions\": 256, \"click_through_rate\": 0.1496}, {\"search_query\": \"golang tutorial\", \"clicks\": 39, \"impressions\": 264, \"click_through_rate\": 0.149}, {\"search_query\": \"django rest framework\", \"clicks\": 98, \"impressions\": 669, \"click_through_rate\": 0.1478}, {\"search_query\": \"vue.js components\", \"clicks\": 14, \"impressions\": 97, \"click_through_rate\": 0.147}, {\"search_query\": \"golang tutorial\", \"clicks\": 63, \"impressions\": 431, \"click_through_rate\": 0.1469}]",
    "low_performance_queries": "[{\"search_query\": \"jenkins pipeline\", \"clicks\": 19, \"impressions\": 439, \"click_through_rate\": 0.0441}, {\"search_query\": \"jenkins pipeline\", \"clicks\": 16, \"impressions\": 424, \"click_through_rate\": 0.0398}, {\"search_query\": \"postman api testing\", \"clicks\": 13, \"impressions\": 422, \"click_through_rate\": 0.0323}, {\"search_query\": \"microservices architecture\", \"clicks\": 9, \"impressions\": 409, \"click_through_rate\": 0.0233}, {\"search_query\": \"caching strategies\", \"clicks\": 10, \"impressions\": 405, \"click_through_rate\": 0.0261}, {\"search_query\": \"kubernetes tutorial\", \"clicks\": 19, \"impressions\": 391, \"click_through_rate\": 0.0493}, {\"search_query\": \"aws cli commands\", \"clicks\": 12, \"impressions\": 363, \"click_through_rate\": 0.0345}, {\"search_query\": \"git commands\", \"clicks\": 12, \"impressions\": 357, \"click_through_rate\": 0.0344}, {\"search_query\": \"ci/cd pipeline\", \"clicks\": 8, \"impressions\": 355, \"click_through_rate\": 0.0236}, {\"search_query\": \"docker compose example\", \"clicks\": 16, \"impressions\": 341, \"click_through_rate\": 0.0493}, {\"search_query\": \"agile methodology\", \"clicks\": 15, \"impressions\": 337, \"click_through_rate\": 0.0457}, {\"search_query\": \"nginx configuration\", \"clicks\": 10, \"impressions\": 337, \"click_through_rate\": 0.0302}, {\"search_query\": \"postman api testing\", \"clicks\": 14, \"impressions\": 334, \"click_through_rate\": 0.0428}, {\"search_query\": \"database indexing\", \"clicks\": 11, \"impressions\": 324, \"click_through_rate\": 0.0363}, {\"search_query\": \"test driven development\", \"clicks\": 13, \"impressions\": 323, \"click_through_rate\": 0.0428}, {\"search_query\": \"terraform basics\", \"clicks\": 15, \"impressions\": 306, \"click_through_rate\": 0.0494}, {\"search_query\": \"aws cli commands\", \"clicks\": 9, \"impressions\": 291, \"click_through_rate\": 0.0332}, {\"search_query\": \"caching strategies\", \"clicks\": 11, \"impressions\": 284, \"click_through_rate\": 0.0407}, {\"search_query\": \"design patterns\", \"clicks\": 11, \"impressions\": 259, \"click_through_rate\": 0.0441}, {\"search_query\": \"test driven development\", \"clicks\": 7, \"impressions\": 259, \"click_through_rate\": 0.0289}, {\"search_query\": \"kubernetes tutorial\", \"clicks\": 12, \"impressions\": 257, \"click_through_rate\": 0.0481}, {\"search_query\": \"aws cli commands\", \"clicks\": 10, \"impressions\": 253, \"click_through_rate\": 0.0423}, {\"search_query\": \"design patterns\", \"clicks\": 10, \"impressions\": 246, \"click_through_rate\": 0.0418}, {\"search_query\": \"clean code principles\", \"clicks\": 11, \"impressions\": 234, \"click_through_rate\": 0.0493}, {\"search_query\": \"vs code extensions\", \"clicks\": 9, \"impressions\": 230, \"click_through_rate\": 0.0395}, {\"search_query\": \"ci/cd pipeline\", \"clicks\": 7, \"impressions\": 230, \"click_through_rate\": 0.0329}, {\"search_query\": \"git commands\", \"clicks\": 11, \"impressions\": 228, \"click_through_rate\": 0.0493}, {\"search_query\": \"microservices architecture\", \"clicks\": 8, \"impressions\": 227, \"click_through_rate\": 0.0383}, {\"search_query\": \"database indexing\", \"clicks\": 10, \"impressions\": 227, \"click_through_rate\": 0.0459}, {\"search_query\": \"ci/cd pipeline\", \"clicks\": 10, \"impressions\": 220, \"click_through_rate\": 0.0457}, {\"search_query\": \"system design basics\", \"clicks\": 6, \"impressions\": 213, \"click_through_rate\": 0.0302}, {\"search_query\": \"caching strategies\", \"clicks\": 5, \"impressions\": 213, \"click_through_rate\": 0.0236}, {\"search_query\": \"caching strategies\", \"clicks\": 7, \"impressions\": 205, \"click_through_rate\": 0.0385}, {\"search_query\": \"git commands\", \"clicks\": 8, \"impressions\": 202, \"click_through_rate\": 0.044}, {\"search_query\": \"microservices architecture\", \"clicks\": 6, \"impressions\": 188, \"click_through_rate\": 0.035}, {\"search_query\": \"kubernetes tutorial\", \"clicks\": 6, \"impressions\": 184, \"click_through_rate\": 0.035}, {\"search_query\": \"agile methodology\", \"clicks\": 3, \"impressions\": 169, \"click_through_rate\": 0.0213}, {\"search_query\": \"agile methodology\", \"clicks\": 4, \"impressions\": 169, \"click_through_rate\": 0.0262}, {\"search_query\": \"microservices architecture\", \"clicks\": 7, \"impressions\": 159, \"click_through_rate\": 0.048}, {\"search_query\": \"postman api testing\", \"clicks\": 5, \"impressions\": 155, \"click_through_rate\": 0.0358}, {\"search_query\": \"vs code extensions\", \"clicks\": 6, \"impressions\": 154, \"click_through_rate\": 0.0395}, {\"search_query\": \"jenkins pipeline\", \"clicks\": 6, \"impressions\": 153, \"click_through_rate\": 0.0425}, {\"search_query\": \"vs code extensions\", \"clicks\": 6, \"impressions\": 153, \"click_through_rate\": 0.0442}, {\"search_query\": \"design patterns\", \"clicks\": 3, \"impressions\": 143, \"click_through_rate\": 0.0227}, {\"search_query\": \"caching strategies\", \"clicks\": 5, \"impressions\": 142, \"click_through_rate\": 0.036}, {\"search_query\": \"vs code extensions\", \"clicks\": 6, \"impressions\": 133, \"click_through_rate\": 0.0457}, {\"search_query\": \"ci/cd pipeline\", \"clicks\": 5, \"impressions\": 133, \"click_through_rate\": 0.0424}, {\"search_query\": \"postman api testing\", \"clicks\": 5, \"impressions\": 130, \"click_through_rate\": 0.0412}, {\"search_query\": \"caching strategies\", \"clicks\": 3, \"impressions\": 128, \"click_through_rate\": 0.0265}, {\"search_query\": \"test driven development\", \"clicks\": 2, \"impressions\": 126, \"click_through_rate\": 0.0219}, {\"search_query\": \"postman api testing\", \"clicks\": 5, \"impressions\": 126, \"click_through_rate\": 0.0427}, {\"search_query\": \"microservices architecture\", \"clicks\": 4, \"impressions\": 124, \"click_through_rate\": 0.0326}, {\"search_query\": \"agile methodology\", \"clicks\": 4, \"impressions\": 122, \"click_through_rate\": 0.0391}, {\"search_query\": \"git commands\", \"clicks\": 4, \"impressions\": 117, \"click_through_rate\": 0.0417}, {\"search_query\": \"git commands\", \"clicks\": 3, \"impressions\": 112, \"click_through_rate\": 0.0347}, {\"search_query\": \"system design basics\", \"clicks\": 4, \"impressions\": 110, \"click_through_rate\": 0.0439}, {\"search_query\": \"clean code principles\", \"clicks\": 3, \"impressions\": 106, \"click_through_rate\": 0.0293}, {\"search_query\": \"system design basics\", \"clicks\": 4, \"impressions\": 104, \"click_through_rate\": 0.0419}, {\"search_query\": \"system design basics\", \"clicks\": 4, \"impressions\": 103, \"click_through_rate\": 0.0401}, {\"search_query\": \"microservices architecture\", \"clicks\": 2, \"impressions\": 102, \"click_through_rate\": 0.0253}, {\"search_query\": \"clean code principles\", \"clicks\": 4, \"impressions\": 102, \"click_through_rate\": 0.0404}, {\"search_query\": \"jenkins pipeline\", \"clicks\": 4, \"impressions\": 100, \"click_through_rate\": 0.0462}, {\"search_query\": \"vs code extensions\", \"clicks\": 4, \"impressions\": 100, \"click_through_rate\": 0.0481}]"
  }
]
```

## Conclusion

This project demonstrates how to use PostgreSQL to analyze and extract insights from search and clicks data, and automate the process using Python and Celery. The application meets the specified requirements and deliverables, including the generation of dummy data, SQL queries, pipeline automation, and sample output.
