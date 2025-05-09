import main
from fastapi import APIRouter, HTTPException, status, Form, UploadFile, File
from schema import UserLoginSchema
from security import pwd_context, create_access_token
import shutil

authrouter = APIRouter()

UPLOAD_DIRECTORY = "uploads"
BASE_URL = "http://localhost:8000"

# UPLOAD_DIRECTORY.mkdir(exist_ok=True)


@authrouter.post("/api/user/auth/sign-up")
def user_signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(None),
):

    image_name = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxANEhAODg0NDw0NDg0PDQ4NEBANDQ4QFhEXFhUVFRMYHSggGBolGxMTITEhJikrLi4uFyAzODMsNygtLisBCgoKDQ0NEA0PDysZFRkrLTctNzctKysrLTcrKystKzc3LSsrNysrLSsrNysrKy0rKysrKysrKysrKysrKysrK//AABEIAOEA4QMBIgACEQEDEQH/xAAbAAEAAwEBAQEAAAAAAAAAAAAAAQQFBgMCB//EADQQAQACAAMEBQsFAQEAAAAAAAABAgMFEQQhMVESQVJhkhUiMjNxgaGxssHREyNCcpGCc//EABYBAQEBAAAAAAAAAAAAAAAAAAABAv/EABYRAQEBAAAAAAAAAAAAAAAAAAABEf/aAAwDAQACEQMRAD8A/RAG2QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfX6kgPkAAAAAAAAAAAAECpEAiQAAAAAAAAAAAAAAAAAAAAAAAIjXd1tHZMqm2+86R1RHF75TsMV/ctvtPCJ6mpozaqrhZfhU4V1nnOqxXDrH8Y/wAfQivO2BSeNY3qmPldLejHRnu4L4I5radjvhelGsdUxweDqsSkWiazwmJiXPbds04VtONZ31lqCsAqAAAAAAAAAAAAAAAAAAC5lezxiX3xrWu+VKW7kuHpTpab7SlVoRAkZVAlAAJBCtt2zxiVndvjfXuWkCOTnlyJWcxw4piWiI47+5Wa0AFQAAAAAAAAAAAAAAABDptirpSvV5sOZdRsvoU/rX5JVewhLKgAAACJSiQYudxpas6cYnXv4M1qZ9xw/Zb7MtUAGkAAAAAAAAAAAAAAAAQ6TLsTpYdZ5Rp/m5zjWyTHjzqTx4xySq1xCWVAAAAEJfN7aRMzwgGHnWLreK9mPnooQ9NqxOna1uczMa8nlDSJAVAQkAAAAAAAAAAAAAAB94GJNLRaOMS+CCq6jAxoxKxaJjv06pernNg2z9Gd+vRnjH3dBh4kWiJid0sK+wAAAGVm+17pw68d3S+axmG2xhRMRvvMTEadU85YFrTMzMzrM8VkR8pBpAAAAAAAAAAAAAAAAAAAgIFQ9tn2q+H6M7uU74eQg1tnznqvX3wsxm2F2p8Nvw58MG7fN8ONdNZ5bpj5qWLmuJbhpWO7izzUwfV7zaZmZmZnmhAqJAAAAAAAAAAAAAAAAAgB9YeHa86ViZ+S9sOW9PffWK7tI65bOFg1pGlaxGiarHwMptO+09HuXKZRhxxm8++Pw0BlVLyVhdmfFJ5LwuzPildAUvJWF2Z8Uo8lYXZnxSvAKPkrC7M+KTyVhdmfFK8Ao+SsLsz4pfNsow54TePZMfeGgAyb5LH8cSffXVUxssxa/wAelHOs6/Di6EXUxyVomN0xMTyndI6jH2emJGl6xPf1x7JYe3ZfbC86POpz649qyimAqAAAAAAAAAAENbLsu/nf3Qr5Ts3Tt0p4V+bfiGbViIhIIqEgAAAAAAAAAAAiY13TwlIDBzPYf0/Pr6Ezvjsz+FB1d6RaJrMaxMaTDmtrwJwrTWerfE846mpUeICoAAAAAAJpWbTERxmYiEL+TYPSv0p4UjX3zw+5VbGybPGFWKx755z1y9gYUAAAAAAAAAAAAAAAAZ2dYHSp04404/1lovjGp0q2r2qzHwByohLbIAAAAAA28ir5lp530/yI/LEb+TR+1Hfa0/HT7JVi8AyoAAAAAAAAAAAAAAAAADldorpe8cr2j4vh67X6zE/9L/VLybZAAAAAAHQ5R6qv/X1S550GUeqr7bfVKVYugMqAAAAAAAAAAAAAAAAAA5nbo/cxP72eCzmcaYt/bHyhWbQAEAAAAHQZR6qvtt9UglWLoDKgAAAAAAAAAAAAAAAIkhIDnc19bf8A5+mFQG4gAIAA/9k="
    if file:
        file_path = f"{UPLOAD_DIRECTORY}/{file.filename}"

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            image_name = f"{BASE_URL}/uploads/{file.filename}"
        except PermissionError:
            raise HTTPException(status_code=500, detail="Permission denied: Cannot write to 'uploads' directory.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File write error: {str(e)}")

    hashed_password = pwd_context.hash(password)

    main.cursor.execute("""INSERT INTO users (name,email,password,image_name) VALUES(%s,%s,%s,%s)""",
                        (name, email, hashed_password, image_name))
    main.conn.commit()

    return "Sign Up Successfully!!"


@authrouter.post("/api/user/auth/login")
def user_login(login_data: UserLoginSchema):
    email = login_data.email
    password = login_data.password

    main.cursor.execute("""SELECT * FROM users WHERE  email = %s""",
                        (email,))

    user = main.cursor.fetchone()
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

