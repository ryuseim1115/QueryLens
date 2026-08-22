from datetime import timedelta

from config import SESSION_MAX_AGE_SECONDS
from infrastructure.mysql.delete_session_by_token import delete_session_by_token
from infrastructure.mysql.find_session_by_token import find_session_by_token
from infrastructure.mysql.insert_session import insert_session
from infrastructure.mysql.utcnow import utcnow
from infrastructure.security.session_token import generate_session_token
from sqlalchemy.orm import Session


# ログイン成功時に呼ばれる。サーバー側(sessionsテーブル)にトークンを新規発行する。
# Cookieへの書き込みはHTTP層の関心事なのでルータ側に任せ、ここではtokenを返すのみ
def create_session(db: Session, user_id: int) -> str:
    token = generate_session_token()
    expires_at = utcnow() + timedelta(seconds=SESSION_MAX_AGE_SECONDS)
    insert_session(db, user_id, token, expires_at)
    return token


# Cookieのトークンから、現在ログイン中のユーザーIDを解決する。
# 該当レコードが無い/期限切れの場合はNone(未ログイン扱い)を返す。
# 期限切れのレコードは、定期実行のクリーンアップジョブを別途持たない代わりに、
# アクセスされたタイミングで遅延削除する
def resolve_user_id(db: Session, token: str | None) -> int | None:
    if token is None:
        return None

    session = find_session_by_token(db, token)
    if session is None:
        return None

    if session.expires_at < utcnow():
        delete_session_by_token(db, token)
        return None

    return session.user_id


# ログアウト時に呼ばれる。該当トークンのセッションをサーバー側で失効させる。
# 既に無効なトークン(未ログイン状態からのログアウト等)を渡されても、
# 何もせず正常終了させてよい
def revoke_session(db: Session, token: str | None) -> None:
    if token is None:
        return
    delete_session_by_token(db, token)
