# IMDb Movie Scraper - CNS3102 Group Assignment

A simple Python script to scrape IMDb's Most Popular Movies list.

---

## Group Member - Group XXX

| Name             | Matric Number |
|------------------|---------------|
| Chan Ci En       | 215035        |
| Chu Xing En      | 215090        |
| Tan Yong Jin     | 217086        |

---

## Installation & Usage

### 1. Clone the repository:
```bash
git clone https://github.com/Chance3009/web-scraping.git
cd web-scraping
```

### 2. Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Run the script:
```bash
python scraper.py
```

---

## Script Functionality

The script will:
1. Scrape the current IMDb Most Popular Movies list
2. Save the data to a CSV file in the `data` directory
3. Display progress in the console

## Output

The script creates CSV files in the `data` directory with the following format:
- Filename: `imdb_popular_movies_YYYYMMDD_HHMMSS.csv`
- Data columns: title, year, rating, votes, url, scraped_date
