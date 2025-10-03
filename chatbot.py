import re

# ---------- Utility Functions ----------
def is_tracking_number(user_input):
    """Check if input looks like a tracking number."""
    return bool(re.match(r"^[A-Za-z0-9]{5,}$", user_input))

def get_user_input(prompt="You: "):
    """Wrapper for input (for easier future expansion, logging, etc.)."""
    return input(prompt).strip()

# ---------- Module: Package Tracking ----------
def package_tracking_module():
    print("Bot: I see that you can't find your package. Can you please provide your tracking number?")

    while True:
        tracking_input = get_user_input()
        
        if tracking_input.lower() in ["bye", "exit", "quit"]:
            return -1

        if is_tracking_number(tracking_input):
            print(f"Bot: Thanks! I’ve found your package. Tracking ID {tracking_input} is currently in transit.")
            return 0
        else:
            print("Bot: Hmm, that doesn’t look like a valid tracking number. Try something like ABC12345.")

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
            print("Bot: Sorry, that’s not a valid option. Please type the number of your choice.")

# ---------- Run ----------
if __name__ == "__main__":
    chatbot()
