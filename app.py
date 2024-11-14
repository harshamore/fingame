import streamlit as st
import random

# Set up the page configuration
st.set_page_config(page_title="Salary Negotiation Simulator", layout="centered")

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'setup'
    st.session_state.round = 1
    st.session_state.max_rounds = 3
    st.session_state.employer_budget = 0
    st.session_state.employee_min_salary = 0
    st.session_state.employer_offer = []
    st.session_state.employee_demand = []
    st.session_state.agreement_reached = False
    st.session_state.payoffs = {'Employer': 0, 'Employee': 0}

# Game Setup
if st.session_state.game_state == 'setup':
    st.title("💼 Salary Negotiation Simulator")
    st.write("Welcome to the Salary Negotiation Simulator! This game models the negotiation between an employer and an employee using game theory concepts.")

    st.header("Game Setup")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Employer Setup")
        st.session_state.employer_budget = st.number_input(
            "Enter the maximum budget for the position (₹):",
            min_value=50000,
            max_value=500000,
            step=5000,
            value=150000,
            key='employer_budget_input'
        )

    with col2:
        st.subheader("Employee Setup")
        st.session_state.employee_min_salary = st.number_input(
            "Enter the minimum acceptable salary (₹):",
            min_value=50000,
            max_value=500000,
            step=5000,
            value=100000,
            key='employee_salary_input'
        )

    if st.button("Start Negotiation"):
        if st.session_state.employer_budget < st.session_state.employee_min_salary:
            st.error("The employer's budget must be equal to or higher than the employee's minimum salary.")
        else:
            st.session_state.game_state = 'negotiation'

# Negotiation Phase
elif st.session_state.game_state == 'negotiation':
    st.title("🤝 Salary Negotiation Simulator")
    st.header(f"Round {st.session_state.round} of {st.session_state.max_rounds}")

    st.write("**Employer and Employee, please enter your proposals.**")
    st.write("Note: Proposals are confidential until both are submitted.")

    # Input forms for simultaneous proposals
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Employer's Offer")
        employer_offer = st.number_input(
            "Enter your salary offer (₹):",
            min_value=st.session_state.employee_min_salary,
            max_value=st.session_state.employer_budget,
            step=5000,
            key=f'employer_offer_round_{st.session_state.round}'
        )

    with col2:
        st.subheader("Employee's Demand")
        employee_demand = st.number_input(
            "Enter your salary demand (₹):",
            min_value=st.session_state.employee_min_salary,
            max_value=st.session_state.employer_budget,
            step=5000,
            key=f'employee_demand_round_{st.session_state.round}'
        )

    if st.button("Submit Proposals"):
        st.session_state.employer_offer.append(employer_offer)
        st.session_state.employee_demand.append(employee_demand)

        # Check for agreement
        if employer_offer >= employee_demand:
            st.session_state.agreement_reached = True
            agreed_salary = employee_demand
            st.success(f"🎉 Agreement reached at a salary of ₹{agreed_salary}!")
            # Calculate payoffs
            employer_value = st.session_state.employer_budget * 1.2  # Assume the employee brings 20% more value
            st.session_state.payoffs['Employer'] = employer_value - agreed_salary
            st.session_state.payoffs['Employee'] = agreed_salary - st.session_state.employee_min_salary
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
        st.write(f"An agreement was reached at a salary of ₹{st.session_state.employee_demand[-1]}.")

        st.subheader("Payoffs")
        st.write(f"**Employer's Payoff**: ₹{st.session_state.payoffs['Employer']}")
        st.write(f"**Employee's Payoff**: ₹{st.session_state.payoffs['Employee']}")
    else:
        st.write("No agreement was reached after all negotiation rounds.")
        st.write("Both parties receive a payoff of **₹0**.")

    # Display the negotiation history
    st.subheader("Negotiation History")
    negotiation_data = {
        'Round': list(range(1, st.session_state.round + 1)),
        'Employer Offer (₹)': st.session_state.employer_offer,
        'Employee Demand (₹)': st.session_state.employee_demand
    }
    st.table(negotiation_data)

    # Reset the game
    if st.button("Restart Game"):
        st.session_state.game_state = 'setup'
        st.session_state.round = 1
        st.session_state.employer_budget = 0
        st.session_state.employee_min_salary = 0
        st.session_state.employer_offer = []
        st.session_state.employee_demand = []
        st.session_state.agreement_reached = False
        st.session_state.payoffs = {'Employer': 0, 'Employee': 0}
