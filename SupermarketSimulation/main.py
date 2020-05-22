import numpy as np
import random
import cv2
from data_wrangling import trans_prob_matrix, initial_state_vector
from market_class import Supermarket

class SupermarketCustomer:
    """Blueprint for customers moving through a store"""

    def __init__(self, prob_matrix, initial_state_array, image, state_space=['dairy', 'fruit', 'drinks', 'spices']):
        self.prob_matrix = prob_matrix
        self.image = image
        self.image[:,:,0] = random.randint(1, 255)
        self.image[:,:,1] = random.randint(1, 255)
        self.image[:,:,2] = random.randint(1, 255)
        self.state_space = state_space
        self.initial_state_array = initial_state_array
        self.current_location = [650, random.randint(680, 880)]
        self.target_aisle = np.random.choice(self.state_space, p=self.initial_state_array)
        self.ty, self.tx = self.get_coord(self.target_aisle)
        self.speed = 1
        self.counter = 0
        self.counter2 = 0


    def get_coord(self, aisle):
        """turning aisles into coordinates in the supermarket"""

        if aisle == 'drinks':
            ty, tx = [random.randint(135, 435), random.randint(65, 175)]
        elif aisle == 'dairy':
            ty, tx = [random.randint(135, 435), random.randint(295, 405)]
        elif aisle == 'spices':
            ty, tx = [random.randint(135, 435), random.randint(535, 640)]
        elif aisle == 'fruit':
            ty, tx = [random.randint(135, 435), random.randint(755, 865)]
        elif aisle == 'checkout':
            ty, tx = [555, random.choice([100, 250, 400, 535])]
        return ty, tx


    def next_target(self, aisle):
        """calculating the next aisle with the probability matrix and
        setting target coordinates to new values"""

        aisle_probas = self.prob_matrix.loc[aisle]
        self.target_aisle = np.random.choice(aisle_probas.index, p=aisle_probas.values)
        self.ty, self.tx = self.get_coord(self.target_aisle)


    def move(self):
        """ Moving a customer through the supermarket"""

        y, x = self.current_location

        # if target is checkout:
        if self.ty == 555:
            if y == self.ty and x == self.tx:
                if self.counter < 150:
                    self.counter += 1
                    self.image = np.zeros((15, 15, 3),dtype=np.uint8)
                    self.image[:,:,2] = 255
                elif self.counter == 150:
                    self.image = np.zeros((15,15,3), dtype=np.uint8)
                    self.image[:,:,0:3] = 255
                    if self.counter2 == 0:
                        customers.append(SupermarketCustomer(trans_prob_matrix, initial_state_vector, customer_image))
                        self.counter2 +=1
            elif y < 470:
                self.current_location[0] += self.speed # go down
            elif y >= 470:
                if  x == self.tx:
                    self.current_location[0] += self.speed # go down
                elif x > self.tx:
                    self.current_location[1] -= self.speed # go left
                elif x < self.tx:
                    self.current_location[1] += self.speed # go right
            elif y < 555:
                self.current_location[0] += self.speed # go down

        # if goal-aisle is reached:
        elif x == self.tx and y == self.ty:
            self.next_target(self.target_aisle)

        # if customer is not exactly under/over target x
        elif x != self.tx:
            if y > 450:
                if self.tx > x:
                    self.current_location[0] -= self.speed # go up
                elif self.tx < x:
                    self.current_location[0] -= self.speed # go up
            elif y == 450:
                if self.tx > x:
                    self.current_location[1] += self.speed # go right
                elif self.tx < x:
                    self.current_location[1] -= self.speed # go left
            elif y == 100:
                if self.tx > x:
                    self.current_location[1] += self.speed  # go right
                elif self.tx < x:
                    self.current_location[1] -= self.speed # go left
            elif y > 100:
                if abs(100 - y) < abs(450 - y):
                    self.current_location[0] -= self.speed # go up
                else:
                    self.current_location[0] += self.speed # go down

        # if customer is right under/over target x
        elif x == self.tx:
            if y == 100:
                self.current_location[0] += self.speed  # go down
            elif y < 450:
                if y > 100:
                    if self.ty < y:
                        self.current_location[0] -= self.speed  # go up
                    elif self.ty > y:
                        self.current_location[0] += self.speed  # go down
            elif y == 450:
                self.current_location[0] -= self.speed  # go up



if __name__ == '__main__':

    print("Please enter how many customers are allowed in the supermarket at the same time:")
    number_customers = input()

    customer_image = np.zeros((15, 15, 3), dtype=np.uint8)
    supermarket_image = cv2.imread('market.png')

    #creating customer-instances:
    customers = []
    for _ in range(int(number_customers)):
        customers.append(SupermarketCustomer(trans_prob_matrix, initial_state_vector, customer_image))

    # creating supermarket-instance:
    simulation = Supermarket(supermarket_image, customers)

    # repeated drawing of the supermarket and moving of customers
    while True:
        simulation.draw(customers)
        for customer in customers:
            customer.move()

        cv2.imshow('frame', simulation.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  #stops if q is pressed
            break

    cv2.destroyAllWindows()
