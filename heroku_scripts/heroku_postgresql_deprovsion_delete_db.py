import subprocess
import time

#This a postgresql heroku db version update using pg:upgrade method
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        exit(result.returncode)
    return result.stdout.strip()

def deprovision_old_db(old_db_url, app_name):
    command = f"heroku addons:destroy {old_db_url} --app {app_name} --confirm {app_name}"
    run_command(command)

def main():
    app_name = "example-app"
    old_db_url = "HEROKU_POSTGRESQL_OLD_URL"
    new_db_version = "13"  # Specify the desired version

    print("Deprovisioning the old primary database...")
    deprovision_old_db(old_db_url, app_name)

if __name__ == "__main__":
    main()



