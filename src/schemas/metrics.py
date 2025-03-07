from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Metric(BaseModel):
    metric_description: str = Field(..., alias="ds_metrica")
    reference_date: str = Field(..., alias="dt_referencia")
    acquisition_channel: str = Field(..., alias="ds_canal_aquisicao")
    segment: str = Field(..., alias="ds_segmento")
    total: float

    @field_validator("reference_date")
    def validate_date(cls, value):
        for format in ["%Y-%m-%d", "%d/%m/%Y"]:
            try:
                return datetime.strptime(value, format).date()
            except ValueError:
                pass

        raise ValueError("Invalid date format")
