from pydantic import BaseModel
from datetime import date

class FarmerJoinDTO(BaseModel):
    class DTO(BaseModel):
        user_id_farmer: str
        user_email: str
        user_password: str
        user_name: str
        user_birth: date
        user_type: str
        phone_number: str
        address: str
        city: str
        state: str
        postal_code: str
        farm_address: str
        animal_types: str
        license_number_farmer: str
    data: DTO

class UserLoginDTO(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str
    type: str