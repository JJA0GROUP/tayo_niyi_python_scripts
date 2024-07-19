import subprocess

def run_heroku_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
    else:
        print(result.stdout)
    return result.returncode == 0

def get_current_stack(app_name):
    command = f"heroku stack --app {app_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.splitlines()
        for line in lines:
            if "*" in line:
                return line.split()[0]  # Current stack is marked with an asterisk
    else:
        print(f"Error getting current stack: {result.stderr}")
    return None

def update_stack(app_name, new_stack):
    # Prepare the app for stack change
    print("Step 1: Preparing the app for stack change")
    command = f"heroku maintenance:on --app {app_name}"
    if not run_heroku_command(command):
        return

    # Change the stack
    print("Step 2: Changing the stack")
    command = f"heroku stack:set {new_stack} --app {app_name}"
    if not run_heroku_command(command):
        # Turn off maintenance if stack change failed
        run_heroku_command(f"heroku maintenance:off --app {app_name}")
        return

    # Deploy the app to the new stack
    #print("Step 3: Deploying the app to the new stack")
    #command = f"git push heroku main"
    #if not run_heroku_command(command):
        #return

    # Resume normal operation
    print("Step 4: Resuming normal operation")
    command = f"heroku maintenance:off --app {app_name}"
    run_heroku_command(command)

def main():
    app_name = "APP_NAME"  # Replace with your Heroku app name
    new_stack = "NEW_STACK"  # Replace with the desired stack, e.g., "heroku-20"

    print(f"Updating Heroku app '{app_name}' to use stack '{new_stack}'")
    current_stack = get_current_stack(app_name)
    if current_stack:
        print(f"Current stack: {current_stack}")
        if current_stack == new_stack:
            print("The app is already using the desired stack.")
        else:
            update_stack(app_name, new_stack)
    else:
        print("Failed to get the current stack information.")

if __name__ == "__main__":
    main()
