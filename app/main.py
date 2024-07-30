from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List
import schemas, models, database
from sqlalchemy.orm import Session
# from routers import members, groups, auth
# from repos import check_login

app = FastAPI()

models.Base.metadata.create_all(database.engine)

get_db = database.get_db

# logged_user = schemas.Logged.logged_user
# logged_user_name = schemas.Logged.logged_user_name
# checkLogin = check_login.loggedUser

# def memberCount(groupName)

logged_user: bool = False
logged_user_name: str = None

def loggedUser(logged: bool):
    if logged != logged_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")

@app.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(schemas.Login), db: Session = Depends(get_db)):
    global logged_user, logged_user_name
    
    user = db.query(models.Member).filter(models.Member.name==request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")
    
    if not user.password == request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password credentials")

    logged_user = True
    logged_user_name = request.username
    return {"Data": f"Welcome back {request.username}"}
    


# app.include_router(members.router)
@app.post("/group/join-{group_name}")
def join_group(*, db: Session = Depends(get_db), group_name: str, logged: bool, group_code: int):
    loggedUser(logged)

    data = db.query(models.Groups).filter(models.Groups.name == group_name).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No group with the given name has been found")

    if data.places_taken == data.member_limit:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="The group is already full")
    
    if group_code != data.code:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid group code")
    
    user = db.query(models.Member).filter(models.Member.name == logged_user_name).first()
    user.groupName = group_name
    data.places_taken = data.places_taken + 1
    db.flush()
    db.commit()
    return {"Data": f"You joined {group_name} successfully"} 



@app.get("/group/{group_name}/show-members", response_model=List[schemas.ShowMember])
def show_members(*, db: Session = Depends(get_db), group_name: str, logged: bool):
    loggedUser(logged)
    data = db.query(models.Member).filter(models.Member.groupName == group_name).all()
    return data



@app.post("/members/sign-in")
def create_members(request: schemas.Members, db: Session = Depends(get_db)):
    global logged_user, logged_user_name

    data = db.query(models.Member).filter(models.Member.name == request.name).first()
    if data:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="This username is already in use")
    new_member = models.Member(name=request.name, age=request.age, city=request.city, password=request.password)
    db.add(new_member)
    db.flush()
    db.commit()
    db.refresh(new_member)
    logged_user = True
    logged_user_name = request.name
    return new_member



@app.get("/member/about", response_model=schemas.About)
def about_member(*, db: Session = Depends(get_db), login_confirmation: bool):
    loggedUser(login_confirmation)
    data = db.query(models.Member).filter(models.Member.name == logged_user_name).first()
    return data



@app.get("/member/messages-sent")
def show_messagesSent(login_confirmation: bool, limit: int = 10):
    loggedUser(login_confirmation)      
    return {"Data":f"Last {limit} Messages Sent"}



@app.get("/group", response_model=List[schemas.ShowGroup])
def show_groups(db: Session = Depends(get_db), limit: int = 10):
    data = db.query(models.Groups).limit(limit).all()
    return data



@app.post("/group/create")
def group_creation(*, request: schemas.Group, db: Session = Depends(get_db), logged: bool):
    loggedUser(logged)
    used_name = admin = db.query(models.Groups).filter(models.Groups.name == request.name).first()
    if used_name:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="This group name is already in use")
     
    new_group = models.Groups(name=request.name, member_limit=request.member_limit, code=request.code, admin_username=logged_user_name, places_taken = 1)
    admin = db.query(models.Member).filter(models.Member.name == logged_user_name).first()
    admin.admin_of_group = request.name
    admin.groupName = request.name
    db.add(new_group)
    db.flush()
    db.commit()
    db.refresh(new_group)
    return new_group