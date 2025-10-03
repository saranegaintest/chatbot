# Package Tracking Chatbot

A simple Python-based command-line chatbot that helps customers track lost packages and file missing package claims.
The bot demonstrates conversational flows, error handling, and modular design principles.

---

## 🚀 Setup & Installation

1. **Clone this repository** (or copy the code into a local folder):

   ```bash
   git clone https://github.com/saranegaintest/chatbot.git
   cd chatbot
   ```

2. **Install Python (>=3.8)**
   Make sure Python is installed and available in your PATH.
   Check with:

   ```bash
   python --version
   ```

3. **Create a virtual environment (optional, recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

4. **Prepare data file**
   Create a folder named `data` with a file `packages.json`.
   Example:

   ```json
   {
     "ABC12345": "In Transit",
     "XYZ98765": "Out for Delivery",
     "LMN55555": "Delivered"
   }
   ```

5. **Run the chatbot**:

   ```bash
   python chatbot.py
   ```

---

## 💡 How It Works

* **Main Menu**
  On first launch, the bot offers:

  * `1` → Track a lost package
    From the second loop onward, it also offers:
  * `2` → End chat

* **Package Tracking Flow**

  * User provides a tracking number (validated by format).
  * Bot looks up status from `data/packages.json`.
  * Status-specific responses:

    * *In Transit*: asks for patience.
    * *Out for Delivery*: reassures delivery is imminent.
    * *Delivered*: triggers a **Delivered Flow**.

* **Delivered Flow**

  * Asks if the user actually received the package.
  * If not received, confirms before starting a **Claim Flow**.

* **Claim Flow**

  * Collects and validates **name** (letters, spaces, hyphens).
  * Collects and validates **contact info** (email or phone).
  * Confirms claim submission.

* **Exit Handling**

  * Users can type `bye`, `quit`, `exit`, or `end` at any point to gracefully exit.
  * After the first menu loop, option `2` ends chat explicitly.

---

## 🛠 Design Approach

* **Separation of Concerns**
  Each flow (`package_tracking`, `delivered_package_flow`, `file_claim_flow`) is isolated for clarity and easy future extension.

* **Reusability**
  Common exit words are stored in `END_CHAT_WORDS`.
  Intent detection is done via `matches_intent()` for more flexible keyword matching.

* **Validation**
  Input checks prevent invalid tracking numbers, names, and contacts.
  Bot loops until a valid response (or exit command) is given.

* **Extensibility**
  The design allows adding new modules (e.g., returns, FAQs) by simply extending the intent matching.

---

## 📖 Example Run

```
Bot: Hello! How can I help you today?
1. Track a lost package
You: 1
Bot: I see that you can't find your package. Can you please provide your tracking number (like ABC12345)?
You: ABC12345
Bot: Thanks! I’ve found your package. Tracking ID ABC12345 status: Delivered.
Bot: Our records show that package ABC12345 was delivered.
Bot: Did you actually receive it? (yes/no)
You: no
Bot: I’m sorry to hear that. I can help you file a missing package claim.
Bot: Are you sure you want to continue with filing a claim? (yes/no)
```

---

## 📌 Future Improvements

* Log submitted claims into a `claims.json` file for tracking.
* Support multiple modules (returns, complaints, FAQs).
* Add NLP intent recognition for more natural queries.
* Wrap as a web or messaging app chatbot.
