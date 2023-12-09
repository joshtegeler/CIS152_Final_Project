import csv
from collections import deque


class Car:
    def __init__(self, year, make, model, price, description):
        self.year = year
        self.make = make
        self.model = model
        self.price = price
        self.description = description

    def __repr__(self):
        return f"{self.year} {self.make} {self.model} - ${self.price} {self.description}"


class Node:
    def __init__(self, car, next_node=None):
        self.car = car
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, car):
        # Add new node
        new_node = Node(car, next_node=self.head)
        self.head = new_node

    def pop(self, index):
        if self.head is None:
            return None

        if index == 0:
            removed_car = self.head.car
            self.head = self.head.next_node
            return removed_car

        current = self.head
        previous = None
        count = 0

        while current is not None and count < index:
            previous = current
            current = current.next_node
            count += 1

        if current is None:
            return None

        removed_car = current.car
        previous.next_node = current.next_node

        return removed_car

    # Placeholder method
    def get_sorted_inventory(self, sorting_key):
        pass

    def update_car(self, index, updated_car):
        # Update car at specified index
        current = self.head
        count = 0

        while current:
            if count == index:
                current.car = updated_car
                return
            current = current.next_node
            count += 1

        raise IndexError("Index out of range. Unable to update car.")


class Inventory:
    def __init__(self, file_path='inventory.csv'):
        self.file_path = file_path
        self.inventory = LinkedList()

    def add_car(self, car):
        # Add car to inventory
        self.inventory.add_node(car)
        self.organize_inventory()
        # Save data to a file
        self.save_data()

    def remove_car(self, index):
        # Remove car from inventory
        removed_car = self.inventory.pop(index)
        self.save_data()
        return removed_car

    def organize_inventory(self):
        # Sort year by descending
        sorted_cars = sorted(self.get_inventory(), key=lambda car: (car.year, car.price), reverse=True)
        self.inventory.head = None
        for car in sorted_cars:
            self.inventory.add_node(car)

    def load_data(self):
        # Load the car data from CSV file into inventory
        try:
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    year, make, model, price, description = row
                    car = Car(int(year), make, model, int(price), description)
                    self.inventory.add_node(car)
        except FileNotFoundError:
            # Handle file not existing
            pass

    def save_data(self):
        # Save the inventory into CSV file
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for car in self.get_inventory():
                writer.writerow([car.year, car.make, car.model, car.price, car.description])

    def get_inventory(self):
        # Return the cars in the inventory
        inventory_list = []
        current = self.inventory.head
        while current is not None:
            inventory_list.append(current.car)
            current = current.next_node
        return inventory_list
