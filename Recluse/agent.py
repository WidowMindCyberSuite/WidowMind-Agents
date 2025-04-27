import platform

def main():
    print("[Recluse] Agent started.")
    os_type = platform.system()
    if os_type == "Windows":
        print("[Recluse] Running Windows-specific logic.")
        # TODO: Implement Windows logic
    elif os_type == "Linux":
        print("[Recluse] Running Linux-specific logic.")
        # TODO: Implement Linux logic
    else:
        print("[Recluse] OS not supported yet.")

if __name__ == "__main__":
    main()
