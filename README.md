# Menu Profitability & Waste Analysis

**A production-ready data analytics solution for restaurant operators**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com)

---

## The Problem

Restaurant operators struggle with menu profitability visibility. Most POS systems track sales, but fail to connect those sales to food costs, waste patterns, and contribution margins. This leads to:

- **Hidden margin killers**: Popular items that lose money on every sale
- **Invisible waste**: $30K-50K+ in annual losses that go untracked
- **Missed optimization opportunities**: High-margin items that aren't being promoted effectively

Without clear data, menu decisions are made on intuition rather than evidence.

---

## The Approach

This project applies **Menu Engineering methodology** combined with comprehensive operational analytics:

### 1. Menu Engineering Matrix
Classifies every menu item into four strategic categories:
- **Stars**: High revenue, high margin → Promote aggressively
- **Plowhorses**: High revenue, low margin → Reprice or optimize costs
- **Puzzles**: Low revenue, high margin → Better marketing needed
- **Dogs**: Low revenue, low margin → Remove or reformulate

### 2. Food Cost Analysis
Tracks actual vs. target food cost percentages at the item level, identifying which items are silently destroying margins.

### 3. Waste Tracking
Quantifies losses by item, type (returns, errors, spoilage), and channel to prioritize waste reduction efforts.

### 4. Time Pattern Analysis
Reveals hourly, daily, and seasonal demand patterns to optimize staffing and inventory.

### 5. Price Simulation
Models the financial impact of menu price changes, accounting for demand elasticity.

---

## Key Findings

Analysis of 18 months of POS data (547,918 transactions, $6.2M revenue) revealed:

- **Overall food cost is 33.2%** — slightly above the 32% target, representing $75K+ in margin improvement opportunity
- **Beverage category has 82% contribution margin** but only 15% of sales — massive upselling opportunity worth $60K+ annually
- **Waste costs $45K over 18 months** — seafood items waste at 2.5% rate vs. 1.5% average
- **Weekend revenue is 45% higher** than weekdays — indicates opportunity for weekday promotions or reduced weekday hours
- **Top 3 revenue items (Ribeye, Salmon, BBQ Burger)** maintain healthy margins and should receive premium menu placement

**Projected annual impact** of implementing recommendations: **$209K-271K additional profit**

---

## Live Dashboard

Access the interactive dashboard here: **https://restaurantsales.streamlit.app/**

### Dashboard Features

**5 Interactive Tabs:**

1. **Overview** — Revenue trends, channel breakdown, category performance, key KPIs
2. **Menu Engineering** — Full matrix visualization, item classification, margin analysis
3. **Waste & Loss** — Cost breakdown by item/type/channel, trends over time
4. **Time Patterns** — Hourly heatmaps, day-of-week analysis, seasonal trends, holiday impact
5. **Price Simulator** — Model price changes with demand elasticity, see projected P&L impact

**Dynamic Filtering:**
- Date range selection
- Category filters
- Channel filters (Dine-In, Takeout, Delivery)
- Adjustable target food cost percentage

---

## Tools & Technologies

**Data Generation & Analysis:**
- Python 3.8+
- pandas — Data manipulation and aggregation
- NumPy — Statistical calculations and simulations

**Visualization:**
- Plotly — All charts and graphs (interactive)
- Streamlit — Dashboard framework

**Methodology:**
- Menu Engineering Matrix (Smith & Kasavana)
- Rolling averages for trend smoothing
- Contribution margin analysis
- ABC waste analysis

---

## Repository Structure

```
restaurant_analysis/
├── .streamlit/
│   └── config.toml          # Dashboard theme configuration
├── data/
│   └── restaurant_pos_data.csv  # 18 months of synthetic POS data
├── generate_data.py         # Data generator (150K+ realistic transactions)
├── analysis.ipynb           # Jupyter notebook with full analysis
├── app.py                   # Streamlit dashboard application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/headply/restaurant_analysis.git
cd restaurant_analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit dashboard
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### 4. Explore the Jupyter notebook
```bash
jupyter notebook analysis.ipynb
```

---

## For Your Restaurant

**This analysis framework can be applied to your actual POS data.**

### Compatible POS Systems
Most modern POS systems export transaction data that can be adapted to this framework:

- **Toast POS** — Export sales reports with item-level detail
- **Square** — Use Transaction API or CSV exports
- **Clover** — Export orders with line items
- **Lightspeed** — Sales detail reports
- **Revel** — Transaction exports
- **Any system** that provides: order date/time, item name, price, quantity, category

### Required Data Fields
To run this analysis on your data, you need:

**Minimum:**
- Order date/time
- Item name
- Item price
- Quantity sold
- Category

**Recommended (for full analysis):**
- Food cost per item
- Order channel (dine-in/takeout/delivery)
- Server/employee ID
- Waste/void tracking

### Customization
The analysis can be customized for your:
- Target food cost percentages
- Menu categories
- Seasonal patterns
- Business hours
- Pricing structure

**Contact me to discuss adapting this framework for your restaurant's data.**

---

## Screenshots

### Dashboard Overview
*Live metrics, revenue trends, and channel breakdown*

![Dashboard Overview Placeholder]

### Menu Engineering Matrix
*Strategic classification of all menu items*

![Menu Engineering Placeholder]

### Waste Analysis
*Quantified losses by item, type, and trend*

![Waste Analysis Placeholder]

---

## About This Project

This is a **portfolio demonstration** of data analytics capabilities for the restaurant industry. The data is synthetic but models realistic patterns observed in actual restaurant operations.

**Skills demonstrated:**
- Data engineering (generating realistic synthetic datasets)
- Statistical analysis (menu engineering, margin analysis)
- Data visualization (interactive dashboards with Plotly)
- Business intelligence (actionable recommendations with quantified impact)
- Python development (clean, production-ready code)

Built by a freelance data analyst specializing in restaurant analytics.

---

## License

MIT License — Free to use for learning and portfolio purposes.

---

## Contact

Have a restaurant analytics project? Let's talk.

**GitHub**: [@headply](https://github.com/headply)
