# AI Assistant Chat

A customer-support-oriented chat interface powered by **GPT-4** via LangChain, served by a **Flask** backend and a vanilla JS/CSS frontend.

Each response includes a direct answer alongside a structured analysis: sentiment score, category classification, and a recommended action for support agents.

---

## Features

- 💬 Real-time chat UI with loading states and message history
- 🤖 GPT-4 integration via LangChain with structured JSON output
- 📊 Per-message analysis: sentiment score, category, and recommended action
- ⚡ Model instance caching (thread-safe) — loads once, reused on every request
- 📋 Structured logging throughout the backend
- 🛡️ XSS-safe frontend rendering

---

## Project Structure

```
ai-assistant-chat/
├── app.py                  # Flask app — routes and request handling
├── config.py               # Central configuration (model ID, temperature, system prompt)
├── requirements.txt
├── .env.example            # Required environment variables
│
├── shared/
│   ├── openai_wrapper.py   # LangChain model loading, caching, and AI chain
│   └── ai_response.py      # AIResponse Pydantic schema and JSON output parser
│
├── templates/
│   └── index.html          # Chat UI
│
├── static/
│   ├── script.js           # Frontend logic
│   └── styles.css
│
└── scripts/
    └── sanity_check.py     # Manual connection and response testing
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd ai-assistant-chat
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-api-key-here
```

### 5. Run the app

```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000`.

---

## API

### `POST /generate`

Accepts a user message and returns a structured AI response.

**Request body**
```json
{
  "message": "What is the return policy?"
}
```

**Response**
```json
{
  "response": "Our return policy allows returns within 30 days of purchase.",
  "summary": "User is asking about the return policy.",
  "sentiment": 60,
  "category": "general",
  "action": "Provide the return policy details to the customer.",
  "duration": 1.23
}
```

| Field | Type | Description |
|---|---|---|
| `response` | `string` | Direct answer to the user's question |
| `summary` | `string` | Summary of the user's message |
| `sentiment` | `integer` | Sentiment score from 0 (negative) to 100 (positive) |
| `category` | `string` | Inquiry category (e.g. `billing`, `technical`, `general`) |
| `action` | `string` | Recommended action for the support representative |
| `duration` | `float` | Response generation time in seconds |

---

## Configuration

All defaults live in `config.py`:

| Constant | Default | Description |
|---|---|---|
| `DEFAULT_MODEL_ID` | `"gpt-4"` | OpenAI model to use |
| `DEFAULT_TEMPERATURE` | `0.2` | Sampling temperature |
| `DEFAULT_MAX_TOKENS` | `512` | Max tokens per response |
| `DEFAULT_SYSTEM_PROMPT` | *(see file)* | System prompt sent with every request |

---

## Scripts

Run the sanity check to verify your API key and model connection:

```bash
python -m scripts.sanity_check
```

---

## License

See [LICENSE](LICENSE).
