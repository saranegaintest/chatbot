import json
import re

END_CHAT_WORDS = ["bye", "end", "quit", "exit"]

# ---------- Utility Functions ----------
def get_user_input(prompt="You: "):
    """Wrapper for input (for easier future expansion, logging, etc.)."""
    return input(prompt).strip()

def matches_intent(user_input, keywords):
    """Return True if any keyword is found in user input (case-insensitive)."""
    user_input = user_input.lower()
    return any(keyword in user_input for keyword in keywords)

def is_tracking_number(user_input):
    """Check if input looks like a tracking number."""
    return bool(re.match(r"^[A-Za-z0-9]{5,}$", user_input))

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
        
        if tracking_input.lower() in END_CHAT_WORDS:
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
            print(f"Bot: Thanks! I’ve found your package. Tracking ID {tracking_input} status: {status}.")
            if status.lower() == "in transit":
                print("Bot: Please wait for your package to arrive. Thanks for your patience!")
            elif status.lower() == "out for delivery":
                print("Bot: Your package is almost there! It should arrive today. Please keep an eye out.")
            elif status.lower() == "delivered":
                return delivered_package_flow(tracking_input)  # start special delivered flow
            else:
                print("Bot: Thanks for your patience while your package is being processed.")
                return 0
        
# ---------- Module: Delivered Package Follow-up ----------
def delivered_package_flow(tracking_id):
    print(f"Bot: Our records show that package {tracking_id} was delivered.")
    print("Bot: Did you actually receive it? (yes/no)")

    while True:
        response = get_user_input()
        if response.lower() in END_CHAT_WORDS:
            return -1
        elif response.lower() in ["yes", "y"]:
            print("Bot: Great! I’m glad your package arrived safely.")
            return 0
        elif response.lower() in ["no", "n"]:
            print("Bot: I’m sorry to hear that. I can help you file a missing package claim.")
            print("Bot: Are you sure you want to continue with filing a claim? (yes/no)")

            while True:
                confirm = get_user_input()
                if confirm.lower() in END_CHAT_WORDS:
                    return -1
                elif confirm.lower() in ["yes", "y"]:
                    return file_claim_flow(tracking_id)
                elif confirm.lower() in ["no", "n"]:
                    print("Bot: Okay, I won’t file a claim.")
                    return 0
                else:
                    print("Bot: Please answer 'yes' or 'no'.")
        else:
            print("Bot: Please answer 'yes' or 'no'.")

# ---------- Module: File a Claim ----------
def file_claim_flow(tracking_id):
    print(f"Bot: Let's start a missing package claim for {tracking_id}.")
    
    # Collect and validate name
    print("Bot: Can you please provide your full name?")
    while True:
        name = get_user_input()
        if validate_name(name):
            break
        elif name.lower() in END_CHAT_WORDS:
            return -1
        else:
            print("Bot: That doesn’t look like a valid name. Please use only letters, spaces, or hyphens.")

    # Collect and validate contact
    print(f"Bot: Thanks, {name}. Can you provide an email or phone number where we can reach you?")
    while True:
        contact = get_user_input()
        if validate_contact(contact):
            break
        elif contact.lower() in END_CHAT_WORDS:
            return -1
        else:
            print("Bot: That doesn’t look like a valid email or phone number. Please try again.")

    # Confirm claim
    print(f"Bot: Thanks, {name}! We’ve submitted a missing package claim for tracking ID {tracking_id}.")
    print(f"Bot: Our team will reach out to you at {contact} within 24 hours.")
    
    return 0

# ---------- Main Chatbot ----------
def chatbot():
    print("\nBot: Hello! How can I help you today?")
    menu_shown_count = 0  # keeps track of how many times menu is displayed

    while True:
        menu_shown_count += 1

        print("1. Track a lost package")
        if menu_shown_count > 1:
            print("2. End chat")

        user_input = get_user_input()
        
        if matches_intent(user_input, ["1", "lost", "track", "package"]):
            package_tracking_outcome =package_tracking_module()
            if package_tracking_outcome == 0:
                print("\nBot: How else can I help you today?")
            elif package_tracking_outcome == -1:
                print("Bot: Thanks for chatting! Have a great day!")
                break 
        elif user_input.lower() in END_CHAT_WORDS or (menu_shown_count > 1 and "2" in user_input):
            print("Bot: Thanks for chatting! Have a great day!")
            break
        else:
            print("Bot: Sorry, that’s not a valid response. Please choose from the options below.")

# ---------- Run ----------
if __name__ == "__main__":
    chatbot()
