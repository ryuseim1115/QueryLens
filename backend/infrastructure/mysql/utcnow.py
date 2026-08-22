from datetime import UTC, datetime


# MySQLのDATETIME型はtzinfoを保持できないため、常にUTCの時刻をtzinfo無しで
# 扱う(=naiveだが実質UTCという約束事にする)。datetime.utcnow()は非推奨なため、
# timezone-awareな現在時刻からtzinfoだけ落として使う
def utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)
