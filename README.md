# vk_dung_scripts

A modular, asynchronous VK scripts toolkit for managing chat interactions and scheduled messages (autopost).

---

## Overview

This project provides a set of asynchronous Python scripts leveraging the VK API to enable:

- **Trigger Buffs**: Monitors VK chats for specific keywords (triggers) and responds with predefined messages, adhering to rate limits.
- **Autopost**: Sends scheduled messages to designated VK chats at regular intervals.
- **Runner**: Launches multiple scripts concurrently for scalable bot functionality.

Sensitive data such as tokens, peer IDs, triggers, and autopost messages are securely managed via environment variables in a `.env` file.

---

## Project Structure

```
project_root/
│
├── scripts/                 # Main executable scripts
│   ├── __init__.py
│   ├── triggerbaff.py      # Trigger handler
│   ├── autopost.py         # Scheduled autoposting script
│   └── runner.py           # Unified launcher for multiple scripts concurrently
│
├── shared/                 # Shared libraries and utilities
│   ├── __init__.py
│   ├── utils.py            # Message sender function from queue
│   ├── vk_api.py           # VK API wrapper functions 
│   ├── triggers.py         # Trigger loader and management
│   ├── config.py           # Configuration loader from environment variables
│   └── logpoll.py          # Long polling listener logic
│
├── .env                    # Environment variables (not committed to repository)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

```ini
VK_TOKEN = ""
VK_AUTOPBAFF_PEER_ID = 2000000XXX
VK_AUTOPOST_PEER_ID = 2000000XXX
VK_AUTOPOST_MESSAGE = "
Hello, this is an automated post!
"
VK_API_VERSION = "5.131"
AUTOPOST_INTERVAL = 3600
TRIGGERBAFF_INTERVAL = 60
TRIGGER_example = "Replied this text on message example"
# Add additional TRIGGER_<keyword>=<response> pairs as needed
# you can use any language
```

**Note**: Ensure the `.env` file is not committed to version control (e.g., add it to `.gitignore`).

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nyawkin-hub/vk_dung_scripts.git
   cd vk_dung_scripts
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # .\venv\Scripts\activate  # Windows PowerShell
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running a Single Script

- To run the trigger buff bot:
  ```bash
  python3 -m scripts.triggerbaff
  ```

- To run the autopost script:
  ```bash
  python3 -m scripts.autopost
  ```

### Running All Scripts Concurrently

Use the runner script to launch both `triggerbaff` and `autopost` simultaneously:
```bash
python3 -m scripts.runner
```

---

## Contributing

Contributions are not welcome!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.