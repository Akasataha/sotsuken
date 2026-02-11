import asyncio
from python_sub.gpio import GpioManager
from python_sub.task import TaskManager
from python_sub.julius import Process
from python_sub.distance import DistanceSensor
from python_sub.motors import Motors


async def main():

    gpioM = GpioManager()
    pi = gpioM.pi
    taskM = TaskManager()
    processM = Process()
    motors = Motors(pi=pi)
    distance = DistanceSensor(pi=pi, trig=14, echo=15)
    dist_queue = asyncio.Queue()
    taskM.start("julius", processM.read_process())
    taskM.start("motor", motors.loop_task())
    taskM.start("command", motors.command_loop(processM.queue))
    taskM.start("distance_sensor", distance.loop(dist_queue))
    taskM.start("distance_watch", motors.distance_watcher(dist_queue))
    taskM.start("debug", motors.debug())

    try:
        await asyncio.Event().wait()
    finally:
        await taskM.stop_all()
        gpioM.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("finished by ctrl+C")
