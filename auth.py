import main
from fastapi import APIRouter, HTTPException, status, Form
from schema import UserLoginSchema
from security import pwd_context, create_access_token

authrouter = APIRouter()

UPLOAD_DIRECTORY = "uploads"
BASE_URL = "http://localhost:8000"

# UPLOAD_DIRECTORY.mkdir(exist_ok=True)


@authrouter.post("/api/user/auth/sign-up")
def user_signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):

    hashed_password = pwd_context.hash(password)

    main.cursor.execute("""INSERT INTO users (name,email,password) VALUES(%s,%s,%s)""",
                        (name, email, hashed_password))
    main.conn.commit()

    return "Sign Up Successfully!!"


@authrouter.post("/api/user/auth/login")
def user_login(login_data: UserLoginSchema):
    email = login_data.email
    password = login_data.password

    main.cursor.execute("""SELECT * FROM users WHERE  email = %s""",
                        (email,))

    user = main.cursor.fetchone()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
    user = dict(user)
    user_password_db = user.get("password")

    if not pwd_context.verify(password, user_password_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="password is not correct!!"
        )

    else:
        user_id_db = user.get("id")
        user_email_db = user.get("email")

        return create_access_token({"id": user_id_db,
                                    "email": user_email_db})

