import turtle
from ctypes import windll, Structure, c_ulong, byref
from math import sqrt

class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return [pt.x,pt.y]

def move_select(x,y):
    global point_turtles
    for each in range(len(point_turtles)):
        pos=queryMousePosition()
        if sqrt(((point_turtles[each].pos()[0]-(pos[0]-screensizex/2-10))**2)+((point_turtles[each].pos()[1]-(-1*(pos[1]-screensizey/2-34)))**2))<15 and move.isvisible()==False:
            point_turtles[each].shape("node-move.gif")
            move_point(each)
            break
    bg.update()

def move_point(n):
    move.st()
    global kill
    kill=False
    while kill==False:
        pos=queryMousePosition()
        move.goto(-1*((screensizex/2)-pos[0]+10),screensizey/2-pos[1]+34)
        bg.update()
        move.onclick(null)
        if mode%3!=0:
            kill=True
    point_turtles[n].goto(move.pos())
    line.clear()
    point_turtles[n].shape("node-idle.gif")
    move.ht()
    draw_lines()

def null(x,y):
    global kill
    n=0
    global point_turtles
    for i in range(len(point_turtles)):
        if move.distance(point_turtles[i].pos())>28:
            n+=1
    if n==len(point_turtles):
        kill=True
    else:
        kill=False

def remove_visible():
    global point_turtles
    for each in range(len(point_turtles)):
        pos=queryMousePosition()
        if sqrt(((point_turtles[each].pos()[0]-(pos[0]-screensizex/2-10))**2)+((point_turtles[each].pos()[1]-(-1*(pos[1]-screensizey/2-34)))**2))<15:
            point_turtles[each].shape("node-remove.gif")
            point_turtles[each].onclick(remove_point)
        else:
            point_turtles[each].shape("node-idle.gif")
        

def remove_point(x,y):
    global points
    global point_turtles
    global number_fade
    global points_previous
    for each in range(len(point_turtles)):
        pos=queryMousePosition()
        if sqrt(((point_turtles[each].pos()[0]-(pos[0]-screensizex/2-10))**2)+((point_turtles[each].pos()[1]-(-1*(pos[1]-screensizey/2-34)))**2))<15:
            point_turtles[each].ht()
            del point_turtles[each]
            points_previous=points
            points-=1
            number_fade=0
            line.clear()
            break
    draw_lines()

def create_new(x,y):
    n=0
    global point_turtles
    for i in range(len(point_turtles)):
        if create.distance(point_turtles[i].pos())>28:
            n+=1
    if n==len(point_turtles):
        global points
        global points_previous
        global number_fade
        points_previous=points
        points+=1
        point_turtles.append(turtle.Turtle())
        point_turtles[-1].shape("node-idle.gif")
        point_turtles[-1].speed(0)
        point_turtles[-1].pu()
        point_turtles[-1].goto(x,y)
        point_turtles[-1].resizemode("noresize")
        number_fade=0
        line.clear()
    draw_lines()
    
def create_loop():
    pos=queryMousePosition()
    create.goto((pos[0]-screensizex/2-10),-1*(pos[1]-screensizey/2-34))
    create.onclick(create_new)
    bg.update()

def up():
    global mode
    global mode_previous
    global text_fade
    if kill!=False:
        text_fade=0
        mode_previous=mode
        mode+=1
        global point_turtles
        for each in range(len(point_turtles)):
            point_turtles[each].shape("node-idle.gif")
        if mode%3!=1:
            create.ht()
        else:
            create.st()
        bg.update()

def down():
    global mode
    global mode_previous
    global text_fade
    if kill!=False:
        text_fade=0
        mode_previous=mode
        mode-=1
        global point_turtles
        for each in range(len(point_turtles)):
            point_turtles[each].shape("node-idle.gif")
        if mode%3!=1:
            create.ht()
        else:
            create.st()
        bg.update()

def display_mode():
    global text_fade
    text_fade+=4.9
    if int(round(127+text_fade))>255:
        text_fade=0
    text.clear()
    text.color(int(round(127+text_fade)),int(round(127+text_fade)),int(round(127+text_fade)))
    text.goto(0,screensizey/-3+(30-(text_fade/128*30)))
    text.write(mode_text[mode%3],False,align="center",font=("Helvetica",24,"normal"))
    text2.clear()
    text2.color(int(round(255-text_fade)),int(round(255-text_fade)),int(round(255-text_fade)))
    text2.goto(0,screensizey/-3-(text_fade/128*30))
    text2.write(mode_text[mode_previous%3],False,align="center",font=("Helvetica",24,"normal"))
    bg.update()

def display_number():
    global number_fade
    number_fade+=4.9
    if int(round(127+number_fade))>255:
        number_fade=0
    number.clear()
    number.color(int(round(127+number_fade)),int(round(127+number_fade)),int(round(127+number_fade)))
    number.goto(screensizex/3-30+(number_fade/128*30),screensizey/-3)
    number.write(points,False,align="center",font=("Helvetica",24,"normal"))
    number2.clear()
    number2.color(int(round(255-number_fade)),int(round(255-number_fade)),int(round(255-number_fade)))
    number2.goto(screensizex/3+(number_fade/128*30),screensizey/-3)
    number2.write(points_previous,False,align="center",font=("Helvetica",24,"normal"))
    bg.update()

