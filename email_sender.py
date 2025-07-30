import pytest
import win32com.client as win32
from pathlib import Path
import re
import sys

# === Configuration ===
TEST_FILE = "gym_db.py"
REPORT_FILE = "report.html"
RECIPIENT = "Abretha.Begam@dell.com"  # Replace with actual email

# === Step 1: Run tests and generate HTML report ===
pytest.main([
    TEST_FILE,
    f"--html={REPORT_FILE}",
    "--self-contained-html"
])

# === Step 2: Parse report.html for summary ===
html_path = Path(REPORT_FILE)
passed = failed = skipped = 0

if html_path.exists():
    html_content = html_path.read_text(encoding="utf-8")

    match = re.search(r"(\d+)\s+Failed,.*?(\d+)\s+Passed,.*?(\d+)\s+Skipped", html_content, re.DOTALL)
    if match:
        failed = int(match.group(1))
        passed = int(match.group(2))
        skipped = int(match.group(3))

    # === Email HTML Body ===
    summary = f"""
    <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px;">
            <p>Dear Team,</p>

            <p>Please find below the <b>pytest automation test results</b> summary for <code>{TEST_FILE}</code>:</p>

            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; margin-top: 10px;">
                <thead style="background-color: #f2f2f2;">
                    <tr>
                        <th>Status</th>
                        <th>Count</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>✅ Passed</td><td><b>{passed}</b></td></tr>
                    <tr><td>❌ Failed</td><td><b>{failed}</b></td></tr>
                    <tr><td>⏭ Skipped</td><td><b>{skipped}</b></td></tr>
                </tbody>
            </table>

            <p style="margin-top: 15px;">
                The detailed HTML test report is attached for your reference.
            </p>

            <p>Best regards,<br>Your Automation Bot</p>
        </body>
    </html>
    """

    # === Step 3: Send Email via Outlook ===
    try:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = RECIPIENT
        mail.Subject = f"Test Report: {passed} Passed, {failed} Failed"
        mail.HTMLBody = summary
        mail.Attachments.Add(str(html_path.resolve()))
        mail.Send()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        sys.exit(1)
else:
    print("❌ Report file not found. Please ensure the pytest HTML report was generated.")
    sys.exit(1)
