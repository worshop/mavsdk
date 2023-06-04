#!/usr/bin/env python3
# 파이썬3 인터프리터를 사용하여 스크립트를 실행하라는 셔뱅(#!) 라인입니다.

import asyncio
# asyncio는 비동기 I/O를 지원하는 라이브러리입니다. 
# 이 라이브러리를 통해 드론의 동시적인 행동(예: 상태 감시, 이동 명령 등)을 수행할 수 있습니다.

from mavsdk import System
# MAVSDK는 드론과 통신하기 위한 API입니다. System 클래스는 드론을 나타냅니다.

async def run():
# 비동기 함수 run을 정의합니다.

    drone = System()
    # 드론 객체를 생성합니다.
    await drone.connect(system_address="udp://:14540")
    # 드론에 연결을 시도합니다. 이 연결은 비동기적으로 이루어집니다.

    status_text_task = asyncio.ensure_future(print_status_text(drone))
    # 드론의 상태 메시지를 출력하는 태스크를 생성하고 시작합니다.

    print("Waiting for drone to connect...")
    # 드론 연결을 기다린다는 메시지를 출력합니다.
    async for state in drone.core.connection_state():
        # 드론의 연결 상태를 비동기적으로 조회합니다.
        if state.is_connected:
            print(f"-- Connected to drone!")
            # 연결되었음을 알립니다.
            break

    print("Waiting for drone to have a global position estimate...")
    # 드론이 글로벌 위치를 파악하도록 기다린다는 메시지를 출력합니다.
    async for health in drone.telemetry.health():
        # 드론의 상태를 비동기적으로 조회합니다.
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            # 글로벌 위치 파악이 완료되었음을 알립니다.
            break

    print("-- Arming")
    # 드론이 이륙 준비를 한다는 메시지를 출력합니다.
    await drone.action.arm()
    # 드론에게 이륙 준비를 하라는 명령을 보냅니다.

    print("-- Taking off")
    # 드론이 이륙한다는 메시지를 출력합니다.
    await drone.action.takeoff()
    # 드론에게 이륙하라는 명령을 보냅니다.

    await asyncio.sleep(10)
    # 드론이 10초 동안 비행하도록 합니다.

    print("-- Landing")
    # 드론이 착륙한다는 메시지를 출력합니다.
    await drone.action.land()
    # 드론에게 착륙하라는 명령을 보냅니다.

    status_text_task.cancel()
    # 상태 메시지 출력 태스크를 취소합니다.

async def print_status_text(drone):
    # 드론의 상태 메시지를 출력하는 비동기 함수를 정의합니다.
    try:
        async for status_text in drone.telemetry.status_text():
            # 드론의 상태 메시지를 비동기적으로 받아옵니다.
            print(f"Status: {status_text.type}: {status_text.text}")
            # 상태 메시지를 출력합니다.
    except asyncio.CancelledError:
        # 상태 메시지 출력이 취소되면 이를 무시하고 종료합니다.
        return

if __name__ == "__main__":
    # 스크립트가 직접 실행되었을 때만, 아래 코드를 실행합니다.
    # Run the asyncio loop
    asyncio.run(run())
    # 비동기 함수 run을 실행합니다. 이 함수가 종료될 때까지 기다립니다.