def percentage_move(x,y):
    pos=queryMousePosition()
    percentage.goto((-1*((screensizex/2)-pos[0]+10-percentage.xcor())/2),screensizey/3)
    if percentage.pos()[0]<-100:
        percentage.goto(-100,screensizey/3)
    elif percentage.pos()[0]>100:
        percentage.goto(100,screensizey/3)
    global percent_complete
    percent_complete=(percentage.pos()[0]+100)/2
    draw_lines()

def draw_lines():
    draw.clear()
    global point_turtles
    global midpoints
    global percent_complete
    midpoints.clear()
    for x in range(len(point_turtles)):
        midpoints.append(point_turtles[x].pos())
    if len(midpoints)>0:
        for n in range(len(midpoints)-1):
            draw.goto(midpoints[0])
            draw.pd()
            for i in range(len(midpoints)):
                draw.goto(midpoints[i])
            draw.pu()
            if len(midpoints)==2:
                draw.shape("node-main.gif")
            elif n==0:
                draw.shape("node-large.gif")
            elif n==1:
                draw.shape("node-medium.gif")
            else:
                draw.shape("node-small.gif")
            for i in range(len(midpoints)-1):
                p1=midpoints[i]
                p2=midpoints[i+1]
                midpoints.insert(i,[p1[0]-((p1[0]-p2[0])*(percent_complete/100)),p1[1]-((p1[1]-p2[1])*(percent_complete/100))])
                midpoints.pop(i+1)
                draw.goto(midpoints[i])
                draw.st()
                draw.stamp()
                draw.ht()
            midpoints.pop(-1)

def smooth_animation():
    if mode%3==1:
        down()
    elif mode%3==2:
        up()
    global percent_complete
    line.clear()
    n=int(round(bg.numinput("Steps","Input the amount of sub-steps the program should take (larger numbers take longer)",200,1,20000)))
    for i in range(n+1):
        percent_complete=i/n*100
        percentage.goto(-100+(percent_complete*2),screensizey/3)
        draw_lines()
        line.goto(midpoints[0])
        line.pd()
        bg.update()
    line.pu()

def quit():
    bg.bye()

screensizex=windll.user32.GetSystemMetrics(0)
screensizey=windll.user32.GetSystemMetrics(1)

bg=turtle.Screen()
bg.setup(width=.75,height=.75,startx=None,starty=None)
bg.colormode(255)
bg.bgcolor(128,128,128)
bg.addshape("node-create.gif")
bg.addshape("node-idle.gif")
bg.addshape("node-move.gif")
bg.addshape("node-remove.gif")
bg.addshape("node-large.gif")
bg.addshape("node-medium.gif")
bg.addshape("node-small.gif")
bg.addshape("node-main.gif")
bg.tracer(0)
bg.title("Interpolation Curves")

mode=0
action=0
points=1
percent_complete=50
point_turtles=[]
midpoints=[]
mode_text=["Move","Create","Delete"]
kill=True
text_fade=0
mode_previous=0
number_fade=0
points_previous=0

draw=turtle.Turtle()
draw.speed=0
draw.pu()
draw.ht()
draw.width(1)
draw.color(0,0,0)

point_turtles.append(turtle.Turtle())
point_turtles[0].shape("node-idle.gif")
point_turtles[0].speed(0)
point_turtles[0].pu()
point_turtles[0].resizemode("noresize")

move=turtle.Turtle()
move.shape("node-idle.gif")
move.speed(0)
move.pu()
move.ht()
move.resizemode("noresize")

create=turtle.Turtle()
create.shape("node-create.gif")
create.speed(0)
create.pu()
create.ht()
create.resizemode("noresize")

text=turtle.Turtle()
text.speed(0)
text.pu()
text.ht()
text2=turtle.Turtle()
text2.speed(0)
text2.pu()
text2.ht()

number=turtle.Turtle()
number.speed(0)
number.pu()
number.ht()
number2=turtle.Turtle()
number2.speed(0)
number2.pu()
number2.ht()

line=turtle.Turtle()
line.speed(0)
line.pu()
line.ht()
line.width(3)
line.color(255,255,255)

percentage=turtle.Turtle()
percentage.speed(0)
percentage.pu()
percentage.ht()
percentage.resizemode("noresize")
percentage.width(8)
percentage.color(255,255,255)
percentage.shape("node-idle.gif")
percentage.goto(-100,screensizey/3)
percentage.pd()
percentage.goto(100,screensizey/3)
percentage.pu()
percentage.st()
percentage.goto(0,screensizey/3)

display_mode()
display_number()

bg.update()

while True:
    if points!=0:
        if mode%3==0:   ##move
            for each in point_turtles:
                t_point=point_turtles.index(each)
                bg.update()
                if points>t_point:
                    each.onclick(move_select)
        elif mode%3==2: ##remove
            remove_visible()
            bg.update()
        else:   ##create
            create_loop()
            bg.update()
    else:
        bg.update()
    if bg.onkey(smooth_animation,"space"):
        bg.update()
    if bg.onkey(up,"Up") or bg.onkey(down,"Down"):
        for each in range(len(point_turtles)):
            point_turtles[each].shape("node_idle.gif")
            print("update image")
        bg.update()
    if text_fade<127:
        display_mode()
    if number_fade<127:
        display_number()
    percentage.ondrag(percentage_move)
    bg.onkey(quit,"q")
    bg.listen()
