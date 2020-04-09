import numpy as np
import random
import time
import cv2
from data_wrangling import trans_prob_matrix, initial_state_vector


class SupermarketCustomer:
    """Blueprint for customers moving through a store"""

    def __init__(self, prob_matrix, initial_state_array, image, state_space=['dairy', 'fruit', 'drinks', 'spices'], speed=1):
        self.prob_matrix = prob_matrix
        self.image = image
        self.image[:,:,0] = random.randint(1, 255)
        #print('Random colours', self.image)
        self.image[:,:,1] = random.randint(1, 255)
        self.image[:,:,2] = random.randint(1, 255)
        self.state_space = state_space
        self.initial_state_array = initial_state_array
        self.current_location = [650, random.randint(680, 880)]
        # to start with: returns the first aisle with initial_state_array
        self.target_aisle = np.random.choice(self.state_space, p=self.initial_state_array)
        self.ty, self.tx = self.get_coord(self.target_aisle)
        self.speed = speed
        self.counter = 0
        self.counter2 = 0

    def get_coord(self, aisle):
        if aisle == 'drinks':
            ty, tx = [random.randint(135, 435), random.randint(65, 175)]
        elif aisle == 'dairy':
            ty, tx = [random.randint(135, 435), random.randint(295, 405)]
        elif aisle == 'spices':
            ty, tx = [random.randint(135, 435), random.randint(535, 645)]
        elif aisle == 'fruit':
            ty, tx = [random.randint(135, 435), random.randint(755, 865)]
        elif aisle == 'checkout':
            ty, tx = [555, random.choice([100, 250, 400, 540])]

        return ty, tx

    def next_target(self, aisle):

        aisle_probas = self.prob_matrix.loc[aisle]
        self.target_aisle = np.random.choice(aisle_probas.index, p=aisle_probas.values)
        self.ty, self.tx = self.get_coord(self.target_aisle)



    def move(self):

        y, x = self.current_location

        #print(self.current_location)
        #print(self.ty, self.tx)


        if self.ty == 555:
            if y == self.ty and x == self.tx:
                if self.counter < 100:
                    self.counter += 1
                    self.image = np.zeros((15, 15, 3),dtype=np.uint8)
                    self.image[:,:,2] = 255
                elif self.counter == 100:
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

        elif x == self.tx and y == self.ty:
            self.next_target(self.target_aisle)


        elif x != self.tx:
            if y > 450:
                if self.tx > x:
                    self.current_location[0] -= self.speed # go up
                    print(1, self.ty, self.tx)
                elif self.tx < x:
                    self.current_location[0] -= self.speed # go up
                    print(2, self.ty, self.tx)


            elif y == 450:
                if self.tx > x:
                    self.current_location[1] += self.speed # go right
                    print(3)
                elif self.tx < x:
                    #print('xtarget', self.tx)
                    #print(self.current_location)
                    self.current_location[1] -= self.speed # go left
                    print(4)

            elif y == 100:
                if self.tx > x:
                    self.current_location[1] += self.speed  # go right

                elif self.tx < x:
                    self.current_location[1] -= self.speed # go left

            elif y > 100:
                if abs(100 - y) < abs(450 - y):  # go up
                    self.current_location[0] -= self.speed
                else: # go down
                    self.current_location[0] += self.speed


        elif x == self.tx:

            if y == 100:
                self.current_location[0] += self.speed  # go down

            elif y < 450:
                if y > 100:
                    if self.ty < y:
                        self.current_location[0] -= self.speed  # go up
                        print(5)
                    elif self.ty > y:
                        self.current_location[0] += self.speed  # go down

            elif y == 450:
                self.current_location[0] -= self.speed  # go up
                print(6)



        # returns: updated self.current_location


class Supermarket:
    """create customers at different times and let them journey through the supermarket"""
    def __init__(self, market_image, customers):
        self.market_image = market_image
        self.customers = customers
        #self.frame = market_image


    def draw(self):  # creating new image for every step taken

        self.frame = self.market_image.copy()
        #print('frame',self.frame.shape)
        for customer in customers:
            #get current_location

            y, x = customer.current_location
            print('current location', customer.current_location)
            print('target', customer.ty, customer.tx)
            #print('test',self.frame[y:y+6,x:x+5,:].shape)
            #print('customerH', self.frame[y:y+customer.h, x:x+customer.w, :].shape)
            #print('frame',self.frame[y:y+customer.h, x:x+customer.w, :])
            self.frame[y:y+15, x:x+15, :] = customer.image



if __name__ == '__main__':
    customer_image = np.zeros((15, 15, 3), dtype=np.uint8)
    supermarket_image = cv2.imread('market.png')
    #supermarket_image.shape (675, 943, 3)

 # create the instances, they don't do anything yet
    customers = []
    for _ in range(10):
        customers.append(SupermarketCustomer(trans_prob_matrix, initial_state_vector, customer_image))


    simulation = Supermarket(supermarket_image, customers)

    #for customer in customers:
    #    test = customer.next_target()
        #print('targets', customer.tx, customer.ty, test)


    while True:
        simulation.draw()
        for customer in customers:
            customer.move()


        cv2.imshow('frame', simulation.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  #stops if q is pressed
            break


    cv2.destroyAllWindows()
