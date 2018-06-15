import ipywidgets as widgets
from IPython.display import display

def on_incorrect_clicked(b):
    print("Please try again.")

def on_correct_clicked(b):
    print("Correct.")

button1 = widgets.Button(description='a. Ozone levels decrease with elevation',layout=widgets.Layout(width='40%', height='40px'))
button2 = widgets.Button(description='b. Wealthy people spend more time outdoors',layout=widgets.Layout(width='40%', height='40px'))
button3 = widgets.Button(description='c. Ozone levels increase throughout the day',layout=widgets.Layout(width='40%', height='40px'))
button4 = widgets.Button(description='d. Too much noise; relationship is not obvious',layout=widgets.Layout(width='40%', height='40px'))
display(button1,button2,button3, button4)

button1.on_click(on_incorrect_clicked)
button2.on_click(on_incorrect_clicked)
button3.on_click(on_correct_clicked)
button4.on_click(on_incorrect_clicked)
