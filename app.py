import streamlit as st
import random

# Set up the page configuration
st.set_page_config(page_title="Market Entry Simulator", layout="centered")

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'intro'
    st.session_state.round = 1
    st.session_state.max_rounds = 5
    st.session_state.player_decisions = []
    st.session_state.competitor_decisions = []
    st.session_state.payoffs = []
    st.session_state.total_payoff = 0

# Game Introduction
if st.session_state.game_state == 'intro':
    st.title("🏪 Market Entry Simulator")
    st.write("""
    **Welcome to the Market Entry Simulator!**

    You are a firm considering entering a new market. The profitability depends on how many firms enter. Make strategic decisions to maximize your total payoff over multiple rounds.

    **Game Concepts:**

    - **Nash Equilibrium**
    - **Dominant Strategies**
    - **Payoff Matrix**

    **Payoff Structure:**

    - **If you enter and total entrants are less than or equal to 2**: Profit of ₹100.
    - **If you enter and total entrants exceed 2**: Loss of ₹50.
    - **If you stay out**: Profit of ₹0.

    """)
    if st.button("Start Game"):
        st.session_state.game_state = 'play'

# Game Play
elif st.session_state.game_state == 'play':
    st.title("🏪 Market Entry Simulator")
    st.header(f"Round {st.session_state.round} of {st.session_state.max_rounds}")

    st.write("**Make your decision:** Do you want to enter the market this round?")
    player_choice = st.radio(
        "Choose your action:",
        ('Enter', 'Stay Out'),
        key=f'player_choice_round_{st.session_state.round}'
    )

    if st.button("Submit Decision"):
        # Record player's decision
        st.session_state.player_decisions.append(player_choice)

        # Simulate competitor decisions
        # For realism, we can have multiple competitors with different strategies
        competitor_choices = []
        num_competitors = 2  # Number of competitors

        for i in range(num_competitors):
            strategy = random.choice(['Aggressive', 'Random'])
            if strategy == 'Aggressive':
                competitor_choice = 'Enter'
            else:
                competitor_choice = random.choice(['Enter', 'Stay Out'])
            competitor_choices.append(competitor_choice)

        st.session_state.competitor_decisions.append(competitor_choices)

        # Calculate total entrants
        total_entrants = competitor_choices.count('Enter')
        if player_choice == 'Enter':
            total_entrants += 1

        # Determine payoff
        if player_choice == 'Enter':
            if total_entrants <= 2:
                payoff = 100
                st.success("You entered the market and made a profit of ₹100.")
            else:
                payoff = -50
                st.warning("Too many firms entered. You incurred a loss of ₹50.")
        else:
            payoff = 0
            st.info("You stayed out of the market.")

        st.session_state.payoffs.append(payoff)
        st.session_state.total_payoff += payoff

        # Display competitor actions
        st.write("**Competitors' Decisions:**")
        for idx, choice in enumerate(competitor_choices, 1):
            st.write(f"Competitor {idx}: {choice}")

        # Move to next round or end game
        if st.session_state.round < st.session_state.max_rounds:
            st.session_state.round += 1
        else:
            st.session_state.game_state = 'results'

# Results Phase
elif st.session_state.game_state == 'results':
    st.title("📈 Game Over - Results")
    st.write("**Your Total Payoff:** ₹{}".format(st.session_state.total_payoff))

    # Display detailed results
    st.subheader("Round-by-Round Summary")
    for i in range(st.session_state.max_rounds):
        st.write(f"### Round {i+1}")
        st.write(f"- **Your Decision:** {st.session_state.player_decisions[i]}")
        st.write(f"- **Competitors' Decisions:** {st.session_state.competitor_decisions[i]}")
        st.write(f"- **Your Payoff:** ₹{st.session_state.payoffs[i]}")
        st.write("---")

    # Educational Insights
    st.subheader("📚 Game Theory Insights")
    st.write("""
    - **Nash Equilibrium:** In this game, the Nash Equilibrium occurs when firms randomize their strategies to keep competitors indifferent.
    - **Dominant Strategy:** No dominant strategy exists here because your best choice depends on competitors' actions.
    - **Strategic Thinking:** Anticipate competitors' strategies to inform your decisions.
    """)

    # Reset the game
    if st.button("Play Again"):
        st.session_state.game_state = 'intro'
        st.session_state.round = 1
        st.session_state.player_decisions = []
        st.session_state.competitor_decisions = []
        st.session_state.payoffs = []
        st.session_state.total_payoff = 0
