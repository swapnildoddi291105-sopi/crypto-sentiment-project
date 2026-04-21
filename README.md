# Crypto Sentiment vs. Trader Performance Analysis

This project explores the relationship between market sentiment (Fear & Greed Index) and daily trading profitability (PnL). It processes large-scale trade logs and merges them with external sentiment data to identify behavioral patterns in trading.

## 🚀 Overview
The pipeline handles over **211,000+ trade logs** across **479 days** of overlapping data. It summarizes individual executions into daily performance metrics and correlates them with market-wide sentiment scores.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:** Pandas (Data Processing), Seaborn/Matplotlib (Visualization), Requests (API integration)
- **IDE:** IntelliJ IDEA / VS Code

## 📊 Key Results
- **Data Points:** 479 days of summarized data.
- **Correlation (PnL vs Sentiment):** `-0.0826`.
- **Insight:** The near-zero correlation suggests that for this specific high-volume strategy, market sentiment is not a strong linear predictor of daily PnL, indicating a more technical or systematic trading approach.

## 📂 Project Structure
- `data_pipeline.py`: The main script for processing, merging, and analyzing data.
- `historical_data.csv`: Raw execution logs (ignored by Git if >100MB).
- `pnl_vs_sentiment_analysis.png`: Statistical visualization output.

## ⚙️ How to Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/swapnildoddi291105-sopi/crypto-sentiment-project.git](https://github.com/swapnildoddi291105-sopi/crypto-sentiment-project.git)
