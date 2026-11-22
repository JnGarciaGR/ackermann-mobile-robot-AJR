# Mechanical Design

## III. MECHANICAL DESIGN

### A. Design Approach

The robot was designed in Autodesk Fusion 360 as a compact, rear-wheel-drive, front-steered vehicle with Ackermann kinematics. The design goal was a simple, simulation-oriented geometry: few parts, exact dimensions and realistic mass properties, so that the model can be exported to URDF/Xacro without manual corrections and simulated in Gazebo.

All parts were modeled top-down in a single hybrid design: each part was created in its final assembly position, and the global origin was used as the robot reference frame. The main dimensions were defined as Fusion 360 *user parameters*, so the geometry can be changed consistently from one table. The robot frame (`base_link`) follows the ROS convention (REP 103): origin at the center of the rear axle, at ground level, with +X pointing forward, +Y to the left and +Z upward.

### B. Design Parameters

TABLE I. Design parameters

| Parameter | Symbol | Value |
|---|---|---|
| Wheelbase | *L* | 300 mm |
| Track width (wheel center to wheel center) | *W* | 220 mm |
| Kingpin (steering pivot) distance | *d* | 160 mm |
| Wheel diameter × width | — | 100 × 30 mm |
| Wheel radius | *r* | 50 mm |
| Axle height above ground | — | 50 mm |
| Maximum vehicle steering angle | δ<sub>max</sub> | 30° (0.524 rad) |
| Steering joint limit (each knuckle) | — | ±35° (±0.611 rad) |
| Minimum turning radius (rear-axle center) | *R*<sub>min</sub> | 0.52 m |
| Chassis plate (length × width × thickness) | — | 400 × 110 × 6 mm |
| Total mass | *m* | ≈ 1.83 kg |

### C. Components

The robot has three distinct parts, assembled into seven components.

1) **Chassis (`base_link`).** A 400 × 110 × 6 mm aluminum 6061 plate placed at axle height. At the rear it carries two support blocks with Ø8 mm stub axles for the rear wheels. At the front it carries two clevis brackets (a vertical wall plus upper and lower tabs) that hold the steering knuckles. Each clevis has a Ø6.5 mm vertical bore for the Ø6 mm kingpin. The plate width (110 mm) was chosen so that the front wheels clear the chassis over the full steering range.

2) **Wheels (×4).** Ø100 × 30 mm rubber wheels with a Ø8.5 mm axle bore and four Ø14 mm lightening holes. Besides reducing mass, the holes make wheel rotation visible in the simulation. Each wheel is a separate component, because the exporter maps one component to one URDF link.

3) **Steering knuckles (×2, mirrored).** A 20 × 20 × 30 mm aluminum block that fits between the clevis tabs with 1 mm of vertical play. It carries:
   - a vertical Ø6 mm kingpin;
   - a horizontal Ø8 mm spindle for the front wheel;
   - a 30 mm steering arm pointing toward the center of the rear axle, which forms the Ackermann trapezoid. The arm ends in a Ø3 mm hole for a tie rod.

All rotating interfaces include a 0.5 mm diametral clearance (Ø6/Ø6.5 at the kingpin and Ø8/Ø8.5 at the axles). This avoids spurious contacts between adjacent links in the physics engine.

### D. Ackermann Steering Geometry

For a given turning radius *R*, measured to the center of the rear axle, the virtual (bicycle-model) steering angle is

δ = arctan(*L* / *R*).   (1)

To avoid tire slip, the inner and outer front wheels must steer about the same instantaneous center of rotation:

δ<sub>i</sub> = arctan( *L* / (*R* − *d*/2) ),   δ<sub>o</sub> = arctan( *L* / (*R* + *d*/2) ).   (2)

With *L* = 0.30 m, *d* = 0.16 m and δ<sub>max</sub> = 30°, (1) gives *R*<sub>min</sub> = 0.52 m, and (2) gives δ<sub>i</sub> = 34.3° and δ<sub>o</sub> = 26.6°. For this reason, the steering joint limits were set to ±35° even though the vehicle steering limit is 30°.

