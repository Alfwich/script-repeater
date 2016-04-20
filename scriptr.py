import sys, os, time

def main():
    command = open("command.txt").readlines()
    repeats = 1
    hasSleepCycle = len(sys.argv) > 1 and float(sys.argv[1])
    if len(command) > 0:
        print("Starting command repeat loop with command:")
        for line in command:
            print("  " + line.strip())

        # Add the desired repeat period as a sleep command at the end of the sript
        if hasSleepCycle:
            sleepCyclePeriod = float(sys.argv[1])
            print(" * Repeating after %f seconds without delay" % sleepCyclePeriod)
            command.append("{{SLEEP}}:%f"%(sleepCyclePeriod))
        while True:
            if not hasSleepCycle:
                try:
                    raw_input("Press Enter to repeat command(exit=ctrl+c)...")
                except KeyboardInterrupt:
                    return
            for line in command:
                formattedCommand = formatCommandLine(line, repeats)
                # Pass the unmatched repeater commands to the system
                if not attemptRepeaterCommand(formattedCommand):
                    sys.stdout.write(">> " + formattedCommand + "\n" )
                    os.system(formattedCommand)

            sys.stdout.write("|  Completed iteration: %d\n" % repeats)
            repeats += 1
    else:
        print("Could not load command from file 'command.txt'!")

def formatCommandLine(rawCommand, repeats=0):
    formattedCommand = rawCommand.strip()
    formattedCommand = formattedCommand.replace("{{#}}", str(repeats))
    formattedCommand = formattedCommand.replace("{{TS}}", str(int(time.time())))
    return formattedCommand

def attemptRepeaterCommand(command):
    # NOOP for comments and empty commands
    if len(command) == 0 or command[0] == "#":
        return True

    # Internal sleep command
    if "{{SLEEP}}" in command:
        sleepTime = float(command.split(":")[1])
        sys.stdout.write("|  Sleeping for %f seconds..." % sleepTime)
        while sleepTime > 0:
            sleepTime -= 1
            time.sleep(1)
            sys.stdout.write(".")
            pass
        sys.stdout.write("done\n")
        return True

    return False


if __name__ == "__main__":
    main()
