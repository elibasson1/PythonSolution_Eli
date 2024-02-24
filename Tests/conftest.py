import paramiko as paramiko
import time
import pytest

from Util.Logger import getLogger
from Util.Read_INI_File import read_config_ini

pytest.global_var = None


@pytest.fixture(scope="class", autouse=True)
def setup(request):
    log = getLogger()
    ssh = establish_ssh_connection()

    # Start the Docker container remotely before the test class
    container_id = start_docker_container(ssh)
    request.cls.container_id = container_id

    # Wait for the container to be up and running (adjust as needed)
    log.info("Docker container has started")
    time.sleep(5)

    yield
    # Cleanup: Stop and remove the Docker container after the test class
    stop_docker_container(ssh, container_id)
    log.info("Docker container has been stopped and removed.")

    # Close the SSH connection
    ssh.close()


# Initiates the Docker container remotely via SSH by executing the docker run command.
def start_docker_container(ssh):
    # run commands
    cmd = "docker run -d -p 5000:5000 elib"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    container_id = stdout.read().strip().decode()
    return container_id


# Stops and removes the Docker container remotely via SSH by executing docker stop and then docker rm commands.
def stop_docker_container(ssh, container_id):
    cmd_stop = f"docker stop {container_id}"
    cmd_remove = f"docker rm {container_id}"
    # Execute the 'docker stop' command
    stdin_stop, stdout_stop, stderr_stop = ssh.exec_command(cmd_stop)
    # Wait for the command to finish
    stdout_stop.channel.recv_exit_status()

    # Execute the 'docker rm' command
    stdin_remove, stdout_remove, stderr_remove = ssh.exec_command(cmd_remove)
    # Wait for the command to finish
    stdout_remove.channel.recv_exit_status()


# Establishes SSH connection based on the settings in the config.ini file.
def establish_ssh_connection():
    username = read_config_ini()['Server']['user']
    private_key_path = read_config_ini()['Server']['private_key_path']
    host = read_config_ini()['Server']['host']
    port = read_config_ini()['Server']['port']

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # key_filename: This parameter specifies the path to the private key file that will be used for authentication.
    # In SSH, instead of using passwords for authentication, it's common to use key pairs, consisting of a public key
    # and a private key. The private key stays on your local machine, and the public key is stored on the server.
    # When you connect to the server, your SSH client (in this case, paramiko) uses your private key to prove your
    # identity.

    ssh.connect(host, port, username, key_filename=private_key_path)
    return ssh
