import subprocess
import time

# Make sure you Install the heroku maintenance plugin by running the command below before running this code
#heroku plugins:install @heroku-cli/plugin-data-maintenance

def run_heroku_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
    else:
        print(result.stdout)

def maintenance_mode(app_name):
    command = f"heroku maintenance:on --app {app_name}"
    run_heroku_command(command)

def perform_upgrade(app_name, version, add_on_name):
    command = f"heroku redis:upgrade {add_on_name} --version {version} --app {app_name} --confirm {app_name}"
    run_heroku_command(command)
    #wait for 25 minutes for heroku to create a maintenance for the redis instance
    time.sleep(1500)

def run_maintenance(app_name, add_on_name):
    command = f"heroku data:maintenances:run {add_on_name} --app {app_name}"
    run_heroku_command(command)
    time.sleep(30)


def resume_normal_operation(app_name):
    command = f"heroku maintenance:off --app {app_name}"
    run_heroku_command(command)

def main():
    print("\nPlease type in the heroku redis details below:")
    app_name = input("App Name: ") #Heroku App Name e.g Staging 1
    version = input("New Redis Version: ") # Heroku New Redis Add On Version e.g 6.1.0
    add_on_name = input("Add On Name: ") # Heroku Redis Add on Name e.g beautiful_moose

    print("Step 1: Putting app in maintenance mode before upgrade")
    maintenance_mode(app_name)
    
    print("Step 2: Performing Upgrade. This will run for 25 minutes, so please grab your popcorn.")
    perform_upgrade(app_name, version, add_on_name)

    print("Step 3: Triggering maintenance")
    run_maintenance(app_name, add_on_name)
    
    print("Step 4: Resume Normal Operation by turning maintenance off")
    resume_normal_operation(app_name)

if __name__ == "__main__":
    main()
