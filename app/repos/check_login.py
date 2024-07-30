# from fastapi import HTTPException, status
# from schemas import Logged

# logged_user = Logged.logged_user

# def loggedUser(logged: bool):
#     if logged != logged_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")