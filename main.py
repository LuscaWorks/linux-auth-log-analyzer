from pathlib import Path
from analyzer import analyze_log_file, save_report

LOG_FILE = Path("logs/sample_auth.log")
REPORT_FILE = Path("reports/report.json")

def main():

    try:
        report = analyze_log_file(LOG_FILE)

        print("=== RELATORIO ===")

        print(
            f"Tentativas bem-sucedidas: "
            f"{report['summary']['successful_logins']}"
        )

        print(
            f"Tentativas mal-sucedidas: "
            f"{report['summary']['failed_logins']}"
        )

        print("=== ANALISE DE IPs ===")

        for ip, data in report["ip_analysis"].items():

            print(f"IP: {ip}")
            print(f"Falhas: {data['failed_attempts']}")
            print(f"Classificacao: {data['classification']}")

        print("=== EVENTOS DE LOGIN ===")

        for event in report["failed_events"]:
            print(
                f"Falha | Usuario: {event['user']} "
                f"| IP: {event['ip']}"
            )

        for event in report["successful_events"]:
            print(
                f"Sucesso | Usuario: {event['user']} "
                f"| IP: {event['ip']}"
            )

        save_report(report, REPORT_FILE)

        print(f"\nRelatorio JSON salvo em: {REPORT_FILE}")

    except FileNotFoundError:
        print("Erro: arquivo de log nao encontrado.")

if __name__ == "__main__":
    main()
