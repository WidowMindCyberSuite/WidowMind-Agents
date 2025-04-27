import platform

def main():
    print("[Trapdoor] Agent started.")
    os_type = platform.system()
    if os_type == "Windows":
        print("[Trapdoor] Running Windows-specific logic.")
        # TODO: Implement Windows logic
    elif os_type == "Linux":
        print("[Trapdoor] Running Linux-specific logic.")
        # TODO: Implement Linux logic
    else:
        print("[Trapdoor] OS not supported yet.")

if __name__ == "__main__":
    main()
