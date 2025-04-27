import platform

def main():
    print("[Huntsman] Agent started.")
    os_type = platform.system()
    if os_type == "Windows":
        print("[Huntsman] Running Windows-specific logic.")
        # TODO: Implement Windows logic
    elif os_type == "Linux":
        print("[Huntsman] Running Linux-specific logic.")
        # TODO: Implement Linux logic
    else:
        print("[Huntsman] OS not supported yet.")

if __name__ == "__main__":
    main()
