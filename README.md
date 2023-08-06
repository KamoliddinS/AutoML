# AutoML FastAPI Application with MongoDB

This is an AutoML FastAPI application that trains and serves machine learning pipelines using data from MongoDB. The application trains a new pipeline every hour, updates it with new data, and serves the latest trained pipeline for predictions.

## Features

- Data is loaded from a CSV file and stored in a MongoDB collection on application startup.
- A new machine learning pipeline is created and trained every hour.
- The latest trained pipeline is served for predictions.
- Endpoints:
  - `/add_data`: Add new data for training.
  - `/predict`: Make predictions using the latest trained pipeline.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Usage

1. Clone this repository:

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```
2. Place your CSV dataset file (e.g., dataset.csv) in the data directory.
3. Modify the Dockerfile and docker-compose.yml files as needed.
4. Build and run the application using Docker Compose:
    
    ```bash
      docker-compose up -d --build
      ```
      
### Endpoints

    /add_data (POST): Add new data for training.
    Request format:
    {
      "client_id": 1,
      "gender": "F",
      "age": 48,
      "marital_status": "MAR",
      "job_position": "BIS",
      "credit_sum": 59998,
      "credit_month": 10,
      "tariff_id": 1.6,
      "score_shk": 0.421599,
      "education": "GRD",
      "living_region": "ЛЕНИНГРАДСКАЯ ОБЛАСТЬ",
      "monthly_income": 30000,
      "credit_count": 1,
      "overdue_credit_count": 0,
      "open_account_flg": 1
    }
    /predict (POST): Make predictions using the latest trained pipeline.
    Request format: 
    {
      "gender": "F",
      "age": 48,
      "marital_status": "MAR",
      "job_position": "BIS",
      "credit_sum": 59998,
      "credit_month": 10,
      "tariff_id": 1.6,
      "score_shk": 0.421599,
      "education": "GRD",
      "living_region": "ЛЕНИНГРАДСКАЯ ОБЛАСТЬ",
      "monthly_income": 30000,
      "credit_count": 1,
      "overdue_credit_count": 0
    }

## License
This project is licensed under the MIT License - see the LICENSE file for details.