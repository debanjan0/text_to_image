from flask import *
import json, requests, time, logging, sys, os

try:
    import requests
except ModuleNotFoundError:
    os.system("pip install requests")
    import requests

try:
    from PIL import Image, ImageDraw, ImageFont
except ModuleNotFoundError:
    os.system("pip install PIL")
    from PIL import Image

try:
    import gofile
except ModuleNotFoundError:
    os.system("pip install gofile")
    import gofile


app = Flask(__name__)
server = gofile.getServer()



app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


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


def random_img():
    random_img_url = "https://api.unsplash.com/photos/random?client_id=bnM8gnAfsGv0X7xKNjwlnm0Mre0UPyNi6qCmdhybSm8"
    img_response = requests.get(random_img_url)
    img_url = img_response.json()["urls"]["regular"]
    response = requests.get(img_url)
    file = open("test_img.png", "wb")
    file.write(response.content)
    file.close()


def reconstructText(words, breaks):                                                                             
    lines = []
    linebreaks = []
    i = 0 
    while True:
        linebreaks.append(breaks[i])
        i = breaks[i]
        if i == len(words):
            linebreaks.append(0)
            break
    for i in range( len(linebreaks) ):
        lines.append(' '.join(words[linebreaks[i-1] : linebreaks[i]]).strip())
    return lines


def badness(screenWidth, words, i, j):
    totalWidth = sum(len(word) for word in words[i : j]) + len(words[i : j]) - 1
    return float("inf") if totalWidth > screenWidth else (screenWidth - totalWidth) ** 3

        
def argmin(arr):
    return min(range(len(arr)), key=lambda x: arr[x])


def text_alingment(txt,screenWidth):
    words = txt.split()
    DP = [0] * (len(words) + 1)
    breaks = [0] * (len(words) + 1)
    for i in range(len(words) - 1, -1, -1):
        temp = [DP[j] + badness(screenWidth, words, i, j) for j in range(i+1,len(words)+1)]
        index = argmin(temp)
        breaks[i] = index + i + 1
    val = (reconstructText(words, breaks))
    
    return ('\n'.join(val)) , val


def most_common_used_color(width, height, img):
    r_total = 0
    g_total = 0
    b_total = 0
    img = img.convert('RGB')
 
    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
 
            r_total += r
            g_total += g
            b_total += b
            count += 1
 
    return r_total/count, g_total/count, b_total/count
 

def quotes_img_bg(x):
    quotes = x.json()[0]["q"]
    author = x.json()[0]["a"]
    width,height = 1080, 720
    random_img()
    # getting the alignment of the text and the total lines of the text
    aligned_text , total_line = text_alingment(quotes, 25)
    #calculate the font size according to the image size
    font_size = (int(height/200)+int(width/200)) * 10
    file_name = "name.png"
    img = Image.open("test_img.png")
    img.resize((width, height))    
    #getting the most common color in the image
    r, g, b = most_common_used_color(width,height,img)
    
    # qfont = ImageFont.truetype("arial.ttf", font_size)
    # afont = ImageFont.truetype("arial.ttf", int(font_size/2))
    
    qfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    afont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(font_size/2))
    
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(aligned_text, font=qfont)
    # xText = (width - (textWidth)) / 2
    
    #getting the y-axis for the text and the author
    yText = (height - (textHeight)) / 2
    author_yText = yText + int(len(total_line)*font_size)

    #for the quotes
    imgDraw.text((20, yText), aligned_text, font=qfont, fill=(int(255-r), int(255-g), int(255-b)))

    #for the author
    imgDraw.text((20, author_yText), author, font=afont, fill=(int(r), int(g), int(b)), align ="left")

    img.save(file_name)
    upload_response = gofile.uploadFile(file_name)
    
    return upload_response


def create_text_2_img(message,font="antic.ttf",font_size=20,width=200,height=70,font_color="black",bg="white"):
    file_name = "name.png"
    aligned_text , total_line = text_alingment(message, 20)
    # font = ImageFont.truetype("\static\arial.ttf", font_size)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    img = Image.new('RGB', (width, height), bg)
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(aligned_text, font=font)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2
    imgDraw.text((xText, yText), aligned_text, font=font, fill=font_color)
    img.save(file_name)
    upload_response = gofile.uploadFile(file_name)
    
    return upload_response


def create_text_2_img_bg(message,font="antic.ttf",font_size=20,font_color="grey"):
    width,height = random_img()
    aligned_text , total_line = text_alingment(message, 20)
    font_size = int(height/100) * 10
    file_name = "name.png"
    # font = ImageFont.truetype("/Library/fonts/Arial.ttf", font_size)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    img = Image.open("test_img.png")
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(aligned_text, font=font)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2
    imgDraw.text((xText, yText), aligned_text, font=font, fill=font_color)
    img.save(file_name)
    upload_response = gofile.uploadFile(file_name)
    
    return upload_response


def create_text_2_custom_img_bg(message,x,font="antic.ttf",font_size=20,font_color="grey"):
    width,height = custom_photo(x)
    aligned_text , total_line = text_alingment(message, 20)
    font_size = int(height/100) * 10
    file_name = "name.png"
    # font = ImageFont.truetype("/Library/fonts/Arial.ttf", font_size)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    img = Image.open("test_img.png")
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(aligned_text, font=font)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2
    imgDraw.text((xText, yText), aligned_text, font=font, fill=font_color)
    img.save(file_name)
    upload_response = gofile.uploadFile(file_name)
    
    return upload_response









@app.route('/',methods=['GET'])
def home_page():
    return render_template("index.html")


@app.route('/hello_having_fun/',methods=['GET'])
def hello():
    # /hello/?test=aefd
    txt = str(request.args.get("test"))
    data_set = {"Massage":txt}
    
    json_dump = json.dumps(data_set)
    return json_dump



@app.route('/img/',methods=['GET'])
def img_page():
    # /img/?text=any text
    txt = str(request.args.get("text"))
        
    data_set = create_text_2_img(txt)
    time.sleep(2)
    
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
    
    if fontsize == "None":
        fontsize = 20
    if fontcolor == "None":
        fontcolor = "black"
    if width == "None":
        width = 200
    if height == "None":
        height = 70
    if bg == "None":
        bg = "white"
        
    data_set = create_text_2_img(txt,font="antic.ttf",font_size=int(fontsize),width=int(width),height=int(height),font_color=fontcolor,bg=bg)
    
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


@app.route('/quotes',methods=['GET'])
def quotes():
    # /quotes/?text=anytext 
    random_quotes_url = "https://zenquotes.io/api/random/403e83af2c2c70b45002437b78b0371915590d4a"
    quotes_response = requests.get(random_quotes_url)    
    data_set = quotes_img_bg(quotes_response)
    
    json_dump = json.dumps(data_set)
    return json_dump




if __name__=="__main__":
    app.run(port=7777)


