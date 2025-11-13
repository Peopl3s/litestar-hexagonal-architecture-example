from typing import final


class InfrastructureError(Exception): ...

@final
class DataMapperError(InfrastructureError): ...

@final
class SQLAlchemyReaderError(InfrastructureError): ...