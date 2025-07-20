# gui.py
import tkinter as tk
from tkinter import font as tkFont

class ElevatorSimulationView(tk.Tk):
    def __init__(self, controller, config):
        super().__init__()
        self.controller = controller
        self.config = config

        # --- UI Constants ---
        self.BG_COLOR = "#2B2B2B"
        self.FRAME_COLOR = "#3C3F41"
        self.TEXT_COLOR = "#BBBBBB"
        self.ACCENT_COLOR = "#007ACC"
        self.LIT_BUTTON_COLOR = "#FFD700"
        self.ELEVATOR_IDLE_COLOR = "#4CAF50"
        self.ELEVATOR_MOVING_COLOR = "#2196F3"

        # --- Fonts ---
        self.title_font = tkFont.Font(family="Segoe UI", size=12, weight="bold")
        self.label_font = tkFont.Font(family="Segoe UI", size=10, weight="bold")
        self.button_font = tkFont.Font(family="Segoe UI", size=9)

        # --- Window Setup ---
        self.title("Elevator Control System")
        self.configure(bg=self.BG_COLOR)
        win_height = self.config['num_floors'] * self.config['floor_height'] + 40
        win_width = self.config['building_width'] + 20
        self.geometry(f"{win_width}x{win_height}")
        self.resizable(False, False)

        # --- Data Structures for UI Elements ---
        self.destination_buttons = {}
        self.call_buttons = {}

        # --- Main Layout Assembly ---
        # CORRECTED: Changed 'main_frame' to 'self.main_frame'
        self.main_frame = tk.Frame(self, bg=self.BG_COLOR, padx=10, pady=10)
        self.main_frame.pack(fill="both", expand=True)

        dest_panel_0 = self.create_destination_panel(0)
        dest_panel_1 = self.create_destination_panel(1)
        self.canvas = tk.Canvas(self.main_frame, bg=self.FRAME_COLOR, highlightthickness=0)

        dest_panel_0.pack(side="left", fill="y", padx=(0, 10))
        dest_panel_1.pack(side="right", fill="y", padx=(10, 0))
        self.canvas.pack(side="left", fill="both", expand=True)

        self.draw_building_structure()
        self.create_floor_call_buttons()

    def create_destination_panel(self, elevator_id):
        panel = tk.Frame(self.main_frame, bg=self.FRAME_COLOR, relief="solid", bd=1)
        
        tk.Label(panel, text=f"Elevator {elevator_id}", font=self.title_font, bg=self.FRAME_COLOR, fg=self.TEXT_COLOR).pack(pady=(10, 5))
        self.destination_buttons[elevator_id] = {}
        
        btn_grid = tk.Frame(panel, bg=self.FRAME_COLOR)
        btn_grid.pack(pady=5, padx=10)

        num_floors = self.config['num_floors']
        for floor_num in range(num_floors):
            btn = tk.Button(btn_grid, text=str(floor_num), state="disabled", font=self.button_font,
                            bg="#555555", fg="white", relief="flat",
                            command=lambda e_id=elevator_id, f=floor_num: self.controller.select_destination(e_id, f))
            btn.grid(row=floor_num // 2, column=floor_num % 2, padx=4, pady=4, sticky="ew")
            self.destination_buttons[elevator_id][floor_num] = btn
        return panel

    def create_floor_call_buttons(self):
        num_floors = self.config['num_floors']
        button_x_pos = 35
        
        for i in range(num_floors):
            y_center = (num_floors - i - 0.5) * self.config['floor_height']
            
            if i < num_floors - 1:
                up_button = tk.Button(self.canvas, text="▲", font=self.label_font, relief="flat", bg="#555555", fg="white",
                                      command=lambda floor=i: self.controller.call_elevator(floor, 'up'))
                self.canvas.create_window(button_x_pos, y_center - 13, window=up_button, width=35)
                self.call_buttons[(i, 'up')] = up_button

            if i > 0:
                down_button = tk.Button(self.canvas, text="▼", font=self.label_font, relief="flat", bg="#555555", fg="white",
                                        command=lambda floor=i: self.controller.call_elevator(floor, 'down'))
                self.canvas.create_window(button_x_pos, y_center + 13, window=down_button, width=35)
                self.call_buttons[(i, 'down')] = down_button
    
    def draw_building_structure(self):
        self.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        num_floors = self.config['num_floors']

        for i in range(num_floors):
            y = (num_floors - i - 0.5) * self.config['floor_height']
            self.canvas.create_line(0, y - self.config['floor_height']/2, canvas_width, y - self.config['floor_height']/2, fill="#555555")
            self.canvas.create_text(75, y, text=str(i), font=self.label_font, fill=self.TEXT_COLOR)

    def update_all_views(self, elevators, pending_calls):
        self.canvas.delete("elevator")
        self._update_call_button_lights(pending_calls)
        for elevator in elevators:
            self._draw_elevator(elevator)
            self._update_destination_panel(elevator)

    def _draw_elevator(self, elevator):
        ELEVATOR_WIDTH = 50
        self.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        total_shafts_width = (ELEVATOR_WIDTH * self.config['num_elevators']) + (15 * (self.config['num_elevators'] - 1))
        start_x = ((canvas_width - total_shafts_width) / 2) + 20

        x0 = start_x + (ELEVATOR_WIDTH + 15) * elevator.id
        x1 = x0 + ELEVATOR_WIDTH
        y1 = (self.config['num_floors'] - elevator.current_floor) * self.config['floor_height']
        y0 = y1 - self.config['floor_height']
        
        fill_color = self.ELEVATOR_MOVING_COLOR if elevator.state == 'moving' else self.ELEVATOR_IDLE_COLOR
        
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline=self.ACCENT_COLOR, width=2, tags="elevator")
        
        direction = "▲ UP" if elevator.moving_up else "▼ DOWN"
        if elevator.state == 'idle': direction = "IDLE"
        
        status_text = f"Floor {elevator.current_floor}\n{direction}"
        self.canvas.create_text(x0 + ELEVATOR_WIDTH / 2, y0 + self.config['floor_height'] / 2,
                                text=status_text, fill="white", font=self.button_font, tags="elevator", justify='center')

    def _update_call_button_lights(self, pending_calls):
        for key, button in self.call_buttons.items():
            if key in pending_calls:
                button.config(bg=self.LIT_BUTTON_COLOR, fg="black")
            else:
                button.config(bg="#555555", fg="white")

    def _update_destination_panel(self, elevator):
        is_stopped = elevator.state != 'moving'
        for floor_num, button in self.destination_buttons[elevator.id].items():
            is_requested = floor_num in elevator.requests
            
            button.config(state="normal" if is_stopped else "disabled")

            if is_requested:
                button.config(bg=self.LIT_BUTTON_COLOR, fg="black")
            else:
                button.config(bg="#555555", fg="white")
            
            if floor_num == elevator.current_floor:
                button.config(bg=self.ACCENT_COLOR, state="disabled")

    def run(self):
        self.mainloop()