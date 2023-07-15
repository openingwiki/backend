import requests


def send_email(EMAILS_DOMEN_NAME: str, MAILGUN_API_KEY: str, to: str, subject: str, text: str) -> requests.Response:
    return requests.post(
		f"https://api.eu.mailgun.net/v3/{EMAILS_DOMEN_NAME}/messages",
		auth=(
            "api",
            f"{MAILGUN_API_KEY}"
        ),
		data={
                "from": "no-reply@opening.wiki",
			    "to": [to],
			    "subject": subject,
			    "text": text
        }
	)
