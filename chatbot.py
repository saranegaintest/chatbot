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

# ---------- Module: Package Tracking ----------
def package_tracking_module():
    print("Bot: I see that you can't find your package. Can you please provide your tracking number?")

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
            print(f"Bot: Thanks! I’ve found your package. Tracking ID {tracking_input} status: {status}.")
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
