"""
Restaurant Menu Profitability & Waste Analysis Dashboard
Production-quality Streamlit application for restaurant analytics.
Modern warm-themed UI with interactive Plotly charts.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Restaurant Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS for clean separation of concerns
import os
_css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(_css_path):
    with open(_css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Lucide SVG icons
ICONS = {
    'dollar': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>',
    'percent': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="5" x2="5" y2="19"></line><circle cx="6.5" cy="6.5" r="2.5"></circle><circle cx="17.5" cy="17.5" r="2.5"></circle></svg>',
    'trash': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>',
    'receipt': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2Z"></path><path d="M8 6v10"></path><path d="M12 6v10"></path><path d="M16 6v10"></path></svg>',
    'calendar': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>',
    'filter': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>',
    'tag': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>',
    'target': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>',
    'trending-up': '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>',
}


@st.cache_data
def load_data():
    """Load and prepare the restaurant POS data."""
    df = pd.read_csv('data/restaurant_pos_data.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['order_datetime'] = pd.to_datetime(df['order_datetime'])
    return df


def create_plotly_theme():
    """Create consistent Plotly theme with warm restaurant palette."""
    return {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'family': 'DM Sans', 'color': '#a89585', 'size': 12},
            'title': {'font': {'color': '#f0e6dd', 'size': 16, 'family': 'DM Sans'}},
            'xaxis': {
                'gridcolor': '#3d302a',
                'showgrid': True,
                'zeroline': False,
                'color': '#a89585',
            },
            'yaxis': {
                'gridcolor': '#3d302a',
                'showgrid': True,
                'zeroline': False,
                'color': '#a89585',
            },
            'hovermode': 'x unified',
            'hoverlabel': {
                'bgcolor': '#2a211c',
                'bordercolor': '#3d302a',
                'font': {'family': 'DM Sans', 'color': '#f0e6dd'}
            },
        }
    }


def metric_card(label, value, icon_key, delta=None):
    """Create a styled metric card."""
    icon = ICONS.get(icon_key, '')
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ''
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """


def filter_data(df, date_range, categories, channels):
    """Apply filters to the dataset."""
    filtered = df[
        (df['order_date'] >= pd.to_datetime(date_range[0])) &
        (df['order_date'] <= pd.to_datetime(date_range[1]))
    ]
    
    if categories:
        filtered = filtered[filtered['category'].isin(categories)]
    
    if channels:
        filtered = filtered[filtered['order_channel'].isin(channels)]
    
    return filtered


