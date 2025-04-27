import platform

def main():
    print("[CamelGate] Agent started.")
    os_type = platform.system()
    if os_type == "Windows":
        print("[CamelGate] Running Windows-specific logic.")
        # TODO: Implement Windows logic
    elif os_type == "Linux":
        print("[CamelGate] Running Linux-specific logic.")
        # TODO: Implement Linux logic
    else:
        print("[CamelGate] OS not supported yet.")

if __name__ == "__main__":
    main()
