from ..credentials import gemini_api_key

models = {
    "deepseek-r1:1.5b": {
        "name": "deepseek-r1:1.5b",
        "service": "ollama"
    },
    "gemini": {
        "name": "gemini",
        "service": "gemini",
        "apikey": gemini_api_key
    }
}