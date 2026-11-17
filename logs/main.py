from pathlib import Path
import re

log_file = Path("logs/sample_auth.log")

failed_attempts = 0
successful_login = 0

failed_by_ip = {}
failed_events = []
succesful_events = []

failed_pattern = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+)"
) 

succesful_pattern = re.compile(
    r"succesful password for (\S+) from (\S+)"
)

try:
    with log_file.open("r", encoding="utf-8") as file:
        for line in file:

            failed_match = failed_pattern.search(line)
            success_match = succesful_pattern.search(line)

            if failed_match:

                username = failed_match.group(1)
                ip = failed_match.group(2)
                failed_attempts += 1
                failed_events.append({
                    "user": username,
                    "ip": ip
                })
                failed_by_ip[ip] = failed_by_ip.get(ip, 0) + 1

            elif success_match:
                username = success_match.group(1)
                ip = success_match.group(2)
                successful_login += 1

                succesful_events.append({
                    "user": username,
                    "ip": ip
                })

    print("=== Relatorio ===")
    print(f"Tentativas bem-sucedidas: {successful_login}")
    print(f"Tentativas mal-sucedidas: {failed_attempts}")
    print("=== Tentativas por IP ===")
    for ip, count in failed_by_ip.items():
        print(f"{ip}: {count} tentativa(s)")
    print("=== Eventos de login")
    for event in failed_events:
        print(f"Falha | Usuario: {event['user']} | IP: {event['ip']}")
    for event in succesful_events:
        print(f"Sucesso | Usuario: {event['user']} | IP: {event['ip']}\n")

except FileNotFoundError:
    print("Erro: Aquivo de log nao encontrado")