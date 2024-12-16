from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import markdown
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, constr,field_validator,ValidationError
import data.config
from fastapi.responses import HTMLResponse
from typing import Optional
from.predict import Predictor

class FormData(BaseModel):
    postal_code : int 
    @field_validator('postal_code')
    def validate_postal_code(cls, v):
        if not isinstance(v, int):
            raise ValueError('Postal code must be an integer')
        if v < 1000 or v > 9999:
            raise ValueError('Postal code must be between 1000 and 9999')
        return v
    modelchoise : str
    subtype : str
    number_of_rooms : int
    living_area : float
    land_area : float
    garden : float
    terrace : float
    open_fire : Optional[str] = None
    furnished : Optional[str] = None
    swiming_pool : Optional[str] = None
    state_of_building : float
    equipped_kitchen : float
    







app = FastAPI()
subtype_options_html = "\n".join(
    f'<option value="{item}">{item.replace("_", " ").capitalize()}</option>'
    for item in data.config.SUBTYPE_LIST
)
# Указываем правильную директорию для шаблонов
templates = Jinja2Templates(directory="api/templates")
config = data.config.config
# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="data/static"), name="static")
about_md = Path("data/static/About.md").read_text()
html_content = markdown.markdown(about_md)
@app.get("/")
async def home(request: Request):
    context = {"request": request, "content": html_content,"config": config ,'options_html':subtype_options_html,'error_msg':None,'prediction':None}

    return templates.TemplateResponse("base.html", context)


@app.post("/predict",response_class=HTMLResponse)
async def submit_form(request : Request,
    postal_code: str = Form(),
    modelchoise = Form(...),
    subtype = Form(),
    number_of_rooms=Form(),
    living_area=Form(),
    furnished = Form(None),
    land_area = Form(),
    garden = Form(),
    terrace = Form(),
    open_fire = Form(None),
    swiming_pool = Form(None),
    state_of_building = Form(),
    equipped_kitchen = Form()
    ):
    context = {"request": request, 
               "content": html_content,
               "config": config ,
               'options_html':subtype_options_html,
               'error_msg':None,
               'prediction':None}
    try:
        form_data = FormData(
            postal_code=postal_code,
            modelchoise=modelchoise,
            subtype=subtype,
            number_of_rooms= number_of_rooms,
            living_area=living_area,
            furnished=furnished,
            land_area=land_area,
            garden=garden,
            terrace=terrace,
            open_fire = open_fire,
            swiming_pool = swiming_pool,
            state_of_building = state_of_building,
            equipped_kitchen = equipped_kitchen)
    except ValueError as e:
        context['error_msg'] = 'Something wrong with postal_code'
        return templates.TemplateResponse("base.html", context)
    predictor = Predictor(form_data=dict(form_data))
    prediction = predictor.model_selection()
    match form_data.modelchoise:
        case 'XGB':
            context['prediction'] = round(prediction[0],2)
        case 'Linear':
            context['prediction'] = round(prediction[0][0],2)
        case _:
            context['prediction'] = prediction

    return templates.TemplateResponse('base.html', context)
    

    
