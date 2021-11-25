import time
from claw import Claw


if __name__ == "__main__":
    claw = Claw(22)

    claw.hor_circle(4, (60, 0, 150), 40, 16, 200)
    
    # while True:
    #     motor.goal_position(1, 0, 1000, timeout=0)
    #     time.sleep(2)
    #     motor.goal_position(1, 45, 1000, timeout=0)
    #     time.sleep(2)