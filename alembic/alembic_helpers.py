from alembic import op
from sqlalchemy import engine_from_config
from sqlalchemy.engine import reflection


def table_does_not_exist(table_name: str, schema: str | None = None) -> bool:
    config = op.get_context().config
    if not config:
        raise Exception("Could not get Alembic config")
    configuration = config.get_section(config.config_ini_section)
    if not configuration:
        raise Exception("Could not get Alembic config section")
    engine = engine_from_config(
        configuration=config.get_section(config.config_ini_section),  # type: ignore
        prefix="sqlalchemy.",
    )
    insp = reflection.Inspector.from_engine(engine)
    return insp.has_table(table_name, schema=schema) is False
