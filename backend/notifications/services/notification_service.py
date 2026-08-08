class NotificationService:

    def send(self, template, user):
        channel = template.channel

        if channel == "EMAIL":
            return self.send_email(template, user)

        if channel == "WHATSAPP":
            return self.send_whatsapp(template, user)

        if channel == "WEB_PUSH":
            return self.send_web_push(template, user)

        raise ValueError(f"Unsupported channel: {channel}")

    def send_email(self, template, user):
        return {
            "channel": "EMAIL",
            "status": "TEST"
        }

    def send_whatsapp(self, template, user):
        return {
            "channel": "WHATSAPP",
            "status": "TEST"
        }

    def send_web_push(self, template, user):
        return {
            "channel": "WEB_PUSH",
            "status": "TEST"
        }