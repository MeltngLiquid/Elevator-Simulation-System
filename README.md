# Elevator Simulator

A fun, college-level project that simulates elevator dispatch in a building using Python and Tkinter. Press buttons, watch the elevators move, and experiment with different scheduling strategies.

---

## 🚀 What’s Inside

* **Interactive GUI**: Click floor buttons to call elevators and see animations in real time.
* **Dispatch Algorithms**: Try the default heuristic or switch to a cost-based approach to compare wait times.
* **Performance Tracking**: Built-in counters show average wait time and total trips made.
* **Configurable**: Change number of floors, elevators, or the dispatch algorithm via a simple JSON or command-line flags.

---

## 👩‍💻 Getting Started

1. **Clone this repo**

   ```bash
   git clone https://github.com/yourusername/elevator-simulator.git
   cd elevator-simulator
   ```
2. **Set up a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # on Windows: venv\\Scripts\\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 Running the Simulation

Just run:

```bash
python main.py --config config.json
```

If you want to tweak settings, try:

```bash
python main.py --floors 15 --elevators 3 --algorithm cost
```

---

## 🎮 How to Use the GUI

1. **Launch the App**

   ```bash
   python main.py --config config.json
   ```

   When the window opens, you’ll see:

   * **Floor Panel** (left): rows of buttons labeled with floor numbers and arrow buttons to request up or down.
   * **Elevator Display** (center): each elevator shaft shows a colored block indicating the elevator’s current floor.
   * **Status Bar** (bottom): live updates of average wait time and total trips completed.

2. **Requesting an Elevator**

   * Click the **Up (▲)** or **Down (▼)** arrow next to the floor you are on. The arrow lights up to show your request is queued.
   * The scheduler dispatches an elevator—watch the colored block move to your floor.

3. **Selecting Your Destination**

   * Once the elevator arrives (the block stops at your floor), click the **floor number** button in the **Floor Panel** again to choose where you want to go.
   * The elevator will move to your chosen floor automatically.

4. **Watching the Ride**

   * Observe the elevator blocks slide smoothly between floors in real time.
   * The **Status Bar** updates after each ride, showing new average wait time and incremented trip count.

5. **Making Multiple Calls**

   * You can queue up several requests by clicking arrows on different floors; each request remains active until an elevator services it.
   * Active requests stay highlighted so you always know which calls are pending.

6. **Changing Settings on the Fly**

   * Press the **Settings** button in the menu bar to:

     * Adjust the number of floors or elevators without restarting.
     * Switch between dispatch strategies (e.g., default vs. cost-based).

---

## 🎬 Demo

* Check out a quick GIF in the `docs/` folder: `docs/demo.gif`

---

## 🗂️ Project Structure

```text
config.json       # Default settings for floors, elevators, etc.
main.py           # Starts up controllers and GUI
models.py         # Elevator and Building logic
gui.py            # Tkinter interface code
tests/            # Basic unit tests
```

---

## 📈 Metrics (Optional)

Run with the `--benchmark` flag to collect stats on average wait time and throughput.

---

### Enjoy!

Feel free to play around, read the code, and drop me an issue if you find bugs or have ideas to improve the scheduler. Great practice for learning threading, GUIs, and basic algorithms!
