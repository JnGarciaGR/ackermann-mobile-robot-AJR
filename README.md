# Ackermann Robot Trajectory & Odometry Controller Package (`ackermann_trajectory_controller`)

This repository contains the ROS 2 package for open-loop trajectory generation (organized into 4 stages with a total duration of 50 seconds) and automated odometry recording for an Ackermann-steered robot in the Gazebo simulation environment.

---

## 1. System Requirements & Environment

* **Operating System:** Ubuntu 26.04 LTS
* **Middleware:** ROS 2 Lyrical
* **Simulator:** Gazebo Harmonic (integrated via `ros_gz`)
* **Python Dependencies:**
  * `python3-matplotlib` (for comparative plotting)
  * `numpy` / `pandas` (optional)

---

## 2. Package Structure

```text
ackermann_trajectory_controller/
├── ackermann_trajectory_controller/
│   ├── __init__.py
│   ├── trajectory_publisher.py   # ROS 2 Node: publishes /cmd_vel (4 stages / 50 s)
│   └── odom_recorder.py         # ROS 2 Node: logs odometry to odom_data.csv
├── generate_plots.py            # Python Script: generates comparative plots (Reference vs /odom)
├── README.md                    # Package documentation & usage instructions
├── package.xml                  # ROS 2 package dependencies
└── setup.py                     # Build configuration and execution entry points (console_scripts)
```

---

## 3. Compilation & Build Instructions

Ensure this package is cloned or copied inside the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src/`).

1. **Navigate to the workspace root:**
   ```bash
   cd ~/ros2_ws
   ```

2. **Build the specific package:**
   ```bash
   colcon build --packages-select ackermann_trajectory_controller
   ```

3. **Source the environment variables:**
   ```bash
   source install/setup.bash
   ```

---

## 4. Step-by-Step Execution Guide

A full test run and data acquisition process requires three separate terminal windows:

### **Terminal 1: Launch Gazebo Simulation**
Loads the Ackermann robot model and simulation environment:
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 launch robot_ackermann_description gazebo.launch.py
```

### **Terminal 2: Start Odometry Logger**
Initiates data logging from the `/odom` topic into a `.csv` file:
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run ackermann_trajectory_controller odom_recorder
```
*Note: This node generates `odom_data.csv` in your current working directory.*

### **Terminal 3: Launch Trajectory Controller**
Publishes the motion command sequence (50.0 s total profile) to `/cmd_vel`:
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run ackermann_trajectory_controller trajectory_publisher
```

---

## 5. Controller Profile & Execution Stages (50 Seconds Total)

* **Stage 1 ($0.0\text{ s} \le t < 5.0\text{ s}$):** Initial straight-line motion with acceleration ramp ($0.0 \rightarrow 0.30\text{ m/s}$, $\omega_z = 0.0\text{ rad/s}$).
* **Stage 2 ($5.0\text{ s} \le t < 35.0\text{ s}$):** Harmonic figure-eight trajectory ($v_x = 0.25\text{ m/s}$, $\omega_z = \pm 0.45\text{ rad/s}$ with gain factor $k_{\text{left}}=1.10$).
* **Stage 3 ($35.0\text{ s} \le t < 45.0\text{ s}$):** Controlled deceleration ramp down to zero speed.
* **Stage 4 ($45.0\text{ s} \le t \le 50.0\text{ s}$):** Full rest and final pose stabilization ($v_x = 0.0\text{ m/s}$, $\omega_z = 0.0\text{ rad/s}$).

---

## 6. Data Analysis & Plot Generation

Once the trajectory completes ($50.0\text{ s}$ total duration), stop the logging node in **Terminal 2** using `Ctrl + C`.

1. Install the plotting library (if not already installed):
   ```bash
   sudo apt update
   sudo apt install python3-matplotlib
   ```

2. Run the script to process the CSV data and render the comparison plots:
   ```bash
   python3 generate_plots.py
   ```

### **Generated Artifacts:**
* **`odom_data.csv`:** Complete timestamped record (0 to 50 s) containing pose $(x, y, \theta)$ and dynamic velocity metrics.
* **`fig1_trajectory_xy.png`:** Comparative 2D path plot contrasting theoretical open-loop reference vs. recorded Gazebo odometry.
* **`fig2_position_error.png`:** Time-series plot of the Euclidean positioning error $e_p(t)$.

---

## 7. Authors & Credits

* **Package:** `ackermann_trajectory_controller`
* **Integration:** ROS 2 / Gazebo Harmonic
* **Date:** November 2026