# main.py
import json
import logging
from models import Building
from gui import ElevatorSimulationView

class SimulationController:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        self.building = Building(self.config['num_elevators'])
        self.view = ElevatorSimulationView(self, self.config)
        
        logging.info("Elevator Control System Initialized.")
        self.update_simulation()

    def call_elevator(self, floor_number, direction):
        logging.info(f"Call button pressed on floor {floor_number} for direction '{direction}'")
        self.building.dispatch_elevator(floor_number, direction)

    def select_destination(self, elevator_id, destination_floor):
        elevator = self.building.elevators[elevator_id]
        if elevator.current_floor == destination_floor: return
        elevator.add_request(destination_floor)
        logging.info(f"Elevator {elevator_id} destination set for floor {destination_floor}")

    def update_simulation(self):
        # NEW: A flag to check if a pickup just occurred in this cycle
        pickup_occurred = False

        for elevator in self.building.elevators:
            destination = elevator.get_next_destination()
            if destination is not None:
                if elevator.current_floor != destination:
                    elevator.move_towards(destination)
                else: 
                    logging.info(f"Elevator {elevator.id} arrived at floor {elevator.current_floor}.")
                    elevator.requests.remove(destination)
                    
                    current_floor = elevator.current_floor
                    up_call = (current_floor, 'up')
                    down_call = (current_floor, 'down')

                    # Check if this arrival was for a pending call
                    if up_call in self.building.pending_calls or down_call in self.building.pending_calls:
                        pickup_occurred = True # Set the flag
                        self.building.pending_calls.discard(up_call)
                        self.building.pending_calls.discard(down_call)
        
        # Pass the building's pending_calls to the view for button lighting
        self.view.update_all_views(self.building.elevators, self.building.pending_calls)
        
        # --- CHANGED: The timing logic is now corrected ---
        any_moving = any(e.state == 'moving' for e in self.building.elevators)
        
        if pickup_occurred:
            # If a pickup just happened, pause for the configured idle time
            delay_ms = int(self.config['idle_time_sec'] * 1000)
        elif any_moving:
            # If elevators are moving, update at elevator speed
            delay_ms = int(self.config['elevator_speed_sec'] * 1000)
        else:
            # If idle, poll for new requests every so often
            delay_ms = 200

        self.view.after(delay_ms, self.update_simulation)

    def start(self):
        self.view.run()

if __name__ == "__main__":
    controller = SimulationController('config.json')
    controller.start()