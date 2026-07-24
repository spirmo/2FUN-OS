import sys
from platform_core.runtime.runtime_context import get_event_bus


def main():
    bus = get_event_bus()

    print("\n🔥 FOUNDER CONTROL PANEL")
    print("commands: list | approve <id> | veto <id> | exit\n")

    while True:
        try:
            cmd = input("founder> ").strip().split()
        except EOFError:
            print("\n👋 input stream closed. exiting founder CLI")
            break

        if not cmd:
            continue

        action = cmd[0]

        # LIST QUEUE
        if action == "list":
            queue = bus.founder_cli.list()
            print(queue)

        # APPROVE
        elif action == "approve":
            if len(cmd) < 2:
                print("❌ event_id required")
                continue

            result = bus.founder_cli.approve(cmd[1])
            print(result)

        # VETO
        elif action == "veto":
            if len(cmd) < 2:
                print("❌ event_id required")
                continue

            result = bus.founder_cli.veto(cmd[1])
            print(result)

        # EXIT
        elif action == "exit":
            print("👋 shutting down founder panel")
            break

        else:
            print("❌ unknown command")


if __name__ == "__main__":
    main()
