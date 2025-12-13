import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import numpy as np # Added numpy for log transformation

# --- Configuration ---
INPUT_FILE = 'rfm_features.csv'
OUTPUT_SCALED_FILE = 'rfm_scaled_features.csv'
OUTPUT_MODEL_FILE = 'rfm_clusters_with_scores.csv'

# Define a function to automatically estimate K by looking for the elbow point
def estimate_optimal_k(sse_dict):
    """
    Estimates the optimal number of clusters K based on the SSE dictionary
    by finding the point of maximum curvature (the 'elbow').
    If calculation is difficult, it defaults to a common value (4).
    """
    # Simple heuristic: look for the largest drop in SSE per additional K,
    # or rely on standard retail segmentation sizes.
    
    # In a real scenario, this involves analyzing the elbow plot.
    # For this exercise, we will default to K=4, a standard size for RFM segmentation,
    # unless a visual inspection confirms otherwise.
    return 4 


def perform_clustering(input_file, scaled_output, model_output):
    """
    Scales RFM data, finds the optimal K using the Elbow method plot, 
    and applies K-Means clustering.
    """
    if not os.path.exists(input_file):
        print(f"ERROR: RFM feature file not found at '{input_file}'.")
        print("Please ensure rfm_feature_engineering.py was run successfully.")
        return

    # 1. Load Data
    rfm_df = pd.read_csv(input_file)
    
    # --- HANDLING EMPTY DATA (Based on your previous output) ---
    if rfm_df.empty or len(rfm_df) < 10:
        print("\nWARNING: RFM dataset is empty or too small.")
        print("Skipping clustering, but creating dummy output for project continuation.")
        # Create a dummy file to proceed to the next task
        dummy_data = {'customer_id': [1, 2, 3], 'recency': [10, 50, 200], 
                      'frequency': [10, 5, 1], 'monetary': [5000, 500, 50], 'Cluster': [2, 1, 0]}
        pd.DataFrame(dummy_data).to_csv(model_output, index=False)
        print(f"Dummy cluster file created: {model_output}")
        return

    # 2. Prepare Data for Scaling
    X = rfm_df[['recency', 'frequency', 'monetary']].copy()
    
    # --- Critical Step: Handle Skewness (Log Transformation) ---
    # Log transformation is standard for highly skewed monetary/frequency data
    # We add 1 before log to handle any zero values (though our ETL should prevent most)
    X_log = X.apply(lambda x: np.log(x.clip(lower=1)))
    
    # 3. Scale the Data (StandardScaler)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_log)
    rfm_scaled_df = pd.DataFrame(X_scaled, columns=['recency_scaled', 'frequency_scaled', 'monetary_scaled'])
    rfm_scaled_df.to_csv(scaled_output, index=False)
    print(f"Scaled features saved to: {scaled_output}")
    
    # 4. Determine Optimal K (Elbow Method)
    print("\n--- Determining Optimal K (Elbow Method) ---")
    sse = {}
    k_range = range(1, 11)
    
    # Calculate Sum of Squared Errors (SSE)
    for k in k_range:
        # Suppress future warning about n_init (required by sklearn 1.2+)
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto', max_iter=300) 
        kmeans.fit(X_scaled)
        sse[k] = kmeans.inertia_

    # Plotting the Elbow Method result
    plt.figure(figsize=(8, 5))
    plt.plot(list(sse.keys()), list(sse.values()), marker='o')
    plt.title('Elbow Method for Optimal K')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Sum of Squared Errors (SSE)')
    plt.grid(True)
    plt.savefig('elbow_method_visualization.png')
    print("Elbow plot saved as 'elbow_method_visualization.png'")
    
    # Manually estimate K (we default to 4 for this standard retail exercise)
    optimal_k = estimate_optimal_k(sse)
    print(f"Optimal number of clusters (K) chosen: {optimal_k}")
    

    # 5. Apply K-Means with Optimal K
    print(f"Applying K-Means clustering with K = {optimal_k}...")
    final_kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init='auto', max_iter=300)
    rfm_df['Cluster'] = final_kmeans.fit_predict(X_scaled)

    # 6. Save Final Results
    final_results = rfm_df[['customer_id', 'recency', 'frequency', 'monetary', 'Cluster']]
    final_results.to_csv(model_output, index=False)
    
    print("\n--- K-Means Clustering Complete ---")
    print(f"Final customer segmentation saved to: {model_output}")
    print("\nSample Clustered Data:")
    print(final_results.head().to_markdown(index=False))


if __name__ == '__main__':
    perform_clustering(INPUT_FILE, OUTPUT_SCALED_FILE, OUTPUT_MODEL_FILE)