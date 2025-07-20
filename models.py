# models.py

class Elevator:
    """Manages the state of a single elevator."""
    def __init__(self, elevator_id):
        self.id = elevator_id
        self.current_floor = 0
        self.requests = set()
        self.moving_up = True
        self.state = 'idle'

    def add_request(self, floor_number):
        self.requests.add(floor_number)

    def get_next_destination(self):
        if not self.requests:
            self.state = 'idle'
            return None

        self.state = 'moving'
        if self.moving_up:
            up_requests = {f for f in self.requests if f >= self.current_floor}
            if up_requests:
                return min(up_requests)
            else:
                self.moving_up = False
                return max(self.requests) if self.requests else None
        else: # moving down
            down_requests = {f for f in self.requests if f <= self.current_floor}
            if down_requests:
                return max(down_requests)
            else:
                self.moving_up = True
                return min(self.requests) if self.requests else None

    def move_towards(self, destination_floor):
        if self.current_floor < destination_floor:
            self.current_floor += 1
        elif self.current_floor > destination_floor:
            self.current_floor -= 1

class Building:
    """Manages all elevators and handles call dispatching."""
    def __init__(self, num_elevators):
        self.elevators = [Elevator(i) for i in range(num_elevators)]
        self.pending_calls = set()

    def dispatch_elevator(self, call_floor, direction):
        if (call_floor, direction) in self.pending_calls:
            return None

        self.pending_calls.add((call_floor, direction))

        best_elevator = None
        perfect_matches = []
        for e in self.elevators:
            if e.state == 'moving':
                if direction == 'up' and e.moving_up and e.current_floor <= call_floor:
                    perfect_matches.append(e)
                elif direction == 'down' and not e.moving_up and e.current_floor >= call_floor:
                    perfect_matches.append(e)
        
        if perfect_matches:
            min_dist = float('inf')
            for e in perfect_matches:
                dist = abs(e.current_floor - call_floor)
                if dist < min_dist:
                    min_dist = dist
                    best_elevator = e
            if best_elevator:
                best_elevator.add_request(call_floor)
                return best_elevator # CHANGED: Added return statement

        idle_elevators = [e for e in self.elevators if e.state == 'idle']
        if idle_elevators:
            min_dist = float('inf')
            for e in idle_elevators:
                dist = abs(e.current_floor - call_floor)
                if dist < min_dist:
                    min_dist = dist
                    best_elevator = e
            if best_elevator:
                best_elevator.add_request(call_floor)
                return best_elevator # CHANGED: Added return statement

        best_elevator = min(self.elevators, key=lambda e: len(e.requests))
        best_elevator.add_request(call_floor)
        return best_elevator # CHANGED: Added return statement