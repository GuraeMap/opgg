import bcrypt


class PasswordBcrypt:

    @staticmethod
    def generate_password_hash(password: str):
        """
        Password 암호화
        """
        return (bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())).decode(
            "utf-8"
        )

    @staticmethod
    def check_password_hash(password: str, saved_password) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), saved_password.encode("utf-8"))
