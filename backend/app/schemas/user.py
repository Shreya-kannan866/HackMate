from pydantic import BaseModel, EmailStr, Field

# --- Shared Base Attributes ---
class UserBase(BaseModel):
    """Fields that are common to reading and writing user data."""
    username: str = Field(..., min_length=3, max_length=50, description="Unique display name")
    email: EmailStr

# --- Incoming Request Schemas ---
class UserCreate(UserBase):
    """Data required from the client when creating a new user (Registration)."""
    password: str = Field(..., min_length=6, description="Raw password string from the registration form")

class UserLogin(BaseModel):
    """Data required from the client when authenticating."""
    username: str
    password: str

# --- Outgoing Response Schemas ---
class UserResponse(UserBase):
    """Data safe to send back to the client. Never include the password hash here!"""
    id: int

    class Config:
        # This tells Pydantic to read standard SQLAlchemy model attributes 
        # (like user.id instead of user['id']) automatically.
        from_attributes = True