# Technology Research

Selection criteria (from the project brief): hardware compatibility, performance, scalability, and implementation feasibility.

---

## Part A: Robotics Middleware and Simulation

### A1. ROS 2 (Robot Operating System 2)

**What it is:** An open-source robotics middleware. It lets separate programs (nodes) such as vision, planning and motor control talk to each other through topics, services and actions.

**Why it fits this project:**
- Matches the modular brain design: each module becomes a node that can be developed and tested separately.
- Standard in the robotics industry, with a large library ecosystem (navigation, SLAM, arm control).
- Supports Python and C++, which are both named in the brief.
- Built on DDS, which supports real-time communication and security (authentication and encryption).
- Works directly with Gazebo for simulation.

**Limitations:**
- Best supported on Ubuntu Linux. On Windows, it is easier to use WSL2 or Docker.
- Steep learning curve at the start.

**Decision:** Use ROS 2 as the main communication backbone. Use a long-term-support (LTS) release, for example Jazzy on Ubuntu 24.04 or Humble on Ubuntu 22.04.

### A2. Gazebo

**What it is:** An open-source robot simulator with physics, sensor simulation (camera, LiDAR, IMU, GPS) and ROS 2 integration.

**Why it fits:**
- Free, and runs on a normal laptop.
- Simulates the sensors listed in the brief.
- Official integration with ROS 2 through bridge packages.
- Lets us demonstrate the full system without physical hardware.

**Limitations:**
- Graphics are less realistic than Isaac Sim.
- Large simulated worlds can be heavy on weak laptops.

**Decision:** Use Gazebo as the primary simulator.

### A3. NVIDIA Isaac (Isaac Sim / Isaac ROS)

**What it is:** NVIDIA's robotics platform with a photorealistic simulator (Isaac Sim) and GPU-accelerated ROS packages (Isaac ROS).

**Strengths:**
- Very realistic rendering, useful for training vision models with synthetic data.
- GPU acceleration for perception and SLAM.

**Limitations:**
- Needs a recent NVIDIA RTX GPU with plenty of VRAM, so it will not run on most student laptops.
- Heavy installation and setup.

**Decision:** Not used for the first prototype. Keep as a future upgrade if a suitable GPU or cloud GPU becomes available.

### A4. MQTT

**What it is:** A lightweight publish/subscribe messaging protocol for IoT devices.

**Where it fits:**
- Communication between the robot and the web dashboard.
- Communication between multiple robots and a central server.
- Low-bandwidth links where full ROS 2 networking is too heavy.

**Limitations:**
- Not a replacement for ROS 2 inside the robot. It is for outside connections.
- Needs a broker (for example Mosquitto) and TLS plus authentication to meet the security requirements.

**Decision:** Use ROS 2 inside the robot and MQTT (with TLS) between the robot and the dashboard or other robots.

### Part A Summary

| Technology | Role in the project | Decision |
|---|---|---|
| ROS 2 | Internal communication between modules | Use (core) |
| Gazebo | Simulation and testing | Use (primary simulator) |
| NVIDIA Isaac | High-fidelity simulation and GPU perception | Later, hardware permitting |
| MQTT | Robot-to-dashboard and multi-robot messaging | Use (with TLS) |

*Parts B (AI and perception: OpenCV, YOLO, PyTorch, TensorFlow, Whisper, LLMs) and C (navigation: SLAM and sensors) follow.*

---

## Part B: AI and Perception

### B1. OpenCV

**What it is:** An open-source computer vision library for image and video processing (capture, filtering, tracking, drawing).

**Why it fits:**
- Handles camera input, preprocessing and visualization for the vision module.
- Runs on CPU, so it works on any laptop.
- Python and C++ support, and it integrates with ROS 2 through cv_bridge.
- Useful for tracking, motion detection and basic hand and gesture pipelines.

**Limitations:** Classic OpenCV is not enough alone for accurate object detection. It is combined with a deep learning model.

**Decision:** Use as the base vision toolkit.

### B2. YOLO (You Only Look Once)

**What it is:** A family of real-time object detection models. Newer versions (for example Ultralytics YOLO) are easy to run, train and export.

**Why it fits:**
- Real-time detection of people, obstacles and objects, as the brief requires.
- Pretrained models are available, and custom training is simple.
- Small model sizes (nano and small) run on a CPU or a modest GPU.
- Supports detection, classification, segmentation and tracking.

**Limitations:**
- Speed depends on hardware. A CPU gives low frame rates with larger models.
- Check the license: Ultralytics YOLO uses AGPL-3.0, which matters for a commercial product. This must be reviewed before commercial use, and alternatives (such as models with permissive licenses) should be considered.

**Decision:** Use a small YOLO model for the prototype and flag the license question for the commercial stage.

### B3. PyTorch

**What it is:** A deep learning framework, widely used in research and in many production systems.

**Strengths:**
- Flexible and easy to debug. Most new models are released for PyTorch first.
- YOLO and Whisper are both built on or run through PyTorch.
- Good GPU support, with ONNX export for deployment.

**Decision:** Use as the main deep learning framework.

### B4. TensorFlow (and TensorFlow Lite)

**What it is:** Google's machine learning framework, strong in deployment, especially on mobile and embedded devices through TensorFlow Lite.

**Strengths:**
- TensorFlow Lite is useful on small hardware such as Raspberry Pi.
- Mature tools for deploying models.

**Limitations:**
- Having two frameworks adds complexity and doubles the maintenance work.

**Decision:** Not part of the core stack. Consider only if a specific model or edge device needs it. Models can often be converted through ONNX instead.

### B5. Whisper (speech recognition)

