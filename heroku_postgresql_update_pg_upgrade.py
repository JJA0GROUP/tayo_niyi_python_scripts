import subprocess
import time
import sys
import os
import signal
import threading


class CommandTimeout(Exception):
    pass

#This a postgresql heroku db version update using pg:upgrade method
#Before you run this script, please confirm your current db version and make sure the new version you want to upgrade to is
#Greater (>) than your current postgress db version on Heroku. If you don't confirm these two things the script may not work as expected.
def run_command(command, check_for=None, timeout=None):
    def target():
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = []

        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()

            if stdout_line:
                output.append(stdout_line.strip())
                print(stdout_line.strip())
                if check_for and check_for in stdout_line:
                    result.append('\n'.join(output))
                    return

            if stderr_line:
                output.append(stderr_line.strip())
                print(stderr_line.strip())

            if stdout_line == '' and stderr_line == '' and process.poll() is not None:
                break

        if process.returncode != 0:
            print(f"Error running command: {command}")
            print(process.stderr.read())
            exit(process.returncode)

        result.append('\n'.join(output))

    result = []
    thread = threading.Thread(target=target)
    thread.start()

    thread.join(timeout)
    if thread.is_alive():
        raise CommandTimeout(f"Command '{command}' timed out after {timeout} seconds")

    return result[0] if result else ""

def provision_follower_db(app_name, old_db_url, version=None):
    command = f"heroku addons:create heroku-postgresql:standard-0 --follow {old_db_url} --app {app_name}"
    if version:
        command += f" --version {version}"
    run_command(command)
    # Wait for a short period to ensure the provisioning starts
    wait_for_db_provision(app_name)
    return get_follower_db_url(app_name, old_db_url)

def get_follower_db_url(app_name, old_db_url):
    command = f"heroku pg:info --app {app_name}"
    output = run_command(command)
    
    # Filter out any warnings or irrelevant lines
    filtered_output = [line for line in output.split("\n") if line.startswith("===") or "Add-on:" in line or "Following:" in line]

    follower_db_url = None
    following_database = False

    for line in filtered_output:
        if "Following:" in line:
            following_database = True
        elif "Add-on:" in line and following_database:
            follower_db_url = line.split(" ")[-1]
            break
        else:
            following_database = False

    if not follower_db_url:
        print("Follower database URL not found.")
        exit(1)
    
    return follower_db_url

def enter_maintenance_mode(app_name):
    command = f"heroku maintenance:on -a {app_name}"
    run_command(command)
    time.sleep(300)

def upgrade_follower_db(follower_db_url, app_name, version=None):
    command = f"heroku pg:upgrade {follower_db_url} --app {app_name} --confirm {app_name}"
    if version:
        command += f" --version {version}"
    run_command(command)
    wait_for_db_upgrade(app_name)

def wait_for_db_upgrade(app_name):
    command = f"heroku pg:wait --app {app_name}"
    print("Waiting for database upgrade to complete...")
    run_command(command)
    print("Database upgrade completed.")

def wait_for_db_provision(app_name):
    command = f"heroku pg:wait --app {app_name}"
    print("Waiting for database provisioning to complete...")
    run_command(command)
    print("Database provision completed.")

def promote_new_db(follower_db_url, app_name):
    command = f"heroku pg:promote {follower_db_url} --app {app_name}"
    try:
        run_command(command, check_for="Checking release phase...", timeout=180)
    except CommandTimeout:
        print(f"Command '{command}' timed out. Proceeding to the next step.")


# def unfollow_db(follower_db_url, app_name):
#     command = f"heroku pg:unfollow {follower_db_url} --app {app_name} --confirm {app_name}"
#     run_command(command)
#     #Wait for seven (7) minutes for the new db to unfollow old db properly
#     time.sleep(420)
    

def exit_maintenance_mode(app_name):
    command = f"heroku maintenance:off -a {app_name}"
    run_command(command)



def main():
    app_name = "liveeasy"
    old_db_url = "ADDON_NAME"
    current_db_version = "CURRENT_DB_VERSION" #Specify current db version. Please specify your current db version
    new_db_version = "NEW_DB_VERSION"  # Specify the desired version. Please make sure this version is greater than (>) current_db_version

    print("Provisioning a follower database...")
    follower_db_url = provision_follower_db(app_name, old_db_url, version=current_db_version)

    print("Entering maintenance mode...")
    enter_maintenance_mode(app_name)

    print("Upgrading the follower database...")
    upgrade_follower_db(follower_db_url, app_name, version=new_db_version)

    # print("Unfollowing leader database and making follower database writable...")
    # unfollow_db(follower_db_url, app_name)

    print("Promoting the new database...")
    promote_new_db(follower_db_url, app_name)

    print("Exiting maintenance mode...")
    exit_maintenance_mode(app_name)

    print("Database upgrade completed successfully.")
    # Simulate Ctrl+C to stop the script
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script execution interrupted. Exiting now.")
        sys.exit(0)