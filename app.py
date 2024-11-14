import streamlit as st
import pandas as pd
import random
import time

# Set up session state to avoid duplicate keys and initialize only once
if "game_data" not in st.session_state:
    st.session_state.game_data = {
        "cash": 100000,
        "inventory": 500,
        "accounts_receivable": 0,
        "accounts_payable": 0,
        "inventory_period": 30,   # Default values in days
        "collection_period": 30,
        "payment_period": 30
    }
    st.session_state.start_time = None  # Game start time placeholder
    st.session_state.purchase_amount = 0  # Placeholder for inventory input
    st.session_state.credit_days = 30     # Placeholder for credit terms input
    st.session_state.payment_action = "Pay on Due Date"  # Placeholder for payment action

# Initialize Game State
st.set_page_config(page_title="Business Balance Simulator", layout="wide")

# Sidebar controls
with st.sidebar:
    st.title("Business Balance Simulator")
    st.write("Objective: Run your business profitably in 15 minutes!")
    if st.button("Start Game") and st.session_state.start_time is None:
        st.session_state.start_time = time.time()  # Start the timer

    # Metrics display placeholders
    cash_balance = st.empty()
    inventory_status = st.empty()
    accounts_receivable = st.empty()
    accounts_payable = st.empty()

# Main game loop
if st.session_state.start_time is not None:
    game_data = st.session_state.game_data
    elapsed_time = time.time() - st.session_state.start_time

    while elapsed_time < 900:  # 15 minutes
        # Display current state
        cash_balance.metric("Cash Balance", f"₹{game_data['cash']}")
        inventory_status.metric("Inventory", f"{game_data['inventory']} units")
        accounts_receivable.metric("Accounts Receivable", f"₹{game_data['accounts_receivable']}")
        accounts_payable.metric("Accounts Payable", f"₹{game_data['accounts_payable']}")

        # Player decision inputs with unique session state keys
        with st.expander("Manage Inventory"):
            st.session_state.purchase_amount = st.number_input("Order Inventory (units)", 
                                                               min_value=0, step=10, 
                                                               key="purchase_inventory_unique")
            # Process inventory purchase
            if st.session_state.purchase_amount > 0:
                cost = st.session_state.purchase_amount * 100  # Assume ₹100 per unit cost
                game_data['cash'] -= cost
                game_data['inventory'] += st.session_state.purchase_amount

        with st.expander("Set Customer Credit Terms"):
            st.session_state.credit_days = st.selectbox("Credit Terms (Days)", 
                                                        [15, 30, 45], 
                                                        key="credit_terms_unique")
            # Adjust collection period
            game_data['collection_period'] = st.session_state.credit_days

        with st.expander("Manage Supplier Payments"):
            st.session_state.payment_action = st.selectbox("Supplier Payment", 
                                                           ["Pay Now", "Pay on Due Date", "Delay Payment"], 
                                                           key="supplier_payment_unique")
            # Adjust payment period
            if st.session_state.payment_action == "Pay Now":
                game_data['payment_period'] -= 5  # Benefit of early payment
            elif st.session_state.payment_action == "Delay Payment":
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

        # Update elapsed time for game loop
        elapsed_time = time.time() - st.session_state.start_time
        time.sleep(1)  # Refresh loop every second

    # End Game
    st.write("**Game Over!** Your final score is calculated based on your cash flow, inventory, and payment performance.")
