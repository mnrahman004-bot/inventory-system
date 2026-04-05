# backend/ml/prediction.py
# AI Stock Prediction using Linear Regression (scikit-learn)
# Predicts future demand based on historical transaction data

import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression


def predict_demand(transactions, days_ahead=30):
    """
    Given a list of transaction dicts with 'type', 'quantity', 'date',
    train a Linear Regression model and predict demand for the next N days.

    Returns:
        dict: {
            'predicted_quantity': int,
            'trend': 'increasing' | 'decreasing' | 'stable',
            'confidence': float (R² score),
            'data_points': int
        }
    """
    if not transactions or len(transactions) < 2:
        return {
            'predicted_quantity': 0,
            'trend': 'stable',
            'confidence': 0.0,
            'data_points': len(transactions) if transactions else 0,
            'message': 'Not enough data for prediction'
        }

    # Build daily demand time series (OUT transactions = demand)
    daily_demand = {}
    for tx in transactions:
        date_val = tx['date']
        # Handle both datetime objects and strings
        if isinstance(date_val, str):
            date_val = datetime.strptime(date_val[:10], '%Y-%m-%d')
        elif hasattr(date_val, 'date'):
            date_val = date_val.date()

        day_key = str(date_val)[:10]
        qty = tx['quantity']
        if tx['type'] == 'IN':
            qty = 0  # Ignore incoming stock for demand prediction

        daily_demand[day_key] = daily_demand.get(day_key, 0) + qty

    if not daily_demand or all(v == 0 for v in daily_demand.values()):
        return {
            'predicted_quantity': 0,
            'trend': 'stable',
            'confidence': 0.0,
            'data_points': 0,
            'message': 'No outgoing transactions found'
        }

    # Convert dates to numeric (days since first date)
    sorted_dates = sorted(daily_demand.keys())
    base_date = datetime.strptime(sorted_dates[0], '%Y-%m-%d')

    X = []
    y = []
    for d in sorted_dates:
        days_since = (datetime.strptime(d, '%Y-%m-%d') - base_date).days
        X.append([days_since])
        y.append(daily_demand[d])

    X = np.array(X)
    y = np.array(y)

    # Train Linear Regression
    model = LinearRegression()
    model.fit(X, y)

    # Predict demand for next N days
    last_day = X[-1][0]
    future_days = np.array([[last_day + days_ahead]])
    predicted = model.predict(future_days)[0]
    predicted = max(0, round(predicted))  # No negative predictions

    # Calculate R² score (model confidence)
    r2 = model.score(X, y) if len(X) > 1 else 0.0
    r2 = round(float(r2), 3)

    # Determine trend from slope
    slope = model.coef_[0]
    if slope > 0.5:
        trend = 'increasing'
    elif slope < -0.5:
        trend = 'decreasing'
    else:
        trend = 'stable'

    return {
        'predicted_quantity': int(predicted),
        'trend': trend,
        'confidence': r2,
        'data_points': len(X),
        'slope': round(float(slope), 4),
        'days_ahead': days_ahead
    }
