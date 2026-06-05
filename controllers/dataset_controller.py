from models.dataset_model import list_datasets, load_dataset
from models.flashcard_model import FlashcardModel


class DatasetController:
    def __init__(self, view):
        self.view = view
        self.deck = None
        self.data = None

    def get_datasets(self):
        files = list_datasets(self.view.app.project_root)
        print("CONTROLLER FILES:", files)
        return files

    def load_dataset(self, filename):
        self.data = load_dataset(self.view.app.project_root, filename)
        self.view.ask_field_selection(self.data)

    def build_flashcards(self, front_fields, back_fields):
        cards = []

        for item in self.data:
            front = "\n".join(str(item.get(f, "")) for f in front_fields)
            back = "\n".join(str(item.get(f, "")) for f in back_fields)

            cards.append({"front": front, "back": back})

        self.deck = FlashcardModel(cards)

        self.view.showing_front = True

        self.update_view()

    def next_card(self):
        if self.deck:
            self.view.showing_front = True
            self.deck.next()
            self.update_view()

    def prev_card(self):
        if self.deck:
            self.view.showing_front = True
            self.deck.prev()
            self.update_view()

    def update_view(self):
        card = self.deck.current()

        self.view.render_card(card)

        current = self.deck.index + 1
        total = len(self.deck.cards)

        self.view.update_counter(current, total)