import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_and_clean_data(trader_file, sentiment_file):
    """
    Standardizes two different datasets and merges them on a daily date key.
    """
    print("--- Phase 1: Processing Trader Data ---")
    df = pd.read_csv(trader_file)
    
    # Standardize IST Timestamp
    df['Timestamp IST'] = pd.to_datetime(df['Timestamp IST'], dayfirst=True)
    df['Date'] = df['Timestamp IST'].dt.date
    
    # Aggregate to Daily level (Summing PnL for the whole day)
    daily_stats = df.groupby(['Date']).agg({
        'Closed PnL': 'sum',
        'Size USD': 'sum',
        'Fee': 'sum'
    }).reset_index()
    print(f"✅ Processed {len(df)} trade logs into {len(daily_stats)} daily summaries.")

    print("\n--- Phase 2: Processing Sentiment Data ---")
    sentiment_df = pd.read_csv(sentiment_file)
    
    # Clean column names (removes hidden spaces/newboarding)
    sentiment_df.columns = sentiment_df.columns.str.strip()
    
    # Robust Date Column Detection
    potential_date_cols = ['Date', 'date', 'timestamp', 'Timestamp', 'time']
    date_col = next((c for c in potential_date_cols if c in sentiment_df.columns), None)
    
    if date_col is None:
        raise KeyError(f"Could not find a date column in sentiment file. Columns found: {sentiment_df.columns.tolist()}")

    # Standardize Sentiment Date
    sentiment_df['Date'] = pd.to_datetime(sentiment_df[date_col]).dt.date
    print(f"✅ Sentiment data loaded using column: '{date_col}'")

    # Phase 3: The Merge
    merged = pd.merge(daily_stats, sentiment_df, on='Date', how='inner')
    print(f"✅ Successfully merged datasets. {len(merged)} days of overlap found.")
    
    return merged

def run_analysis(df):
    """
    Performs statistical correlation and generates a visualization.
    """
    print("\n--- Phase 4: Statistical Analysis ---")
    
    # 1. Correlation Check
    # We look for 'Value' (the 0-100 score)
    val_col = next((c for c in ['Value', 'value', 'fng_value'] if c in df.columns), None)
    
    if val_col:
        correlation = df['Closed PnL'].corr(df[val_col])
        print(f"📈 Correlation (PnL vs Sentiment Score): {correlation:.4f}")
    else:
        print("⚠️ No numeric 'Value' column found for precise correlation.")

    # 2. Visual Insight: PnL vs Classification
    class_col = next((c for c in ['Classification', 'classification', 'sentiment'] if c in df.columns), None)
    
    if class_col:
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        
        # Plotting the distribution
        sns.boxplot(x=class_col, y='Closed PnL', data=df, palette="viridis")
        
        plt.title('Trader Performance vs. Market Sentiment (Fear & Greed)', fontsize=14)
        plt.axhline(0, color='red', linestyle='--', alpha=0.5) # Zero line for PnL
        plt.ylabel('Daily Total PnL (USD)')
        plt.xlabel('Market Sentiment')
        
        output_plot = 'pnl_vs_sentiment_analysis.png'
        plt.savefig(output_plot)
        plt.show()
        print(f"📊 Visualization saved as '{output_plot}'")
    else:
        print("⚠️ No 'Classification' column found for the boxplot.")

if __name__ == "__main__":
    # Define filenames
    TRADER_LOGS = 'historical_data.csv'
    SENTIMENT_LOGS = 'fear_greed_index.csv' # Ensure this matches your file name!

    if os.path.exists(TRADER_LOGS) and os.path.exists(SENTIMENT_LOGS):
        try:
            final_data = load_and_clean_data(TRADER_LOGS, SENTIMENT_LOGS)
            run_analysis(final_data)
            
            # Print a quick preview of the merged data
            print("\n--- Final Data Preview ---")
            print(final_data[['Date', 'Closed PnL', 'Size USD']].tail())
            
        except Exception as e:
            print(f"❌ An error occurred: {e}")
    else:
        print("❌ Error: One or both CSV files are missing from the project directory.")
        print(f"Looking for: {TRADER_LOGS} and {SENTIMENT_LOGS}")