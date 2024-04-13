import os
from typing import Any, Callable, Dict, Optional

import pydantic


def user_configurable(
    default: Any = pydantic.Field(default=None, user_configurable=True),
    default_factory: Optional[Callable[[], Any]] = None,
    from_env: Optional[str | Callable[[], Any]] = None,
    description: str = "",
) -> pydantic.Field:
    return pydantic.Field(
        default=default,
        default_factory=default_factory,
        from_env=from_env,
        description=description,
        user_configurable=True,
    )


class SystemConfiguration(pydantic.BaseModel):
    def get_user_config(self) -> Dict[str, Any]:
        return _recurse_user_config_values(self)

    @classmethod
    def from_env(cls):
        def infer_field_value(field: pydantic.fields.ModelField):
            default_value = field.default
            if default_value is pydantic.Undefined:
                default_value = field.default_factory() if field.default_factory else None
            if from_env := field.field_info.extra.get("from_env"):
                val_from_env = os.getenv(from_env) if type(from_env) is str else from_env()
                if val_from_env is not None:
                    return val_from_env
            return default_value

        return _recursive_init_model(cls, infer_field_value)

    class Config:
        extra = "forbid"
        use_enum_values = True
        validate_assignment = True


class SystemSettings(pydantic.BaseModel):
    """A base class for all system settings."""

    name: str
    description: str

    class Config:
        extra = "forbid"
        use_enum_values = True
        validate_assignment = True


class Configurable:
    prefix: str = ""
    default_settings: Any

    @classmethod
    def get_user_config(cls) -> Dict[str, Any]:
        return _recurse_user_config_values(cls.default_settings)

    @classmethod
    def build_agent_configuration(cls, overrides: dict = {}) -> Any:
        base_config = _update_user_config_from_env(cls.default_settings)
        final_configuration = {**base_config, **overrides}
        return cls.default_settings.__class__.parse_obj(final_configuration)


def _update_user_config_from_env(instance: pydantic.BaseModel) -> Dict[str, Any]:
    def infer_field_value(field: pydantic.fields.ModelField, value):
        default_value = field.default
        if value == default_value and (from_env := field.field_info.extra.get("from_env")):
            val_from_env = os.getenv(from_env) if type(from_env) is str else from_env()
            if val_from_env is not None:
                return val_from_env
        return value

    def init_sub_config(model: type) -> Any:
        try:
            return model.from_env()
        except pydantic.ValidationError as e:
            if all(e.errors()[0]["type"] == "value_error.missing" for e in e.errors()):
                return None
            raise

    return _recurse_user_config_fields(instance, infer_field_value, init_sub_config)


def _recursive_init_model(
    model: type, infer_field_value: Callable[[pydantic.fields.ModelField], Any]
) -> Any:
    user_config_fields = {}
    for name, field in model.__fields__.items():
        if field.field_info.extra.get("user_configurable"):
            user_config_fields[name] = infer_field_value(field)
        elif issubclass(field.outer_type_, SystemConfiguration):
            try:
                user_config_fields[name] = _recursive_init_model(
                    model=field.outer_type_, infer_field_value=infer_field_value
                )
            except pydantic.ValidationError as e:
                if all(e.errors()[0]["type"] == "value_error.missing" for e in e.errors()):
                    user_config_fields[name] = None
                raise

    user_config_fields = {k: v for k, v in user_config_fields.items() if v is not None}

    return model.parse_obj(user_config_fields)


def _recurse_user_config_fields(
    model: pydantic.BaseModel,
    infer_field_value: Callable[[pydantic.fields.ModelField, Any], Any],
    init_sub_config: Optional[Callable[[type], Any]] = None,
) -> Dict[str, Any]:
    user_config_fields = {}

    for name, field in model.__fields__.items():
        value = getattr(model, name)

        if field.field_info.extra.get("user_configurable"):
            user_config_fields[name] = infer_field_value(field, value)

        elif isinstance(value, SystemConfiguration):
            user_config_fields[name] = _recurse_user_config_fields(
                model=value,
                infer_field_value=infer_field_value,
                init_sub_config=init_sub_config,
            )

        elif init_sub_config and value is None:
            sub_config_type =
