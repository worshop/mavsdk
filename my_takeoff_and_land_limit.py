#!/usr/bin/env python3

import asyncio
from mavsdk import System

target_altitude = 50.0  # 착륙을 위한 목표 고도

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone connected!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("Global position estimate ok")
            break

    print("Arming")
    await drone.action.arm()

    print("Setting takeoff altitude")
    await drone.action.set_takeoff_altitude(target_altitude)

    print("Taking off")
    await drone.action.takeoff()

    print("Checking altitude")
    async for position in drone.telemetry.position():
        if position.relative_altitude_m > target_altitude:
            print("Reached target altitude, landing now")
            await drone.action.land()
            break

if __name__ == "__main__":
    asyncio.run(run())
