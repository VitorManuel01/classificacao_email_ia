from ai_provider import AIProvider

if __name__ == "__main__":
    email = """
    Olá, estou com um problema para acessar minha conta. 
    O site diz que minha senha está incorreta, mas tenho certeza que está certa.
    """

    ia = AIProvider(provider="gemini")
    resposta = ia.analyse_email(email)
    print(f"{resposta}")