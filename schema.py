from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserNameChangeSchema(BaseModel):
    name: str


class UserPasswordChangeSchema(BaseModel):
    password: str


class AdminPasswordRecoverSchema(BaseModel):
    code: str
    new_password: str


class UserFeedbackSchema(BaseModel):
    user_id:int
    comment: str
    rating: int


class UserOrdersSchema(BaseModel):
    quantity: int
    shipping_address: str
    product_id: int
