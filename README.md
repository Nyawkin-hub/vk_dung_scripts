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
│   ├── triggerbaff.py      # Trigger listening and responding bot
│   ├── autopost.py         # Scheduled autoposting script
│   └── runner.py           # Unified launcher for multiple scripts concurrently
│
├── shared/                 # Shared libraries and utilities
│   ├── __init__.py
│   ├── vk_api.py           # VK API wrapper functions (e.g., send_message, longpoll params)
│   ├── triggers.py         # Trigger loader and management
│   ├── config.py           # Configuration loader from environment variables
│   └── logpoll.py          # Long polling listener logic
│
├── .env                    # Environment variables (not committed to repository)
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

```ini
VK_TOKEN="your_vk_api_token"
VK_PEER_ID=123456789                 # Peer ID for triggerbaff chat
VK_AUTOPOST_PEER_ID=987654321        # Peer ID for autopost chat
VK_AUTOPOST_MESSAGE="Your autopost message text"
TRIGGER_hello="Hi there! How can I help you?"
TRIGGER_blessing="Blessing is active, wait 61 seconds before next."
# Add additional TRIGGER_<keyword>=<response> pairs as needed
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

## Development Notes

- **Triggers Management**: Triggers are dynamically loaded from `.env` variables prefixed with `TRIGGER_`.
- **Rate Limiting**: The `triggerbaff` bot enforces a 61-second cooldown between messages to comply with VK API rate limits.
- **Extensibility**: Add new scripts to the `scripts/` directory and shared utilities to the `shared/` directory to expand functionality.
- **Logging**: Currently uses minimal console output. Enhanced logging integration is planned for better diagnostics.

---

## Contributing

Contributions are not welcome!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.