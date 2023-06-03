from fastapi import FastAPI

app = FastAPI()
dummy_uuid = [
    '00823b94-5cd1-4a77-90ba-67824d0e621b',
    '00e78ec5-12db-4312-b9cc-078e15dfd4d0',
    '00f2ea6d-487f-45f3-9ad9-cef8bb2506f8'
]


@app.get("/")
async def root():
    return {"error": False, "message": "KuToKo API"}


@app.get("/v1/users/{uuid}/recommendation")
async def businesses_recommendation(uuid: str):
    return {"error": False, "message": "Success", "data": dummy_uuid}


@app.get("/v1/businesses/{uuid}/similar")
async def businesses_similar(uuid: str):
    return {"error": False, "message": "Success", "data": dummy_uuid}
