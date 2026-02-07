"""
Restaurant POS Data Generator
Generates 18 months of realistic transaction data for menu profitability analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Define menu items with realistic pricing and costs
MENU_ITEMS = {
    'Starters': [
        {'name': 'French Onion Soup', 'price': 8.99, 'food_cost': 2.50, 'prep_time': 15},
        {'name': 'Caesar Salad', 'price': 9.99, 'food_cost': 3.20, 'prep_time': 10},
        {'name': 'Buffalo Wings (8pc)', 'price': 12.99, 'food_cost': 5.50, 'prep_time': 18},
        {'name': 'Calamari', 'price': 13.99, 'food_cost': 4.80, 'prep_time': 12},
        {'name': 'Spinach Artichoke Dip', 'price': 10.99, 'food_cost': 3.50, 'prep_time': 8},
        {'name': 'Bruschetta', 'price': 8.99, 'food_cost': 2.80, 'prep_time': 10},
    ],
    'Mains': [
        {'name': 'Classic Burger', 'price': 14.99, 'food_cost': 5.20, 'prep_time': 15},
        {'name': 'BBQ Bacon Burger', 'price': 16.99, 'food_cost': 6.50, 'prep_time': 18},
        {'name': 'Grilled Chicken Sandwich', 'price': 13.99, 'food_cost': 4.80, 'prep_time': 14},
        {'name': 'Fish and Chips', 'price': 17.99, 'food_cost': 7.20, 'prep_time': 20},
        {'name': 'Ribeye Steak (12oz)', 'price': 32.99, 'food_cost': 14.50, 'prep_time': 25},
        {'name': 'Grilled Salmon', 'price': 24.99, 'food_cost': 11.00, 'prep_time': 20},
        {'name': 'Pasta Carbonara', 'price': 16.99, 'food_cost': 5.50, 'prep_time': 15},
        {'name': 'Vegetable Stir Fry', 'price': 14.99, 'food_cost': 4.20, 'prep_time': 12},
    ],
    'Sides': [
        {'name': 'French Fries', 'price': 4.99, 'food_cost': 1.20, 'prep_time': 8},
        {'name': 'Onion Rings', 'price': 5.99, 'food_cost': 1.80, 'prep_time': 10},
        {'name': 'Coleslaw', 'price': 3.99, 'food_cost': 1.00, 'prep_time': 5},
        {'name': 'Sweet Potato Fries', 'price': 5.99, 'food_cost': 2.20, 'prep_time': 10},
    ],
    'Desserts': [
        {'name': 'Chocolate Lava Cake', 'price': 8.99, 'food_cost': 2.80, 'prep_time': 5},
        {'name': 'New York Cheesecake', 'price': 7.99, 'food_cost': 2.40, 'prep_time': 3},
        {'name': 'Ice Cream Sundae', 'price': 6.99, 'food_cost': 1.80, 'prep_time': 5},
        {'name': 'Apple Pie', 'price': 6.99, 'food_cost': 2.00, 'prep_time': 4},
    ],
    'Beverages': [
        {'name': 'Soft Drink', 'price': 2.99, 'food_cost': 0.50, 'prep_time': 2},
        {'name': 'Iced Tea', 'price': 2.99, 'food_cost': 0.40, 'prep_time': 2},
        {'name': 'Coffee', 'price': 3.49, 'food_cost': 0.60, 'prep_time': 3},
        {'name': 'Craft Beer', 'price': 6.99, 'food_cost': 1.50, 'prep_time': 1},
        {'name': 'House Wine (Glass)', 'price': 8.99, 'food_cost': 2.00, 'prep_time': 1},
        {'name': 'Signature Cocktail', 'price': 11.99, 'food_cost': 3.00, 'prep_time': 5},
    ],
    'Kids Menu': [
        {'name': 'Kids Burger & Fries', 'price': 7.99, 'food_cost': 2.50, 'prep_time': 12},
        {'name': 'Kids Chicken Tenders', 'price': 6.99, 'food_cost': 2.20, 'prep_time': 10},
        {'name': 'Kids Mac & Cheese', 'price': 6.49, 'food_cost': 1.80, 'prep_time': 8},
    ],
}

# Server IDs
SERVERS = [f'S{str(i).zfill(3)}' for i in range(1, 11)]  # S001 to S010

# Channels
CHANNELS = ['Dine-In', 'Takeout', 'Delivery']
CHANNEL_WEIGHTS = [0.60, 0.25, 0.15]

# Payment methods
PAYMENT_METHODS = ['Cash', 'Credit Card', 'Debit Card', 'Mobile Pay']
PAYMENT_WEIGHTS = [0.15, 0.55, 0.20, 0.10]

# Waste types
WASTE_TYPES = ['Customer Return', 'Kitchen Error', 'Spoilage']

# Holiday dates (2023-2024)
HOLIDAYS = [
    '2023-02-14',  # Valentine's Day
    '2023-05-14',  # Mother's Day
    '2023-11-23',  # Thanksgiving
    '2023-12-24',  # Christmas Eve
    '2023-12-25',  # Christmas
    '2024-02-14',  # Valentine's Day
    '2024-05-12',  # Mother's Day
]


def get_day_multiplier(date):
    """Get order volume multiplier based on day of week."""
    day = date.weekday()  # Monday = 0, Sunday = 6
    if day in [4, 5]:  # Friday, Saturday
        return np.random.uniform(1.4, 1.6)
    elif day == 6:  # Sunday (brunch)
        return np.random.uniform(1.2, 1.4)
    else:  # Monday-Thursday
        return np.random.uniform(0.8, 1.0)


def get_hour_multiplier(hour):
    """Get order volume multiplier based on hour of day."""
    if 11 <= hour <= 13:  # Lunch peak
        return np.random.uniform(2.5, 3.5)
    elif 18 <= hour <= 20:  # Dinner peak
        return np.random.uniform(3.0, 4.0)
    elif 6 <= hour <= 10:  # Breakfast
        return np.random.uniform(0.5, 1.0)
    elif 14 <= hour <= 17:  # Afternoon
        return np.random.uniform(0.8, 1.2)
    elif 21 <= hour <= 22:  # Late evening
        return np.random.uniform(0.6, 1.0)
    else:  # Very early/late
        return np.random.uniform(0.1, 0.3)


def get_seasonal_multiplier(date):
    """Get order volume multiplier based on season."""
    month = date.month
    if month == 1:  # January slowdown
        return np.random.uniform(0.7, 0.85)
    elif month in [6, 7, 8]:  # Summer busy
        return np.random.uniform(1.15, 1.3)
    elif month in [11, 12]:  # Holiday season
        return np.random.uniform(1.1, 1.25)
    else:
        return np.random.uniform(0.95, 1.05)


def is_holiday(date):
    """Check if date is a holiday."""
    return date.strftime('%Y-%m-%d') in HOLIDAYS


def get_price_inflation(date, base_price):
    """Apply gradual price inflation over time."""
    start_date = datetime(2023, 1, 1)
    days_elapsed = (date - start_date).days
    # 5-8% inflation over 18 months (547 days)
    inflation_rate = np.random.uniform(0.05, 0.08)
    daily_rate = inflation_rate / 547
    return base_price * (1 + daily_rate * days_elapsed)


def generate_order_items(date, hour, channel, is_rainy, server_id, table_num):
    """Generate realistic order items with combos."""
    items = []
    
    # Most orders include a main + drink
    main_item = np.random.choice([item for item in MENU_ITEMS['Mains']])
    drink_item = np.random.choice([item for item in MENU_ITEMS['Beverages']])
    
    items.append(('Mains', main_item))
    items.append(('Beverages', drink_item))
    
    # 40% add a starter
    if np.random.random() < 0.40:
        starter = np.random.choice([item for item in MENU_ITEMS['Starters']])
        items.append(('Starters', starter))
    
    # 25% add dessert
    if np.random.random() < 0.25:
        dessert = np.random.choice([item for item in MENU_ITEMS['Desserts']])
        items.append(('Desserts', dessert))
    
    # 30% add a side
    if np.random.random() < 0.30:
        side = np.random.choice([item for item in MENU_ITEMS['Sides']])
        items.append(('Sides', side))
    
    # 15% chance of kids menu item
    if np.random.random() < 0.15:
        kids_item = np.random.choice([item for item in MENU_ITEMS['Kids Menu']])
        items.append(('Kids Menu', kids_item))
    
    return items


def generate_transactions():
    """Generate all transaction records."""
    print("Generating restaurant POS data...")
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 6, 30)
    
    records = []
    order_id = 1
    
    current_date = start_date
    while current_date <= end_date:
        # Determine if it's a rainy day (20% chance)
        is_rainy = np.random.random() < 0.20
        rainy_multiplier = 0.85 if is_rainy else 1.0
        
        # Get multipliers
        day_mult = get_day_multiplier(current_date)
        seasonal_mult = get_seasonal_multiplier(current_date)
        holiday_mult = 1.5 if is_holiday(current_date) else 1.0
        
        # Base orders per day
        base_orders = 280
        daily_orders = int(base_orders * day_mult * seasonal_mult * holiday_mult * rainy_multiplier)
        
        # Generate orders throughout the day
        for _ in range(daily_orders):
            # Select hour with realistic distribution
            hour_probs = [get_hour_multiplier(h) for h in range(24)]
            hour_probs = np.array(hour_probs) / sum(hour_probs)
            hour = np.random.choice(range(24), p=hour_probs)
            minute = np.random.randint(0, 60)
            
            order_datetime = current_date.replace(hour=hour, minute=minute)
            
            # Select channel
            channel = np.random.choice(CHANNELS, p=CHANNEL_WEIGHTS)
            
            # Server and table (only for dine-in)
            server_id = np.random.choice(SERVERS)
            table_num = np.random.randint(1, 21) if channel == 'Dine-In' else None
            
            # Payment method
            payment_method = np.random.choice(PAYMENT_METHODS, p=PAYMENT_WEIGHTS)
            
            # Generate items for this order
            order_items = generate_order_items(current_date, hour, channel, is_rainy, server_id, table_num)
            
            # Create transaction records for each item
            for category, item in order_items:
                # Get inflated price
                menu_price = get_price_inflation(current_date, item['price'])
                actual_price = menu_price  # Could add discounts/promos here
                
                # Food cost (slightly higher for delivery due to packaging)
                food_cost = item['food_cost']
                if channel == 'Delivery':
                    food_cost *= 1.10
                
                quantity = 1
                
                # Determine if this item is waste
                is_waste = False
                waste_type = None
                
                # Waste rates vary by category
                if category == 'Mains':
                    if np.random.random() < 0.015:  # 1.5% waste for mains
                        is_waste = True
                        waste_type = np.random.choice(['Customer Return', 'Kitchen Error'], p=[0.6, 0.4])
                elif category in ['Starters', 'Desserts']:
                    if np.random.random() < 0.012:  # 1.2% waste
                        is_waste = True
                        waste_type = np.random.choice(['Customer Return', 'Kitchen Error'], p=[0.7, 0.3])
                elif 'Salmon' in item['name'] or 'Fish' in item['name']:
                    if np.random.random() < 0.025:  # Higher waste for seafood
                        is_waste = True
                        waste_type = np.random.choice(['Customer Return', 'Kitchen Error', 'Spoilage'], p=[0.4, 0.3, 0.3])
                
                # Calculate financials
                total_revenue = actual_price * quantity if not is_waste else 0
                total_food_cost = food_cost * quantity
                contribution_margin = total_revenue - total_food_cost
                food_cost_pct = (total_food_cost / total_revenue * 100) if total_revenue > 0 else 0
                
                record = {
                    'order_id': f'ORD{str(order_id).zfill(7)}',
                    'order_date': current_date.strftime('%Y-%m-%d'),
                    'order_datetime': order_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    'order_channel': channel,
                    'table_number': table_num,
                    'server_id': server_id,
                    'item_name': item['name'],
                    'category': category,
                    'menu_price': round(menu_price, 2),
                    'actual_price': round(actual_price, 2),
                    'food_cost_per_unit': round(food_cost, 2),
                    'quantity': quantity,
                    'total_revenue': round(total_revenue, 2),
                    'total_food_cost': round(total_food_cost, 2),
                    'contribution_margin': round(contribution_margin, 2),
                    'food_cost_pct': round(food_cost_pct, 2),
                    'prep_time_min': item['prep_time'],
                    'is_waste': is_waste,
                    'waste_type': waste_type,
                    'day_of_week': current_date.strftime('%A'),
                    'month': current_date.strftime('%B'),
                    'hour': hour,
                    'is_weekend': current_date.weekday() >= 5,
                    'is_holiday': is_holiday(current_date),
                    'is_rainy': is_rainy,
                    'payment_method': payment_method,
                }
                
                records.append(record)
            
            order_id += 1
        
        current_date += timedelta(days=1)
        
        # Progress indicator
        if current_date.day == 1:
            print(f"  Generated data through {current_date.strftime('%B %Y')}")
    
    return pd.DataFrame(records)


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("Restaurant POS Data Generator")
    print("="*60 + "\n")
    
    # Generate data
    df = generate_transactions()
    

    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    output_path = 'data/restaurant_pos_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n{'='*60}")
    print("Data Generation Complete!")
    print(f"{'='*60}")
    print(f"\nTotal Records: {len(df):,}")
    print(f"Date Range: {df['order_date'].min()} to {df['order_date'].max()}")
    print(f"Total Orders: {df['order_id'].nunique():,}")
    print(f"Total Revenue: ${df['total_revenue'].sum():,.2f}")
    print(f"Total Food Cost: ${df['total_food_cost'].sum():,.2f}")
    print(f"Overall Food Cost %: {(df['total_food_cost'].sum() / df['total_revenue'].sum() * 100):.2f}%")
    print(f"Waste Records: {df['is_waste'].sum():,} ({df['is_waste'].sum() / len(df) * 100:.2f}%)")
    print(f"\nData saved to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB\n")


if __name__ == '__main__':
    main()
