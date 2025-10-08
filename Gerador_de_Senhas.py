# Gerador de Senhas Seguras em Python
# - Comprimento customizável
# - Incluir/excluir maiúsculas, minúsculas, dígitos e símbolos
# - Evitar caracteres ambíguos (0,O,l,1,i)
# - Copiar para área de transferência (se pyperclip estiver instalado)
# - Exibe entropia estimada e classificação de força

import secrets
import string
import math

# Caracteres ambíguos que podem ser evitados
AMBIGUOUS = set("O0oIl1|`'\".,;:")


def build_charset(use_upper=True, use_lower=True, use_digits=True, use_symbols=True, avoid_ambiguous=False):
    charset = ""
    if use_upper:
        charset += string.ascii_uppercase
    if use_lower:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += "!@#$%^&*()-_=+[]{}<>?/\\~"

    if avoid_ambiguous:
        charset = "".join(ch for ch in charset if ch not in AMBIGUOUS)

    # Remove duplicatas e mantém a ordem original
    return "".join(sorted(set(charset), key=lambda x: charset.index(x)))


def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True, avoid_ambiguous=False):
    if length <= 0:
        raise ValueError("O comprimento deve ser maior que zero.")
    charset = build_charset(use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous)
    if not charset:
        raise ValueError("Charset vazio. Ative pelo menos uma categoria de caracteres.")

    # Usa secrets.choice para gerar senhas criptograficamente seguras
    return "".join(secrets.choice(charset) for _ in range(length))


def estimate_entropy_bits(length, charset_size):
    # Entropia aproximada: bits = length * log2(charset_size)
    if charset_size <= 1:
        return 0.0
    return length * math.log2(charset_size)


def classify_entropy(bits):
    if bits < 28:
        return "Fraca"
    elif bits < 56:
        return "Média"
    elif bits < 80:
        return "Forte"
    else:
        return "Muito forte"


def main():
    print("Gerador de Senhas Seguras\n----------")

    try:
        length = int(input("Comprimento da senha (recomendado 12-20): ") or "16")
    except ValueError:
        print("Valor inválido. Usando 16.")
        length = 16

    use_upper = input("Incluir letras maiúsculas? (S/n): ").strip().lower() != "n"
    use_lower = input("Incluir letras minúsculas? (S/n): ").strip().lower() != "n"
    use_digits = input("Incluir dígitos? (S/n): ").strip().lower() != "n"
    use_symbols = input("Incluir símbolos? (S/n): ").strip().lower() != "n"
    avoid_ambiguous = input("Evitar caracteres ambíguos (O,0,l,1 etc.)? (S/n): ").strip().lower() != "n"

    pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous)
    charset = build_charset(use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous)
    bits = estimate_entropy_bits(len(pwd), len(charset))
    classification = classify_entropy(bits)

    print("\nSenha gerada:")
    print(pwd)
    print(f"\nComprimento: {len(pwd)} | Tamanho do charset: {len(charset)} | Entropia aprox.: {bits:.1f} bits ({classification})")

    # Copiar para a área de transferência (opcional)
    try:
        import pyperclip
        pyperclip.copy(pwd)
        print("(Senha copiada para a área de transferência.)")
    except Exception:
        print("(pyperclip não disponível; instale com: pip install pyperclip para suporte ao clipboard)")


if __name__ == "__main__":
    main()
