from pydantic import BaseModel, Field, ConfigDict

from app.handler.commands.command_activity_coef import HandlerCommandActivityCoef
from app.handler.commands.command_exports import HandlerExport
from app.handler.commands.command_statistics import HandlerStatistics
from app.handler.handler_edit_weight import HandlerEditWeight


class HandlersModel(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    handler_edit_weight: HandlerEditWeight | None = Field(None)
    handler_activity_coef: HandlerCommandActivityCoef | None = Field(None)
    handler_statistics: HandlerStatistics | None = Field(None)
    handler_export: HandlerExport | None = Field(None)
