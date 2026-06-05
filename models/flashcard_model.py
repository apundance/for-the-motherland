class FlashcardModel:
    def __init__(self, cards):
        self.cards = cards
        self.index = 0

    def current(self):
        if not self.cards:
            return None
        return self.cards[self.index]

    def next(self):
        if self.cards:
            self.index = (self.index + 1) % len(self.cards)

    def prev(self):
        if self.cards:
            self.index = (self.index - 1) % len(self.cards)