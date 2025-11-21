from pydantic import BaseModel, Field, field_validator

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=4, max_length=50)

    @field_validator("name")
    def validate_name(cls,v):
        if not v.strip():
            raise ValueError("Category name cannot be empty")
        if not v.replace(" ","").isalpha():
            raise ValueError("Category name must contain only letters and spaces")
        return v


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True   # Pydantic v2 replacement for orm_mode
