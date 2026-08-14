
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class TaskBase(BaseModel):
    title: str
    priority: str = Field(..., pattern="^(low|medium|high)$")
    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = Field(
        default=None,
        pattern="^(low|medium|high)$"
    )
    due_date: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError("Title cannot be blank")

        return value


class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    owner_id: int


class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True