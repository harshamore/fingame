import streamlit as st
import random

# Set up the page configuration
st.set_page_config(page_title="Market Entry Simulator", layout="centered")

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'intro'
    st.session_state.round = 1
    st.session_state.max_rounds = 3  # Updated to 3 rounds
    st.session_state.player_decisions = []
    st.session_state.competitor_decisions = []
    st.session_state.payoffs = []
    st.session_state.total_payoff = 0
    st.session_state.num_competitors = 4  # Total competitors (5 firms including player)
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

    - **If you enter and total entrants are ≤ 3**: Profit of **$100**.
    - **If you enter and total entrants exceed 3**: Loss of **$50**.
    - **If you stay out**: Profit of **$0**.

    """)

    # Display Competitor Strategies
    st.header("Competitor Strategies")
    st.write("The competitors in this game use different strategies:")
    strategies_list = [
        'Aggressive Entry: Always enter the market.',
        'Cautious Entry: Enter only if conditions are favorable.',
        'Randomized Strategy: Enter based on probability.',
        'Tit-for-Tat: Mimic your previous action.'
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
    - **If you enter and total entrants are ≤ 3**: Profit of **$100**.
    - **If you enter and total entrants exceed 3**: Loss of **$50**.
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
                    # Randomized with a lower probability to enter
                    competitor_choice = random.choices(['Enter', 'Stay Out'], weights=[0.4, 0.6])[0]
                elif 'Tit-for-Tat' in strategy:
                    if st.session_state.round == 1:
                        competitor_choice = random.choice(['Enter', 'Stay Out'])
                    else:
                        competitor_choice = st.session_state.player_decisions[-2]
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
                if total_entrants <= 3:
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
                # Clear the radio button selection for the next round
                key_to_delete = f'player_choice_round_{st.session_state.round}'
                if key_to_delete in st.session_state:
                    del st.session_state[key_to_delete]
                st.session_state.round += 1
                st.session_state.show_results = False
        else:
            st.write("**End of the game. Click 'View Results' to see the analysis.**")
            if st.button("View Results"):
                st.session_state.game_state = 'results'
                st.session_state.show_results = False

# Results Phase
elif st.session_state.game_state == 'results':
    st.title("📈 Game Over - Results")
    st.write("**Your Total Payoff:** ${}".format(st.session_state.total_payoff))

    # Display detailed results with analysis
    st.subheader("Round-by-Round Analysis")
    for i in range(st.session_state.max_rounds):
        st.write(f"### Round {i+1}")
        player_decision = st.session_state.player_decisions[i]
        st.write(f"- **Your Decision:** {player_decision}")
        competitor_decisions = st.session_state.competitor_decisions[i]
        competitor_strategies = st.session_state.competitor_strategies
        st.write("**Competitors' Decisions and Strategies:**")
        for idx in range(st.session_state.num_competitors):
            strategy_name = competitor_strategies[idx].split(':')[0]
            st.write(f"Competitor {idx+1} ({strategy_name}): {competitor_decisions[idx]}")

        total_entrants = competitor_decisions.count('Enter')
        if player_decision == 'Enter':
            total_entrants += 1

        st.write(f"- **Total Entrants:** {total_entrants}")
        st.write(f"- **Your Payoff:** ${st.session_state.payoffs[i]}")

        # Analysis
        st.markdown(f"#### Analysis for Round {i+1}")
        st.write(f"You chose to **{player_decision}**.")
        st.write(f"Competitors chose: {', '.join(competitor_decisions)}.")

        if player_decision == 'Enter':
            if total_entrants <= 3:
                st.write("Since total entrants were ≤ 3, you made a profit of $100.")
                st.write("Your decision to enter was profitable.")
            else:
                st.write("Since total entrants exceeded 3, you incurred a loss of $50.")
                st.write("Market over-saturation led to losses for entrants.")
        else:
            st.write("You stayed out of the market and neither gained nor lost money.")
            if total_entrants > 3:
                st.write("Your decision to stay out was wise, as entrants incurred losses due to over-saturation.")
            else:
                st.write("You missed an opportunity for profit, as total entrants were ≤ 3.")

        # Explain competitors' strategies and their impact
        for idx in range(st.session_state.num_competitors):
            strategy_name = competitor_strategies[idx].split(':')[0]
            competitor_decision = competitor_decisions[idx]
            st.write(f"Competitor {idx+1} used the **{strategy_name}** strategy and chose to **{competitor_decision}**.")

        # Game theory insights for the round
        st.write("**Game Theory Analysis:**")
        st.write("- **Strategic Thinking:** Understanding competitors' strategies could help predict their actions.")
        st.write("- **Nash Equilibrium:** No player can benefit by unilaterally changing their decision if others' decisions remain the same.")
        st.write("---")

    # Overall Game Theory Insights
    st.subheader("📚 Overall Game Theory Insights")
    st.write("""
    - **Nash Equilibrium:** Throughout the game, you might have observed situations where your best response depended on the competitors' actions.
    - **Dominant Strategy:** In this game, no dominant strategy exists because the best choice (Enter or Stay Out) depends on competitors' decisions.
    - **Strategic Thinking:** Anticipating competitors' strategies is crucial. By understanding their behavior patterns, you can adjust your decisions to maximize payoffs.
    - **Market Dynamics:** Entering a saturated market leads to losses, demonstrating the importance of considering market capacity.
    """)

    # Reset the game
    if st.button("Play Again"):
        reset_game()
