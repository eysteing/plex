import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
ssh.connect("192.168.1.9", username="Eystein", password="sytorax135", port=22)

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls -la")
exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error

for line in ssh_stdout:
    print(line.strip())
