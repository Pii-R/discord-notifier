class Message:
    @staticmethod
    def format_daily_recap_message(daily_recap: dict) -> str:
        header = ""
        content = f"""
        Aujourd'hui:
        victoires: {daily_recap['wins']}
        défaites: {daily_recap["lost"]}
        """
        footer = ""

        return header + content + footer
