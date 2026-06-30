"""
Afficionado Coffee - Advanced ML & Data Engineering Architecture Module
Author: Principal Data Scientist / Software Engineer Architect
"""

import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

class CoffeeAnalyticsEngine:
    def __init__(self, filepath):
        """ Initializes pipeline parameters and loads base telemetry matrices. """
        self.raw_data = pd.read_csv(filepath)
        self.clean_data = None
        self.customer_profiles = None
        self.model = None
        self.best_params = {}
        self.optimal_threshold = 0.5
        self.feature_importances = {}
        
        # Initialize Core Pipeline Layers
        self.process_data()
        self.engineer_customer_profiles(self.clean_data)
        self.train_optimized_churn_model()

    def process_data(self):
        """ Standardizes data frames, strips string headers, and structures chronologies. """
        df = self.raw_data.copy()
        df.columns = [col.strip() for col in df.columns]
        
        rename_map = {
            'transaction_id': 'Transaction_ID',
            'transaction_qty': 'Quantity',
            'store_location': 'Store',
            'product_category': 'Category',
            'product_type': 'Brand',
            'product_detail': 'Product_Name',
            'unit_price': 'Unit_Price'
        }
        df.rename(columns=rename_map, inplace=True)
        
        if 'transaction_time' in df.columns:
            df['Transaction_Time_Raw'] = df['transaction_time'].astype(str).str.strip()
        else:
            df['Transaction_Time_Raw'] = "12:00:00"
            
        df.drop_duplicates(subset=['Transaction_ID', 'Product_Name'], keep='first', inplace=True)
        df.sort_values(by='Transaction_ID', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        total_rows = len(df)
        base_start = pd.Timestamp('2025-01-01 06:00:00')
        base_end = pd.Timestamp('2025-12-31 21:00:00')
        
        time_deltas = (base_end - base_start) * (np.arange(total_rows) / total_rows)
        df['Date'] = base_start + time_deltas
        
        if 'transaction_time' in self.raw_data.columns:
            try:
                times = pd.to_timedelta(df['transaction_time'].astype(str))
                df['Date'] = df['Date'].dt.normalize() + times
            except Exception:
                pass
                
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1).clip(lower=1)
        df['Unit_Price'] = pd.to_numeric(df['Unit_Price'], errors='coerce').fillna(3.50).clip(lower=0.50)
        df['Revenue'] = df['Quantity'] * df['Unit_Price']
        
        df['Day'] = df['Date'].dt.strftime('%A')
        df['Hour'] = df['Date'].dt.hour
        
        self.clean_data = df

    def engineer_customer_profiles(self, reference_df=None):
        """ Generates behavioral profiles, CLV metrics, and risk flags over slice filters. """
        if reference_df is None:
            df = self.clean_data.copy()
        else:
            df = reference_df.copy()
            
        if df.empty:
            self.customer_profiles = pd.DataFrame()
            return
        
        df['Customer_ID'] = 'CUST-' + ((df['Transaction_ID'] % 4500) + 1000).astype(str)
        max_date = df['Date'].max() if not df.empty else pd.Timestamp('2025-12-31')
        
        cust_df = df.groupby('Customer_ID').agg(
            Recency_Hours=('Date', lambda x: int((max_date - x.max()).total_seconds() / 3600) if len(x) > 0 else 0),
            Frequency=('Transaction_ID', 'nunique'),
            Monetary=('Revenue', 'sum'),
            Avg_Ticket_Items=('Quantity', 'mean'),
            Plant_Byproduct_Ratio=('Category', lambda x: x.isin(['Tea', 'Drinking Chocolate', 'Bakery']).sum() / len(x) if len(x) > 0 else 0),
            Night_Ratio=('Hour', lambda x: (x >= 16).sum() / len(x) if len(x) > 0 else 0)
        ).reset_index()
        
        cust_df['CLV'] = cust_df['Monetary'] * 1.45
        churn_threshold = cust_df['Recency_Hours'].quantile(0.82) if not cust_df.empty else 720
        cust_df['Churned'] = (cust_df['Recency_Hours'] >= churn_threshold).astype(int)
        
        def segment_logic(row):
            if row['Monetary'] > cust_df['Monetary'].quantile(0.85): return 'Specialty Micro-Lot Connoisseur'
            if row['Frequency'] > cust_df['Frequency'].quantile(0.75): return 'Hell\'s Kitchen Ritualist'
            if row['Plant_Byproduct_Ratio'] > 0.35: return 'Sustainable Plant-Part Innovator'
            return 'Casual Explorer'
            
        cust_df['Segment'] = cust_df.apply(segment_logic, axis=1)
        self.customer_profiles = cust_df

    def train_optimized_churn_model(self):
        """ Evaluates validations over Random Forest nodes to configure weights. """
        cust_df = self.customer_profiles.copy()
        if cust_df.empty or cust_df['Churned'].nunique() < 2:
            self.feature_importances = {'Frequency': 0.4, 'Monetary': 0.3, 'Avg_Ticket_Items': 0.1, 'Plant_Byproduct_Ratio': 0.1, 'Night_Ratio': 0.1}
            return
            
        features = ['Frequency', 'Monetary', 'Avg_Ticket_Items', 'Plant_Byproduct_Ratio', 'Night_Ratio']
        X = cust_df[features]
        y = cust_df['Churned']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
        base_rf = RandomForestClassifier(random_state=42, class_weight='balanced', max_depth=8)
        
        param_grid = {'n_estimators': [50, 100]}
        grid_search = GridSearchCV(base_rf, param_grid, cv=3, scoring='f1', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        self.model = grid_search.best_estimator_
        self.best_params = grid_search.best_params_
        
        for col, imp in zip(features, self.model.feature_importances_):
            self.feature_importances[col] = float(imp)
            
        y_probs = self.model.predict_proba(X_test)[:, 1]
        best_f1 = 0
        for thresh in np.arange(0.1, 0.9, 0.05):
            preds = (y_probs >= thresh).astype(int)
            score = f1_score(y_test, preds)
            if score > best_f1:
                best_f1 = score
                self.optimal_threshold = thresh

    def predict_custom_scenario(self, frequency, monetary, avg_items, byproduct_ratio, night_ratio):
        if self.model is None:
            return {"churn_probability": 0.5, "classification": 0, "retention_playbook": "Engine warming up."}
        features = np.array([[frequency, monetary, avg_items, byproduct_ratio, night_ratio]])
        prob = self.model.predict_proba(features)[0][1]
        prediction = 1 if prob >= self.optimal_threshold else 0
        
        if prob > 0.75:
            action = "🚨 Critical Risk: Deploy single-origin anaerobic micro-lot rewards workflow."
        elif prob >= self.optimal_threshold:
            action = "⚠️ Moderate Risk: Auto-trigger cross-category circular byproduct combo discount."
        else:
            action = "✅ Stable Account: Maintain default seasonal catalog notification channels."
            
        return {"churn_probability": prob, "classification": prediction, "retention_playbook": action}

    def compute_market_basket_affinities(self, filtered_df) -> pd.DataFrame:
        if filtered_df.empty:
            return pd.DataFrame(columns=['Item A', 'Item B', 'Co-Occurrence Count'])
        
        df_basket = filtered_df.copy()
        df_basket['Proxy_Basket_ID'] = (
            df_basket['Store'].astype(str) + "_" + 
            df_basket['Date'].dt.date.astype(str) + "_" + 
            df_basket['Transaction_Time_Raw'].astype(str)
        )
        
        tx_groups = df_basket.groupby('Proxy_Basket_ID')['Product_Name'].apply(list)
        combo_counter = Counter()
        
        for item_list in tx_groups:
            if len(item_list) > 1:
                unique_items = sorted(list(set(item_list)))
                for combo in combinations(unique_items, 2):
                    combo_counter[combo] += 1
                    
        if not combo_counter:
            return pd.DataFrame(columns=['Item A', 'Item B', 'Co-Occurrence Count'])
            
        return pd.DataFrame([
            {'Item A': k[0], 'Item B': k[1], 'Co-Occurrence Count': v}
            for k, v in combo_counter.items()
        ]).sort_values(by='Co-Occurrence Count', ascending=False).reset_index(drop=True)

    def evaluate_pricing_elasticity(self, filtered_df):
        if filtered_df.empty:
            return pd.DataFrame()
        p_matrix = filtered_df.groupby(['Product_Name', 'Category']).agg(
            Average_Unit_Price=('Unit_Price', 'mean'),
            Total_Volume=('Quantity', 'sum'),
            Total_Gross_Revenue=('Revenue', 'sum')
        ).reset_index()
        rev_quantile = p_matrix['Total_Gross_Revenue'].median()
        p_matrix['Strategic_Pricing_Recommendation'] = p_matrix.apply(
            lambda r: "Premium Margin Optimization Target" if r['Total_Gross_Revenue'] >= rev_quantile and r['Average_Unit_Price'] < 4.00
            else ("Cross-Bundle Value Driver" if r['Total_Volume'] > p_matrix['Total_Volume'].median() else "Maintain Baseline Core Menu Structure"),
            axis=1
        )
        return p_matrix

    def get_kpis(self, filtered_df):
        if filtered_df.empty:
            return {'total_revenue': 0, 'transactions': 0, 'units_sold': 0, 'aov': 0}
        total_rev = filtered_df['Revenue'].sum()
        tx_count = filtered_df['Transaction_ID'].nunique()
        return {'total_revenue': total_rev, 'transactions': tx_count, 'units_sold': int(filtered_df['Quantity'].sum()), 'aov': total_rev / tx_count if tx_count > 0 else 0}

    def get_pareto_analysis(self, filtered_df):
        if filtered_df.empty:
            return pd.DataFrame(), [], []
        prod_perf = filtered_df.groupby(['Product_Name', 'Category']).agg(Total_Revenue=('Revenue', 'sum')).reset_index()
        prod_perf = prod_perf.sort_values(by='Total_Revenue', ascending=False).reset_index(drop=True)
        total_revenue = prod_perf['Total_Revenue'].sum()
        prod_perf['Cumulative_Revenue_%'] = prod_perf['Total_Revenue'].cumsum() / total_revenue * 100
        heroes = prod_perf[prod_perf['Cumulative_Revenue_%'] <= 80.001]['Product_Name'].tolist()
        tails = prod_perf[prod_perf['Cumulative_Revenue_%'] > 80.001]['Product_Name'].tolist()
        return prod_perf, heroes, tails

    def generate_automated_insights(self, filtered_df):
        if filtered_df.empty:
            return {'best_product': 'N/A', 'best_category': 'N/A', 'best_store': 'N/A', 'underperforming_products': ['N/A'], 'revenue_concentration': 0, 'inventory_suggestions': ['No data'], 'promotional_suggestions': ['No data']}
        best_product = filtered_df.groupby('Product_Name')['Revenue'].sum().idxmax()
        best_category = filtered_df.groupby('Category')['Revenue'].sum().idxmax()
        best_store = filtered_df.groupby('Store')['Revenue'].sum().idxmax()
        underperforming = filtered_df.groupby('Product_Name')['Quantity'].sum().nsmallest(3).index.tolist()
        _, heroes, _ = self.get_pareto_analysis(filtered_df)
        rev_concentration = (filtered_df[filtered_df['Product_Name'].isin(heroes)]['Revenue'].sum() / filtered_df['Revenue'].sum()) * 100
        return {
            'best_product': best_product, 'best_category': best_category, 'best_store': best_store, 'underperforming_products': underperforming, 'revenue_concentration': rev_concentration,
            'inventory_suggestions': [f"Scale production profiles on 'The Tank' for '{best_product}'."],
            'promotional_suggestions': [f"Bundle slower lines like '{underperforming[0]}' with core cash drivers."]
        }