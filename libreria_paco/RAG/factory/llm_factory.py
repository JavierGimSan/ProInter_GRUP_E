from ..models.LLM import LLM
from ..models.aviable_models import models
import sys, os, django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libreria_paco.settings")
django.setup()
from libreria_paco.settings import LLM_MODEL

def get(name: str = LLM_MODEL) -> LLM:
    if not name in models: raise KeyError("Model not aviable")

    model = models[name]

    if model["service"] == "ollama":
        from langchain_ollama.llms import OllamaLLM
        from libreria_paco.settings import OLLAMA_SERVER

        return LLM(model=OllamaLLM(model=name, base_url=OLLAMA_SERVER))
    
    if model["service"] == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return LLM(model=ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=model["apikey"]))