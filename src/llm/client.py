import os
import json
import requests
from typing import Optional

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.config import LLM_PROVIDER, OLLAMA_MODEL_NAME, API_MODEL_NAME, LLM_TEMPERATURE

class LLMClient:
    def __init__(self):
        """
        Agent'lar ve RAG sistemleri için birleştirilmiş LLM İstemcisi.
        config.py dosyasındaki LLM_PROVIDER ayarına göre istekleri 
        ya yerel Ollama'ya ya da uzak bir API'ye (örn. OpenAI) yönlendirir.
        """
        self.provider = LLM_PROVIDER
        # Ollama'nın varsayılan yerel API adresi
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def generate(self, prompt: str, system_prompt: str = "", format_json: bool = False) -> str:
        """LLM çağrısını soyutlayan ana metod."""
        if self.provider == "ollama":
            return self._call_ollama(prompt, system_prompt, format_json)
        elif self.provider == "api":
            return self._call_api(prompt, system_prompt, format_json)
        else:
            raise ValueError(f"Geçersiz LLM sağlayıcısı: {self.provider}")
            
    def _call_ollama(self, prompt: str, system_prompt: str, format_json: bool) -> str:
        payload = {
            "model": OLLAMA_MODEL_NAME,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": LLM_TEMPERATURE
            }
        }
        
        # Agent'ların JSON dönmesini garanti altına almak için (Llama 3.1 format zorlamayı destekler)
        if format_json:
            payload["format"] = "json"
            
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"[LLM Hatası - Ollama] {e}")
            return ""

    def _call_api(self, prompt: str, system_prompt: str, format_json: bool) -> str:
        """Karşılaştırma (Baseline) deneylerinde kullanmak için API çağrısı."""
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("[LLM Hatası] API modeli seçildi fakat .env dosyasında OPENAI_API_KEY bulunamadı.")
            return ""
            
        headers = {
            "Authorization": f"Bearer {api_key}", 
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": API_MODEL_NAME,
            "messages": messages,
            "temperature": LLM_TEMPERATURE
        }
        
        if format_json:
            payload["response_format"] = {"type": "json_object"}
            
        try:
            resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[LLM Hatası - API] {e}")
            return ""
