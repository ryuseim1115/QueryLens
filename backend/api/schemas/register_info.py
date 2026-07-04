from pydantic import BaseModel, model_validator


class RegisterInfo(BaseModel):
    username: str
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("パスワードが一致しません")
        return self
