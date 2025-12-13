import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import os

# --- Configuration ---
INPUT_FILE = 'synthetic_transactions.csv'

def run_association_mining(input_file):
    """
    Loads transactional data, applies Apriori algorithm, and finds association rules.
    """
    if not os.path.exists(input_file):
        print(f"ERROR: Transactional file not found at '{input_file}'.")
        return

    # 1. Load Data
    with open(input_file, 'r') as f:
        # Transactions are read as a list of lists (e.g., [['milk', 'bread'], ['beer', 'diapers', 'chips']])
        transactions_raw = [line.strip().split(',') for line in f if line.strip()]
    
    # 2. Convert to One-Hot Encoded Format
    te = TransactionEncoder()
    te_ary = te.fit(transactions_raw).transform(transactions_raw)
    df_transactions = pd.DataFrame(te_ary, columns=te.columns_)

    # 3. Apply Apriori Algorithm
    print("\n--- Applying Apriori Algorithm ---")
    frequent_itemsets = apriori(
        df_transactions, 
        min_support=0.2, 
        use_colnames=True
    )
    print(f"Found {len(frequent_itemsets)} frequent itemsets with min_support=0.2")

    # 4. Generate Association Rules
    rules = association_rules(
        frequent_itemsets, 
        metric="confidence", 
        min_threshold=0.5
    )
    
    # 5. Filter, Sort, and Display Top 5 Rules
    rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    
    # Convert frozensets to strings for clean display
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
    
    rules_sorted = rules.sort_values(by='lift', ascending=False).head(5)
    
    print("\n--- Top 5 Association Rules (Sorted by Lift) ---")
    print(rules_sorted.to_markdown(index=False))

    # 6. Analysis (Discuss one rule)
    if not rules_sorted.empty:
        top_rule = rules_sorted.iloc[0]
        print("\n--- Rule Analysis ---")
        print(f"Top Rule: IF ({top_rule['antecedents']}) THEN ({top_rule['consequents']})")
        print(f"Lift: {top_rule['lift']:.2f}, Confidence: {top_rule['confidence']:.2f}")
        
        print("\nDiscussion (Example):")
        print("This rule has a high Lift, indicating the relationship is stronger than random chance. The high Confidence suggests that when a customer buys the antecedent item(s), they are highly likely to also buy the consequent item(s).")
        print("Implication for Retail Recommendations: Place the consequent item(s) near the antecedent item(s) or use this rule in the online store's 'Customers Who Bought This Also Bought' section to drive cross-selling and increase total basket size.")
    else:
        print("\nNo association rules found with the given minimum support and confidence thresholds. Try lowering the thresholds.")


if __name__ == '__main__':
    run_association_mining(INPUT_FILE)