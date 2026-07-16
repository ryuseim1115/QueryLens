from fastapi import HTTPException, Request


class NotLoggedInError(Exception):
    pass


def _get_user_id_or_raise(request: Request, error: Exception) -> int:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise error
    return user_id


# JSのfetch()から呼ばれるAPI用。fetch()はリダイレクトを自動追跡してしまうため、
# ここでリダイレクトを返すとJS側が401を検知できず壊れる。必ず401を返すこと。
def require_login_api(request: Request) -> int:
    return _get_user_id_or_raise(
        request, HTTPException(status_code=401, detail="ログインが必要です")
    )


# ブラウザが直接開くページ用。401(生のJSON)をそのまま返すと画面に表示されて
# しまうため、NotLoggedInErrorを投げてmain.pyの例外ハンドラーで/loginへ
# リダイレクトさせる。
def require_login_page(request: Request) -> int:
    return _get_user_id_or_raise(request, NotLoggedInError())
