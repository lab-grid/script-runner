import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from typing_extensions import Literal
from pydantic import BaseSettings, BaseModel

def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    encoding = settings.__config__.env_file_encoding
    return json.loads(Path('config.json').read_text(encoding))

class InputPathArg(BaseModel):
    env_var_name: str
    path_regex: str
    path_regex_match_group: int

class InputQueryArg(BaseModel):
    env_var_name: str
    query_var_name: str

class InputBodyArg(BaseModel):
    env_var_name: str
    body_jsonpath: str

class InputSettings(BaseModel):
    path_args: List[InputPathArg]
    query_args: List[InputQueryArg]
    body_args: List[InputBodyArg]

class JSONOutput(BaseModel):
    kind: Literal['stdout', 'stderr', 'file']
    format: Literal['json']

    input_path: str

class CSVOutputColumn(BaseModel):
    output_name: str
    input_name: str

    skip_list: Optional[List[str]]

class CSVOutput(BaseModel):
    kind: Literal['stdout', 'stderr', 'file']
    format: Literal['csv']

    input_path: str
    remapped_columns: Optional[List[CSVOutputColumn]]

class OutputSettings(BaseModel):
    results: Union[JSONOutput, CSVOutput]
    attachments: List[str]

class Settings(BaseSettings):
    celery_result_backend: Optional[str]
    celery_broker_url: Optional[str]

    command: List[str]
    command_rundir: Optional[str]
    command_rundir_base: Optional[str]
    inputs: InputSettings
    outputs: OutputSettings

    debug: Optional[bool]

    class Config:
        env_file_encoding = 'utf-8'

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                json_config_settings_source,
                env_settings,
                file_secret_settings,
            )


settings = Settings()
