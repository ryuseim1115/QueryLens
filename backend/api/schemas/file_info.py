from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class FileInfo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    file_name: str
