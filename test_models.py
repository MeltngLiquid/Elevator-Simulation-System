import unittest
from models import Elevator, Building

class TestElevatorLogic(unittest.TestCase):

    def test_scan_algorithm_upward_trip(self):
        # SETUP: Create an elevator and add requests
        elevator = Elevator(0)
        elevator.add_request(5)
        elevator.add_request(9)
        
        # ACTION & ASSERTION
        # From floor 0, the next stop should be 5
        self.assertEqual(elevator.get_next_destination(), 5)
        
        # Simulate moving to floor 5
        elevator.current_floor = 5
        elevator.requests.remove(5)
        
        # From floor 5, the next stop should be 9
        self.assertEqual(elevator.get_next_destination(), 9)

    def test_dispatch_closest_idle_elevator(self):
        # SETUP: Create a building with two idle elevators
        building = Building(2)
        building.elevators[0].current_floor = 1
        building.elevators[1].current_floor = 8

        # ACTION: Dispatch an elevator to floor 7
        assigned_elevator = building.dispatch_elevator(7, 'up')

        # ASSERTION: It should have assigned Elevator 1, which is closer
        self.assertEqual(assigned_elevator.id, 1)

if __name__ == '__main__':
    unittest.main()