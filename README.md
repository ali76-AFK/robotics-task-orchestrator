# Robotics Task Orchestrator




Monorepo for a robotics task orchestration stack, including:

- `app/` – main application code (GUI, services, orchestration logic)
- `vla_service/` – vision–language–action (VLA) service integration
- `ros2_ws/` – ROS 2 workspace for robot control and perception (`src/orchestrator_demo`)
- `tests/` – integration and unit tests
- `src/`, `docker/`, `examples/`, `output/` – supporting code, containers, and examples

## Build & Run

The ROS 2 workspace is built inside Docker; do not build `ros2_ws` directly on the host.

Typical workflow:

```bash
# From repository root
# (exact commands depend on your docker setup; adjust as needed)
docker compose up --build
# or
./scripts/run_in_docker.sh
```

Inside the container:

```bash
cd /ws/ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch orchestrator_demo <your_launch>.launch.py
```

For the Python app / VLA service, see `app/` and `vla_service/` for entry points and scripts.

## Development

- Keep secrets out of the repo (use `.env` files, never commit tokens/keys).
- ROS build artifacts (`build/`, `install/`, `log/`) are gitignored.
- Use `tests/` for integration and unit tests.

## License

BSD-3-Clause (unless otherwise specified in subdirectories).
