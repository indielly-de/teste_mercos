from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Transaction(BaseModel):
    id_transaction: int = Field(..., alias="id_lancamento")
    competence_date: str = Field(..., alias="dt_competencia")
    cost_center_id: int = Field(..., alias="id_centro_custo")
    payment_method_id: int = Field(..., alias="id_forma_pagamento")
    due_date: str = Field(..., alias="dt_vencimento")
    payment_date: Optional[str] = Field(..., alias="dt_pagamento")
    periodicity: Optional[str] = Field(..., alias="ds_periodicidade")
    result_center_id: int = Field(..., alias="id_centro_resultado")
    amount: float = Field(..., alias="valor")

    @field_validator("competence_date", "due_date")
    def validate_date(cls, value):
        if not value:
            raise ValueError("Competence date is required")

        for format in ["%Y-%m-%d", "%d/%m/%Y"]:
            try:
                return datetime.strptime(value, format).date()
            except ValueError:
                pass

        raise ValueError("Invalid date format")
