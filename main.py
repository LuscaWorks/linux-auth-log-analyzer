from pathlib import Path
import re
import json

log_file = Path("logs/sample_auth.log")

failed_attempts = 0
successful_login = 0

failed_by_ip = {}
failed_events = []
successful_events = []
ip_analysis = {}

failed_pattern = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+)"
) 

succesful_pattern = re.compile(
    r"Accepted password for (\S+) from (\S+)"
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

                successful_events.append({
                    "user": username,
                    "ip": ip
                })

    print("=== Relatorio ===")
    print(f"Tentativas bem-sucedidas: {successful_login}")
    print(f"Tentativas mal-sucedidas: {failed_attempts}")
    print("=== Tentativas por IP ===")
    for ip, count in failed_by_ip.items():
        print(f"{ip}: {count} tentativa(s)")
        if count >= 5:
            print("Classificacao: Alto risco")
        elif count >= 3:
            print("Classificacao: Atenção")
        elif count > 0:
            print("Classificacao:Normal")
    print("=== Eventos de login ===")
    for event in failed_events:
        print(f"Falha | Usuario: {event['user']} | IP: {event['ip']}")
    for event in successful_events:
        print(f"Sucesso | Usuario: {event['user']} | IP: {event['ip']}\n")

    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    for ip, count in failed_by_ip.items():
        if count >= 5:
            classification = "ALTO RISCO"
        elif count >= 3:
            classification = "ATENCAO"
        else:
            classification = "NORMAL"
        ip_analysis[ip]= {
            "failed_attempts": count,
            "classification": classification
    }
    report = {
        "summary": {
            "successful_logins": successful_login,
            "failed_logins": failed_attempts,
            "total_ips_analyzed": len(failed_by_ip),
        },
        "ip_analysis": ip_analysis,
        "failed_events": failed_events,
        "successful_events": successful_events
    }
    report_path = reports_dir / "report.json"

    with report_path.open("w", encoding="utf-8") as json_file:
        json.dump(
            report,
            json_file,
            indent=4,
            ensure_ascii=False
    )

    print(f"Relatorio Json Salvo em {report_path}")


except FileNotFoundError:
    print("Erro: Aquivo de log nao encontrado")