**What it is:** OpenAI's open-source speech-to-text model. It supports many languages and handles noisy audio reasonably well.

**Why it fits:**
- Multilingual speech recognition, as the brief requires.
- Runs locally, so there is no internet dependency and voice data stays on the device.
- Several sizes (tiny to large), so we can trade speed for accuracy.
- Faster implementations (such as faster-whisper) run well on a CPU.

**Limitations:**
- Not truly streaming by design. Real-time use needs short audio chunks and voice activity detection.
- Larger models need a GPU for low delay.

**Supporting components still needed:**
- Wake-word detection (for example openWakeWord or Porcupine)
- Voice activity detection (for example Silero VAD)
- Text-to-speech (for example Piper for offline use)
- Noise suppression (for example RNNoise)

**Decision:** Use Whisper (small or base size) for speech-to-text, with a separate wake-word model and VAD in front of it.

### B6. LLMs: APIs vs local models

| Option | Pros | Cons |
|---|---|---|
| LLM API (cloud) |

---

## Part C: Navigation, SLAM and Sensors

### C1. SLAM (Simultaneous Localization and Mapping)

**What it is:** The robot builds a map of an unknown space while tracking its own position inside that map.

| Option | Type | Notes |
|---|---|---|
| SLAM Toolbox | 2D LiDAR SLAM | Standard choice with ROS 2 and Nav2. Easy to set up, works well in simulation. |
| Cartographer | 2D/3D LiDAR SLAM | Accurate, but more complex to configure. |
| RTAB-Map | Visual / RGB-D SLAM | Uses camera or depth camera. Heavier on CPU. |
| ORB-SLAM3 | Visual SLAM | Camera-only, strong research tool, harder to integrate. |

**Decision:** Use SLAM Toolbox with a simulated 2D LiDAR for the prototype. Evaluate visual SLAM later if a LiDAR is not available on real hardware.

### C2. Autonomous Navigation (Nav2)

**What it is:** Nav2 is the standard ROS 2 navigation framework. It provides path planning, obstacle avoidance, recovery behaviors and map-based localization.

**Why it fits:**
- Covers autonomous navigation, movement planning, obstacle avoidance and recovery from the brief.
- Works with SLAM Toolbox and Gazebo out of the box.
- Supports restricted zones through "keepout" maps, which matches the requirement for restricted movement zones.
- Recovery behaviors (back up, spin, clear costmap) support autonomous recovery.

**Decision:** Use Nav2 as the navigation layer. The AI planner only sends goals such as "go to the kitchen" (a map position). Nav2 handles the actual path and obstacle avoidance.

### C3. Sensors and Sensor Fusion

| Sensor | Purpose | Typical hardware example |
|---|---|---|
| Ultrasonic | Short-range obstacle distance | HC-SR04 |
| LiDAR | 2D/3D mapping, obstacle detection | RPLIDAR A1 (budget 2D) |
| Infrared | Edge/cliff detection, close proximity | IR distance modules |
| Camera | Vision, object detection | USB camera, Raspberry Pi camera |
| Temperature | Hardware and environment monitoring | DHT22, DS18B20 |
| Pressure | Touch or grip feedback, environment | FSR, BMP280 |
| Motion | Presence detection | PIR sensor |
| Gyroscope and accelerometer (IMU) | Orientation and movement | MPU6050 and similar |
| GPS | Outdoor location | u-blox modules |

**Sensor fusion approach:**
- Combine wheel odometry and IMU with an Extended Kalman Filter (the `robot_localization` package in ROS 2) for a stable position estimate.
- Combine LiDAR, ultrasonic and camera detections into one obstacle picture (costmap) used by navigation and the safety layer.
- GPS is only useful outdoors, so it is optional for the indoor prototype.

**Hardware bridge:** Microcontrollers (Arduino, ESP32) read the sensors and drive the motors. They connect to ROS 2 through micro-ROS or a serial bridge. A **hardware-level emergency stop and limit check should live on the microcontroller**, so safety still works even if the main computer or AI fails.

**Decision:** Simulate LiDAR, camera, IMU and ultrasonic in Gazebo first. Treat real sensor hardware as a Phase 4 task.

### C4. Other Capabilities (research notes)

- **Object manipulation:** MoveIt 2 is the standard ROS 2 framework for robotic arm motion planning. Vision (YOLO) finds the object, and MoveIt plans the arm movement. A later-phase item.
- **Multi-robot coordination:** ROS 2 namespaces for robots on the same network, plus MQTT for communication with a central server. Nav2 and fleet-management tools can be explored later.
- **Predictive intelligence:** Start with simple methods: predict collisions from tracked obstacle velocity, and watch battery, temperature and motor-current trends for early warnings.
- **Adaptive learning:** Controlled feedback only: store human ratings or corrections of task results, and use them to improve prompts, rules or settings. No uncontrolled self-modification of safety behavior.

### Part C Summary

| Technology | Role | Decision |
|---|---|---|
| SLAM Toolbox | Mapping and localization | Use (2D LiDAR) |
| Nav2 | Path planning and obstacle avoidance | Use |
| robot_localization (EKF) | Sensor fusion | Use |
| micro-ROS / serial bridge | Connect microcontrollers to ROS 2 | Use in hardware phase |
| MoveIt 2 | Robotic arm planning | Later phase |

---

## Overall Research Conclusion

The recommended stack is ROS 2 and Gazebo (with Nav2 and SLAM Toolbox) for the robot and simulation, OpenCV and YOLO on PyTorch for vision, Whisper for speech, a swappable LLM planner, and MQTT with TLS for dashboard and multi-robot links. A separate safety layer sits between the AI planner and every hardware command. Full details are in `tech-stack.md` and `architecture.md`.