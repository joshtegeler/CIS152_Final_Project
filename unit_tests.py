import unittest
from main import Car, LinkedList, Inventory


class TestCar(unittest.TestCase):
    def test_car_representation(self):
        car = Car(2022, "Toyota", "Camry", 25000, "Sedan")
        self.assertEqual(repr(car), "2022 Toyota Camry - $25000 Sedan")

    def test_car_equality(self):
        car1 = Car(2022, "Toyota", "Camry", 25000, "Sedan")
        car2 = Car(2022, "Toyota", "Camry", 25000, "Sedan")
        self.assertEqual(car1, car2)

        car3 = Car(2021, "Honda", "Accord", 28000, "Sedan")
        self.assertNotEqual(car1, car3)


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.linked_list = LinkedList()

    def test_add_node(self):
        car1 = Car(2022, "Toyota", "Camry", 25000, "Sedan")
        car2 = Car(2021, "Honda", "Accord", 28000, "Sedan")

        self.linked_list.add_node(car1)
        self.assertEqual(self.linked_list.head.car, car1)

        self.linked_list.add_node(car2)
        self.assertEqual(self.linked_list.head.car, car2)
        self.assertEqual(self.linked_list.head.next_node.car, car1)

    def test_get_sorted_inventory(self):
        car1 = Car(2022, "Toyota", "Camry", 25000, "Sedan")
        car2 = Car(2021, "Honda", "Accord", 28000, "Sedan")
        car3 = Car(2023, "Ford", "Mustang", 35000, "Coupe")

        self.linked_list.add_node(car1)
        self.linked_list.add_node(car2)
        self.linked_list.add_node(car3)

        sorted_inventory = self.linked_list.get_sorted_inventory("Year (Low to High)")
        self.assertEqual(sorted_inventory, [car2, car1, car3])


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()

    def test_add_car(self):
        car = Car(2022, "Toyota", "Camry", 25000, "Sedan")
        self.inventory.add_car(car)
        self.assertEqual(len(self.inventory.get_inventory()), 1)
        self.assertEqual(self.inventory.get_inventory()[0], car)

    def test_remove_car(self):
        car = Car(2022, "Toyota", "Camry", 25000, "Sedan")
        self.inventory.add_car(car)
        removed_car = self.inventory.remove_car(0)
        self.assertEqual(removed_car, car)
        self.assertEqual(len(self.inventory.get_inventory()), 0)


if __name__ == '__main__':
    unittest.main()
