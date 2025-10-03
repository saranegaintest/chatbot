import json
import re

# ---------- Utility Functions ----------
def is_tracking_number(user_input):
    """Check if input looks like a tracking number."""
    return bool(re.match(r"^[A-Za-z0-9]{5,}$", user_input))

def get_user_input(prompt="You: "):
    """Wrapper for input (for easier future expansion, logging, etc.)."""
    return input(prompt).strip()

def lookup_tracking_status(tracking_id, filename="data/packages.json"):
    """Look up the tracking status from a JSON file."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data.get(tracking_id.upper(), None)
    except FileNotFoundError:
        return "Error: package data file not found."
    
def validate_name(name: str) -> bool:
    """
    Validates a name: must be alphabetic (with spaces or hyphens allowed),
    at least 2 characters long.
    """
    return bool(re.match(r"^[A-Za-z\s\-']{2,}$", name.strip()))

def validate_contact(contact: str) -> bool:
    """
    Validates contact as either:
    - An email (basic check for pattern something@something.domain)
    - A phone number (digits, spaces, dashes, plus sign)
    """
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    phone_pattern = r"^\+?[0-9\s\-]{7,15}$"
    return bool(re.match(email_pattern, contact)) or bool(re.match(phone_pattern, contact))

# ---------- Module: Package Tracking ----------
def package_tracking_module():
    print("Bot: I see that you can't find your package. Can you please provide your tracking number (like ABC12345)?")

    while True:
        tracking_input = get_user_input()
        
        if tracking_input.lower() in ["bye", "exit", "quit"]:
            return -1
        
        if not is_tracking_number(tracking_input):
            print("Bot: Hmm, that doesn’t look like a valid tracking number. Try something like ABC12345.")
            continue
        
        status = lookup_tracking_status(tracking_input)
        if status is None:
            print(f"Bot: I couldn’t find tracking ID {tracking_input}. Please check your number and try again.")
        elif "Error" in status:
            print("Bot: We are facing some issues on our side. Please try again later!")
            return 0
        else:
            if status.lower() == "delivered":
                return delivered_package_flow(tracking_input)
            else:
                print(f"Bot: Thanks! I’ve found your package. Tracking ID {tracking_input} status: {status}.")
                return 0
        
# ---------- Module: Delivered Package Follow-up ----------
def delivered_package_flow(tracking_id):
    print(f"Bot: Our records show that package {tracking_id} was delivered.")
    print("Bot: Did you actually receive it? (yes/no)")

    while True:
        response = get_user_input()
        if response.lower() in ["bye", "exit", "quit"]:
            return -1
        elif response.lower() in ["yes", "y"]:
            print("Bot: Great! I’m glad your package arrived safely.")
            return 0
        elif response.lower() in ["no", "n"]:
            print("Bot: I’m sorry to hear that. I’ll guide you to file a missing package claim.")
            return file_claim_flow(tracking_id)
        else:
            print("Bot: Please answer 'yes' or 'no'.")

# ---------- Module: File a Claim ----------
def file_claim_flow(tracking_id):
    print(f"Bot: Let's start a missing package claim for {tracking_id}.")
    
    # Collect and validate name
    print("Bot: Can you please provide your full name?")
    while True:
        name = get_user_input()
        if name.lower() in ["bye", "exit", "quit"]:
            return -1
        if validate_name(name):
            break
        else:
            print("Bot: That doesn’t look like a valid name. Please use only letters, spaces, or hyphens.")

    # Collect and validate contact
    print(f"Bot: Thanks, {name}. Can you provide an email or phone number where we can reach you?")
    while True:
        contact = get_user_input()
        if contact.lower() in ["bye", "exit", "quit"]:
            return -1
        if validate_contact(contact):
            break
        else:
            print("Bot: That doesn’t look like a valid email or phone number. Please try again.")

    # Confirm claim
    print(f"Bot: Thanks, {name}! We’ve submitted a missing package claim for tracking ID {tracking_id}.")
    print(f"Bot: Our team will reach out to you at {contact} within 24 hours.")
    
    return 0

# ---------- Main Chatbot ----------
def chatbot():
    print("\nBot: Hello! How can I help you today?")
    
    while True:
        print("1. Track a lost package")

        user_input = get_user_input()

        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Bot: Thanks for chatting! Have a great day!")
            break
        
        elif "1" in user_input or "lost" in user_input or "track" in user_input or "package" in user_input:
            package_tracking_outcome =package_tracking_module()
            if package_tracking_outcome == 0:
                print("\nBot: How else can I help you today?")
            elif package_tracking_outcome == -1:
                print("Bot: Thanks for chatting! Have a great day!")
                break
        
        else:
            print("Bot: Sorry, that’s not a valid response. Please choose from the options below.")

# ---------- Run ----------
if __name__ == "__main__":
    chatbot()
