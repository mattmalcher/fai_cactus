
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse

from fastai.vision import (open_image, load_learner)

from io import BytesIO
import uvicorn
import aiohttp

# Load Learner:
learner = load_learner(path=".", file="export.pkl")


# Define function to??
async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


app = Starlette()

# endpoint for classifier
@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    img = open_image(BytesIO(bytes))
    _, _, losses = learner.predict(img)
    return JSONResponse({
        "predictions": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    })

# landing page
@app.route("/")
def form(request):
    return HTMLResponse(
        """
        <h1>Cactus Classifier</h1>
        <p>Demo tool - API for classifying images of succulents. Can recognise: 
        <ul>
        <li>Purple Echeveria</li>
        <li>Lithops</li>
        <li>Crassula Ovata</li>
        <li>Haworthi Retusa</li>
        </ul>
        </p>
        
        <p>Will return a JSON of class labels and probabilities.</p>
            
        Please submit a succulent URL:
        <form action="/classify-url" method="get">
            <input type="url" name="url">
            <input type="submit" value="Fetch and analyze image">
        </form>
    """)

# run app
uvicorn.run(app, host="0.0.0.0", port=8008)

