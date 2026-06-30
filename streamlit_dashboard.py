import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from coffee_sales_analysis import CoffeeAnalyticsEngine

# -- Viewport Configurations --
st.set_page_config(page_title="Afficionado Coffee Intelligence", page_icon="☕", layout="wide")

# -- Premium Corporate Styling Directives --
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght=300;400;600&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        
        .metric-card {
            background-color: #FDFBF7;
            border-top: 4px solid #3D2314;
            padding: 22px;
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.04);
            margin-bottom: 12px;
        }
        .metric-title { font-size: 0.8rem; text-transform: uppercase; color: #7F7F7F; font-weight: 600; letter-spacing: 0.8px; }
        .metric-value { font-size: 2rem; font-weight: 700; color: #2B160A; margin-top: 4px; }
        .section-title { font-family: 'DM Serif Display', serif; color: #3D2314; margin-top: 20px; border-bottom: 1px solid #EAEAEA; padding-bottom: 5px; }
        .expanded-para { line-height: 1.6; text-align: justify; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# -- Automated Data Pipeline Loading Layer --
@st.cache_resource
def load_and_cache_engine():
    return CoffeeAnalyticsEngine(r"C:\Users\paras\OneDrive\My Projects or codes\Unified Mentor Projects\Project 2\Afficionado Coffee Roasters.xlsx - Transactions.csv")

try:
    engine = load_and_cache_engine()
    df = engine.clean_data
except Exception as e:
    st.error(f"⚠️ Failed to map file target destination stream pathway: {e}")
    st.stop()

# -- Framework Header --
st.title("☕ Afficionado Coffee Roasters")
st.markdown("### **Enterprise Strategy Suite & Machine Learning Core Operations**")
st.markdown("---")

# -- Filter Component Controllers --
st.sidebar.markdown("### **Control Panel Filters**")
selected_stores = st.sidebar.multiselect("Store Infrastructure Nodes", options=sorted(df['Store'].unique()), default=sorted(df['Store'].unique()))
selected_categories = st.sidebar.multiselect("Product Category Tiers", options=sorted(df['Category'].unique()), default=sorted(df['Category'].unique()))

# ====== STATIC TIMELINE FILTER WIDGET ======
static_min_date = date(2025, 1, 1)
static_max_date = date(2025, 12, 31)

date_bounds = st.sidebar.date_input(
    "Temporal Window Selection", 
    [static_min_date, static_max_date], 
    min_value=static_min_date, 
    max_value=static_max_date,
    help="Filter analytics view over the synchronized 2025 transaction timeline generated from Afficionado Coffee Roasters.xlsx - Transactions.csv."
)

# Robust defensive check to ensure the user has completed a dual-bound date range choice 
# (Streamlit transiently returns a single-element list while the user is actively clicking)
if isinstance(date_bounds, (list, tuple)) and len(date_bounds) == 2:
    start_date, end_date = date_bounds
else:
    start_date, end_date = static_min_date, static_max_date
# ==========================================

top_n_slider = st.sidebar.slider("Global Focus Cutoff (Top-N Rows)", min_value=5, max_value=30, value=10)

# -- Navigation Module Elements --
page_route = st.sidebar.radio("Navigate Analytics Modules", [
    "Home Overview", 
    "Executive Dashboard", 
    "Product Analytics", 
    "Category & Brand Analytics", 
    "Store Analytics", 
    "Pareto 80/20 Analysis", 
    "Market Basket Affinity Matrix",       
    "Dynamic Price Optimization Matrix",    
    "Business Insights Engine",
    "Customer Segments & Retention Risk",  
    "What-If Churn Simulator",            
    "ML Pipeline & Tuning Diagnostics"     
])

# -- Execute Filter Slicing Metrics --
filtered_df = df[df['Store'].isin(selected_stores) & df['Category'].isin(selected_categories)]
with st.sidebar.expander("📂 Dataset Actions", expanded=False):

    st.download_button(
        label="📥 Download Filtered CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_sales.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.subheader("Dataset Summary")

    if not filtered_df.empty:
        st.write(f"**Records:** {len(filtered_df):,}")
        st.write(f"**Columns:** {filtered_df.shape[1]}")
        st.write(f"**Stores:** {filtered_df['Store'].nunique()}")
        st.write(f"**Categories:** {filtered_df['Category'].nunique()}")

        # Dynamically detect the date column
        if "Date" in filtered_df.columns:
            st.write(
                f"**Date Range:** "
                f"{filtered_df['Date'].min().date()} → "
                f"{filtered_df['Date'].max().date()}"
            )

        # Show total sales if the column exists
        if "Revenue" in filtered_df.columns:
            st.write(f"**Total Revenue:** ${filtered_df['Revenue'].sum():,.2f}")
        elif "Sales" in filtered_df.columns:
            st.write(f"**Total Sales:** ${filtered_df['Sales'].sum():,.2f}")

    else:
        st.info("No data available for the selected filters.")

    st.markdown("---")
    st.caption(
        f"Current Dataset: {len(filtered_df):,} rows × "
        f"{filtered_df.shape[1]} columns"
    )
if not filtered_df.empty:
    engine.engineer_customer_profiles(filtered_df)
    customers = engine.customer_profiles
else:
    customers = pd.DataFrame()

AFF_PALETTE = ['#3D2314', '#C6A052', '#E5D3B3', '#8B5A2B', '#5C4033', '#D2B48C']

# -- Navigation Route Layouts --
if page_route == "Home Overview":
        st.subheader("Welcome to Business Intelligence for Premium Coffee")
        st.markdown("""
### About Afficionado Coffee Roasters

Founded in **2008**, Afficionado Coffee Roasters is a premium specialty coffee company dedicated to delivering exceptional coffee experiences through **direct trade sourcing, artisanal roasting, and sustainable partnerships**.

The company works closely with coffee farmers across renowned coffee-growing regions to build long-term relationships that ensure consistent quality, ethical sourcing, and economic sustainability for farming communities. Every coffee bean is carefully selected, expertly roasted, and crafted to highlight its unique origin and flavor profile.

Beyond producing world-class espresso, single-origin coffees, and signature blends, Afficionado focuses on innovation, hospitality, and environmental responsibility. Their commitment extends from farm to cup, emphasizing transparency, quality, and continuous improvement throughout the coffee supply chain.

This analytics dashboard transforms transaction-level sales data into actionable business intelligence, enabling stakeholders to:

- Analyze product popularity and profitability.
- Identify high-performing and underperforming menu items.
- Understand category-wise revenue contribution.
- Monitor sales trends and customer purchasing behavior.
- Support data-driven inventory, pricing, and marketing decisions.
- Drive operational efficiency and sustainable business growth.

By combining advanced analytics with Afficionado's commitment to quality and sustainability, this dashboard empowers informed decision-making across the organization.
""")
    
        st.markdown("---")
    
        st.subheader("🎓 Project Information")
        st.info("""
**Deployment Ready**: This dashboard is production-ready and suitable for:
- Real-world business deployment
- Executive reporting and decision-making

**Built With**: Python, Streamlit, Pandas, Plotly  
**Data Source**: Afficionado Coffee transaction database  
**Last Updated**: 2026-06-26
    """)
        st.markdown("---")
        st.subheader("🎯 Primary Objectives")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
1. **Analyze Overall Sales Performance**
   - Track revenue trends over time
   - Monitor transaction volume and patterns
   - Identify peak sales periods

2. **Identify Top-Selling Products**
   - Rank products by revenue and units sold
   - Track product-level profitability
   - Monitor product popularity by store
        """)
        with col2:
            st.markdown("""
3. **Measure Revenue Contribution**
   - Category-level revenue breakdown
   - Brand performance benchmarking
   - Store revenue comparison

4. **Support Data-Driven Decisions**
   - Inventory optimization recommendations
   - Promotional strategy guidance
   - Store performance benchmarking
        """)
    
        st.markdown("---")

        st.subheader("🚀 Secondary Objectives")
        with st.expander("View Secondary Features"):
            st.markdown("""
- **Inventory Optimization**: Identify slow-moving products and reorder strategies
- **Hero Product Identification**: Use Pareto analysis to find 80/20 revenue drivers
- **Long-Tail Analysis**: Detect low-volume products for bundling or discontinuation
- **Customer Behavior**: Analyze purchasing patterns by customer type
- **Automated Insights**: Generate business recommendations automatically
- **Promotional Guidance**: Identify products and categories for promotional campaigns
- **Multi-Store Benchmarking**: Compare performance across all store locations
- **Payment Analytics**: Understand payment method preferences and trends
        """)
    
        st.markdown("---")
        st.subheader("💡 How to Use This Dashboard")
    
        with st.expander("Step 1: Use Sidebar Filters", expanded=True):
            st.markdown("""
1. **Select Stores** — Choose which store locations to analyze
2. **Select Categories** — Filter by coffee, tea, bakery, etc.
3. **Select Brands** — Focus on specific brands or products
4. **Date Range** — Pick analysis time period
5. **Top N Slider** — Control how many products to display in detail views
        """)
    
        with st.expander("Step 2: Navigate Dashboard Sections"):
            st.markdown("""
Use the left navigation menu to jump between dashboard pages. Each page provides 
specific insights:
- Start with **Executive Dashboard** for high-level overview
- Drill into **Product Analytics** for detailed product performance
- Check **Store Analytics** for location-specific insights
- Review **Business Insights** for automated recommendations
        """)
    
        with st.expander("Step 3: Interact with Charts"):
            st.markdown("""
- **Hover** over charts to see detailed values
- **Click** legend items to show/hide data series
- **Zoom** by dragging on charts
- **Download** chart as PNG using camera icon
- **Export filtered data** using the download button in sidebar
        """)
    
        st.markdown("---")     
        st.subheader("📊 Insights")
    
        col1, col2 = st.columns(2)
    
        with col1:
            st.success("""
**✓ Hero Product Identification**

Use Pareto analysis to identify the 20% of products 
driving 80% of revenue. Focus inventory and marketing 
on these high-impact items.
        """)
    
        with col2:
            st.warning("""
**⚠ Inventory Optimization**

Identify slow-moving products consuming shelf space. 
Consider bundling, promotions, or discontinuation 
to improve overall profitability.
        """)
    
        st.markdown("---")

        st.subheader("🔧 Technology Stack")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
**Backend**
- Python 3.10+
- Pandas (data manipulation)
- NumPy (numerical computing)
        """)
        with col2:
            st.markdown("""
**Frontend**
- Streamlit (web framework)
- Plotly (interactive charts)
- HTML/CSS (styling)
        """)
        with col3:
            st.markdown("""
**Data Science**
- Scikit-learn (analytics)
- Pareto analysis
- Statistical aggregation
        """)
    
        st.markdown("---")
    
        st.subheader("📈 Key Metrics Available")
    
        metric_cols = st.columns(4)
    
        metrics = [
        ("Total Revenue", "Aggregate sales revenue across all channels"),
        ("Total Transactions", "Complete count of customer transactions"),
        ("Products Sold", "Total quantity of products sold"),
        ("Avg Order Value", "Average revenue per transaction"),
    ]
    
        for idx, (metric_name, metric_desc) in enumerate(metrics):
            with metric_cols[idx]:
                st.markdown(f"**{metric_name}**\n\n{metric_desc}")
    
        st.markdown("---")
        
# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================
# Purpose:
# This page provides a high-level overview of the business
# performance using Key Performance Indicators (KPIs),
# sales trends, and automated business insights.
#
# It serves as the landing page for executives and managers
# to quickly understand overall business health.
# ============================================================

elif page_route == "Executive Dashboard":

    # Display the section heading for the Executive Dashboard.
    st.markdown("<h2 class='section-title'>Executive Summary Overviews</h2>", unsafe_allow_html=True)

    # Retrieve all key performance indicators (KPIs)
    # from the analytics engine based on the currently
    # filtered dataset.
    kpis = engine.get_kpis(filtered_df)

    # Create four equal-width columns for KPI cards.
    c1, c2, c3, c4 = st.columns(4)

    # Display Total Revenue generated.
    with c1:
        st.markdown(
            f"<div class='metric-card'><div class='metric-title'>Gross Revenue Portfolio</div><div class='metric-value'>${kpis['total_revenue']:,.2f}</div></div>",
            unsafe_allow_html=True
        )

    # Display total number of completed transactions.
    with c2:
        st.markdown(
            f"<div class='metric-card'><div class='metric-title'>Consolidated Transactions</div><div class='metric-value'>{kpis['transactions']:,}</div></div>",
            unsafe_allow_html=True
        )

    # Display total quantity of products sold.
    with c3:
        st.markdown(
            f"<div class='metric-card'><div class='metric-title'>Product Units Dispatched</div><div class='metric-value'>{kpis['units_sold']:,}</div></div>",
            unsafe_allow_html=True
        )

    # Display Average Order Value (Revenue per Transaction).
    with c4:
        st.markdown(
            f"<div class='metric-card'><div class='metric-title'>Average Order Value (AOV)</div><div class='metric-value'>${kpis['aov']:,.2f}</div></div>",
            unsafe_allow_html=True
        )

    # Continue only if the filtered dataset contains records.
    if not filtered_df.empty:

        # Create two columns to display sales trend charts.
        cx1, cx2 = st.columns(2)

        # ------------------------------------------------------
        # Hourly Revenue Trend
        # ------------------------------------------------------
        with cx1:

            # Aggregate total revenue for every hour of the day.
            hourly_perf = (
                filtered_df
                .groupby('Hour')['Revenue']
                .sum()
                .reset_index()
            )

            # Display hourly revenue trend using a line chart.
            st.plotly_chart(
                px.line(
                    hourly_perf,
                    x='Hour',
                    y='Revenue',
                    title="Intraday Revenue Patterns",
                    color_discrete_sequence=['#3D2314']
                ),
                use_container_width=True
            )

        # ------------------------------------------------------
        # Daily Revenue Trend
        # ------------------------------------------------------
        with cx2:

            # Aggregate revenue for every weekday.
            # Reindex keeps weekdays in chronological order.
            day_perf = (
                filtered_df
                .groupby('Day')['Revenue']
                .sum()
                .reindex([
                    'Monday',
                    'Tuesday',
                    'Wednesday',
                    'Thursday',
                    'Friday',
                    'Saturday',
                    'Sunday'
                ])
                .reset_index()
            )

            # Display weekday revenue comparison.
            st.plotly_chart(
                px.bar(
                    day_perf,
                    x='Day',
                    y='Revenue',
                    title="Weekly Footprint Analysis",
                    color_discrete_sequence=['#C6A052']
                ),
                use_container_width=True
            )

    # ==========================================================
    # Executive Dashboard Insights
    # ==========================================================
    # The following calculations generate automatic business
    # insights based on the currently filtered dataset.
    # These values are displayed below the charts to help
    # executives quickly interpret business performance.
    # ==========================================================

    # ----------------------------------------------------------
    # Hour-wise Revenue Analysis
    # ----------------------------------------------------------
    # Calculate total revenue generated during each hour.
    hourly_summary = filtered_df.groupby("Hour")["Revenue"].sum()

    # Identify the hour with maximum revenue.
    peak_hour = hourly_summary.idxmax()
    peak_hour_sales = hourly_summary.max()

    # Identify the hour with minimum revenue.
    low_hour = hourly_summary.idxmin()
    low_hour_sales = hourly_summary.min()

    # ----------------------------------------------------------
    # Day-wise Revenue Analysis
    # ----------------------------------------------------------
    # Calculate revenue generated on each weekday.
    day_summary = (
        filtered_df.groupby("Day")["Revenue"]
        .sum()
        .reindex([
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ])
    )

    # Determine the highest-performing day.
    best_day = day_summary.idxmax()
    best_day_sales = day_summary.max()

    # Determine the lowest-performing day.
    worst_day = day_summary.idxmin()
    worst_day_sales = day_summary.min()

    # ----------------------------------------------------------
    # Average Revenue Calculation
    # ----------------------------------------------------------
    # Calculate average revenue generated every hour.
    avg_hourly_sales = hourly_summary.mean()

    # ----------------------------------------------------------
    # Weekday vs Weekend Business Pattern
    # ----------------------------------------------------------
    # Calculate total weekday revenue.
    weekday_revenue = day_summary.loc[
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    ].sum()

    # Calculate total weekend revenue.
    weekend_revenue = day_summary.loc[
        ["Saturday", "Sunday"]
    ].sum()

    # Identify whether business performs better
    # on weekdays or weekends.
    business_pattern = (
        "Weekend-driven"
        if weekend_revenue > weekday_revenue
        else "Weekday-driven"
    )

    # ----------------------------------------------------------
    # Display Automatically Generated Business Insights
    # ----------------------------------------------------------
    # The insights below summarize the key findings
    # calculated from the current filtered dataset
    # and provide actionable business recommendations.
    st.info(f"""
### 📌 Insights

### 1. Peak Sales Hour
The highest revenue was recorded at **{peak_hour}:00**, generating **${peak_hour_sales:,.2f}**.

### 2. Lowest Sales Hour
The lowest revenue was recorded at **{low_hour}:00**, generating **${low_hour_sales:,.2f}**.

### 3. Best Performing Day
The highest revenue was achieved on **{best_day}**, with total sales of **${best_day_sales:,.2f}**.

### 4. Lowest Performing Day
The lowest revenue was recorded on **{worst_day}**, with total sales of **${worst_day_sales:,.2f}**.

### 5. Average Hourly Revenue
The average revenue generated per hour is **${avg_hourly_sales:,.2f}**.

### 6. Business Demand Pattern
Sales are predominantly **{business_pattern.lower()}**, indicating where customer demand is concentrated.

""")
# ============================================================
# PRODUCT ANALYTICS MODULE
# ============================================================
# Purpose:
# This module provides detailed product-level performance
# analysis by evaluating revenue, sales volume, pricing,
# and comparative rankings.
#
# Business Objectives:
# • Identify best-selling products.
# • Detect underperforming products.
# • Compare revenue against quantity sold.
# • Support pricing and inventory decisions.
# ============================================================

elif page_route == "Product Analytics":

    # Display page heading.
    st.markdown(
        "<h2 class='section-title'>Product Metrics & Performance Matrices</h2>",
        unsafe_allow_html=True
    )

    # Brief description of the analytics available.
    st.markdown(
        "<p style='color: #666; font-size: 0.95rem; margin-bottom: 20px;'>"
        "Granular product item breakdowns pairing financial gross income "
        "yields with physical inventory dispatch frequencies."
        "</p>",
        unsafe_allow_html=True
    )

    # Continue only if records exist after filtering.
    if not filtered_df.empty:

        # ----------------------------------------------------
        # Product Performance Aggregation
        # ----------------------------------------------------
        # Aggregate product-level statistics including:
        # • Total Revenue
        # • Total Units Sold
        # • Average Selling Price
        #
        # The resulting dataframe is sorted in descending
        # order of revenue.
        prod_stats = (
            filtered_df
            .groupby(['Product_Name', 'Category'])
            .agg(
                Revenue_Generated=('Revenue', 'sum'),
                Volume_Sold=('Quantity', 'sum'),
                Mean_Price=('Unit_Price', 'mean')
            )
            .reset_index()
            .sort_values(
                by='Revenue_Generated',
                ascending=False
            )
        )

        # ----------------------------------------------------
        # Dashboard Layout
        # ----------------------------------------------------
        # Create two columns:
        #
        # Left:
        # Product performance table.
        #
        # Right:
        # Revenue vs Volume scatter plot.
        col_table, col_graph = st.columns([1, 1])

        # ====================================================
        # Product Performance Table
        # ====================================================
        with col_table:

            # Section title.
            st.markdown("#### 📋 **Performance Data Grid**")

            # Display Top-N products selected
            # from the sidebar slider.
            st.dataframe(
                prod_stats.head(top_n_slider).style.format({
                    'Revenue_Generated': '${:,.2f}',
                    'Mean_Price': '${:,.2f}',
                    'Volume_Sold': '{:,}'
                }),
                use_container_width=True
            )

        # ====================================================
        # Revenue vs Volume Scatter Plot
        # ====================================================
        with col_graph:

            # Section title.
            st.markdown("#### 🎯 **Volume vs. Revenue Yield Scatter Matrix**")

            # Scatter Plot Explanation
            #
            # X-axis:
            # Units Sold
            #
            # Y-axis:
            # Revenue Generated
            #
            # Bubble Size:
            # Revenue
            #
            # Bubble Color:
            # Product Category
            #
            # Used to identify:
            # • Hero Products
            # • Premium Products
            # • High Volume Low Revenue products
            # • Slow Moving products

            fig_scatter = px.scatter(
                prod_stats.head(top_n_slider),
                x='Volume_Sold',
                y='Revenue_Generated',
                size='Revenue_Generated',
                color='Category',
                hover_name='Product_Name',
                color_discrete_sequence=AFF_PALETTE,
                labels={
                    'Volume_Sold': 'Units Sold',
                    'Revenue_Generated': 'Gross Revenue ($)'
                }
            )

            # Improve chart appearance by reducing
            # margins and moving legend above chart.
            fig_scatter.update_layout(
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=10
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

            # Display interactive scatter plot.
            st.plotly_chart(
                fig_scatter,
                use_container_width=True
            )

        # Add visual separator.
        st.markdown(
            "<hr style='margin: 25px 0; border-color: #EAEAEA;'>",
            unsafe_allow_html=True
        )

        # ====================================================
        # Revenue Ranking Analysis
        # ====================================================
        # Compare highest-performing and lowest-performing
        # products based on revenue generated.
        st.markdown("#### 📈 **Portfolio Extremity Visualizer**")

        col_p1, col_p2 = st.columns(2)

        # ====================================================
        # Top Revenue Products
        # ====================================================
        with col_p1:

            # Horizontal bar chart displaying
            # highest revenue-generating products.
            fig_top = px.bar(
                prod_stats.head(top_n_slider),
                x='Revenue_Generated',
                y='Product_Name',
                orientation='h',
                color_discrete_sequence=['#3D2314'],
                title=f"Top {top_n_slider} Revenue Drivers"
            )

            # Sort products from lowest to highest
            # within the chart for better readability.
            fig_top.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                xaxis_title="Revenue ($)",
                yaxis_title=""
            )

            # Display chart.
            st.plotly_chart(
                fig_top,
                use_container_width=True
            )

        # ====================================================
        # Bottom Revenue Products
        # ====================================================
        with col_p2:

            # Horizontal bar chart displaying
            # lowest revenue-generating products.
            fig_tail = px.bar(
                prod_stats.tail(top_n_slider),
                x='Revenue_Generated',
                y='Product_Name',
                orientation='h',
                color_discrete_sequence=['#C6A052'],
                title=f"Trailing {top_n_slider} Long-Tail SKUs"
            )

            # Display lowest-performing products.
            fig_tail.update_layout(
                yaxis={'categoryorder': 'total descending'},
                xaxis_title="Revenue ($)",
                yaxis_title=""
            )

            # Display chart.
            st.plotly_chart(
                fig_tail,
                use_container_width=True
            )

    else:

        # Display warning when the selected filters
        # produce an empty dataset.
        st.warning(
            "No data points matching active filter conditions "
            "to map inside the product analytics module."
        )
# ============================================================
# Product Analytics Insights
# ============================================================
# Generate business insights dynamically based on the
# filtered product performance data.
# ============================================================

    st.markdown("---")
    st.subheader("📊 Product Performance Insights")

# Overall statistics
    total_products = prod_stats.shape[0]
    top_product = prod_stats.iloc[0]
    bottom_product = prod_stats.iloc[-1]

    avg_revenue = prod_stats["Revenue_Generated"].mean()
    avg_volume = prod_stats["Volume_Sold"].mean()
    avg_price = prod_stats["Mean_Price"].mean()

# Highest volume product
    highest_volume = prod_stats.loc[
    prod_stats["Volume_Sold"].idxmax()
]

# Highest priced product
    highest_price = prod_stats.loc[
    prod_stats["Mean_Price"].idxmax()
]

# Revenue concentration of Top-N products
    top_revenue = prod_stats.head(top_n_slider)["Revenue_Generated"].sum()
    overall_revenue = prod_stats["Revenue_Generated"].sum()
    top_revenue_pct = (top_revenue / overall_revenue) * 100

# KPI Cards
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Products Analysed", total_products)

    with m2:
        st.metric(
        "Highest Revenue Product",
        top_product["Product_Name"]
    )

    with m3:
        st.metric(
        "Highest Volume Product",
        highest_volume["Product_Name"]
    )

    with m4:
        st.metric(
        "Highest Price Product",
        highest_price["Product_Name"]
    )

    st.info(f"""
### Summary

### 1. Product Portfolio
A total of **{total_products} products** are included in the current analysis after applying the selected filters.

### 2. Highest Revenue Product
**{top_product['Product_Name']}** generated the highest revenue of **${top_product['Revenue_Generated']:,.2f}**, making it the strongest contributor to overall sales.

### 3. Highest Selling Product
**{highest_volume['Product_Name']}** recorded the highest sales volume with **{highest_volume['Volume_Sold']:,} units sold**, indicating strong customer demand.

### 4. Premium Product
**{highest_price['Product_Name']}** has the highest average selling price of **${highest_price['Mean_Price']:,.2f}**, representing the premium-priced offering in the portfolio.

### 5. Lowest Performing Product
**{bottom_product['Product_Name']}** generated the lowest revenue of **${bottom_product['Revenue_Generated']:,.2f}**, making it a potential candidate for promotional campaigns or portfolio review.

### 6. Revenue Concentration
The **Top {top_n_slider} products** contribute **{top_revenue_pct:.1f}%** of the total product revenue, indicating the level of revenue dependency on the leading products.

### 7. Average Product Performance
• Average Revenue per Product: **${avg_revenue:,.2f}**

• Average Units Sold per Product: **{avg_volume:,.0f}**

• Average Selling Price: **${avg_price:,.2f}**

""")

# ============================================================
# CATEGORY & BRAND ANALYTICS MODULE
# ============================================================
# Purpose:
# This module analyzes the hierarchical relationship between
# Product Categories, Brands, and Individual Products.
#
# Business Objectives:
# • Identify the highest revenue-generating categories.
# • Compare brand performance within each category.
# • Understand product contribution to overall revenue.
# • Visualize revenue hierarchy using a Treemap.
# ============================================================

elif page_route == "Category & Brand Analytics":

    # Display page title.
    st.markdown(
        "<h2 class='section-title'>Segment Decomposition Hierarchy</h2>",
        unsafe_allow_html=True
    )

    # Continue only if the filtered dataset contains records.
    if not filtered_df.empty:

        # ----------------------------------------------------
        # Hierarchical Revenue Aggregation
        # ----------------------------------------------------
        # Aggregate revenue at three business levels:
        #
        # Category
        #    └── Brand
        #          └── Product
        #
        # This dataframe is used to generate the Treemap.
        tree_df = (
            filtered_df
            .groupby(
                ['Category', 'Brand', 'Product_Name']
            )['Revenue']
            .sum()
            .reset_index()
        )

        # ----------------------------------------------------
        # Treemap Visualization
        # ----------------------------------------------------
        # Rectangle Size:
        # Revenue
        #
        # Rectangle Color:
        # Revenue intensity
        #
        # Purpose:
        # Provides a drill-down view from
        # Category → Brand → Product.
        fig = px.treemap(
            tree_df,
            path=['Category', 'Brand', 'Product_Name'],
            values='Revenue',
            color='Revenue',
            color_continuous_scale='YlOrBr'
        )

        # Display interactive treemap.
        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Add visual separator before insights.
        st.markdown("---")

        # ====================================================
        # Category & Brand Insights
        # ====================================================
        # Generate dynamic business insights based on the
        # currently selected filters.
        # ====================================================

        # Calculate total revenue for all visible products.
        total_revenue = tree_df["Revenue"].sum()

        # ----------------------------------------------------
        # Category Performance
        # ----------------------------------------------------
        # Calculate total revenue generated
        # by each product category.
        category_summary = (
            tree_df.groupby("Category")["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        # Identify the highest-performing category.
        top_category = category_summary.index[0]
        top_category_rev = category_summary.iloc[0]

        # Calculate revenue contribution percentage.
        top_category_pct = (
            top_category_rev / total_revenue
        ) * 100

        # ----------------------------------------------------
        # Brand Performance
        # ----------------------------------------------------
        # Calculate total revenue generated
        # by each brand.
        brand_summary = (
            tree_df.groupby("Brand")["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        # Identify highest-performing brand.
        top_brand = brand_summary.index[0]
        top_brand_rev = brand_summary.iloc[0]

        # Calculate brand contribution percentage.
        top_brand_pct = (
            top_brand_rev / total_revenue
        ) * 100

        # ----------------------------------------------------
        # Product Performance
        # ----------------------------------------------------
        # Calculate revenue generated by
        # individual products.
        product_summary = (
            tree_df.groupby("Product_Name")["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        # Identify highest revenue product.
        top_product = product_summary.index[0]
        top_product_rev = product_summary.iloc[0]

        # ----------------------------------------------------
        # Portfolio Statistics
        # ----------------------------------------------------
        # Count the number of unique
        # Categories, Brands and Products.
        total_categories = tree_df["Category"].nunique()
        total_brands = tree_df["Brand"].nunique()
        total_products = tree_df["Product_Name"].nunique()

        # ----------------------------------------------------
        # KPI Cards
        # ----------------------------------------------------
        # Display quick statistics for the
        # currently filtered dataset.
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Categories",
                total_categories
            )

        with col2:
            st.metric(
                "Brands",
                total_brands
            )

        with col3:
            st.metric(
                "Products",
                total_products
            )

        # ----------------------------------------------------
        # Dynamic Business Insights
        # ----------------------------------------------------
        # These insights summarize the
        # treemap analysis and automatically
        # update whenever the user changes
        # the dashboard filters.
        st.info(f"""
**Revenue Overview**

• **Total Revenue:** ₹{total_revenue:,.2f}

• **Highest Revenue Category:** **{top_category}**
  - Revenue: ₹{top_category_rev:,.2f}
  - Contribution: **{top_category_pct:.1f}%**

• **Highest Revenue Brand:** **{top_brand}**
  - Revenue: ₹{top_brand_rev:,.2f}
  - Contribution: **{top_brand_pct:.1f}%**

• **Best Performing Product:** **{top_product}**
  - Revenue: ₹{top_product_rev:,.2f}

• The treemap highlights revenue concentration from **Category → Brand → Product**, making it easy to identify the strongest and weakest revenue contributors.
""")

# ============================================================
# STORE ANALYTICS MODULE
# ============================================================
# Purpose:
# Analyze the business performance of each retail store by
# comparing revenue, transactions, sales volume, and
# Average Order Value (AOV).
#
# Business Objectives:
# • Compare revenue across stores.
# • Measure customer traffic at each location.
# • Identify stores with the highest average bill value.
# • Benchmark store performance for business decisions.
# ============================================================

elif page_route == "Store Analytics":

    # Display page title.
    st.markdown(
        "<h2 class='section-title'>Location Profile Performance Mapping</h2>",
        unsafe_allow_html=True
    )

    # Brief description of the page.
    st.markdown(
        "<p style='color: #666; font-size: 0.95rem; margin-bottom: 20px;'>"
        "Comparative evaluation of physical retail units assessing store throughput velocity, "
        "cash capture margins, and transactional values."
        "</p>",
        unsafe_allow_html=True
    )

    # Continue only if filtered data is available.
    if not filtered_df.empty:

        # ----------------------------------------------------
        # Store Level Aggregation
        # ----------------------------------------------------
        # Calculate store-wise business metrics:
        #
        # • Total Revenue
        # • Number of Transactions
        # • Total Quantity Sold
        #
        # Stores are sorted based on revenue.
        store_stats = (
            filtered_df
            .groupby('Store')
            .agg(
                Revenue=('Revenue', 'sum'),
                Transactions=('Transaction_ID', 'nunique'),
                Volume_Units=('Quantity', 'sum')
            )
            .reset_index()
            .sort_values(
                by='Revenue',
                ascending=False
            )
        )

        # Calculate Average Order Value (AOV)
        # for every store.
        store_stats['Calculated_AOV'] = (
            store_stats['Revenue']
            / store_stats['Transactions']
        )

        # ----------------------------------------------------
        # Dashboard Layout
        # ----------------------------------------------------
        # Left Column:
        # • Metrics Table
        # • AOV Chart
        #
        # Right Column:
        # • Revenue vs Transactions Chart
        col_st_left, col_st_right = st.columns([1, 1])

        # ====================================================
        # LEFT PANEL
        # ====================================================
        with col_st_left:

            # Display store performance table.
            st.markdown(
                "#### 🏢 **Location Footprint Metrics Table**"
            )

            # Format values for better readability.
            st.dataframe(
                store_stats.style.format({
                    'Revenue': '${:,.2f}',
                    'Transactions': '{:,}',
                    'Volume_Units': '{:,}',
                    'Calculated_AOV': '${:,.2f}'
                }),
                use_container_width=True
            )

            # ------------------------------------------------
            # Average Order Value Chart
            # ------------------------------------------------
            # Compare the average amount spent
            # by customers at each store.
            st.markdown(
                "#### 💰 **Average Order Value (AOV) Efficiency**"
            )

            fig_aov = px.bar(
                store_stats,
                x='Store',
                y='Calculated_AOV',
                text_auto='$.2f',
                color_discrete_sequence=['#8B5A2B'],
                title="Shed Benchmarks: Transaction Basket Ticket Size"
            )

            # Improve chart labels.
            fig_aov.update_layout(
                xaxis_title="",
                yaxis_title="AOV ($)"
            )

            # Display chart.
            st.plotly_chart(
                fig_aov,
                use_container_width=True
            )

        # ====================================================
        # RIGHT PANEL
        # ====================================================
        with col_st_right:

            # Display comparison chart title.
            st.markdown(
                "#### 📊 **Volume Throughput vs Gross Capture Breakdown**"
            )

            # ------------------------------------------------
            # Composite Revenue vs Transactions Chart
            # ------------------------------------------------
            # Create grouped bar chart for comparing:
            #
            # • Revenue
            # • Number of Transactions
            #
            # across all stores.
            fig_composite = go.Figure()

            # Revenue Bar
            fig_composite.add_trace(
                go.Bar(
                    x=store_stats['Store'],
                    y=store_stats['Revenue'],
                    name='Gross Revenue ($)',
                    marker_color='#3D2314',
                    text=store_stats['Revenue'].map('${:,.0f}'.format),
                    textposition='auto'
                )
            )

            # Transaction Count Bar
            fig_composite.add_trace(
                go.Bar(
                    x=store_stats['Store'],
                    y=store_stats['Transactions'],
                    name='Footfall Ticket Count',
                    marker_color='#C6A052',
                    text=store_stats['Transactions'].map('{:,}'.format),
                    textposition='auto'
                )
            )

            # Improve chart appearance.
            fig_composite.update_layout(
    title=dict(
        text="Location Market Contribution & Traffic Profiles",
        x=0.5,
        xanchor="center",
        y=0.93,          # Lower than the default
        yanchor="top",
        font=dict(size=18)
    ),
    barmode='group',
    xaxis_title="",
    yaxis_title="Scale Units",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(
        l=10,
        r=10,
        t=90,
        b=10
    )
)

            # Display grouped comparison chart.
            st.plotly_chart(
                fig_composite,
                use_container_width=True
            )

    else:

        # Display warning when no records
        # are available after filtering.
        st.warning(
            "No data points matching active filter conditions "
            "to map inside the store analytics module."
        )
# ============================================================
# Store Analytics Insights
# ============================================================
# Generate dynamic insights for store performance.
# These insights automatically update based on the
# selected dashboard filters.
# ============================================================

    st.markdown("---")
    st.subheader("📊 Store Performance Insights")

# Identify best and worst performing stores
    best_revenue_store = store_stats.loc[store_stats["Revenue"].idxmax()]
    worst_revenue_store = store_stats.loc[store_stats["Revenue"].idxmin()]

    highest_aov_store = store_stats.loc[store_stats["Calculated_AOV"].idxmax()]
    highest_transaction_store = store_stats.loc[store_stats["Transactions"].idxmax()]

    avg_store_revenue = store_stats["Revenue"].mean()
    avg_store_transactions = store_stats["Transactions"].mean()
    avg_store_aov = store_stats["Calculated_AOV"].mean()

# KPI Cards
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric("Best Revenue Store", best_revenue_store["Store"])

    with k2:
        st.metric("Highest AOV Store", highest_aov_store["Store"])

    with k3:
        st.metric("Highest Footfall Store", highest_transaction_store["Store"])

    with k4:
            st.metric("Stores Analysed", len(store_stats))

    st.info(f"""
### 📌 Store Performance Summary

**1. Highest Revenue Store**

**{best_revenue_store['Store']}** generated the highest revenue of **${best_revenue_store['Revenue']:,.2f}**, making it the leading contributor to overall business revenue.

**2. Highest Customer Footfall**

**{highest_transaction_store['Store']}** recorded the highest number of transactions with **{highest_transaction_store['Transactions']:,}** customer purchases, indicating the strongest customer traffic.

**3. Highest Average Order Value (AOV)**

Customers at **{highest_aov_store['Store']}** spent an average of **${highest_aov_store['Calculated_AOV']:,.2f}** per transaction, representing the highest customer spending among all stores.

**4. Lowest Revenue Store**

**{worst_revenue_store['Store']}** generated the lowest revenue of **${worst_revenue_store['Revenue']:,.2f}**, making it the weakest-performing location in the selected period.

**5. Average Store Performance**

• Average Revenue per Store: **${avg_store_revenue:,.2f}**

• Average Transactions per Store: **{avg_store_transactions:,.0f}**

• Average Order Value: **${avg_store_aov:,.2f}**

**6. Revenue vs Customer Traffic Analysis**

The grouped comparison chart shows whether store revenue is primarily driven by **high customer traffic** or by **higher customer spending per transaction**, allowing easy comparison of store performance.

**7. Overall Store Benchmark**

The store metrics table provides a comprehensive comparison of revenue, transaction count, sales volume, and Average Order Value, enabling quick identification of high-performing and low-performing stores within the selected filters.
""")

# ============================================================
# PARETO 80/20 ANALYSIS MODULE
# ============================================================
# Purpose:
# Identify the small percentage of products that contribute
# the majority of total revenue using the Pareto Principle
# (80/20 Rule).
#
# Business Objectives:
# • Identify Hero Products.
# • Measure revenue concentration.
# • Detect Long-Tail products.
# • Support inventory optimization.
# ============================================================

elif page_route == "Pareto 80/20 Analysis":

    # Display page title.
    st.markdown(
        "<h2 class='section-title'>Pareto Concentration Vectors</h2>",
        unsafe_allow_html=True
    )

    # Perform Pareto analysis using the analytics engine.
    #
    # Returns:
    # p_df   -> Complete Pareto dataframe
    # heroes -> High-performing products
    # tails  -> Low-performing products
    p_df, heroes, tails = engine.get_pareto_analysis(filtered_df)

    # Continue only if products are available.
    if not p_df.empty:

        # Create a bar chart showing the
        # highest revenue-generating products.
        fig_p = go.Figure()

        fig_p.add_trace(
            go.Bar(
                x=p_df['Product_Name'].head(15),
                y=p_df['Total_Revenue'].head(15),
                name='SKU Revenue',
                marker_color='#3D2314'
            )
        )

        # Display Pareto chart.
        st.plotly_chart(
            fig_p,
            use_container_width=True
        )
# ============================================================
# Pareto Analysis Insights
# ============================================================

    st.markdown("---")
    st.subheader("📊 Pareto Analysis Insights")

# Overall statistics
    total_products = len(p_df)

# Number of Hero and Long-Tail products
    hero_products = len(heroes)
    tail_products = len(tails)

# Total Revenue
    total_revenue = p_df["Total_Revenue"].sum()

# Revenue generated by Hero Products
    hero_revenue = (
    p_df[p_df["Product_Name"].isin(heroes)]["Total_Revenue"].sum()
)

# Revenue generated by Long-Tail Products
    tail_revenue = (
    p_df[p_df["Product_Name"].isin(tails)]["Total_Revenue"].sum()
)

# Percentage Contribution
    hero_pct = (hero_revenue / total_revenue) * 100 if total_revenue else 0
    tail_pct = (tail_revenue / total_revenue) * 100 if total_revenue else 0

# Highest Revenue Product
    top_product = p_df.iloc[0]

# KPI Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Hero Products", hero_products)

    with c2:
        st.metric("Long-Tail Products", tail_products)

    with c3:
        st.metric("Top Revenue Product", top_product["Product_Name"])

    with c4:
        st.metric("Products Analysed", total_products)

    st.info(f"""
### 📌 Summary

**1. Product Portfolio**

A total of **{total_products} products** were analyzed under the current dashboard filters.

**2. Hero Products**

The identified **{hero_products} Hero Products** contribute **{hero_pct:.1f}%** of the total revenue.

**3. Long-Tail Products**

The remaining **{tail_products} Long-Tail Products** contribute **{tail_pct:.1f}%** of the total revenue.

**4. Highest Revenue Product**

**{top_product['Product_Name']}** generated the highest revenue of **${top_product['Total_Revenue']:,.2f}**.

**5. Revenue Concentration**

The Pareto chart demonstrates how revenue is concentrated among the highest-performing products, helping identify the products that contribute the largest share of business revenue.

**6. Product Distribution**

The comparison between Hero Products and Long-Tail Products highlights the distribution of revenue across the product portfolio and identifies the products with the greatest business impact.
""")

# ============================================================
# MARKET BASKET AFFINITY MATRIX
# ============================================================
# Purpose:
# Analyze products that are frequently purchased together
# within the same transaction.
#
# Business Objectives:
# • Identify frequently purchased product pairs.
# • Discover cross-selling opportunities.
# • Understand customer purchasing patterns.
# • Support bundle and combo analysis.
# ============================================================

elif page_route == "Market Basket Affinity Matrix":

    # Display page heading.
    st.markdown("<h2 class='section-title'>Advanced Product Affinity & Co-Occurrence Matrix</h2>", unsafe_allow_html=True)

    # Brief explanation of the analysis.
    st.markdown(
        "This module groups items purchased at the exact same location, date, and timestamp "
        "to calculate cross-category bundling targets."
    )

    # --------------------------------------------------------
    # Compute product affinity relationships.
    # Each row represents one frequently occurring product pair.
    # --------------------------------------------------------
    basket_df = engine.compute_market_basket_affinities(filtered_df)

    # Continue only if product pair combinations exist.
    if not basket_df.empty:

        # Split page into two sections:
        # Left  -> Table + Bar Chart
        # Right -> Quick Summary
        col_b1, col_b2 = st.columns([2, 1])

        # ====================================================
        # LEFT PANEL
        # ====================================================
        with col_b1:

            # Display the strongest product combinations.
            st.subheader("Top Correlated Operational Product Pairs")

            # Product pair table with conditional formatting.
            st.dataframe(
                basket_df.head(top_n_slider)
                .style.background_gradient(
                    cmap='YlOrBr',
                    subset=['Co-Occurrence Count']
                ),
                use_container_width=True
            )

            # ------------------------------------------------
            # Product Pair Visualization
            # ------------------------------------------------
            # Horizontal bar chart showing the
            # most frequently purchased combinations.
            st.subheader("Cross-Selling Affinity Volume Visualizer")

            chart_data = basket_df.head(
                min(len(basket_df), top_n_slider)
            )

            # Combine two product names into one label.
            chart_data['Combo_Label'] = (
                chart_data['Item A']
                + " + "
                + chart_data['Item B']
            )

            st.plotly_chart(
                px.bar(
                    chart_data,
                    x='Co-Occurrence Count',
                    y='Combo_Label',
                    orientation='h',
                    color='Co-Occurrence Count',
                    color_continuous_scale='YlOrBr'
                ).update_layout(
                    yaxis={'categoryorder': 'total ascending'}
                ),
                use_container_width=True
            )

        # ====================================================
        # RIGHT PANEL
        # ====================================================
        with col_b2:

            # Highlight the strongest product pair.
            st.info("### Strategic Merchandising Playbook")

            top_pair = basket_df.iloc[0]

            # Display the strongest affinity pair.
            st.markdown(
                f"**Identified Core Pairing Node:**\n\n"
                f"`{top_pair['Item A']}`\n\n"
                f"**and**\n\n"
                f"`{top_pair['Item B']}`"
            )

            # Display pair frequency.
            st.markdown(
                f"**Cross-Purchase Volume:** "
                f"`{top_pair['Co-Occurrence Count']}` "
                f"matching basket records inside selected filters."
            )

            # Highlight the strongest affinity combination.
            st.success(
                "💡 **Action Vector:** Launch an integrated point-of-sale "
                "layout adjustment or digital check-out pairing suggestion "
                "to capitalize on this high-affinity node."
            )

    else:

        # Display warning if no matching
        # product combinations are found.
        st.warning(
            "No overlapping proxy checkout timestamps detected "
            "inside this filtered slice profile layout."
        )
    # ============================================================
    # Market Basket Insights
    # ============================================================
    # Generate dynamic insights for product affinity analysis.
    # ============================================================

    st.markdown("---")
    st.subheader("📊 Market Basket Insights")

    # Overall statistics
    total_pairs = len(basket_df)

    top_pair = basket_df.iloc[0]
    lowest_pair = basket_df.iloc[-1]

    avg_occurrence = basket_df["Co-Occurrence Count"].mean()
    max_occurrence = basket_df["Co-Occurrence Count"].max()
    min_occurrence = basket_df["Co-Occurrence Count"].min()

    # KPI Cards
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Product Pairs", total_pairs)

    with m2:
        st.metric(
            "Top Affinity Pair",
            f"{top_pair['Item A']} + {top_pair['Item B']}"
        )

    with m3:
        st.metric(
            "Highest Co-Occurrence",
            int(max_occurrence)
        )

    with m4:
        st.metric(
            "Average Co-Occurrence",
            f"{avg_occurrence:.1f}"
        )

    st.info(f"""
    ### 📌 Summary

    **1. Product Pair Analysis**

    A total of **{total_pairs} product combinations** were identified from the filtered transaction data.

    **2. Strongest Product Affinity**

    The combination of **{top_pair['Item A']}** and **{top_pair['Item B']}** appears most frequently with **{int(max_occurrence)}** co-occurring purchases.

    **3. Average Basket Association**

    Across all identified product pairs, the average co-occurrence count is **{avg_occurrence:.1f}**, indicating the typical frequency of products being purchased together.

    **4. Lowest Product Affinity**

    The combination **{lowest_pair['Item A']}** and **{lowest_pair['Item B']}** recorded the lowest co-occurrence count of **{int(min_occurrence)}**.

    **5. Cross-Selling Distribution**

    The horizontal bar chart ranks product combinations by purchase frequency, making it easy to identify the strongest customer purchasing relationships.

    **6. Product Pair Matrix**

    The affinity table provides a detailed comparison of all detected product pairs and their purchase frequencies, enabling quick identification of the most common shopping combinations.
    """)

# ============================================================
# DYNAMIC PRICE OPTIMIZATION MATRIX
# ============================================================
# Purpose:
# Analyze product pricing performance by comparing
# selling price, revenue generation, and sales volume.
#
# Business Objectives:
# • Identify premium-priced products.
# • Compare price against revenue performance.
# • Detect products suitable for pricing adjustments.
# • Support data-driven pricing strategies.
# ============================================================

elif page_route == "Dynamic Price Optimization Matrix":

    # Display page heading.
    st.markdown(
        "<h2 class='section-title'>Dynamic Pricing Elasticity Matrix</h2>",
        unsafe_allow_html=True
    )

    # Generate pricing elasticity metrics for each product.
    pricing_df = engine.evaluate_pricing_elasticity(filtered_df)

    # Continue only if pricing data is available.
    if not pricing_df.empty:

        # ----------------------------------------------------
        # Pricing Performance Table
        # ----------------------------------------------------
        # Display all calculated pricing metrics.
        st.dataframe(
            pricing_df,
            use_container_width=True
        )

        # ----------------------------------------------------
        # Price vs Revenue Scatter Plot
        # ----------------------------------------------------
        #
        # X-axis:
        # Average Selling Price
        #
        # Y-axis:
        # Total Revenue
        #
        # Bubble Size:
        # Total Sales Volume
        #
        # Bubble Color:
        # Pricing Recommendation
        #
        # Purpose:
        # Visualize the relationship between
        # pricing, revenue generation,
        # and product demand.
        st.plotly_chart(
            px.scatter(
                pricing_df,
                x='Average_Unit_Price',
                y='Total_Gross_Revenue',
                size='Total_Volume',
                color='Strategic_Pricing_Recommendation',
                color_discrete_sequence=AFF_PALETTE
            ),
            use_container_width=True
        )

    # ============================================================
    # Dynamic Pricing Insights
    # ============================================================
    # Generate pricing insights dynamically based on the
    # selected dashboard filters.
    # ============================================================

    st.markdown("---")
    st.subheader("📊 Pricing Performance Insights")

    # Overall statistics
    total_products = len(pricing_df)

    highest_revenue = pricing_df.loc[
        pricing_df["Total_Gross_Revenue"].idxmax()
    ]

    highest_price = pricing_df.loc[
        pricing_df["Average_Unit_Price"].idxmax()
    ]

    highest_volume = pricing_df.loc[
        pricing_df["Total_Volume"].idxmax()
    ]

    avg_price = pricing_df["Average_Unit_Price"].mean()
    avg_revenue = pricing_df["Total_Gross_Revenue"].mean()
    avg_volume = pricing_df["Total_Volume"].mean()

    # Count products in each pricing recommendation
    pricing_summary = (
        pricing_df["Strategic_Pricing_Recommendation"]
        .value_counts()
    )

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Products Analysed", total_products)

    with c2:
        st.metric("Highest Revenue Product", highest_revenue["Product_Name"])

    with c3:
        st.metric("Highest Price Product", highest_price["Product_Name"])

    with c4:
        st.metric("Highest Volume Product", highest_volume["Product_Name"])

    st.info(f"""
    ### 📌 Pricing Analysis Summary

    **1. Product Coverage**

    A total of **{total_products} products** were evaluated for pricing performance under the current dashboard filters.

    **2. Highest Revenue Product**

    **{highest_revenue['Product_Name']}** generated the highest revenue of **${highest_revenue['Total_Gross_Revenue']:,.2f}**.

    **3. Highest Priced Product**

    **{highest_price['Product_Name']}** has the highest average selling price of **${highest_price['Average_Unit_Price']:,.2f}**.

    **4. Highest Sales Volume**

    **{highest_volume['Product_Name']}** recorded the highest sales volume with **{highest_volume['Total_Volume']:,} units sold**.

    **5. Average Product Performance**

    • Average Selling Price: **${avg_price:,.2f}**

    • Average Revenue: **${avg_revenue:,.2f}**

    • Average Sales Volume: **{avg_volume:,.0f} units**

    **6. Pricing Recommendation Distribution**

    The pricing matrix classified products into **{pricing_summary.shape[0]} pricing recommendation categories**, allowing quick comparison of pricing opportunities across the product portfolio.

    **7. Price vs Revenue Relationship**

    The scatter plot illustrates how product pricing influences revenue generation while considering sales volume, making it easier to distinguish premium products, high-demand products, and pricing outliers.
    """)

elif page_route == "Business Insights Engine":
    st.markdown("<h2 class='section-title'>Automated Business Strategies</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8A8A8A; font-size: 0.95rem; margin-bottom: 25px;'>Real-time operational heuristics and programmatic inventory health strategies generated from active transactional telemetry buffers.</p>", unsafe_allow_html=True)
    
    insights = engine.generate_automated_insights(filtered_df)
    
    col_ins1, col_ins2, col_ins3 = st.columns(3)
    
    with col_ins1:
        st.markdown(f"""
            <div style="background: #FDFBF7; padding: 20px; border-radius: 6px; border-left: 4px solid #3D2314; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #7F7F7F; letter-spacing: 0.5px;">Top SKU Asset Line</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #2B160A; margin-top: 5px;">{insights['best_product']}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_ins2:
        st.markdown(f"""
            <div style="background: #FDFBF7; padding: 20px; border-radius: 6px; border-left: 4px solid #C6A052; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #7F7F7F; letter-spacing: 0.5px;">Top Category Tier</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #2B160A; margin-top: 5px;">{insights['best_category']}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_ins3:
        st.markdown(f"""
            <div style="background: #FDFBF7; padding: 20px; border-radius: 6px; border-left: 4px solid #8B5A2B; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #7F7F7F; letter-spacing: 0.5px;">Top Performing Location</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #2B160A; margin-top: 5px;">{insights['best_store']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_audit_left, col_audit_right = st.columns([1, 1])
    
    with col_audit_left:
        # Title updated to a high-contrast, professional crimson-accented warning title
        st.markdown("<h4 style='font-family: \"Inter\", sans-serif; font-weight: 700; font-size: 1.15rem; color: #E03C31; letter-spacing: 0.3px; margin-bottom: 12px;'>📊 Portfolio Risk Assessment</h4>", unsafe_allow_html=True)
        
        concentration = insights['revenue_concentration']
        badge_color = "#E03C31" if concentration > 75.0 else "#F0AD4E"
        
        st.markdown(f"""
            <div style="background: #FFFBFB; border: 1px solid #F5EAEB; padding: 20px; border-radius: 6px; margin-bottom: 15px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #2B160A; font-size: 0.95rem;">Revenue Concentration Index</span>
                    <span style="background: {badge_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">{concentration:.2f}%</span>
                </div>
                <p style="font-size: 0.85rem; color: #555; margin-top: 8px; line-height: 1.45;">
                    <strong>Risk Warning:</strong> Critical volume threshold breached. Your top performing Core SKU assets generate over 75% of your global gross intake yield. Portfolio vulnerability parameters are currently elevated.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_audit_right:
        # Title updated to an active, high-visibility corporate amber-brown blend
        st.markdown("<h4 style='font-family: \"Inter\", sans-serif; font-weight: 700; font-size: 1.15rem; color: #D48C2A; letter-spacing: 0.3px; margin-bottom: 12px;'>📉 Slowing Stock Buffers</h4>", unsafe_allow_html=True)
        
        items_html = "".join([f"<li style='padding: 6px 0; border-bottom: 1px solid #F0F0F0; font-size: 0.9rem; color: #333; font-weight: 500;'>⚠️ {item}</li>" for item in insights['underperforming_products']])
        
        st.markdown(f"""
            <div style="background: #F8F9FA; border: 1px solid #ECEEEF; padding: 15px 20px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <ul style="list-style-type: none; padding-left: 0; margin: 0;">
                    {items_html}
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h4 style='font-family: \"Inter\", sans-serif; font-weight: 700; font-size: 1.2rem; color: #C6A052; letter-spacing: 0.3px; margin-top: 25px; margin-bottom: 12px;'>⚡ Prescriptive Executive Actions</h4>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background: white; border: 1px solid #EAEAEA; border-radius: 6px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #F5F5F5;">
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <span style="font-size: 1.1rem; margin-right: 8px;">📦</span>
                    <strong style="color: #3D2314; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;">Inventory Allocation Strategy</strong>
                </div>
                <p style="margin: 0; font-size: 0.9rem; color: #444; line-height: 1.5; padding-left: 26px;">
                    {insights['inventory_suggestions'][0]} Adjust green coffee storage limits immediately to account for elevated convective heat-run periods on <em>"The Tank"</em>.
                </p>
            </div>
            <div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <span style="font-size: 1.1rem; margin-right: 8px;">🏷️</span>
                    <strong style="color: #C6A052; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;">Target Merchandising Campaign</strong>
                </div>
                <p style="margin: 0; font-size: 0.9rem; color: #444; line-height: 1.5; padding-left: 26px;">
                    {insights['promotional_suggestions'][0]} Design dynamic menu board modifications pairing under-utilized portfolio lines into unified cross-category bundles with main revenue drivers.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# CUSTOMER SEGMENTS & RETENTION RISK MODULE
# ============================================================
# Purpose:
# Analyze customer behaviour using Customer Lifetime Value (CLV),
# purchase frequency, spending patterns, and churn status.
#
# Business Objectives:
# • Identify high-value customer segments.
# • Compare Customer Lifetime Value across segments.
# • Detect customers with churn risk.
# • Understand customer purchasing behaviour.
# ============================================================

elif page_route == "Customer Segments & Retention Risk":

    # Display page heading.
    st.markdown(
        "<h2 class='section-title'>Customer Cohorts & Action Matrices</h2>",
        unsafe_allow_html=True
    )

    # Continue only if customer records exist.
    if not customers.empty:

        # ----------------------------------------------------
        # Customer Lifetime Value Distribution
        # ----------------------------------------------------
        # Box plot comparing Customer Lifetime Value (CLV)
        # across different customer segments.
        #
        # X-axis:
        # Customer Segment
        #
        # Y-axis:
        # Customer Lifetime Value
        #
        # Purpose:
        # Compare spending behaviour and identify
        # high-value customer groups.
        st.plotly_chart(
            px.box(
                customers,
                x='Segment',
                y='CLV',
                color='Segment',
                color_discrete_sequence=AFF_PALETTE
            ),
            use_container_width=True
        )

        # ----------------------------------------------------
        # Customer Summary Table
        # ----------------------------------------------------
        # Display customer-level metrics including:
        # • Customer ID
        # • Purchase Frequency
        # • Monetary Value
        # • Customer Lifetime Value
        # • Customer Segment
        # • Churn Status
        st.dataframe(
            customers[
                [
                    'Customer_ID',
                    'Frequency',
                    'Monetary',
                    'CLV',
                    'Segment',
                    'Churned'
                ]
            ],
            use_container_width=True
        )

# ============================================================
# Customer Segment Insights
# ============================================================
# Generate customer segmentation insights dynamically
# based on the selected dashboard filters.
# ============================================================

    st.markdown("---")
    st.subheader("📊 Customer Segment Insights")

    # Overall statistics
    total_customers = len(customers)

    highest_clv_customer = customers.loc[
        customers["CLV"].idxmax()
    ]

    highest_frequency_customer = customers.loc[
        customers["Frequency"].idxmax()
    ]

    highest_spending_customer = customers.loc[
        customers["Monetary"].idxmax()
    ]

    avg_clv = customers["CLV"].mean()
    avg_frequency = customers["Frequency"].mean()
    avg_monetary = customers["Monetary"].mean()

    segment_counts = customers["Segment"].value_counts()

    churn_count = customers["Churned"].sum()
    active_count = total_customers - churn_count

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Customers", total_customers)

    with c2:
        st.metric("Customer Segments", customers["Segment"].nunique())

    with c3:
        st.metric("Active Customers", active_count)

    with c4:
        st.metric("Churned Customers", churn_count)

    st.info(f"""
    ### 📌 Summary

    **1. Customer Coverage**

    A total of **{total_customers} customers** are included in the current analysis.

    **2. Highest Customer Lifetime Value**

    Customer **{highest_clv_customer['Customer_ID']}** has the highest Customer Lifetime Value (CLV) of **${highest_clv_customer['CLV']:,.2f}**.

    **3. Most Frequent Customer**

    Customer **{highest_frequency_customer['Customer_ID']}** completed **{highest_frequency_customer['Frequency']} purchases**, representing the highest purchase frequency.

    **4. Highest Spending Customer**

    Customer **{highest_spending_customer['Customer_ID']}** generated the highest monetary value of **${highest_spending_customer['Monetary']:,.2f}**.

    **5. Average Customer Performance**

    • Average Customer Lifetime Value: **${avg_clv:,.2f}**

    • Average Purchase Frequency: **{avg_frequency:.1f}**

    • Average Monetary Value: **${avg_monetary:,.2f}**

    **6. Customer Segmentation**

    The customer portfolio is distributed across **{customers['Segment'].nunique()} customer segments**, allowing comparison of purchasing behaviour and customer value.

    **7. Customer Retention Overview**

    Out of **{total_customers} customers**, **{active_count}** are currently active while **{churn_count}** are identified as churned based on the selected criteria.

    **8. Segment Distribution**

    The box plot illustrates the variation in Customer Lifetime Value across different customer segments, highlighting differences in customer value and purchasing behaviour.
    """)

# ============================================================
# WHAT-IF CHURN SIMULATOR MODULE
# ============================================================
# Purpose:
# Simulate different customer behaviour scenarios and
# predict the probability of customer churn using the
# trained Machine Learning model.
#
# Business Objectives:
# • Predict churn probability in real time.
# • Evaluate different customer behaviour scenarios.
# • Classify customers based on risk level.
# • Generate automated retention strategies.
# ============================================================

elif page_route == "What-If Churn Simulator":

    # Display the page title.
    st.markdown("<h2 class='section-title'>Real-Time Predictive What-If Simulator</h2>", unsafe_allow_html=True)

    # Display a brief description of the simulator.
    st.markdown("<p style='color: #8A8A8A; font-size: 0.95rem; margin-bottom: 25px;'>Adjust synthetic retention profiles to dynamically calculate customer churn probabilities and trigger automated risk playbooks.</p>", unsafe_allow_html=True)

    # Create a two-column layout:
    # Left  - Customer simulation inputs.
    # Right - Prediction results and retention strategy.
    col_sim_left, col_sim_right = st.columns([1, 1])

    # ========================================================
    # Customer Simulation Controls
    # ========================================================
    with col_sim_left:

        # Display the simulation controls heading.
        st.markdown("<h4 style='font-family: \"Inter\", sans-serif; font-weight: 700; font-size: 1.15rem; color: #ff0000; letter-spacing: 0.3px; margin-bottom: 15px;'>🎛️ Simulation Controls</h4>", unsafe_allow_html=True)

        # Input slider for customer purchase frequency.
        sim_freq = st.slider("Simulated Orders Frequency Count", 1, 60, 15, help="Total transactions a customer has made over the tracking window.")

        # Input slider for total customer spending.
        sim_money = st.slider("Simulated Financial Monetary Yield ($)", 5.0, 500.0, 85.0, help="Total gross dollar value spent by this user segment.")

        # Input slider for average number of items purchased per transaction.
        sim_items = st.slider("Average Ticket Item Quantity", 1.0, 10.0, 2.2, step=0.1)

        # Input slider representing purchases from Circular Economy product categories.
        sim_byproduct = st.slider("Plant Byproduct Basket Ratio", 0.0, 1.0, 0.25, step=0.05, help="Percentage of purchases from Circular Economy lines (Tea/Chocolate/Bakery).")

        # Input slider representing the proportion of evening purchases.
        sim_night = st.slider("Night-Time Transaction Ratio", 0.0, 1.0, 0.10, step=0.05, help="Ratio of visits logging past 16:00 (4 PM).")

    # Generate churn prediction using the trained machine learning model.
    res = engine.predict_custom_scenario(sim_freq, sim_money, sim_items, sim_byproduct, sim_night)

    # Convert churn probability into percentage format.
    prob_pct = res['churn_probability'] * 100

    # Determine the customer risk category based on churn probability.
    if prob_pct > 75.0:
        # Critical churn risk.
        status_color = "#E03C31"
        status_lbl = "CRITICAL RISK PROFILE"

    elif prob_pct >= (engine.optimal_threshold * 100):
        # Moderate churn risk.
        status_color = "#D48C2A"
        status_lbl = "ELEVATED RISK PROFILE"

    else:
        # Low churn risk.
        status_color = "#2E7D32"
        status_lbl = "STABLE RETENTION ACCOUNT"

    # ========================================================
    # Prediction Results
    # ========================================================
    with col_sim_right:

        # Display the prediction results heading.
        st.markdown("<h4 style='font-family: \"Inter\", sans-serif; font-weight: 700; font-size: 1.15rem; color: #ff0000; letter-spacing: 0.3px; margin-bottom: 15px;'>🔮 ML Engine Evaluation</h4>", unsafe_allow_html=True)

        # Display the predicted churn probability and customer risk level.
        st.markdown(f"""
            <div style="background: #FDFBF7; padding: 25px; border-radius: 6px; border-left: 5px solid {status_color}; box-shadow: 0 2px 4px rgba(0,0,0,0.03); margin-bottom: 20px;">
                <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #7F7F7F; letter-spacing: 0.5px;">Calculated Churn Probability</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #2B160A; margin-top: 2px;">{prob_pct:.1f}%</div>
                <div style="display: inline-block; background: {status_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; margin-top: 10px;">
                    {status_lbl}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Display the retention strategy heading.
        st.markdown("<h4 style='font-family: \"Inter\", sans-serif; font-weight: 700; font-size: 1.15rem; color: #C6A052; letter-spacing: 0.3px; margin-bottom: 12px;'>⚡ Prescriptive Retention Playbook</h4>", unsafe_allow_html=True)

        # Display the retention playbook generated by the prediction engine.
        st.markdown(f"""
            <div style="background: white; border: 1px solid #EAEAEA; border-radius: 6px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                <div style="display: flex; align-items: flex-start;">
                    <span style="font-size: 1.2rem; margin-right: 10px; margin-top: 2px;">⚙️</span>
                    <div>
                        <strong style="color: #3D2314; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;">Automated Action Vector</strong>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #444; line-height: 1.5;">
                            {res['retention_playbook']}
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# MACHINE LEARNING PIPELINE & TUNING DIAGNOSTICS MODULE
# ============================================================
# Purpose:
# This module provides a technical overview of the trained
# Machine Learning pipeline, including model configuration,
# optimized hyperparameters, and feature importance.
#
# Business Objectives:
# • Display the ML model architecture.
# • Present optimized tuning parameters.
# • Show the optimal decision threshold.
# • Visualize feature importance.
# ============================================================

elif page_route == "ML Pipeline & Tuning Diagnostics":

    # Display the page title.
    st.markdown("<h2 class='section-title'>Model Diagnostics & Pipeline Tuning Architecture</h2>", unsafe_allow_html=True)

    # Display a brief description of the diagnostics page.
    st.markdown("<p style='color: #8A8A8A; font-size: 0.95rem; margin-bottom: 25px;'>Technical inspection layer exposing cross-validated hyperparameter matrices, decision thresholds, and calculated algorithmic feature weights.</p>", unsafe_allow_html=True)

    # Create three KPI cards to summarize the trained model.
    col_diag1, col_diag2, col_diag3 = st.columns(3)

    # Display the machine learning algorithm used for prediction.
    with col_diag1:
        st.markdown(f"""
            <div style="background: #FDFBF7; padding: 20px; border-radius: 6px; border-left: 4px solid #3D2314; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #7F7F7F; letter-spacing: 0.5px;">Core Estimator Class</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #2B160A; margin-top: 5px;">RandomForestClassifier</div>
            </div>
        """, unsafe_allow_html=True)

    # Display the optimized probability threshold used for classification.
    with col_diag2:
        st.markdown(f"""
            <div style="background: #FDFBF7; padding: 20px; border-radius: 6px; border-left: 4px solid #C6A052; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #7F7F7F; letter-spacing: 0.5px;">Optimized Classification Cutoff</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #2B160A; margin-top: 5px;">{engine.optimal_threshold:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    # Display the evaluation metric used during model optimization.
    with col_diag3:
        st.markdown(f"""
            <div style="background: #FDFBF7; padding: 20px; border-radius: 6px; border-left: 4px solid #8B5A2B; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #7F7F7F; letter-spacing: 0.5px;">CV Optimization Scoring Metric</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #2B160A; margin-top: 5px;">Stratified F1-Macro</div>
            </div>
        """, unsafe_allow_html=True)

    # Add spacing before the diagnostics section.
    st.markdown("<br>", unsafe_allow_html=True)

    # Create a two-column layout:
    # Left  - Hyperparameter summary.
    # Right - Feature importance visualization.
    col_work_left, col_work_right = st.columns([2, 3])

    # ========================================================
    # Hyperparameter Summary
    # ========================================================
    with col_work_left:

        # Display the hyperparameter section heading.
        st.markdown("<h4 style='font-family: \"Inter\", sans-serif; font-weight: 700; font-size: 1.15rem; color: #D48C2A; letter-spacing: 0.3px; margin-bottom: 12px;'>📉 Hyperparameter Best Estimators</h4>", unsafe_allow_html=True)

        # Explain how the optimal parameters were obtained.
        st.markdown("<p style='font-size: 0.85rem; color: #666; margin-top: -5px;'>Active tuning parameters configured dynamically via stratified 3-Fold GridSearch validations:</p>", unsafe_allow_html=True)

        # Retrieve the optimized number of trees.
        # If unavailable, use the default value.
        best_est = engine.best_params.get('n_estimators', 100) if engine.best_params else 100

        # Retrieve the optimized maximum tree depth.
        # If unavailable, use the default value.
        max_dp = engine.best_params.get('max_depth', 8) if engine.best_params else 8

        # Display the optimized hyperparameters.
        st.markdown(f"""
            <div style="background: #FFFBFB; border: 1px solid #F5EAEB; padding: 20px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 12px; border-bottom: 1px solid #F9EDED;">
                    <span style="font-weight: 600; color: #2B160A; font-size: 0.9rem; font-family: monospace;">n_estimators</span>
                    <span style="background: #3D2314; color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.85rem; font-weight: 700; font-family: monospace;">{best_est}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 12px;">
                    <span style="font-weight: 600; color: #2B160A; font-size: 0.9rem; font-family: monospace;">max_depth</span>
                    <span style="background: #C6A052; color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.85rem; font-weight: 700; font-family: monospace;">{max_dp}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Display additional pipeline configuration details.
        st.markdown("""
            <div style="background: #F8F9FA; border: 1px solid #ECEEEF; padding: 15px; border-radius: 6px; margin-top: 15px;">
                <small style="color: #666; line-height: 1.4; display: block;">
                    💡 <strong>Pipeline Health Check:</strong> Class balancing vectors are set to <code>balanced</code> to neutralize minority class distortions within highly irregular baseline customer cohorts.
                </small>
            </div>
        """, unsafe_allow_html=True)

    # ========================================================
    # Feature Importance Analysis
    # ========================================================
    with col_work_right:

        # Display the feature importance section heading.
        st.markdown("<h4 style='font-family: \"Inter\", sans-serif; font-weight: 700; font-size: 1.15rem; color: #E03C31; letter-spacing: 0.3px; margin-bottom: 12px;'>📊 Mathematical Feature Weight Distributions</h4>", unsafe_allow_html=True)

        # Continue only if feature importance values are available.
        if engine.feature_importances:

            # Convert the feature importance dictionary into a DataFrame.
            imp_df = pd.DataFrame(list(engine.feature_importances.items()), columns=['Gini_Feature', 'Mathematical_Weight'])

            # Sort features from lowest to highest importance.
            imp_df = imp_df.sort_values(by='Mathematical_Weight', ascending=True)

            # Create a horizontal bar chart showing the relative
            # importance of each feature used by the model.
            fig_imp = px.bar(
                imp_df,
                x='Mathematical_Weight',
                y='Gini_Feature',
                orientation='h',
                color='Mathematical_Weight',
                color_continuous_scale='YlOrBr',
                labels={
                    'Mathematical_Weight': 'Relative Predictive Weight (Gini)',
                    'Gini_Feature': 'Feature Vector'
                }
            )

            # Improve the appearance of the feature importance chart.
            fig_imp.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False,
                height=230,
                xaxis_title="Predictive Influence",
                yaxis_title=""
            )

            # Display the feature importance visualization.
            st.plotly_chart(fig_imp, use_container_width=True)

        else:

            # Display a fallback message when feature importance
            # values are unavailable.
            st.info("Mathematical backend weights utilizing fallback defaults.")