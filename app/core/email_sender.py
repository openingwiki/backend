"""
Email sender.
"""
import requests


def send_email(emails_domen_name: str, mailgun_api_key: str, to: str, subject: str, text: str) -> requests.Response:
	"""
	Function for email sending.
	
	Parameters:
		email_domen_name: str - domen registered for email sending in mailgun.
		mailgun_api_key: str - mailgun api key.
		to: str - email adress to send.
		subject: str - letter subject.
		text: str - letter text.
	
	Returns:
		requests.Response - mailgun api response.
	"""
	return requests.post(
        f"https://api.eu.mailgun.net/v3/{emails_domen_name}/messages",
        auth=("api", f"{mailgun_api_key}"),
		data={"from": "no-reply@opening.wiki", "to": [to], "subject": subject, "text": text},
	)