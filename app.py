import logging
import time

from flask import Flask, jsonify, render_template, request

from config import DEFAULT_SYSTEM_PROMPT
from shared.openai_wrapper import load_model, get_ai_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Missing message"}), 400

    logger.info("Received message: %.80s...", user_message)
    model = load_model()
    start_time = time.time()

    try:
        result = get_ai_response(model, DEFAULT_SYSTEM_PROMPT, user_message)
        duration = time.time() - start_time
        logger.info("Response generated in %.2fs", duration)
        return jsonify({**result, "duration": duration})
    except Exception as e:
        logger.error("Failed to generate response: %s", e)
        return jsonify({"error": "Failed to generate a response. Please try again."}), 500


if __name__ == "__main__":
    app.run(debug=True)
