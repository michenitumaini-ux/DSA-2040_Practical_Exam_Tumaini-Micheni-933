import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import os

# --- Configuration ---
INPUT_FILE = 'rfm_clusters_with_scores.csv'
TARGET_COLUMN = 'Cluster'

def perform_classification(input_file):
    """
    Trains Decision Tree and KNN classifiers on RFM data to predict cluster segments,
    computes metrics, and visualizes the Decision Tree.
    """
    if not os.path.exists(input_file):
        print(f"ERROR: Input file not found at '{input_file}'. Cannot proceed with classification.")
        return

    df = pd.read_csv(input_file)
    
    # Handling small/dummy data for demonstration
    if len(df) < 5:
        print("WARNING: Data is based on dummy output (3 rows). Metrics are for demonstration only.")
        test_size = 1 / len(df) if len(df) > 1 else 0.5
    else:
        test_size = 0.33

    features = ['recency', 'frequency', 'monetary']
    X = df[features]
    y = df[TARGET_COLUMN]

    # Split Data (Removed 'stratify' due to tiny dummy dataset)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    results = {}

    # --- Model 1: Decision Tree Classifier ---
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    y_pred_dt = dt_model.predict(X_test)

    results['Decision Tree'] = {
        'Accuracy': accuracy_score(y_test, y_pred_dt),
        'Precision': precision_score(y_test, y_pred_dt, average='weighted', zero_division=0),
        'Recall': recall_score(y_test, y_pred_dt, average='weighted', zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_dt, average='weighted', zero_division=0),
    }

    # Visualize the Decision Tree
    plt.figure(figsize=(15, 10))
    plot_tree(
        dt_model, 
        filled=True, 
        feature_names=features, 
        class_names=[str(c) for c in dt_model.classes_],
        rounded=True
    )
    plt.title("Decision Tree Classifier for RFM Segments")
    plt.savefig('decision_tree_visualization.png')
    print("Decision Tree Visualization saved as 'decision_tree_visualization.png'")

    # --- Model 2: K-Nearest Neighbors (KNN) Classifier ---
    k_neighbors = 1 
    knn_model = KNeighborsClassifier(n_neighbors=k_neighbors)
    knn_model.fit(X_train, y_train)
    y_pred_knn = knn_model.predict(X_test)

    results[f'KNN (k={k_neighbors})'] = {
        'Accuracy': accuracy_score(y_test, y_pred_knn),
        'Precision': precision_score(y_test, y_pred_knn, average='weighted', zero_division=0),
        'Recall': recall_score(y_test, y_pred_knn, average='weighted', zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_knn, average='weighted', zero_division=0),
    }

    # Print Results and Comparison
    print("\n--- Classification Performance Metrics ---")
    results_df = pd.DataFrame(results).T.round(4)
    print(results_df.to_markdown())
    
    best_model = results_df['Accuracy'].idxmax()
    print(f"\n--- Model Comparison ---\nBased on Accuracy, the {best_model} is better.")
    
    
if __name__ == '__main__':
    perform_classification(INPUT_FILE)