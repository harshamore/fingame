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
    st.session_state.num_competitors = 4  # Total competitors
    st.session_state.competitor_strategies = []
    st.session_state.show_results = False

# Function to reset the game
def reset_game():
    st.session_state.game_state = 'intro'
    st.session_state.round = 1
    st.session_state.player_decisions = []
    st.session_state.competitor_decisions = []
    st.session_state.payoffs = []
    st.session_state.total_payoff = 0
    st.session_state.competitor_strategies = []
    st.session_state.show_results = False

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
    - **Strategic Thinking**

    **Payoff Structure:**

    - **If you enter and total entrants are ≤ 2**: Profit of **$100**.
    - **If you enter and total entrants exceed 2**: Loss of **$50**.
    - **If you stay out**: Profit of **$0**.

    """)

    # Display Competitor Strategies
    st.header("Competitor Strategies")
    st.write("The competitors in this game use different strategies:")
    strategies_list = [
        'Aggressive Entry: Always enter the market.',
        'Cautious Entry: Enter only if conditions are favorable.',
        'Randomized Strategy: Enter based on probability.',
        'Tit-for-Tat: Mimic your previous action.',
        'Adaptive Strategy: Adjust based on past outcomes.'
    ]
    for idx, strategy in enumerate(strategies_list, 1):
        st.write(f"**Competitor {idx}**: {strategy}")

    if st.button("Start Game"):
        # Assign strategies to competitors
        st.session_state.competitor_strategies = random.sample(strategies_list, st.session_state.num_competitors)
        st.session_state.game_state = 'play'

# Game Play
elif st.session_state.game_state == 'play':
    st.title("🏪 Market Entry Simulator")
    st.header(f"Round {st.session_state.round} of {st.session_state.max_rounds}")

    # Show Payoff Structure
    st.subheader("Payoff Structure")
    st.write("""
    - **If you enter and total entrants are ≤ 2**: Profit of **$100**.
    - **If you enter and total entrants exceed 2**: Loss of **$50**.
    - **If you stay out**: Profit of **$0**.
    """)

    # Show Competitor Strategies
    st.subheader("Competitor Strategies")
    st.write("Your competitors are using the following strategies:")
    for idx, strategy in enumerate(st.session_state.competitor_strategies, 1):
        st.write(f"**Competitor {idx}**: {strategy}")

    if not st.session_state.show_results:
        st.write("**Make your decision:** Do you want to enter the market this round?")
        player_choice = st.radio(
            "Choose your action:",
            ('Enter', 'Stay Out'),
            key=f'player_choice_round_{st.session_state.round}'
        )

        if st.button("Submit Decision"):
            # Record player's decision
            st.session_state.player_decisions.append(player_choice)

            # Simulate competitor decisions based on their strategies
            competitor_choices = []
            for idx in range(st.session_state.num_competitors):
                strategy = st.session_state.competitor_strategies[idx]
                if 'Aggressive' in strategy:
                    competitor_choice = 'Enter'
                elif 'Cautious' in strategy:
                    # Cautious entry if previous payoff was positive
                    if st.session_state.round == 1 or st.session_state.payoffs[-1] >= 0:
                        competitor_choice = 'Enter'
                    else:
                        competitor_choice = 'Stay Out'
                elif 'Randomized' in strategy:
                    competitor_choice = random.choice(['Enter', 'Stay Out'])
                elif 'Tit-for-Tat' in strategy:
                    if st.session_state.round == 1:
                        competitor_choice = 'Enter'
                    else:
                        competitor_choice = st.session_state.player_decisions[-2]
                elif 'Adaptive' in strategy:
                    if st.session_state.round == 1:
                        competitor_choice = random.choice(['Enter', 'Stay Out'])
                    else:
                        # If last payoff was positive, repeat action; else, switch
                        last_payoff = st.session_state.payoffs[-1]
                        if last_payoff >= 0:
                            competitor_choice = st.session_state.competitor_decisions[-1][idx]
                        else:
                            competitor_choice = 'Enter' if st.session_state.competitor_decisions[-1][idx] == 'Stay Out' else 'Stay Out'
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
                    st.success("You entered the market and made a profit of **$100**.")
                else:
                    payoff = -50
                    st.warning("Too many firms entered. You incurred a loss of **$50**.")
            else:
                payoff = 0
                st.info("You stayed out of the market.")

            st.session_state.payoffs.append(payoff)
            st.session_state.total_payoff += payoff

            # Display competitor actions
            st.write("**Competitors' Decisions:**")
            for idx, choice in enumerate(competitor_choices, 1):
                st.write(f"Competitor {idx}: {choice}")

            # Set flag to show results
            st.session_state.show_results = True
    else:
        if st.session_state.round < st.session_state.max_rounds:
            if st.button("Next Round"):
                st.session_state.round += 1
                st.session_state.show_results = False
                # Clear the radio button selection for the next round
                del st.session_state[f'player_choice_round_{st.session_state.round - 1}']
        else:
            st.session_state.game_state = 'results'

# Results Phase
elif st.session_state.game_state == 'results':
    st.title("📈 Game Over - Results")
    st.write("**Your Total Payoff:** ${}".format(st.session_state.total_payoff))

    # Display detailed results
    st.subheader("Round-by-Round Summary")
    for i in range(st.session_state.max_rounds):
        st.write(f"### Round {i+1}")
        st.write(f"- **Your Decision:** {st.session_state.player_decisions[i]}")
        competitor_decisions = st.session_state.competitor_decisions[i]
        competitor_strategies = st.session_state.competitor_strategies
        st.write("**Competitors' Decisions and Strategies:**")
        for idx in range(st.session_state.num_competitors):
            strategy_name = competitor_strategies[idx].split(':')[0]
            st.write(f"Competitor {idx+1} ({strategy_name}): {competitor_decisions[idx]}")
        st.write(f"- **Your Payoff:** ${st.session_state.payoffs[i]}")
        st.write("---")

    # Educational Insights
    st.subheader("📚 Game Theory Insights")
    st.write("""
    - **Nash Equilibrium:** In this game, Nash Equilibrium occurs when firms randomize their strategies, making others indifferent.
    - **Dominant Strategy:** No dominant strategy exists; the best action depends on competitors.
    - **Strategic Thinking:** Anticipate competitors' strategies and adapt your decisions.
    """)

    # Reset the game
    if st.button("Play Again"):
        reset_game()
