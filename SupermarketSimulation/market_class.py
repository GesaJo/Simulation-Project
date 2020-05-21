
class Supermarket:
    """Let customers journey through the supermarket"""

    def __init__(self, market_image, customers):
        self.market_image = market_image
        self.customers = customers


    def draw(self, customers):
        """ Draws the supermarket with customer locations"""

        self.frame = self.market_image.copy()
        for customer in customers:
            y, x = customer.current_location
            self.frame[y:y+15, x:x+15, :] = customer.image
