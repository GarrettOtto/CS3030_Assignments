# Questions asked AI:
# Help me write a Python script that checks a site's certificate expiry date (ssl). Explain each line of code that you provide. Thank you!
# Could you code this more simply? I keep getting lost in the code
# Can you explain what each function does and why it is used?
# Can you explain what each function does in the entire file?
# Why are we creating a secure SSL context and not connection? What is a ssl context?

import ssl
import socket
from datetime import datetime

# Function used to check the SSL certificate expiration
# Args:
#   hostname (str)
# Returns:
#   String with expiration information
#   Error message
def check_ssl_expiry(hostname):
    # Creating the rules for the connection that we are about to make with `ssl context`
    ssl_context = ssl.create_default_context()

    try:
        # Connect to the host and wrap the socket with SSL in a single step.
        with ssl_context.wrap_socket(
            # Creating a socket connection with the hostname (getting IP address)
            sock = socket.create_connection((hostname, 443), timeout=5),
            # Getting domain name under the IP address that we want to talk to
            server_hostname = hostname
        ) as s:
            # Get the certificate's information as a dictionary.
            cert_info = s.getpeercert()
            # Get the expiration date string from the dictionary.
            expiry_date_str = cert_info['notAfter']
            
            # This essentially puts the datetime object into something that is easier to read and use:
            # Convert the date string into a datetime object. Format: %b %d %H:%M:%S %Y %Z
            # Argument 1: expiry_date_str - Raw text of the expiration date. Example: Oct 26 12:00:00 2025 GMT
            # Argument 2: '%b %d %H:%M:%S %Y %Z' - Tells strptime exactly how to read the date string. | %b - Month | %d - Day | %H - Hour | %M - Minute | %S - Second | %Y - Year | %Z - Timezone |
            expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
            # Calculate how many days are left until the certificate expires. (.days pulls only the days)
            days_remaining = (expiry_date - datetime.now()).days

            # Return a clear, formatted message with the result.
            return f"The certificate for '{hostname}' expires in {days_remaining} days (on {expiry_date.strftime('%Y-%m-%d')})."

    # Error handling
    except socket.gaierror:
        return f"Error: Could not find the host '{hostname}'."
    except socket.timeout:
         return f"Error: Connection to '{hostname}' timed out."
    except ConnectionRefusedError:
        return f"Error: Connection to '{hostname}' was refused."
    except Exception as e:
        # Catch any other issues, such as SSL handshake failures.
        return f"An error occurred for '{hostname}': {e}"

# Main function
if __name__ == "__main__":
    print("--- SSL Certificate Expiry Checker ---")
    # Getting user input
    website_to_check = input("Enter a website to check (e.g., google.com): ")
    # Calling function to get the SSL cert info. Returns a string
    result = check_ssl_expiry(website_to_check)
    # Printing string
    print(result)