def calculate_menu_engineering(df):
    """Calculate menu engineering classification (Star/Plowhorse/Puzzle/Dog)."""
    # Group by item
    item_stats = df.groupby('item_name').agg({
        'total_revenue': 'sum',
        'contribution_margin': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    item_stats.columns = ['item_name', 'revenue', 'margin', 'quantity_sold']
    item_stats['margin_per_unit'] = item_stats['margin'] / item_stats['quantity_sold']
    
    # Calculate medians
    median_revenue = item_stats['revenue'].median()
    median_margin = item_stats['margin_per_unit'].median()
    
    # Classify items
    def classify(row):
        if row['revenue'] >= median_revenue and row['margin_per_unit'] >= median_margin:
            return 'Star'
        elif row['revenue'] >= median_revenue and row['margin_per_unit'] < median_margin:
            return 'Plowhorse'
        elif row['revenue'] < median_revenue and row['margin_per_unit'] >= median_margin:
            return 'Puzzle'
        else:
            return 'Dog'
    
    item_stats['classification'] = item_stats.apply(classify, axis=1)
    
    return item_stats, median_revenue, median_margin


# Load data
df = load_data()

# Sidebar filters
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-label">
            {ICONS['calendar']} Date Range
        </div>
    """, unsafe_allow_html=True)
    
    date_range = st.slider(
        "Select date range",
        min_value=df['order_date'].min().date(),
        max_value=df['order_date'].max().date(),
        value=(df['order_date'].min().date(), df['order_date'].max().date()),
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="sidebar-label">
            {ICONS['tag']} Categories
        </div>
    """, unsafe_allow_html=True)
    
    categories = st.multiselect(
        "Filter by category",
        options=sorted(df['category'].unique()),
        default=sorted(df['category'].unique()),
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="sidebar-label">
            {ICONS['filter']} Order Channel
        </div>
    """, unsafe_allow_html=True)
    
    channels = st.multiselect(
        "Filter by channel",
        options=sorted(df['order_channel'].unique()),
        default=sorted(df['order_channel'].unique()),
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="sidebar-label">
            {ICONS['target']} Target Food Cost %
        </div>
    """, unsafe_allow_html=True)
    
    target_food_cost = st.slider(
        "Target food cost percentage",
        min_value=20.0,
        max_value=40.0,
        value=32.0,
        step=0.5,
        format="%.1f%%",
        label_visibility="collapsed"
    )

# Filter data
filtered_df = filter_data(df, date_range, categories, channels)

# Main content — Dashboard header
st.markdown("""
<div class="dashboard-header">
    <div>
        <div class="header-title">🍽️ Restaurant Analytics</div>
        <div class="header-subtitle">Menu profitability, waste tracking &amp; data-driven optimization</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Menu Engineering",
    "Waste & Loss",
    "Time Patterns",
    "Price Simulator"
])

# Tab 1: Overview
with tab1:
    # Calculate key metrics
    total_revenue = filtered_df['total_revenue'].sum()
    total_food_cost = filtered_df['total_food_cost'].sum()
    food_cost_pct = (total_food_cost / total_revenue * 100) if total_revenue > 0 else 0
    gross_margin = total_revenue - total_food_cost
    waste_cost = filtered_df[filtered_df['is_waste'] == True]['total_food_cost'].sum()
    avg_ticket = filtered_df.groupby('order_id')['total_revenue'].sum().mean()
    
    # Additional KPIs
    total_orders = filtered_df['order_id'].nunique()
    if len(filtered_df) > 0:
        num_days = (filtered_df['order_date'].max() - filtered_df['order_date'].min()).days + 1
    else:
        num_days = 1
    daily_revenue_avg = total_revenue / num_days if num_days > 0 else 0

    # Status badge
    if food_cost_pct <= target_food_cost:
        status_class = "status-healthy"
        status_text = "Healthy"
    elif food_cost_pct <= target_food_cost + 3:
        status_class = "status-warning"
        status_text = "Watch"
    else:
        status_class = "status-danger"
        status_text = "Critical"
    
    st.markdown(f'<span class="status-badge {status_class}">Food Cost: {status_text}</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI Cards — two rows for better spacing
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            metric_card("Total Revenue", f"${total_revenue:,.0f}", "dollar"),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            metric_card("Gross Margin", f"${gross_margin:,.0f}", "trending-up", f"{(gross_margin/total_revenue*100):.1f}%"),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            metric_card("Food Cost %", f"{food_cost_pct:.1f}%", "percent", f"Target: {target_food_cost:.1f}%"),
            unsafe_allow_html=True
        )
    
    # Second row of KPIs
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(
            metric_card("Total Orders", f"{total_orders:,}", "receipt", f"{num_days} days"),
            unsafe_allow_html=True
        )
    
    with col5:
        st.markdown(
            metric_card("Waste Cost", f"${waste_cost:,.0f}", "trash", f"{(waste_cost/total_food_cost*100):.1f}% of food cost"),
            unsafe_allow_html=True
        )
    
    with col6:
        st.markdown(
            metric_card("Avg Daily Revenue", f"${daily_revenue_avg:,.0f}", "dollar", f"Avg Ticket: ${avg_ticket:.2f}"),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Daily revenue trend
    daily_revenue = filtered_df.groupby('order_date').agg({
        'total_revenue': 'sum',
        'contribution_margin': 'sum'
    }).reset_index()
    
    daily_revenue['revenue_7d'] = daily_revenue['total_revenue'].rolling(7, min_periods=1).mean()
    daily_revenue['margin_7d'] = daily_revenue['contribution_margin'].rolling(7, min_periods=1).mean()
    
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(
        x=daily_revenue['order_date'],
        y=daily_revenue['total_revenue'],
        name='Daily Revenue',
        line=dict(color='#e0b48c', width=1),
        opacity=0.3
    ))
    fig_daily.add_trace(go.Scatter(
        x=daily_revenue['order_date'],
        y=daily_revenue['revenue_7d'],
        name='7-Day Average',
        line=dict(color='#c8956c', width=2)
    ))
    
    fig_daily.update_layout(create_plotly_theme()['layout'])
    fig_daily.update_layout(
        title='Daily Revenue Trend',
        height=350,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Revenue breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by channel
        channel_revenue = filtered_df.groupby('order_channel')['total_revenue'].sum().sort_values()
        
        fig_channel = go.Figure(go.Bar(
            x=channel_revenue.values,
            y=channel_revenue.index,
            orientation='h',
            marker_color='#c8956c'
        ))
        
        fig_channel.update_layout(create_plotly_theme()['layout'])
        fig_channel.update_layout(
            title='Revenue by Channel',
            height=300,
            xaxis_title='Revenue ($)',
            yaxis_title=''
        )
        
        st.plotly_chart(fig_channel, use_container_width=True)
    
    with col2:
        # Revenue by category
        category_revenue = filtered_df.groupby('category')['total_revenue'].sum()
        
        fig_category = go.Figure(go.Pie(
            labels=category_revenue.index,
            values=category_revenue.values,
            hole=0.4,
            marker=dict(colors=['#c8956c', '#e0b48c', '#a0785a', '#d4a87c', '#8c6548', '#f0d4b8'])
        ))
        
        fig_category.update_layout(create_plotly_theme()['layout'])
        fig_category.update_layout(
            title='Revenue by Category',
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Peak hours and recent orders preview
    col_peak, col_orders = st.columns(2)
    
    with col_peak:
        # Peak hours area chart
        hourly_orders = filtered_df.groupby('hour')['order_id'].nunique().reset_index()
        hourly_orders.columns = ['hour', 'orders']
        
        fig_peak = go.Figure(go.Scatter(
            x=hourly_orders['hour'],
            y=hourly_orders['orders'],
            fill='tozeroy',
            line=dict(color='#c8956c', width=2),
            fillcolor='rgba(200, 149, 108, 0.15)',
            hovertemplate='Hour %{x}:00<br>Orders: %{y}<extra></extra>'
        ))
        fig_peak.update_layout(create_plotly_theme()['layout'])
        fig_peak.update_layout(
            title='Peak Hours',
            xaxis_title='Hour of Day',
            yaxis_title='Orders',
            height=340
        )
        st.plotly_chart(fig_peak, use_container_width=True)
    
    with col_orders:
        # Recent orders preview
        st.markdown('<div class="section-title">📋 Recent Orders</div>', unsafe_allow_html=True)
        recent = (
            filtered_df.sort_values('order_datetime', ascending=False)
            .drop_duplicates(subset='order_id')
            .head(8)
        )
        rows_html = ""
        for _, row in recent.iterrows():
            rows_html += f"""
            <div class="order-row">
                <span class="order-id">{row['order_id']}</span>
                <span class="order-item">{row['item_name']}</span>
                <span class="order-channel-badge">{row['order_channel']}</span>
                <span class="order-amount">${row['total_revenue']:.2f}</span>
            </div>"""
        st.markdown(
            f'<div class="section-panel" style="padding: 12px 0;">{rows_html}</div>',
            unsafe_allow_html=True
        )

# Tab 2: Menu Engineering
with tab2:
    st.subheader("Menu Engineering Matrix")
    
    # Calculate menu engineering
    item_stats, median_revenue, median_margin = calculate_menu_engineering(filtered_df)
    
    # Add category info
    category_map = filtered_df.groupby('item_name')['category'].first().to_dict()
    item_stats['category'] = item_stats['item_name'].map(category_map)
    
    # Color mapping — warm palette for menu engineering quadrants
    color_map = {
        'Star': '#6bcb77',
        'Plowhorse': '#f0c040',
        'Puzzle': '#c8956c',
        'Dog': '#e05252'
    }
    
    # Scatter plot
    fig_matrix = go.Figure()
    
    for classification in ['Star', 'Plowhorse', 'Puzzle', 'Dog']:
        subset = item_stats[item_stats['classification'] == classification]
        fig_matrix.add_trace(go.Scatter(
            x=subset['revenue'],
            y=subset['margin_per_unit'],
            mode='markers',
            name=classification,
            marker=dict(
                size=subset['revenue'] / subset['revenue'].max() * 50 + 10,
                color=color_map[classification],
                line=dict(color='#3d302a', width=1)
            ),
            text=subset['item_name'],
            hovertemplate='<b>%{text}</b><br>Revenue: $%{x:,.0f}<br>Margin/Unit: $%{y:.2f}<extra></extra>'
        ))
    
    # Add median lines
    fig_matrix.add_hline(y=median_margin, line_dash="dash", line_color="#7a6b5e", opacity=0.5)
    fig_matrix.add_vline(x=median_revenue, line_dash="dash", line_color="#7a6b5e", opacity=0.5)
    
    # Add quadrant labels
    fig_matrix.add_annotation(x=median_revenue * 1.5, y=item_stats['margin_per_unit'].max() * 0.95,
                             text="STARS", showarrow=False, font=dict(size=14, color="#6bcb77"))
    fig_matrix.add_annotation(x=median_revenue * 1.5, y=item_stats['margin_per_unit'].min() * 1.5,
                             text="PLOWHORSES", showarrow=False, font=dict(size=14, color="#f0c040"))
    fig_matrix.add_annotation(x=median_revenue * 0.5, y=item_stats['margin_per_unit'].max() * 0.95,
                             text="PUZZLES", showarrow=False, font=dict(size=14, color="#c8956c"))
    fig_matrix.add_annotation(x=median_revenue * 0.5, y=item_stats['margin_per_unit'].min() * 1.5,
                             text="DOGS", showarrow=False, font=dict(size=14, color="#e05252"))
    
    fig_matrix.update_layout(create_plotly_theme()['layout'])
    fig_matrix.update_layout(
        title='Menu Engineering Matrix',
        xaxis_title='Total Revenue ($)',
        yaxis_title='Contribution Margin per Unit ($)',
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Item breakdown table — expandable section
    with st.expander("📊 Item Performance Details", expanded=False):
        # Prepare table data
        table_data = item_stats.copy()
        table_data['food_cost_pct'] = filtered_df.groupby('item_name')['food_cost_pct'].mean().values
        table_data = table_data.sort_values('revenue', ascending=False)
        
        # Format for display
        display_df = table_data[[
            'item_name', 'category', 'classification', 'revenue', 
            'margin', 'margin_per_unit', 'quantity_sold', 'food_cost_pct'
        ]].copy()
        
        display_df.columns = [
            'Item', 'Category', 'Classification', 'Revenue', 
            'Total Margin', 'Margin/Unit', 'Qty Sold', 'Food Cost %'
        ]
        
        display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f'${x:,.0f}')
        display_df['Total Margin'] = display_df['Total Margin'].apply(lambda x: f'${x:,.0f}')
        display_df['Margin/Unit'] = display_df['Margin/Unit'].apply(lambda x: f'${x:.2f}')
        display_df['Food Cost %'] = display_df['Food Cost %'].apply(lambda x: f'{x:.1f}%')
        
        st.dataframe(display_df, use_container_width=True, height=400)
    
    # Category comparison
    col1, col2 = st.columns(2)
    
    with col1:
        category_stats = filtered_df.groupby('category').agg({
            'total_revenue': 'sum',
            'contribution_margin': 'sum'
        }).reset_index()
        
        category_stats['margin_pct'] = (category_stats['contribution_margin'] / category_stats['total_revenue'] * 100)
        category_stats = category_stats.sort_values('margin_pct')
        
        fig_cat_margin = go.Figure()
        fig_cat_margin.add_trace(go.Bar(
            x=category_stats['margin_pct'],
            y=category_stats['category'],
            orientation='h',
            marker_color='#c8956c'
        ))
        
        fig_cat_margin.update_layout(create_plotly_theme()['layout'])
        fig_cat_margin.update_layout(
            title='Margin % by Category',
            xaxis_title='Margin %',
            yaxis_title='',
            height=350
        )
        
        st.plotly_chart(fig_cat_margin, use_container_width=True)
    
    with col2:
        # Food cost % by item
        item_food_cost = filtered_df.groupby('item_name').agg({
            'food_cost_pct': 'mean',
            'total_revenue': 'sum'
        }).sort_values('food_cost_pct', ascending=False).head(15)
        
        colors = ['#e05252' if x > target_food_cost else '#6bcb77' for x in item_food_cost['food_cost_pct']]
        
        fig_food_cost = go.Figure(go.Bar(
            x=item_food_cost['food_cost_pct'],
            y=item_food_cost.index,
            orientation='h',
            marker_color=colors
        ))
        
        fig_food_cost.add_vline(x=target_food_cost, line_dash="dash", line_color="#f0c040", opacity=0.7)
        
        fig_food_cost.update_layout(create_plotly_theme()['layout'])
        fig_food_cost.update_layout(
            title=f'Food Cost % by Item (Top 15)',
            xaxis_title='Food Cost %',
            yaxis_title='',
            height=350
        )
        
        st.plotly_chart(fig_food_cost, use_container_width=True)

# Tab 3: Waste & Loss
with tab3:
    waste_df = filtered_df[filtered_df['is_waste'] == True]
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_waste_cost = waste_df['total_food_cost'].sum()
    waste_rate = (len(waste_df) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    top_waste_item = waste_df.groupby('item_name')['total_food_cost'].sum().idxmax() if len(waste_df) > 0 else "N/A"
    annual_waste_estimate = total_waste_cost * (365 / ((date_range[1] - date_range[0]).days + 1))
    
    with col1:
        st.markdown(
            metric_card("Total Waste Cost", f"${total_waste_cost:,.0f}", "trash"),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            metric_card("Waste Rate", f"{waste_rate:.2f}%", "percent", "of all transactions"),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            metric_card("Highest Waste Item", top_waste_item[:20], "tag"),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            metric_card("Est. Annual Waste", f"${annual_waste_estimate:,.0f}", "trending-up"),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Waste analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Waste by item
        waste_by_item = waste_df.groupby('item_name')['total_food_cost'].sum().sort_values(ascending=True).tail(15)
        
        fig_waste_item = go.Figure(go.Bar(
            x=waste_by_item.values,
            y=waste_by_item.index,
            orientation='h',
            marker_color='#e05252'
        ))
        
        fig_waste_item.update_layout(create_plotly_theme()['layout'])
        fig_waste_item.update_layout(
            title='Waste Cost by Item (Top 15)',
            xaxis_title='Waste Cost ($)',
            yaxis_title='',
            height=400
        )
        
        st.plotly_chart(fig_waste_item, use_container_width=True)
    
    with col2:
        # Waste by type
        waste_by_type = waste_df.groupby('waste_type')['total_food_cost'].sum()
        
        fig_waste_type = go.Figure(go.Pie(
            labels=waste_by_type.index,
            values=waste_by_type.values,
            hole=0.4,
            marker=dict(colors=['#e05252', '#d47070', '#c49090'])
        ))
        
        fig_waste_type.update_layout(create_plotly_theme()['layout'])
        fig_waste_type.update_layout(
            title='Waste Cost by Type',
            height=400
        )
        
        st.plotly_chart(fig_waste_type, use_container_width=True)
    
    # Waste trend over time
    waste_df['month'] = pd.to_datetime(waste_df['order_date']).dt.to_period('M').astype(str)
    monthly_waste = waste_df.groupby('month')['total_food_cost'].sum().reset_index()
    
    fig_waste_trend = go.Figure(go.Bar(
        x=monthly_waste['month'],
        y=monthly_waste['total_food_cost'],
        marker_color='#e05252'
    ))
    
    fig_waste_trend.update_layout(create_plotly_theme()['layout'])
    fig_waste_trend.update_layout(
        title='Monthly Waste Cost Trend',
        xaxis_title='Month',
        yaxis_title='Waste Cost ($)',
        height=350
    )
    
    st.plotly_chart(fig_waste_trend, use_container_width=True)
    
    # Waste by channel
    waste_by_channel = waste_df.groupby('order_channel')['total_food_cost'].sum().sort_values()
    
    fig_waste_channel = go.Figure(go.Bar(
        x=waste_by_channel.values,
        y=waste_by_channel.index,
        orientation='h',
        marker_color='#e05252'
    ))
    
    fig_waste_channel.update_layout(create_plotly_theme()['layout'])
    fig_waste_channel.update_layout(
        title='Waste Cost by Channel',
        xaxis_title='Waste Cost ($)',
        yaxis_title='',
        height=300
    )
    
    st.plotly_chart(fig_waste_channel, use_container_width=True)

# Tab 4: Time Patterns
with tab4:
    # Hourly demand heatmap
    hourly_dow = filtered_df.groupby(['hour', 'day_of_week']).size().reset_index(name='orders')
    
    # Pivot for heatmap
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = hourly_dow.pivot(index='hour', columns='day_of_week', values='orders')
    heatmap_data = heatmap_data.reindex(columns=days_order)
    
    fig_heatmap = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlOrRd',
        hovertemplate='Day: %{x}<br>Hour: %{y}<br>Orders: %{z}<extra></extra>'
    ))

    fig_heatmap.update_layout(create_plotly_theme()['layout'])
    fig_heatmap.update_layout(
        title='Hourly Demand Heatmap',
        xaxis_title='Day of Week',
        yaxis_title='Hour of Day',
        height=500
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Day of week analysis
    col1, col2 = st.columns(2)
    
    with col1:
        dow_revenue = filtered_df.groupby('day_of_week')['total_revenue'].sum().reindex(days_order)
        
        fig_dow = go.Figure(go.Bar(
            x=dow_revenue.index,
            y=dow_revenue.values,
            marker_color='#c8956c'
        ))
        
        fig_dow.update_layout(create_plotly_theme()['layout'])
        fig_dow.update_layout(
            title='Revenue by Day of Week',
            xaxis_title='',
            yaxis_title='Revenue ($)',
            height=350
        )
        
        st.plotly_chart(fig_dow, use_container_width=True)
    
    with col2:
        # Monthly revenue trend
        monthly_revenue = filtered_df.copy()
        monthly_revenue['month_year'] = pd.to_datetime(monthly_revenue['order_date']).dt.to_period('M').astype(str)
        monthly_revenue = monthly_revenue.groupby('month_year')['total_revenue'].sum().reset_index()
        
        fig_monthly = go.Figure(go.Scatter(
            x=monthly_revenue['month_year'],
            y=monthly_revenue['total_revenue'],
            mode='lines+markers',
            line=dict(color='#c8956c', width=2),
            marker=dict(size=8)
        ))
        
        fig_monthly.update_layout(create_plotly_theme()['layout'])
        fig_monthly.update_layout(
            title='Monthly Revenue Trend',
            xaxis_title='',
            yaxis_title='Revenue ($)',
            height=350
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Hourly revenue
    hourly_revenue = filtered_df.groupby('hour')['total_revenue'].sum().reset_index()
    
    fig_hourly = go.Figure(go.Scatter(
        x=hourly_revenue['hour'],
        y=hourly_revenue['total_revenue'],
        fill='tozeroy',
        line=dict(color='#c8956c'),
        fillcolor='rgba(200, 149, 108, 0.2)'
    ))
    
    fig_hourly.update_layout(create_plotly_theme()['layout'])
    fig_hourly.update_layout(
        title='Revenue by Hour of Day',
        xaxis_title='Hour',
        yaxis_title='Revenue ($)',
        height=350
    )
    
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Holiday impact
    holiday_revenue = filtered_df.groupby('is_holiday')['total_revenue'].sum()
    holiday_avg = filtered_df.groupby(['is_holiday', 'order_date'])['total_revenue'].sum().groupby('is_holiday').mean()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            metric_card(
                "Avg Daily Revenue (Regular)", 
                f"${holiday_avg[False]:,.0f}" if False in holiday_avg else "$0",
                "calendar"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            metric_card(
                "Avg Daily Revenue (Holiday)", 
                f"${holiday_avg[True]:,.0f}" if True in holiday_avg else "$0",
                "calendar",
                f"+{((holiday_avg[True] / holiday_avg[False] - 1) * 100):.1f}%" if (True in holiday_avg and False in holiday_avg) else ""
            ),
            unsafe_allow_html=True
        )

# Tab 5: Price Simulator
with tab5:
    st.subheader("Menu Item Price Simulator")
    
    # Get menu engineering data
    item_stats, median_revenue, median_margin = calculate_menu_engineering(filtered_df)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### Simulation Parameters")
        
        # Item selection
        selected_item = st.selectbox("Select menu item", sorted(filtered_df['item_name'].unique()))
        
        # Get current item data
        item_data = filtered_df[filtered_df['item_name'] == selected_item]
        current_price = item_data['actual_price'].mean()
        current_food_cost = item_data['food_cost_per_unit'].mean()
        current_quantity = len(item_data)
        current_revenue = item_data['total_revenue'].sum()
        current_margin = item_data['contribution_margin'].sum()
        current_margin_per_unit = current_margin / current_quantity
        
        # Get current classification
        current_class = item_stats[item_stats['item_name'] == selected_item]['classification'].values[0]
        
        # Price change slider
        price_change = st.slider(
            "Price change",
            min_value=-20.0,
            max_value=30.0,
            value=0.0,
            step=1.0,
            format="%.0f%%"
        )
        
        # Demand elasticity slider
        elasticity = st.slider(
            "Estimated demand drop",
            min_value=0.0,
            max_value=30.0,
            value=10.0,
            step=1.0,
            format="%.0f%%",
            help="Estimated % reduction in volume due to price increase"
        )
        
        # Calculate projections
        new_price = current_price * (1 + price_change / 100)
        volume_change = -elasticity if price_change > 0 else abs(elasticity / 2)
        new_quantity = current_quantity * (1 + volume_change / 100)
        new_revenue = new_price * new_quantity
        new_margin = (new_price - current_food_cost) * new_quantity
        new_margin_per_unit = new_margin / new_quantity if new_quantity > 0 else 0
        
        # Projected classification
        if new_revenue >= median_revenue and new_margin_per_unit >= median_margin:
            new_class = 'Star'
        elif new_revenue >= median_revenue and new_margin_per_unit < median_margin:
            new_class = 'Plowhorse'
        elif new_revenue < median_revenue and new_margin_per_unit >= median_margin:
            new_class = 'Puzzle'
        else:
            new_class = 'Dog'
        
        net_impact = new_margin - current_margin
        
    with col2:
        st.markdown("##### Simulation Results")
        
        # Comparison table
        comparison_data = {
            'Metric': ['Price', 'Volume (units)', 'Revenue', 'Margin', 'Margin/Unit', 'Classification'],
            'Current': [
                f'${current_price:.2f}',
                f'{current_quantity:,}',
                f'${current_revenue:,.0f}',
                f'${current_margin:,.0f}',
                f'${current_margin_per_unit:.2f}',
                current_class
            ],
            'Projected': [
                f'${new_price:.2f}',
                f'{int(new_quantity):,}',
                f'${new_revenue:,.0f}',
                f'${new_margin:,.0f}',
                f'${new_margin_per_unit:.2f}',
                new_class
            ],
            'Change': [
                f'{price_change:+.1f}%',
                f'{volume_change:+.1f}%',
                f'{((new_revenue / current_revenue - 1) * 100):+.1f}%',
                f'{((new_margin / current_margin - 1) * 100):+.1f}%',
                f'{((new_margin_per_unit / current_margin_per_unit - 1) * 100):+.1f}%',
                '→ ' + new_class if new_class != current_class else '—'
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Net impact card
        impact_color = "#6bcb77" if net_impact > 0 else "#e05252"
        impact_icon = "▲" if net_impact > 0 else "▼"
        
        st.markdown(f"""
        <div class="impact-card" style="border: 2px solid {impact_color};">
            <div class="impact-label">Net Margin Impact</div>
            <div class="impact-value" style="color: {impact_color};">
                {impact_icon} ${abs(net_impact):,.0f}
            </div>
            <div class="impact-detail">
                {'+' if net_impact > 0 else ''}{((new_margin / current_margin - 1) * 100):.1f}% change in contribution margin
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visualization
        fig_comparison = go.Figure()
        
        fig_comparison.add_trace(go.Bar(
            name='Current',
            x=['Revenue', 'Margin'],
            y=[current_revenue, current_margin],
            marker_color='#7a6b5e'
        ))
        
        fig_comparison.add_trace(go.Bar(
            name='Projected',
            x=['Revenue', 'Margin'],
            y=[new_revenue, new_margin],
            marker_color='#c8956c'
        ))
        
        fig_comparison.update_layout(create_plotly_theme()['layout'])
        fig_comparison.update_layout(
            title='Current vs. Projected Performance',
            barmode='group',
            height=300,
            yaxis_title='Amount ($)'
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)

st.markdown("""
<div class="dashboard-footer">
    🍽️ Restaurant Analytics Dashboard &bull; Data-driven menu optimization
</div>
""", unsafe_allow_html=True)
