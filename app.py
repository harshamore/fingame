import streamlit as st
import random

# Set up the page configuration
st.set_page_config(page_title="Salary Negotiation Simulator", layout="centered")

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'setup'
    st.session_state.round = 1
    st.session_state.max_rounds = 3
    st.session_state.user_role = None
    st.session_state.user_min_salary = 0
    st.session_state.user_max_budget = 0
    st.session_state.app_min_salary = 0
    st.session_state.app_max_budget = 0
    st.session_state.user_proposals = []
    st.session_state.app_proposals = []
    st.session_state.agreement_reached = False
    st.session_state.agreed_salary = 0
    st.session_state.payoffs = {'You': 0, 'Application': 0}

# Game Setup
if st.session_state.game_state == 'setup':
    st.title("💼 Salary Negotiation Simulator")
    st.write("Negotiate a salary with the application acting as your opponent.")

    st.header("Select Your Role")
    st.session_state.user_role = st.radio(
        "Choose your role:",
        ('Employer', 'Employee'),
        key='user_role_selection'
    )

    if st.session_state.user_role == 'Employer':
        st.subheader("Your Role: Employer")
        st.session_state.user_max_budget = st.number_input(
            "Enter your maximum budget for the position (₹):",
            min_value=50000,
            max_value=500000,
            step=5000,
            value=150000,
            key='user_max_budget_input'
        )
        # Application sets its minimum acceptable salary
        st.session_state.app_min_salary = random.randint(50000, st.session_state.user_max_budget)
        st.write("You will negotiate with an Employee (the application).")
    else:
        st.subheader("Your Role: Employee")
        st.session_state.user_min_salary = st.number_input(
            "Enter your minimum acceptable salary (₹):",
            min_value=50000,
            max_value=500000,
            step=5000,
            value=100000,
            key='user_min_salary_input'
        )
        # Application sets its maximum budget
        st.session_state.app_max_budget = random.randint(st.session_state.user_min_salary, 500000)
        st.write("You will negotiate with an Employer (the application).")

    if st.button("Start Negotiation"):
        st.session_state.game_state = 'negotiation'

# Negotiation Phase
elif st.session_state.game_state == 'negotiation':
    st.title("🤝 Salary Negotiation Simulator")
    st.header(f"Round {st.session_state.round} of {st.session_state.max_rounds}")

    # User and Application make proposals
    if st.session_state.user_role == 'Employer':
        # User is Employer
        st.subheader("Your Turn: Employer's Offer")
        user_offer = st.number_input(
            "Enter your salary offer to the Employee (₹):",
            min_value=st.session_state.app_min_salary,
            max_value=st.session_state.user_max_budget,
            step=5000,
            key=f'user_offer_round_{st.session_state.round}'
        )

        # Application (Employee) makes a demand
        app_demand = random.randint(st.session_state.app_min_salary, st.session_state.user_max_budget)
        st.write("Waiting for the Employee's response...")

        if st.button("Submit Offer"):
            st.session_state.user_proposals.append(user_offer)
            st.session_state.app_proposals.append(app_demand)
            st.write(f"Employee (Application) demands: ₹{app_demand}")

            # Check for agreement
            if user_offer >= app_demand:
                st.session_state.agreement_reached = True
                st.session_state.agreed_salary = app_demand
                st.success(f"🎉 Agreement reached at a salary of ₹{st.session_state.agreed_salary}!")
                # Calculate payoffs
                employer_value = st.session_state.user_max_budget * 1.2  # Assume employee brings 20% more value
                st.session_state.payoffs['You'] = employer_value - st.session_state.agreed_salary
                st.session_state.payoffs['Application'] = st.session_state.agreed_salary - st.session_state.app_min_salary
                st.session_state.game_state = 'results'
            else:
                st.warning("No agreement reached this round.")
                # Move to next round or end game
                if st.session_state.round < st.session_state.max_rounds:
                    st.session_state.round += 1
                else:
                    st.session_state.game_state = 'results'

    else:
        # User is Employee
        st.subheader("Your Turn: Employee's Demand")
        user_demand = st.number_input(
            "Enter your salary demand to the Employer (₹):",
            min_value=st.session_state.user_min_salary,
            max_value=st.session_state.app_max_budget,
            step=5000,
            key=f'user_demand_round_{st.session_state.round}'
        )

        # Application (Employer) makes an offer
        app_offer = random.randint(st.session_state.user_min_salary, st.session_state.app_max_budget)
        st.write("Waiting for the Employer's offer...")

        if st.button("Submit Demand"):
            st.session_state.user_proposals.append(user_demand)
            st.session_state.app_proposals.append(app_offer)
            st.write(f"Employer (Application) offers: ₹{app_offer}")

            # Check for agreement
            if app_offer >= user_demand:
                st.session_state.agreement_reached = True
                st.session_state.agreed_salary = user_demand
                st.success(f"🎉 Agreement reached at a salary of ₹{st.session_state.agreed_salary}!")
                # Calculate payoffs
                employer_value = st.session_state.app_max_budget * 1.2  # Assume employee brings 20% more value
                st.session_state.payoffs['You'] = st.session_state.agreed_salary - st.session_state.user_min_salary
                st.session_state.payoffs['Application'] = employer_value - st.session_state.agreed_salary
                st.session_state.game_state = 'results'
            else:
                st.warning("No agreement reached this round.")
                # Move to next round or end game
                if st.session_state.round < st.session_state.max_rounds:
                    st.session_state.round += 1
                else:
                    st.session_state.game_state = 'results'

# Results Phase
elif st.session_state.game_state == 'results':
    st.title("📈 Negotiation Results")
    if st.session_state.agreement_reached:
        st.write(f"An agreement was reached at a salary of ₹{st.session_state.agreed_salary}.")

        st.subheader("Payoffs")
        st.write(f"**Your Payoff**: ₹{st.session_state.payoffs['You']}")
        st.write(f"**Application's Payoff**: ₹{st.session_state.payoffs['Application']}")
    else:
        st.write("No agreement was reached after all negotiation rounds.")
        st.write("Both parties receive a payoff of **₹0**.")

    # Display the negotiation history
    st.subheader("Negotiation History")
    negotiation_data = {
        'Round': list(range(1, st.session_state.round + 1)),
        'Your Proposal (₹)': st.session_state.user_proposals,
        "Application's Proposal (₹)": st.session_state.app_proposals
    }
    st.table(negotiation_data)

    # Reset the game
    if st.button("Restart Game"):
        st.session_state.game_state = 'setup'
        st.session_state.round = 1
        st.session_state.user_role = None
        st.session_state.user_min_salary = 0
        st.session_state.user_max_budget = 0
        st.session_state.app_min_salary = 0
        st.session_state.app_max_budget = 0
        st.session_state.user_proposals = []
        st.session_state.app_proposals = []
        st.session_state.agreement_reached = False
        st.session_state.agreed_salary = 0
        st.session_state.payoffs = {'You': 0, 'Application': 0}
