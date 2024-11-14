import streamlit as st
import pandas as pd
import random
import time

# Initialize Game State
st.set_page_config(page_title="Business Balance Simulator", layout="wide")

# Sidebar controls
with st.sidebar:
    st.title("Business Balance Simulator")
    st.write("Objective: Run your business profitably in 15 minutes!")
    start_game = st.button("Start Game")

    # Metrics display
    cash_balance = st.empty()
    inventory_status = st.empty()
    accounts_receivable = st.empty()
    accounts_payable = st.empty()

# Game variables initialization
if start_game:
    game_data = {
        "cash": 100000,
        "inventory": 500,
        "accounts_receivable": 0,
        "accounts_payable": 0,
        "inventory_period": 30,   # Default values in days
        "collection_period": 30,
        "payment_period": 30
    }
    start_time = time.time()

# Main game loop
while start_game and time.time() - start_time < 900:  # 15 minutes
    # Display current state
    cash_balance.metric("Cash Balance", f"₹{game_data['cash']}")
    inventory_status.metric("Inventory", f"{game_data['inventory']} units")
    accounts_receivable.metric("Accounts Receivable", f"₹{game_data['accounts_receivable']}")
    accounts_payable.metric("Accounts Payable", f"₹{game_data['accounts_payable']}")

    # Player decision inputs
    with st.beta_expander("Manage Inventory"):
        purchase_amount = st.number_input("Order Inventory (units)", min_value=0, step=10)
        # Process inventory purchase
        if purchase_amount > 0:
            cost = purchase_amount * 100  # Assume ₹100 per unit cost
            game_data['cash'] -= cost
            game_data['inventory'] += purchase_amount

    with st.beta_expander("Set Customer Credit Terms"):
        credit_days = st.selectbox("Credit Terms (Days)", [15, 30, 45])
        # Adjust collection period
        game_data['collection_period'] = credit_days

    with st.beta_expander("Manage Supplier Payments"):
        payment_action = st.selectbox("Supplier Payment", ["Pay Now", "Pay on Due Date", "Delay Payment"])
        # Adjust payment period
        if payment_action == "Pay Now":
            game_data['payment_period'] -= 5  # Benefit of early payment
        elif payment_action == "Delay Payment":
            game_data['payment_period'] += 5  # Late fees may apply

    # Random events
    event_trigger = random.randint(1, 100)
    if event_trigger < 20:
        st.write("**Sales Spike!** Demand has increased temporarily.")
        game_data['inventory'] -= 50  # Increase in demand
    elif event_trigger < 30:
        st.write("**Delayed Payments** Customers are delaying payments.")
        game_data['collection_period'] += 15

    # Update metrics
    st.write("---")
    st.write("### Game Events and Score Updates")
    st.write(f"Inventory Period: {game_data['inventory_period']} days")
    st.write(f"Collection Period: {game_data['collection_period']} days")
    st.write(f"Payment Period: {game_data['payment_period']} days")
    st.write(f"Score: {game_data['cash']}")

    # Game refresh every second
    time.sleep(1)

# End Game
st.write("**Game Over!** Your final score is calculated based on your cash flow, inventory, and payment performance.")
