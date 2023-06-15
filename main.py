from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
import tensorflow as tf
import joblib

from models import User, Business, session
from dependencies import verify_token

app = FastAPI()
recommendation = tf.saved_model.load('saved_models/recommendation')
similar = tf.keras.models.load_model('saved_models/similar.h5')
vectorized = joblib.load('saved_models/vectorized.joblib')


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail},
    )


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
        scores, titles = recommendation([serial])
        titles = [title.decode("utf-8") for title in titles.numpy()[0]]
        businesses = session.query(Business.id).filter(Business.name.in_(titles)).all()
        businesses_ids = [business.id for business in businesses]
        return {"error": False, "message": "Success", "data": businesses_ids}
    except (ValueError, KeyError):
        raise HTTPException(status_code=500, detail="Something went wrong")


@app.get("/v1/businesses/{uuid}/similar")
async def businesses_similar(uuid: str, authorization: str = Depends(verify_token)):
    try:
        business = session.query(Business).filter(Business.id == uuid).first()
        if business is None:
            raise HTTPException(status_code=404, detail="Business not found")
        business_name = [business.name]
        business_vector = vectorized.transform(business_name)
        predictions = similar.predict(business_vector)
        similar_indices = predictions.argsort()[0][-5:]
        serials = similar_indices.tolist()
        businesses = session.query(Business.id).filter(Business.serial.in_(serials)).all()
        businesses_ids = [business.id for business in businesses]
        return {"error": False, "message": "Success", "data": businesses_ids}
    except (ValueError, KeyError):
        raise HTTPException(status_code=500, detail="Something went wrong")
