# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from typing import Optional, List
# import schemas, models, database
# from sqlalchemy.orm import Session
# from repos import check_login

# router = APIRouter()

# get_db = database.get_db

# logged_user = schemas.Logged.logged_user
# logged_user_name = schemas.Logged.logged_user_name
# checkLogin = check_login.loggedUser



# @router.post("/group/join-{group_name}")
# def join_group(*, db: Session = Depends(get_db), group_name: str, logged: bool, group_code: int):
#     check_login(logged)

#     data = db.query(models.Groups).filter(models.Groups.name == group_name).first()
#     if not data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No group with the given name has been found")

#     if data.places_taken == data.member_limit:
#         raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="The group is already full")
    
#     if group_code != data.code:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid group code")
    
#     user = db.query(models.Member).filter(models.Member.name == logged_user_name).first()
#     user.groupName = group_name
#     data.places_taken = data.places_taken + 1
#     db.flush()
#     db.commit()
#     return {"Data": f"You joined {group_name} successfully"}