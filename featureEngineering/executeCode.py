import subprocess

def runCode(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to finish and get the output
    stdout, stderr = process.communicate()

    # Check if there were any errors
    if process.returncode != 0:
        print("Error executing command:", stderr.decode())
        return stderr.decode()
    else:
        print("Command output:")
        print(stdout.decode())
        return stdout.decode()