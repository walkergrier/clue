from math import floor

import pandas as pd

from constants import ALL_CARDS, CARD_CATEGORIES, ROOMS, SUSPECTS, WEAPONS, Status


class ClueGame:
    """
    The main class for the Clue Analyzer. It holds the current state of knowledge
    (the deduction grid, disjunctions, and known hand sizes) for a single game.
    """

    def __init__(self, player_names: list[str], my_hand_cards: set[str]):
        """
        Initializes the game state.

        :param player_names: List of all players in turn order (e.g., ['Me', 'Bob', 'Alice']).
        :param my_hand_cards: The set of cards the human player (us) holds.
        """
        print("Initializing Clue Game State...")

        # --- Core Properties ---
        self.player_names: list[str] = player_names
        # Column names for the grid: All players + the solution envelope
        self.columns: list[str] = player_names + ["Solution"]

        # 1. The primary deduction data structure (Truth Matrix)
        # Rows: ALL_CARDS (21 total)
        # Columns: All Players + 'Solution' (3-6 players + 1 Solution column)
        self.grid: pd.DataFrame = self._initialize_grid()

        # 2. Stores 'OR' facts derived from non-reveals, e.g., Alice has one of {Pipe, Hall, Green}
        # Item format: {'player': str, 'cards': Set[str], 'count': int (always 1 for Clue)}
        self.disjunctions: list[dict] = []

        # 3. Stores the known hand sizes for the hand size completion rule
        self.hand_sizes: dict[str, int] = {}

        # 4. Stores direct evidence (YES facts) for quick reference and logging
        self.known_cards: dict[str, set[str]] = {name: set() for name in self.columns}

        # --- Initialization Steps ---
        self._calculate_initial_hand_sizes()
        self._set_initial_facts(my_hand_cards)

        print("Initial facts recorded.")

    def _initialize_grid(self) -> pd.DataFrame:
        """
        Creates the initial Truth Matrix, setting all cells to Status.MAYBE (0).
        """
        # Create an array filled with the Status.MAYBE enum value (which is 0)
        # Rows are ALL_CARDS, Columns are player names + 'Solution'
        data = [[Status.MAYBE.value] * len(self.columns) for _ in range(len(ALL_CARDS))]

        # Use ALL_CARDS as the index (rows) and the calculated columns as the column headers
        grid = pd.DataFrame(data, index=ALL_CARDS, columns=self.columns)

        # Convert the integer values back to the Status type for safer use
        return grid.applymap(lambda x: Status(x))

    def _calculate_initial_hand_sizes(self):
        """
        Determines the number of cards each player holds based on the total number of players.
        The Solution always holds 3 cards (1 S, 1 W, 1 R).
        The remaining cards (21 - 3 = 18) are divided among the players.
        """
        total_cards_to_deal = len(ALL_CARDS) - 3  # 18 cards to deal
        num_players = len(self.player_names)

        # The first few players get the floor(18 / N) + 1 extra card
        base_size = floor(total_cards_to_deal / num_players)
        remainder = total_cards_to_deal % num_players

        # Calculate sizes and store them
        for i, player in enumerate(self.player_names):
            self.hand_sizes[player] = base_size + (1 if i < remainder else 0)

        # The Solution is special; it always has 3 cards
        self.hand_sizes["Solution"] = 3

        # Confirmation check: total cards must be 21
        # print(f"Hand sizes: {self.hand_sizes}. Total: {sum(self.hand_sizes.values())}")

    def _set_initial_facts(self, my_hand_cards: set[str]):
        """
        Logs the cards in the player's (our) hand, which are definite YES facts for us
        and definite NO facts for everyone else (including the Solution).
        """
        my_name = self.player_names[0]  # Assumes the human player is always the first one entered

        for card in my_hand_cards:
            # 1. Update our hand: We MUST have this card (YES)
            self._update_grid_cell(card, my_name, Status.YES)

            # 2. Propagate NO facts: Everyone else (including Solution) MUST NOT have this card (NO)
            for column in self.columns:
                if column != my_name:
                    self._update_grid_cell(card, column, Status.NO)

    def _update_grid_cell(self, card: str, column: str, status: Status):
        """
        A helper method to safely update the grid and also update the known_cards set.
        """
        if status == Status.YES:
            # Add to known_cards set if it's a YES
            self.known_cards[column].add(card)
        elif status == Status.NO and card in self.known_cards[column]:
            # Should not happen, but good safeguard
            self.known_cards[column].remove(card)

        # Update the pandas DataFrame cell value
        self.grid.loc[card, column] = status

    # --- Public Methods for CLI Interaction (Placeholder for now) ---

    def record_turn_outcome(
        self, suggester: str, suggestion_cards: set[str], passers: list[str], shower: str
    ):
        """
        Records the outcome of a suggestion where the shower is known,
        but the card shown is NOT known to the Analyzer.
        This often results in adding a new disjunction fact.
        """
        print(f"Recording turn: {suggester} suggested {suggestion_cards}. Shower: {shower}.")
        # Implementation to be added later based on DeductionEngine needs.

    def record_reveal(self, player_name: str, card_name: str):
        """
        Records a direct revelation of a card (e.g., when the Analyzer is the suggester).
        This results in a direct YES fact for player_name and a NO fact for everyone else.
        """
        print(f"Recording direct reveal: {player_name} showed {card_name}.")
        # The _update_grid_cell method already handles the required logic.
        self._update_grid_cell(card_name, player_name, Status.YES)