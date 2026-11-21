from pathlib import Path
import json
import re


FAILED_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+)"
)

SUCCESSFUL_PATTERN = re.compile(
    r"Accepted password for (\S+) from (\S+)"
)

# Identifica eventos de autenticacao em uma linha de log.
def parse_log_line(line):

    failed_match = FAILED_PATTERN.search(line)

    if failed_match:
        return {
            "status": "failed",
            "user": failed_match.group(1),
            "ip": failed_match.group(2)
        }

    success_match = SUCCESSFUL_PATTERN.search(line)

    if success_match:
        return {
            "status": "success",
            "user": success_match.group(1),
            "ip": success_match.group(2)
        }

    return None

# Classifica um IP conforme a quantidade de falhas.
def classify_ip(count):


    if count >= 5:
        return "ALTO RISCO"

    elif count >= 3:
        return "ATENCAO"

    else:
        return "NORMAL"

# Le os logs e retorna um relatorio com os eventos encontrados.
def analyze_log_file(log_path):


    failed_events = []
    successful_events = []
    failed_by_ip = {}

    with Path(log_path).open("r", encoding="utf-8") as file:

        for line in file:

            event = parse_log_line(line)

            if event is None:
                continue

            if event["status"] == "failed":

                failed_events.append({
                    "user": event["user"],
                    "ip": event["ip"]
                })

                ip = event["ip"]
                failed_by_ip[ip] = failed_by_ip.get(ip, 0) + 1

            elif event["status"] == "success":

                successful_events.append({
                    "user": event["user"],
                    "ip": event["ip"]
                })

    ip_analysis = {}

    for ip, count in failed_by_ip.items():

        ip_analysis[ip] = {
            "failed_attempts": count,
            "classification": classify_ip(count)
        }

    report = {
        "summary": {
            "successful_logins": len(successful_events),
            "failed_logins": len(failed_events),
            "total_ips_with_failed_logins": len(failed_by_ip)
        },
        "ip_analysis": ip_analysis,
        "failed_events": failed_events,
        "successful_events": successful_events
    }

    return report

# Salva o relatorio em formato JSON.
def save_report(report, output_path):

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as json_file:

        json.dump(
            report,
            json_file,
            indent=4,
            ensure_ascii=False
        )
