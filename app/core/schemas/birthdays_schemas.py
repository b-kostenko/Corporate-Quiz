from datetime import datetime
from typing import Annotated

from pydantic import Field, BaseModel, computed_field, UUID4


class BirthdayInputSchema(BaseModel):
    person_name: str
    birth_date: datetime


class BirthdayOutputSchema(BaseModel):
    id: UUID4
    person_name: str
    birth_date: datetime

    @computed_field
    @property
    def age(self) -> Annotated[int, Field(gt=0, description="Age in years")]:
        today = datetime.today().date()
        birth_date = self.birth_date.date()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    class Config:
        from_attributes = True
