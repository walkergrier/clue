from enum import Enum

# --- CARD DEFINITIONS ---
# Standard 6 Suspects (People)
SUSPECTS: list[str] = [
    "Miss Scarlett",
    "Colonel Mustard",
    "Mrs. White",
    "Mr. Green",
    "Mrs. Peacock",
    "Professor Plum",
]

# Standard 6 Weapons
WEAPONS: list[str] = [
    "Candlestick",
    "Dagger",
    "Lead Pipe",
    "Revolver",
    "Rope",
    "Wrench",
]

# Standard 9 Rooms
ROOMS: list[str] = [
    "Hall",
    "Lounge",
    "Dining Room",
    "Kitchen",
    "Ballroom",
    "Conservatory",
    "Billiard Room",
    "Library",
    "Study",
]

# The complete list of all cards (21 total)
ALL_CARDS: list[str] = SUSPECTS + WEAPONS + ROOMS


# --- DEDUCTION ENUMERATION ---
# Status represents the state of a card for a given hand (player or solution)
class Status(Enum):
    """
    Represents the known status of a card within a specific player's hand or the Solution.
    -1: NO, 0: MAYBE, 1: YES
    """

    NO = -1  # The player/solution MUST NOT have this card.
    MAYBE = 0  # Default: We don't know yet.
    YES = 1  # The player/solution MUST have this card.

    def __str__(self):
        # Human-readable representation for CLI output
        if self.value == 0:
            return " "
        elif self.value == 1:
            return "Y"
        elif self.value == -1:
            return "N"
        else:
            return "?"

    def __repr__(self):
        return f"Status.{self.name}"


# A list of card categories for use in Solution logic
CARD_CATEGORIES: list[list[str]] = [SUSPECTS, WEAPONS, ROOMS]
