import random
import string

def gerar_chave_alfanumerica():
        letras = random.choices(string.ascii_letters, k=3)
        numeros = random.choices(string.digits, k=3)
        combinacao = letras + numeros
        random.shuffle(combinacao)  # Embaralha a ordem
        return ''.join(combinacao)