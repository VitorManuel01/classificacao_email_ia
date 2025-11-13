from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
from google import genai

from openai import OpenAI


class AIProvider:
    def __init__(self, provider="gemini"):
        self.provider = provider.lower()

        if self.provider == "gemini":
            self.client = genai.Client()
        elif self.provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        else:
            raise ValueError("Unsupported AI provider. Choose 'gemini' or 'openai'.")

    # def classify(self, texto_email):
    #     prompt = f"Classifique o seguinte email como 'produtivo' ou 'improdutivo':\n\n\"{texto_email}\"\n\nResponda apenas com 'produtivo' ou 'improdutivo'.\n\nCategorias:\n- Produtivo: {categoria_produtivo_desc}\n- Improdutivo: {categoria_improdutivo_desc}"
    #     return self._generate_prompt(prompt)
    #
    # def suggest_response(self, texto_email, categoria):
    #     if categoria == "produtivo":
    #         prompt = f"Com base no seguinte email classificado como 'produtivo', sugira uma resposta adequada:\n\n\"{texto_email}\"\n\nForneça uma resposta clara e profissional. Faça apenas 1 sugestão que de fato ajude o problema apresentado no email."
    #     else:
    #         prompt = f"Com base no seguinte email classificado como 'improdutivo', sugira uma resposta breve ou educada para indicar que o email foi recebido, mas não requer ação:\n\n\"{texto_email}\"\n\nForneça uma resposta curta e educada."
    #     return self._generate_prompt(prompt)

    def analyse_email(self, texto_email):
        categoria_produtivo_desc = "Emails que requerem uma ação ou resposta específica como solicitações, atualização sobre caso em aberto ou dúvidas."
        categoria_improdutivo_desc = "Emails que não requerem ação ou resposta, como newsletters ou anúncios."

        prompt = f"""Analíse o seguinte email: \n\n\"{texto_email}\"\n\n
        
        Passos a seguir: 
        1. Classifique o email com base nos seguintes critérios: Produtivo: {categoria_produtivo_desc}\n\n Improdutivo: {categoria_improdutivo_desc}.
        2. Se o email for classificado como 'Produtivo', sugira uma resposta adequada, profissional, direta e que de fato ajude o problema proposto no email. Se for 'Improdutivo', sugira uma resposta breve ou educada para indicar que o email foi recebido, mas não requer ação.
        3. Forneça apenas 1 sugestão de resposta.
        4. Ao aprensentar a categoria seguindo o formato abaixo, não inclua nenhuma outra informação além do solicitado.
        5. Responda no seguinte formato:
        Categoria: <produtivo/improdutivo>
        <sua resposta aqui>
        """
        return self._generate_prompt(prompt)


    def _generate_prompt(self, prompt):
        if self.provider == "gemini":
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
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
