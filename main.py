from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
import tensorflow as tf
from sqlalchemy import func

from models import User, Business, session
from dependencies import verify_token
from icecream import ic

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail},
    )


recommender_path = "saved_model"
recommender = tf.saved_model.load(recommender_path)


@app.get("/")
async def root():
    return {"error": False, "message": "KuToKo Recommendation System"}


@app.get("/v1/users/{uuid}/recommendation")
async def businesses_recommendation(uuid: str, authorization: str = Depends(verify_token)):
    try:
        user = session.query(User).filter(User.id == uuid).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        serial = user.serial
        scores, titles = recommender([serial])
        titles = [title.decode("utf-8") for title in titles.numpy()[0]]
        businesses = session.query(Business.id).filter(Business.name.in_(titles)).all()
        businesses_ids = [business.id for business in businesses]
        return {"error": False, "message": "Success", "data": businesses_ids}
    except (ValueError, KeyError):
        raise HTTPException(status_code=500, detail="Something went wrong")


@app.get("/v1/businesses/{uuid}/similar")
async def businesses_similar(uuid: str, authorization: str = Depends(verify_token)):
    try:
        # TODO: Implement this
        business = session.query(Business).filter(Business.id == uuid).first()
        if business is None:
            raise HTTPException(status_code=404, detail="Business not found")

        # make dummy limit 10 businesses random
        businesses = session.query(Business.id).order_by(func.random()).limit(10).all()
        businesses_ids = [business.id for business in businesses]
        return {"error": False, "message": "Success", "data": businesses_ids}
    except (ValueError, KeyError):
        raise HTTPException(status_code=500, detail="Something went wrong")
