import rtde_control
import rtde_receive

robot_ip = "192.168.77.2"

rtde_r = None
rtde_c = None

try:
    rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)

    print("Connected to UR5e")

    while True:

        # Read the robot's current position
        current_pose = rtde_r.getActualTCPPose()

        print("\nCurrent TCP position [m]:")
        print("X:", current_pose[0])
        print("Y:", current_pose[1])
        print("Z:", current_pose[2])

        # Get coordinates from the user
        x_input = input("\nEnter X coordinate (m), or q to quit: ")

        if x_input.strip().lower() == "q":
            break

        try:
            x = float(x_input)
            y = float(input("Enter Y coordinate (m): "))
            z = float(input("Enter Z coordinate (m): "))
        except ValueError:
            print("Invalid coordinates. Please enter numbers.")
            continue

        # Keep the current orientation
        target_pose = current_pose.copy()

        target_pose[0] = x
        target_pose[1] = y
        target_pose[2] = z + 0.21 #offset 

        print("\nTarget TCP position:")
        print("X:", x)
        print("Y:", y)
        print("Z:", z)

        confirm = input("Move robot? (yes/no): ")

        if confirm.strip().lower() != "yes":
            print("Movement cancelled.")
            continue

        # Connect to control interface when needed
        if rtde_c is None:
            rtde_c = rtde_control.RTDEControlInterface(robot_ip)

        velocity = 0.05
        acceleration = 0.1

        try:
            success = rtde_c.moveL(
                target_pose,
                velocity,
                acceleration
            )
            print("Movement result:", success)

            if not success:
                print("Movement did not complete. Check the robot before continuing.")
                break

        except Exception as e:
            print("Movement error:", e)
            break

finally:
    if rtde_c is not None:
        rtde_c.disconnect()

    if rtde_r is not None:
        rtde_r.disconnect()

print("Program finished.")