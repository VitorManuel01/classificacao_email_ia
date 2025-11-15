# python
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()  # Load environment variables from .env file
from google import genai

from openai import OpenAI

# Import NLP cleaner (supports both package and local execution)
try:
    from .nlp import clean_text_basic
except ImportError:
    try:
        from nlp import clean_text_basic
    except ImportError:
        # Fallback: no-op cleaner if import path is different during execution
        def clean_text_basic(text: str) -> str:
            return text


class AIProvider:
    def __init__(self, provider="gemini"):
        self.provider = provider.lower()

        if self.provider == "gemini":
            self.client = genai.Client()
        elif self.provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        else:
            raise ValueError("Unsupported AI provider. Choose 'gemini' or 'openai'.")

    def analyze_email_portuguese(self, email_text, email_sender, company_name):
        # Clean email text with NLP before sending to the model
        cleaned_email_text = clean_text_basic(email_text)

        productive_category_desc = "Emails que requerem uma ação ou resposta específica como solicitações, atualização sobre caso em aberto ou dúvidas."
        unproductive_category_desc = "Emails que não requerem ação ou resposta, como newsletters ou anúncios."

        prompt = f"""
                                Você deve analisar o email abaixo e responder **EXCLUSIVAMENTE** com um objeto JSON válido.
            
                                Email:
                                \"\"\"{cleaned_email_text}\"\"\"
            
                                REGRAS OBRIGATÓRIAS (siga exatamente):
                                1. Você deve classificar o email como "Produtivo" ou "Improdutivo" com base nos critérios:
                                   - Produtivo: {productive_category_desc}
                                   - Improdutivo: {unproductive_category_desc}
            
                                2. Você deve gerar SOMENTE 1 resposta sugerida.
            
                                3. A resposta sugerida deve seguir EXATAMENTE este formato:
                                   "Prezado(a) {email_sender}, <resposta> Atenciosamente, {company_name}"
            
                                   - NÃO use placeholders como [link], [seu nome], etc.
                                   - NÃO ofereça links, telefones ou emails de contato fictícios.
                                   - NÃO peça mais informações.
                                   - NÃO seja genérico ou vago.
                                   - Seja claro e direto ao ponto.
                                   - Escreva a resposta completa.
                                   - Não altere o nome do remetente nem o nome da empresa.
            
                                4. Você deve retornar SOMENTE o JSON.
                                   - Nada antes.
                                   - Nada depois.
                                   - Nada fora do objeto.
            
                                5. O JSON deve ter exatamente estas chaves:
                                {{
                                    "classification": "<Produtivo/Improdutivo>",
                                    "suggestedResponse": "Prezado(a) {email_sender}, <sua resposta aqui> Atenciosamente, {company_name}"
                                }}
            
                                6. NÃO use markdown, NÃO explique nada, NÃO coloque texto fora do JSON.
            
                                Agora gere o JSON final.
                                """

        # Generate a string from the ai response
        text = self._generate_prompt(prompt)

        # Try to extract JSON from the response
        m = re.search(r'\{.*\}', text, re.S)

        # if we found a JSON-like structure, try to parse it
        if m:
            json_str = m.group(0)
            try:
                parsed_json = json.loads(json_str)
                classification = parsed_json.get("classification")
                suggested_response = parsed_json.get("suggestedResponse")
                return {
                    "classification": classification,
                    "suggestedResponse": suggested_response
                }
            except json.JSONDecodeError:
                cleaned = json_str.replace('\n', ' ').strip()
                cleaned = re.sub(r'\s+', ' ', cleaned)
                try:
                    parsed_json = json.loads(cleaned)
                    return {
                        "classification": parsed_json.get("classification", ""),
                        "suggestedResponse": parsed_json.get("suggestedResponse", "")
                    }
                except Exception:
                    pass

        # Fallback: infer classification and create a basic response
        inferred_class = "Produtivo" if "produtivo" in text.lower() else "Improdutivo"
        fallback_response = f"Prezado(a) {email_sender}, {text.strip()[:400]}... Atenciosamente, {company_name}"
        return {
            "classification": inferred_class,
            "suggestedResponse": fallback_response
        }

    def _generate_prompt(self, prompt):
        if self.provider == "gemini":
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )
            return response.text.strip()
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
