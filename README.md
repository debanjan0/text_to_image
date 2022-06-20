# text_to_image

This is a very simple text to image api which you can use to automate your social media posts, blogs, etc.

feel free to find any error or mistake and help in improving the code in github



## Documentation

Get the text with simple white background color ?

```https://texttoimg.herokuapp.com/img/?text=text```

|Feild|Requeird|Val|
|-----|--------|---|
|text|yes|the text you want to convert into img|

Exmaple :-
```https://texttoimg.herokuapp.com/img/?text=this is an exmaple```


Get the text with custom size & background color ?

```https://texttoimg.herokuapp.com/custom-img/?text=text&fontsize=value&fontcolor=value&width=value&height=value&bg=value```


|Feild|Requeird|Val|
|-----|--------|---|
|text|yes|the text you want to convert into img|
|fontsize|yes|Font size of the text|
|fontcolor|yes|Font color of the text|
|width|yes|The width of the image|
|height|yes|The heigth of the image|
|bg|yes|The background color|

Exmaple :-
```https://texttoimg.herokuapp.com/custom-img/?text=any text&fontsize=20&fontcolor=black&width=200&height=70&bg=white```


Get the text with a random backgroung image ?

```https://texttoimg.herokuapp.com/photo/?text=text```

|Feild|Requeird|Val|
|-----|--------|---|
|text|yes|the text you want to convert into img|


Exmaple :-
```https://texttoimg.herokuapp.com/photo/?text=any text```

Get the text with a specific backgroung image ?

```https://texttoimg.herokuapp.com/custom-photo/?text=text&bg=value```

|Feild|Requeird|Val|
|-----|--------|---|
|text|yes|the text you want to convert into img|
|bg|yes|The type of backdround image you want|

Exmaple :-
```https://texttoimg.herokuapp.com/custom-photo/?text=any text&bg=india```




