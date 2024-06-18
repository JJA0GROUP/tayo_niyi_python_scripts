import subprocess
import time

#This a postgresql heroku db version update using pg:copy method
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        exit(result.returncode)
    return result.stdout.strip()

def provision_new_db(app_name, version=None):
    command = f"heroku addons:create heroku-postgresql:standard-0 --app {app_name}"
    if version:
        command += f" --version {version}"
    run_command(command)
    print("Provisioning new database... This might take a few minutes.")
    time.sleep(10)  # Sleep for a short time to allow Heroku to start provisioning
    wait_for_db_provisioning(app_name)

def wait_for_db_provisioning(app_name):
    command = f"heroku pg:wait --app {app_name}"
    print("Waiting for new database provisioning to complete...")
    run_command(command)
    print("New database provisioning completed.")

def enter_maintenance_mode(app_name):
    command = f"heroku maintenance:on -a {app_name}"
    run_command(command)

def transfer_data(old_db_url, new_db_url, app_name):
    command = f"heroku pg:copy {old_db_url} {new_db_url} --app {app_name}"
    run_command(command)

def promote_new_db(new_db_url, app_name):
    command = f"heroku pg:promote {new_db_url} --app {app_name}"
    run_command(command)

def exit_maintenance_mode(app_name):
    command = f"heroku maintenance:off --app {app_name}"
    run_command(command)

def destroy_old_db(old_db_url, app_name):
    command = f"heroku addons:destroy {old_db_url} --app {app_name} --confirm {app_name}"
    run_command(command)

def main():
    app_name = "example-app"
    old_db_url = "HEROKU_POSTGRESQL_OLD_URL"
    new_db_version = "13"  # Change as needed

    print("Provisioning new database...")
    provision_new_db(app_name, version=new_db_version)

    print("Entering maintenance mode...")
    enter_maintenance_mode(app_name)

    print("Transferring data to new database...")
    new_db_url = "HEROKU_POSTGRESQL_NEW_URL"  # Replace with actual new DB URL after provisioning
    transfer_data(old_db_url, new_db_url, app_name)

    print("Promoting new database...")
    promote_new_db(new_db_url, app_name)

    print("Exiting maintenance mode...")
    exit_maintenance_mode(app_name)

    print("Destroying old database...")
    destroy_old_db(old_db_url, app_name)

    print("Database upgrade completed successfully.")

if __name__ == "__main__":
    main()
