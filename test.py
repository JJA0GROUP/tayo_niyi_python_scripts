import subprocess
import time
import re
import threading


class CommandTimeout(Exception):
    pass

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



def promote_new_db(follower_db_url, app_name):
    command = f"heroku pg:promote {follower_db_url} --app {app_name}"
    try:
        run_command(command, check_for="Checking release phase...", timeout=1)
    except CommandTimeout:
        print(f"Command '{command}' timed out. Proceeding to the next step.")



test = promote_new_db("postgresql-octagonal-01167", "liveeasy")
print(test)