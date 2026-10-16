"""Pydantic model for CampusLearning Hub student registrations."""

from pydantic import BaseModel, EmailStr, Field


class Student(BaseModel):
    student_id: int
    name: str = Field(min_length=2)
    email: EmailStr
    age: int = Field(ge=16, le=100)
    course: str = Field(min_length=3)
