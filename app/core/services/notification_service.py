from email.message import EmailMessage
from typing import List, Optional

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import EmailStr


class AsyncEmailSender:

    def __init__(self, host: str, port: int, username: str, password: str, use_tls: bool = True, templates_dir: str = "templates"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    async def send_email(
        self,
        subject: str,
        to_emails: List[str | EmailStr],
        template: str,
        payload: dict,
        from_email: Optional[str] = None
    ):
        html_content = self.env.get_template(template).render(payload)

        message = EmailMessage()
        message["From"] = from_email or self.username
        message["To"] = ", ".join(to_emails)
        message["Subject"] = subject
        message.add_alternative(html_content, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            start_tls=self.use_tls,
        )
