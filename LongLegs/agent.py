import platform

def main():
    print("[LongLegs] Agent started.")
    os_type = platform.system()
    if os_type == "Windows":
        print("[LongLegs] Running Windows-specific logic.")
        # TODO: Implement Windows logic
    elif os_type == "Linux":
        print("[LongLegs] Running Linux-specific logic.")
        # TODO: Implement Linux logic
    else:
        print("[LongLegs] OS not supported yet.")

if __name__ == "__main__":
    main()
