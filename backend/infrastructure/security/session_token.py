import secrets


# ログイン成功時に呼ばれ、推測不可能なランダムトークンを生成する。
# このトークンはDBに書き込まれ、以降はログインしているかを確認するために使われる
def generate_session_token() -> str:
    return secrets.token_urlsafe(32)
