import streamlit as st
import random
import time

# Initialize Game State in Session State
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.start_time = None
    st.session_state.game_data = {
        "cash": 100000,
        "inventory": 500,
        "accounts_receivable": 0,
        "accounts_payable": 0,
        "inventory_period": 30,   # Default values in days
        "collection_period": 30,
        "payment_period": 30
    }
    st.session_state.purchase_amount = 0
    st.session_state.credit_days = 30
    st.session_state.payment_action = "Pay on Due Date"
    st.session_state.last_event_time = time.time()
    st.session_state.random_event_triggered = False

# Set page configuration
st.set_page_config(page_title="Business Balance Simulator", layout="wide")

# Sidebar controls
with st.sidebar:
    st.title("Business Balance Simulator")
    st.write("Objective: Run your business profitably in 15 minutes!")

    if not st.session_state.game_started:
        if st.button("Start Game"):
            st.session_state.game_started = True
            st.session_state.start_time = time.time()
            st.success("Game Started! Good luck.")
    else:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = int(900 - elapsed_time)
        st.write(f"Time Remaining: {remaining_time} seconds")

# Main game interface
if st.session_state.game_started:
    game_data = st.session_state.game_data
    elapsed_time = time.time() - st.session_state.start_time

    if elapsed_time >= 900:
        st.session_state.game_started = False
        st.write("**Game Over!** Your final score is calculated based on your cash flow, inventory, and payment performance.")
        # Display final scores or any end-of-game summaries here
    else:
        # Display current state
        st.markdown("### Business Dashboard")
        cols = st.columns(4)
        cols[0].metric("Cash Balance", f"₹{game_data['cash']}")
        cols[1].metric("Inventory", f"{game_data['inventory']} units")
        cols[2].metric("Accounts Receivable", f"₹{game_data['accounts_receivable']}")
        cols[3].metric("Accounts Payable", f"₹{game_data['accounts_payable']}")

        st.markdown("---")

        # Player decision inputs
        st.markdown("### Make Your Decisions")

        # Manage Inventory
        with st.expander("Manage Inventory"):
            purchase_amount = st.number_input(
                "Order Inventory (units)",
                min_value=0,
                step=10,
                key="purchase_inventory_unique"
            )
            if st.button("Purchase Inventory"):
                cost = purchase_amount * 100  # Assume ₹100 per unit cost
                if game_data['cash'] >= cost:
                    game_data['cash'] -= cost
                    game_data['inventory'] += purchase_amount
                    st.success(f"Purchased {purchase_amount} units of inventory for ₹{cost}.")
                    st.session_state.purchase_amount = 0  # Reset input after purchase
                else:
                    st.error("Insufficient cash to purchase inventory.")

        # Set Customer Credit Terms
        with st.expander("Set Customer Credit Terms"):
            credit_days = st.selectbox(
                "Credit Terms (Days)",
                [15, 30, 45],
                index=[15, 30, 45].index(st.session_state.credit_days),
                key="credit_terms_unique"
            )
            if credit_days != st.session_state.credit_days:
                st.session_state.credit_days = credit_days
                game_data['collection_period'] = credit_days
                st.info(f"Customer credit terms set to {credit_days} days.")

        # Manage Supplier Payments
        with st.expander("Manage Supplier Payments"):
            payment_action = st.selectbox(
                "Supplier Payment",
                ["Pay Now", "Pay on Due Date", "Delay Payment"],
                index=["Pay Now", "Pay on Due Date", "Delay Payment"].index(st.session_state.payment_action),
                key="supplier_payment_unique"
            )
            if payment_action != st.session_state.payment_action:
                st.session_state.payment_action = payment_action
                if payment_action == "Pay Now":
                    game_data['payment_period'] -= 5  # Benefit of early payment
                    st.info("You chose to pay suppliers now. Payment period decreased by 5 days.")
                elif payment_action == "Delay Payment":
                    game_data['payment_period'] += 5  # Late fees may apply
                    st.warning("You chose to delay payment. Payment period increased by 5 days.")
                else:
                    st.info("You chose to pay on the due date.")

        st.markdown("---")

        # Random events (triggered every 30 seconds)
        current_time = time.time()
        if current_time - st.session_state.last_event_time >= 30:
            event_trigger = random.randint(1, 100)
            st.session_state.last_event_time = current_time

            if event_trigger < 20:
                st.success("**Sales Spike!** Demand has increased temporarily.")
                game_data['inventory'] -= 50  # Increase in demand
            elif event_trigger < 30:
                st.warning("**Delayed Payments** Customers are delaying payments.")
                game_data['collection_period'] += 15
            else:
                st.info("Business as usual.")

        # Update other game metrics or handle automatic processes here

        # Display updated periods
        st.markdown("### Current Period Metrics")
        cols = st.columns(3)
        cols[0].metric("Inventory Period", f"{game_data['inventory_period']} days")
        cols[1].metric("Collection Period", f"{game_data['collection_period']} days")
        cols[2].metric("Payment Period", f"{game_data['payment_period']} days")

        # You can add more game logic here, such as handling sales, updating accounts receivable/payable, etc.
