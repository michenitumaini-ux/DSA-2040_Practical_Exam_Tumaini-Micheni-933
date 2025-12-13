import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
INPUT_FILE = 'rfm_clusters_with_scores.csv'

def profile_segments(input_file):
    """
    Loads clustered RFM data, profiles each segment, and generates visualizations.
    """
    if not os.path.exists(input_file):
        print(f"ERROR: Clustered file not found at '{input_file}'.")
        return

    # 1. Load Data
    rfm_clustered_df = pd.read_csv(input_file)
    
    # Ensure 'Cluster' is treated as a category
    rfm_clustered_df['Cluster'] = rfm_clustered_df['Cluster'].astype(str)

    # 2. Calculate Mean RFM Values per Cluster
    # This is the core of profiling: understanding what defines each group.
    segment_profiles = rfm_clustered_df.groupby('Cluster')[['recency', 'frequency', 'monetary']].mean().reset_index()
    
    # Rounding for clean display
    segment_profiles['recency'] = segment_profiles['recency'].round(0)
    segment_profiles['frequency'] = segment_profiles['frequency'].round(1)
    segment_profiles['monetary'] = segment_profiles['monetary'].round(2)
    
    # 3. Print Segment Profiles
    print("\n--- Segment Profiling (Mean RFM Scores) ---")
    print(segment_profiles.to_markdown(index=False))

    # --- 4. Assigning Segment Names ---
    # NOTE: Since your data is dummy, the logic below is for demonstration 
    # but the segment names are based on the dummy output provided in rfm_clusters_with_scores.csv
    
    # Based on dummy data:
    # Cluster 0: High Recency (200), Low F(1), Low M(50) -> 'Losing Customers'
    # Cluster 1: Medium Recency (50), Medium F(5), Medium M(500) -> 'Loyal Customers'
    # Cluster 2: Low Recency (10), High F(10), High M(5000) -> 'Champions'
    
    segment_map = {
        '2': '01_Champions',
        '1': '02_Loyal_Customers',
        '0': '03_Losing_Customers' 
    }
    
    # If more clusters were present, the mapping would be larger. We rely on K=4 analysis.
    rfm_clustered_df['Segment_Name'] = rfm_clustered_df['Cluster'].map(segment_map)
    
    # 5. Visualization

    # Melt the data for easier plotting
    rfm_melt = pd.melt(
        rfm_clustered_df, 
        id_vars=['Segment_Name'], 
        value_vars=['recency', 'frequency', 'monetary'],
        var_name='Metric', 
        value_name='Value' # This is the Y-axis value
    )
    
    # Create Box Plots for R, F, M across Segments
    plt.figure(figsize=(15, 6))
    
    # Define plot order and titles
    plot_metrics = {
        'recency': 'Recency (Days)', 
        'frequency': 'Frequency (Orders)', 
        'monetary': 'Monetary (Spent)'
    }
    
    for i, (metric_col, title) in enumerate(plot_metrics.items()):
        plt.subplot(1, 3, i + 1)
        
        # Filter the melted data for the current metric
        metric_data = rfm_melt[rfm_melt['Metric'] == metric_col]
        
        # Use the 'Value' column (which holds the R, F, or M score) for the Y-axis
        sns.boxplot(
            x='Segment_Name', 
            y='Value', 
            data=metric_data, 
            palette='viridis'
        )
        
        plt.title(f'Segments by {title}', fontsize=14)
        plt.xlabel('Customer Segment', fontsize=12)
        plt.ylabel(title, fontsize=12)
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('rfm_segment_boxplots.png')
    print("\nSegment visualization saved as 'rfm_segment_boxplots.png'")
    
    # 6. Save the final profiled list (for completeness)
    rfm_clustered_df[['customer_id', 'recency', 'frequency', 'monetary', 'Segment_Name']].to_csv('final_customer_segments.csv', index=False)
    print("Final segmentation table saved as 'final_customer_segments.csv'")
    
    print("\n--- Section 2: Data Mining Complete! ---")

if __name__ == '__main__':
    profile_segments(INPUT_FILE)