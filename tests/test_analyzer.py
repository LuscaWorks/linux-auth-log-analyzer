import json
import pytest

from analyzer import (
    parse_log_line,
    classify_ip,
    analyze_log_file,
    save_report
)


def test_parse_failed_login():

    line = (
        "Nov 16 10:00:01 server sshd[1234]: "
        "Failed password for invalid user admin "
        "from 203.0.113.50 port 5001 ssh2"
    )

    result = parse_log_line(line)

    assert result == {
        "status": "failed",
        "user": "admin",
        "ip": "203.0.113.50"
    }


def test_parse_successful_login():

    line = (
        "Nov 16 10:01:12 server sshd[1237]: "
        "Accepted password for lucas "
        "from 192.0.2.25 port 5004 ssh2"
    )

    result = parse_log_line(line)

    assert result == {
        "status": "success",
        "user": "lucas",
        "ip": "192.0.2.25"
    }


def test_ignore_unrecognized_line():

    line = "Nov 16 10:05:00 server systemd[100]: Service started"

    result = parse_log_line(line)

    assert result is None


@pytest.mark.parametrize(
    "count, expected",
    [
        (1, "NORMAL"),
        (3, "ATENCAO"),
        (5, "ALTO RISCO")
    ]
)
def test_classify_ip(count, expected):

    result = classify_ip(count)

    assert result == expected


def test_analyze_log_file(tmp_path):

    log_file = tmp_path / "sample_auth.log"

    logs = [
        "Nov 16 10:00:01 server sshd[1]: Failed password for admin from 203.0.113.50 port 5001 ssh2",
        "Nov 16 10:00:02 server sshd[2]: Failed password for admin from 203.0.113.50 port 5002 ssh2",
        "Nov 16 10:00:03 server sshd[3]: Failed password for root from 203.0.113.50 port 5003 ssh2",
        "Nov 16 10:01:12 server sshd[4]: Accepted password for lucas from 192.0.2.25 port 5004 ssh2",
        "Nov 16 10:02:15 server sshd[5]: Failed password for test from 198.51.100.23 port 5005 ssh2"
    ]

    log_file.write_text("\n".join(logs), encoding="utf-8")

    report = analyze_log_file(log_file)

    assert report["summary"]["failed_logins"] == 4
    assert report["summary"]["successful_logins"] == 1
    assert report["summary"]["total_ips_with_failed_logins"] == 2

    assert report["ip_analysis"]["203.0.113.50"]["classification"] == "ATENCAO"
    assert report["ip_analysis"]["198.51.100.23"]["classification"] == "NORMAL"


def test_save_report(tmp_path):

    report = {
        "summary": {
            "failed_logins": 3
        }
    }

    output_file = tmp_path / "reports" / "report.json"

    save_report(report, output_file)

    saved_report = json.loads(
        output_file.read_text(encoding="utf-8")
    )

    assert saved_report == report