The steering arms are aligned with the line from each kingpin to the center of the rear axle (14.9° inward), which is the classical Ackermann trapezoid. The tie rod that would close this four-bar linkage is not modeled, because URDF only supports tree-shaped (open-chain) kinematics. In simulation, the Gazebo `AckermannSteering` system commands each steering joint with the angles in (2).

### E. Kinematic Structure (URDF)

The assembly was defined with six revolute joints in Fusion 360. TABLE II lists them as exported to URDF.

TABLE II. Joints of the model

| Joint | Parent → child | URDF type | Axis | Origin (m) |
|---|---|---|---|---|
| `rear_left_wheel_joint` | `base_link` → rear left wheel | continuous | +Y | (0, 0.11, 0.05) |
| `rear_right_wheel_joint` | `base_link` → rear right wheel | continuous | +Y | (0, −0.11, 0.05) |
| `front_left_steer_joint` | `base_link` → left knuckle | revolute, ±0.611 rad | +Z | (0.30, 0.08, 0.05) |
| `front_right_steer_joint` | `base_link` → right knuckle | revolute, ±0.611 rad | +Z | (0.30, −0.08, 0.05) |
| `front_left_wheel_joint` | left knuckle → front left wheel | continuous | +Y | (0, 0.03, 0) |
| `front_right_wheel_joint` | right knuckle → front right wheel | continuous | +Y | (0, −0.03, 0) |

The rear wheels are the driven wheels and the front wheels roll freely, so the drive is rear-wheel only.

### F. Mass Properties

A physical material was assigned to each body (aluminum 6061 for the chassis and knuckles, rubber for the wheels). Fusion 360 computed the mass, center of mass and inertia tensor of every link, and these values were exported directly into the URDF (TABLE III).

TABLE III. Mass properties (inertia about the center of mass)

| Link | Material | Mass (kg) | I<sub>xx</sub>, I<sub>yy</sub>, I<sub>zz</sub> (kg·m²) |
|---|---|---|---|
| `base_link` (chassis) | Al 6061 | 0.950 | 1.86e-3, 1.46e-2, 1.64e-2 |
| Wheel (each, ×4) | Rubber | 0.200 | 1.45e-4, 2.60e-4, 1.45e-4 |
| Steering knuckle (each, ×2) | Al 6061 | 0.041 | 8e-6, 5e-6, 7e-6 |
| **Total** | | **≈ 1.83** | |

### G. Range-of-Motion and Interference Verification

Fusion 360's interference analysis was run on all seven components with the steering at 0°, ±20° and ±35°, and no interferences were found in any position. At the ±35° joint limit, the minimum clearances computed from the geometry are:
- wheel to chassis: 8.6 mm;
- wheel to clevis tab: 3.4 mm;
- knuckle to chassis: 10.9 mm.

### H. Export to URDF/Xacro

The model was exported with the open-source Fusion 360 add-in *fusion360-urdf-ros2*, which targets ROS 2 Humble/Jazzy. The design follows the exporter's rules:
- every link is a top-level component that contains only bodies;
- the root link is named `base_link`;
- each joint is defined with the child as Component 1 and the parent as Component 2;
- revolute joints with both limits become `revolute`, and revolute joints without limits become `continuous`.

Meshes are exported as STL in millimeters, with a 0.001 scale factor in the URDF.

The generated package (`robot_ackermann_description`) contains the Xacro description, the meshes, and launch files for RViz2 and Gazebo Harmonic. For simulation with ROS 2 Jazzy and Gazebo Harmonic, the following changes were made:
1) the wheel friction coefficient was raised from 0.2 to 1.0 to avoid wheel slip;
2) self-collision was disabled;
3) the `gz::sim::systems::AckermannSteering` system was added with the parameters in TABLE I (wheel_base 0.30 m, wheel_separation 0.22 m, kingpin_width 0.16 m, wheel_radius 0.05 m, steering_limit 0.524 rad), together with a joint-state publisher;
4) the `/cmd_vel`, `/odom`, `/tf`, `/joint_states` and `/clock` topics were bridged between ROS 2 and Gazebo.
