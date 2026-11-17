from pathlib import Path

log_file = Path("logs/sample_auth.log")

failed_attempts = 0
successful_Attempts = 0
try:
    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
            if "Failed password" in line:
                failed_attempts += 1

            elif "Accepted password" in line:
                successful_Attempts += 1

    print("=== Relatorio ===")
    print(f"Tentativas bem-sucedidas: {successful_Attempts}")
    print(f"Tentativas mal-sucedidas: {failed_attempts}")

except FileNotFoundError:
    print("Erro: Aquivo de log nao encontrado")