from pydantic import BaseModel, Field, model_validator


class RegisterInfo(BaseModel):
    # max_lengthはusersテーブルのusername列(String(50))に合わせている
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1)
    password_confirm: str = Field(min_length=1)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("パスワードが一致しません")
        return self
