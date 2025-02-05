from pprint import pprint

from src.models.marketplaces.sello.order_row import SelloOrderRow
from src.views.my_base_view import MyBaseView


class SelloOrderRowView(SelloOrderRow, MyBaseView):
    def ask_questions(self):
        """Ask the questions we need"""
        print(f"Line: {self.title}, {self.image_url}")
        self.determine_quantity()
        self.determine_dolibarr_reference()
        # pprint(self.model_dump())

    def determine_quantity(self):
        quantity = self.ask_int(text="Enter quantity of products: (Enter = 1 or int)")
        if not quantity:
            # Default to 1
            quantity = 1
        self.quantity = quantity
        if self.quantity > 50:
            print(f"Quantity: {self.quantity} seems wrong, please enter quantity")
            self.quantity = self.ask_int(
                text="Enter quantity of products: (Enter = 1 or int)"
            )
        if self.quantity == 0:
            print(f"Quantity: {self.quantity} seems wrong, please enter quantity")
            self.quantity = self.ask_int(
                text="Enter quantity of products: (Enter = 1 or int)"
            )
        if self.quantity > 1:
            self.calculate_new_price_based_on_quantity()

    def determine_dolibarr_reference(self):
        """This is the product id in the Dolibarr database table"""
        if self.reference is not None and self.reference:
            return int(self.reference)
        else:
            self.reference = self.ask_mandatory(text="Enter dolibarr reference: (int)")
