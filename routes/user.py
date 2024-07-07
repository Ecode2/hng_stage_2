from fastapi import APIRouter, Body, HTTPException, status
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from db.db import get_db
from db import models
from db.hash import Hash
from utils import create_access_token, get_current_user 
from schemas import LoginModel, OrganisationModel, UserModel


router = APIRouter(
    tags=["User Endpoints"],
    prefix="/api"
    )

@router.get("/organisations")
async def get_user_organisations(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    user = db.query(models.User).filter(models.User.email == current_user["email"]).first().__dict__

    organisations = []

    for orgid in user["organisation_id"]:
        org_info = db.query(models.Organisation).filter(models.Organisation.orgId == orgid).first().__dict__
        org_info.pop("user_id")
        organisations.append(org_info)
    
    return {
            "status": "success",
            "message": "Organisations Information",
            "data": {
                "organisations": organisations,
            }
        }

@router.post("/organisations", status_code=201)
async def create_new_organisation(org_info: OrganisationModel, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    try:
        new_org = models.Organisation(
            name = org_info.name,
            description = org_info.description,
            user_id = current_user["userId"]
        )

        db.add(new_org)
        db.commit()
        db.refresh(new_org)

        new_org_info = db.query(models.Organisation).filter(models.Organisation.name == org_info.name).first().__dict__
        new_org_info.pop("user_id")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=
                          {"status": "Bad request",
                           "message": "Client error",
                           "statusCode": 400})

    return {
            "status": "success",
            "message": "Organisation crested successfully",
            "data": {**new_org_info}
        }

@router.post("/organisations/{orgid}/users", status_code=200)
async def add_user_to_organisation(orgid: str, userId: str = Body(), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    user_organisation = db.query(models.Organisation).filter(models.Organisation.orgId == orgid)
    if user_organisation is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=
                          {"status": "Bad request",
                           "message": "Organisation not found",
                           "statusCode": 400})

    user_ids: list = user_organisation.__dict__["user_id"]
    user_ids.append(userId)

    user_organisation.update({models.User.organisation_id: user_ids})
    db.commit()

    return {
        "status": "success",
        "message": "User added to organisation successfully",
        }

@router.get("/organisations/{orgid}")
async def get_user_organisation(orgid: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    org_info = db.query(models.Organisation).filter(models.Organisation.orgId == orgid).first()
    
    if org_info is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=
                          {"status": "Bad request",
                           "message": "Organisation not found",
                           "statusCode": 400})
    org_info.__dict__.pop("user_id")

    return {
        "status": "success",
        "message": "User Information",
        "data": {**org_info.__dict__}
        }


@router.get("/users/{id}")
async def get_user_by_id(id: str, current_user: dict = Depends(get_current_user)):

    if id == current_user["userId"]:

        current_user.pop("password")
        return {
        "status": "success",
        "message": "User Information",
        "data": {**current_user}
        }

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=
                          {"status": "Bad request",
                           "message": "Authentication Failed",
                           "statusCode": 400})