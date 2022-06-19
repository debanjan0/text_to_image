from flask import *
import json , requests
import gofile
from PIL import Image, ImageDraw, ImageFont

server = gofile.getServer()
font="antic.ttf"
font_size=20
width=200
height=70
font_color="black"
bg="white"
app = Flask(__name__)


def random_img():
    random_img_url = "https://api.unsplash.com/photos/random?client_id=bnM8gnAfsGv0X7xKNjwlnm0Mre0UPyNi6qCmdhybSm8"
    img_response = requests.get(random_img_url)
    img_url = img_response.json()["urls"]["regular"]
    response = requests.get(img_url)
    file = open("test_img.png", "wb")
    file.write(response.content)
    file.close()
    i = Image.open("test_img.png")
    width, height = i.size
    return width, height


def custom_photo(x):
    search_url = "https://api.unsplash.com/search/photos?page=1&query="+x+"&client_id=bnM8gnAfsGv0X7xKNjwlnm0Mre0UPyNi6qCmdhybSm8"
    img_response = requests.get(search_url)
    img_url = img_response.json()["results"][0]["urls"]["regular"]
    response = requests.get(img_url)
    file = open("test_img.png", "wb")
    file.write(response.content)
    file.close()
    i = Image.open("test_img.png")
    width, height = i.size
    return width, height


def create_text_2_img(message,font="antic.ttf",font_size=20,width=200,height=70,font_color="black",bg="white"):
    file_name = "name.png"
    font = ImageFont.truetype("arial.ttf", font_size)
    img = Image.new('RGB', (width, height), bg)
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(message, font=font)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2
    imgDraw.text((xText, yText), message, font=font, fill=font_color)
    img.save(file_name)
    upload_response = gofile.uploadFile(file_name)
    
    return upload_response


def create_text_2_img_bg(message,font="antic.ttf",font_size=20,font_color="grey"):
    width,height = random_img()
    font_size = int(height/100) * 10
    file_name = "name.png"
    font = ImageFont.truetype("arial.ttf", font_size)
    img = Image.open("test_img.png")
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(message, font=font)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2
    imgDraw.text((xText, yText), message, font=font, fill=font_color)
    img.save(file_name)
    upload_response = gofile.uploadFile(file_name)
    
    return upload_response


def create_text_2_custom_img_bg(message,x,font="antic.ttf",font_size=20,font_color="grey"):
    width,height = custom_photo(x)
    font_size = int(height/100) * 10
    file_name = "name.png"
    font = ImageFont.truetype("arial.ttf", font_size)
    img = Image.open("test_img.png")
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(message, font=font)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2
    imgDraw.text((xText, yText), message, font=font, fill=font_color)
    img.save(file_name)
    upload_response = gofile.uploadFile(file_name)
    
    return upload_response


@app.route('/',methods=['GET'])
def home_page():
    return render_template("index.html")

@app.route('/hello/',methods=['GET'])
def hello():
    # /hello/?test=aefd
    txt = str(request.args.get("test"))
    data_set = {"Massage":txt}
    
    json_dump = json.dumps(data_set)
    return json_dump



@app.route('/img/',methods=['GET'])
def img_page():
    # /img/?text=any text
    txt = str(request.args("text"))
        
    if None != (txt):
        data_set = create_text_2_img(txt)
    else:
        data_set = {"Massage":"All the values are required."}
    
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/custom-img/',methods=['GET'])
def custom_img_page():
    # /custom-img/?text=any text&fontsize=20&fontcolor=black&width=200&height=70&bg=white
    txt = str(request.args.get("text")) 
    fontsize = str(request.args.get("fontsize")) 
    fontcolor = str(request.args.get("fontcolor")) 
    width = str(request.args.get("width")) 
    height = str(request.args.get("height")) 
    bg = str(request.args.get("bg"))
        
    if None not in (txt, fontsize, fontsize, width, height, bg):
        data_set = create_text_2_img(txt,font="antic.ttf",font_size=int(fontsize),width=int(width),height=int(height),font_color=fontcolor,bg=bg)
    else:
        data_set = {"Massage":"All the values are required otherwise use the normal method"}
    
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/photo/',methods=['GET'])
def photo_page():
    # /photo/?text=any text
    user_query = str(request.args.get("text"))
    data_set = create_text_2_img_bg(user_query)
    
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/custom-photo/',methods=['GET'])
def custom_photo_page():
    # /custom-photo/?text=anytext&bg=kolkata
    txt = str(request.args.get("text"))
    x = str(request.args.get("bg"))
    data_set = create_text_2_custom_img_bg(txt,x)
    
    json_dump = json.dumps(data_set)
    return json_dump


if __name__=="__main__":
    app.run(port=7777)



