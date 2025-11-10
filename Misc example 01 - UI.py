from guizero import App, Text, TextBox, PushButton


def say_my_name():
    welcome_message2.value = my_name.value

app = App(title="Hello world", layout='grid')
welcome_message1 = Text(app, text="Welcome to my app", grid=[0,0])
welcome_message2 = Text(app, text="Welcome to my app", size=40, font="Times New Roman", color="lightblue", grid=[5,0])
my_name = TextBox(app, grid=[10,0])
update_text = PushButton(app, command=say_my_name, text="Display my name", grid=[0,10])
app.display()