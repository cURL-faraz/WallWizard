from rich.console import Console
import json
import copy
from rich.theme import Theme
import time
import os
start_time = time.time()
custom_theme = Theme({"success": "green", "error":"red"})
console = Console(theme=custom_theme)
def clear():
    os.system('cls||clear')
clear()
def endtime (start_time):
    end_time = time.time()
    

    print (f"{end_time - start_time}.2f")
def run (red,blue,wall_a,wall_o,neighborhood,redwall,bluewall,usedcenter_a,usedcenter_o,usedcenter,start_time):
    r=True
    x=0
    while r:
        print("m:move   w:wall   q:quit")
        if x%2==0:
            while True:
                b=0
                if blue[0]==1:
                    r=False
                    break
                a=input("player1: ")
                if a=='q':
                    r=False
                    endtime(start_time)
                    break
                
                if a=='m':
                    while True:
                        m=input("enter direction: ")
                        t=move(red,blue,m,wall_a,wall_o)
                        if t!=None:
                            clear()
                            console.print(generate_table(wall_a, wall_o,red,blue))
                            x+=1
                            b+=1
                            break
                        if t==None:
                            console.print("invalid direction",style="error") 
                            break
                    if b==1:
                        b=0
                        break
                if a=="w":
                    print(f"your remaining number of walls: {redwall}")
                    while redwall>0:
                        c=0
                        w=list(input("enter centr of the wall and its state(enter horizontal or vertical),such as (1,2,v): ").split(","))
                        centers = [(w[0],w[1])]
                        if w[-1]=="h":
                            if checkwall(neighborhood,"blue",tuple(blue),int(w[0]),int(w[1]),"h",usedcenter,usedcenter_a,usedcenter_o):
                                remove_neighborhood(neighborhood,int(w[0]),int(w[1]),"h")
                                block_wall_o(wall_o,int(w[0]),int(w[1]))
                                redwall-=1
                                clear()
                                console.print(generate_table(wall_a, wall_o,red,blue))
                                x+=1
                                c+=1
                                break
                            else:
                                console.print("invalid wall",style="error")
                                break
                        if w[-1]=="v":
                            if checkwall(neighborhood,"blue",tuple(blue),int(w[0]),int(w[1]),"v",usedcenter,usedcenter_a,usedcenter_o):
                                remove_neighborhood(neighborhood,int(w[0]),int(w[1]),"v")
                                block_wall_a(wall_a,int(w[0]),int(w[1]))
                                redwall-=1
                                clear()
                                console.print(generate_table(wall_a, wall_o,red,blue))
                                x+=1
                                c+=1
                                break
                            else:
                                console.print("invalid wall",style="error")
                                break
                    if c==1:
                        c=0
                        break
        print("m:move   w:wall   q:quit")        
        if x%2!=0:
            while True:
                b=0
                c=0
                if red[0]==9:
                    r=False
                    break
                a=input("player2: ")
                if a=='q':
                    r=False
                    
                    endtime(start_time)
                    break
                if a=='m':
                    while True:
                        m=input("enter direction: ")
                        t=move(blue,red,m,wall_a,wall_o)
                        if t!=None:
                            clear()
                            console.print(generate_table(wall_a, wall_o,red,blue))
                            x+=1
                            b+=1
                            break
                        if t==None:
                            console.print("invalid direction",style="error")
                            break
                    if b==1:
                        b=0
                        break
                if a=="w":
                    print(f"your remaining number of walls: {bluewall}")
                    while bluewall>0:
                        w=list(input("enter centr of the wall and its state(enter horizontal or vertical),such as (1,2,v): ").split(","))
                        if w[-1]=="h":
                            if checkwall(neighborhood,"red",tuple(red),int(w[0]),int(w[1]),"h",usedcenter,usedcenter_a,usedcenter_o):
                                remove_neighborhood(neighborhood,int(w[0]),int(w[1]),"h")
                                block_wall_o(wall_o,int(w[0]),int(w[1]))
                                clear()
                                console.print(generate_table(wall_a, wall_o,red,blue))
                                bluewall-=1
                                x+=1
                                c+=1
                                break
                            else:
                                console.print("invalid wall",style="error")
                                break
                        if w[-1]=="v":
                            if checkwall(neighborhood,"red",tuple(red),int(w[0]),int(w[1]),"v",usedcenter,usedcenter_a,usedcenter_o):
                                remove_neighborhood(neighborhood,int(w[0]),int(w[1]),"v")
                                block_wall_a(wall_a,int(w[0]),int(w[1]))
                                clear()
                                console.print(generate_table(wall_a, wall_o,red,blue))
                                bluewall-=1
                                x+=1
                                c+=1
                                break
                            else:
                                console.print("invalid wall",style="error")
                                break
                    if c==1:
                        c=0
                        break
def block_wall_a(wall_a : list,x_center,y_center):
    if x_center <= 9 and y_center <= 9 :
        wall_a[x_center-1][y_center-1]="Blocked"
        wall_a[x_center][y_center-1]="Blocked"
        return(wall_a)
def block_wall_o(wall_o : list,x_center,y_center):
    if x_center <= 9 and y_center <= 9 :
        wall_o[x_center-1][y_center-1]="Blocked"
        wall_o[x_center-1][y_center]="Blocked"
        return(wall_o)
def move(s,k,move,wall_a,wall_o):
    if move =="u"and (1<s[0]<=9) and wall_o[s[0]-2][s[1]-1]=="Available" and (s[1]!=k[1] or (s[1]==k[1] and s[0]!=k[0]+1)) :
        s[0]-=1
        return(s)
    if move =="u" and (2<s[0]<=9) and wall_o[s[0]-2][s[1]-1]=="Available" and wall_o[s[0]-3][s[1]-1]=="Available" and (s[1]==k[1] and s[0]==k[0]+1) :
        s[0]-=2
        return(s)
    if move =="d"and (1<=s[0]<9) and wall_o[s[0]-1][s[1]-1]=="Available" and (s[1]!=k[1]or (s[1]==k[1] and s[0]!=k[0]-1)) :
        s[0]+=1
        return(s)
    if move =="d"and (1<=s[0]<8) and wall_o[s[0]-1][s[1]-1]=="Available" and wall_o[s[0]][s[1]-1]=="Available" and (s[1]==k[1] and s[0]==k[0]-1) :
        s[0]+=2
        return(s)
    if move =="r" and (1<=s[1]<9)and wall_a[s[0]-1][s[1]-1]=="Available" and (s[0]!=k[0]or (s[0]==k[0] and s[1]!=k[1]-1)) :
        s[1]+=1
        return(s)
    if move =="r"and (1<=s[1]<8) and wall_a[s[0]-1][s[1]-1]=="Available" and wall_a[s[0]-1][s[1]]=="Available" and (s[0]==k[0] and s[1]==k[1]-1) :
        s[1]+=2
        return(s)
    if move =="l" and (1<s[1]<=9)and wall_a[s[0]-1][s[1]-2]=="Available" and (s[0]!=k[0]or (s[0]==k[0] and s[1]!=k[1]+1)) :
        s[1]-=1
        return(s)
    if move =="l"and (2<s[1]<=9) and wall_a[s[0]-1][s[1]-1]=="Available" and wall_a[s[0]-1][s[1]-3]=="Available" and (s[0]==k[0] and s[1]==k[1]+1) :
        s[1]-=2
        return(s)
    if (move =="ul" or move=="lu")and (1<s[1]<=9 and 1<s[0]<=9) and wall_o[s[0]-2][s[1]-1]=="Available" and wall_o[s[0]-3][s[1]-1]=="Blocked" and wall_a[s[0]-2][s[0]-2]=="Available" and (s[1]==k[1] and s[0]==k[0]+1) :
        s[0]-=1
        s[1]-=1
        return(s)
    if (move =="ur" or move=="ru")and (1<=s[1]<9 and 1<s[0]<=9) and wall_o[s[0]-2][s[1]-1]=="Available" and wall_o[s[0]-3][s[1]-1]=="Blocked" and wall_a[s[0]-2][s[0]-1]=="Available" and (s[1]==k[1] and s[0]==k[0]+1) :
        s[0]-=1
        s[1]+=1
        return(s)
    if (move =="dr" or move=="rd")and (1<=s[1]<9 and 1<=s[0]<9) and wall_o[s[0]-1][s[1]-1]=="Available" and wall_o[s[0]][s[1]-1]=="Blocked" and wall_a[s[0]+1][s[0]]=="Available" and (s[1]==k[1] and s[0]==k[0]-1) :
        s[0]+=1
        s[1]+=1
        return(s)
    if (move =="dl" or move=="ld")and (1<s[1]<=9 and 1<=s[0]<9) and wall_o[s[0]-1][s[1]-1]=="Available" and wall_o[s[0]][s[1]-1]=="Blocked" and wall_a[s[0]+1][s[0]-1]=="Available" and (s[1]==k[1] and s[0]==k[0]-1):
        s[0]+=1
        s[1]-=1
        return(s)
    if (move =="ul" or move=="lu")and (1<s[1]<=9 and 1<s[0]<=9) and wall_a[s[0]-1][s[1]-2]=="Available" and wall_a[s[0]-1][s[1]-3]=="Blocked" and wall_o[s[0]-2][s[1]-2]=="Available" and (s[0]==k[0] and s[1]==k[1]+1) : 
        s[0]-=1
        s[1]-=1
        return(s)
    if (move =="dl" or move=="ld")and (1<s[1]<=9 and 1<=s[0]<9) and wall_a[s[0]-1][s[1]-2]=="Available" and wall_a[s[0]-1][s[1]-3]=="Blocked" and wall_o[s[0]-1][s[1]-2]=="Available" and (s[0]==k[0] and s[1]==k[1]+1)  :
        s[0]+=1
        s[1]-=1
        return(s)
    if (move =="dr" or move=="rd") and (1<=s[1]<9 and 1<=s[0]<9)and wall_a[s[0]-1][s[1]-1]=="Available" and wall_a[s[0]-1][s[1]]=="Blocked" and wall_o[s[0]-1][s[1]]=="Available" and (s[0]==k[0] and s[1]==k[1]-1) :
        s[0]+=1
        s[1]+=1
        return(s)
    if (move =="ur" or move=="ru")and (1<=s[1]<9 and 1<s[0]<=9) and wall_a[s[0]-1][s[1]-1]=="Available" and wall_a[s[0]-1][s[1]]=="Blocked" and wall_o[s[0]-2][s[1]]=="Available" and (s[0]==k[0] and s[1]==k[1]-1) :
        s[0]-=1
        s[1]+=1
        return(s)
def remove_neighborhood(neighborhood,x_center,y_center,state):
    if state=="h":
        if (x_center+1,y_center) in neighborhood[(x_center,y_center)]:
            neighborhood[(x_center,y_center)].remove((x_center+1,y_center))

        if (x_center,y_center) in neighborhood[(x_center+1,y_center)]:    
            neighborhood[(x_center+1,y_center)].remove((x_center,y_center))

        if (x_center+1,y_center+1) in neighborhood[(x_center,y_center+1)]:
            neighborhood[(x_center,y_center+1)].remove((x_center+1,y_center+1))

        if (x_center,y_center+1) in neighborhood[(x_center+1,y_center+1)]:
            neighborhood[(x_center+1,y_center+1)].remove((x_center,y_center+1))
    if state=="v":
        if (x_center,y_center+1) in neighborhood[(x_center,y_center)]:
            neighborhood[(x_center,y_center)].remove((x_center,y_center+1))
        if (x_center,y_center) in neighborhood[(x_center,y_center+1)]:
            neighborhood[(x_center,y_center+1)].remove((x_center,y_center))
        if (x_center+1,y_center+1) in neighborhood[(x_center+1,y_center)]:
            neighborhood[(x_center+1,y_center)].remove((x_center+1,y_center+1))
        if (x_center+1,y_center) in neighborhood[(x_center+1,y_center+1)]:
            neighborhood[(x_center+1,y_center+1)].remove((x_center+1,y_center))
    return(neighborhood)
def dfs(start, target, visited,neighborhood_c):
    if start == target:
        return True
    visited.add(start)
    for neighbor in neighborhood_c[start]:
        if neighbor not in visited:
            if dfs(neighbor, target, visited,neighborhood_c):
                return True
    return False
def checkwall(neighborhood,enemycolor,positon,x_center,y_center,state,usedcenter,usedcenter_a,usedcenter_o):
    neighborhood_c=copy.deepcopy(neighborhood)
    remove_neighborhood(neighborhood_c,x_center,y_center,state)
    if state == "v":
        if not((x_center,y_center) in usedcenter) and not((x_center+1,y_center) in usedcenter_a) and not((x_center-1,y_center) in usedcenter_a):
            center=(x_center,y_center)
            usedcenter.append(center);usedcenter_a.append(center)
        else:
            return False
    if state == "h":
        if not((x_center,y_center) in usedcenter) and not((x_center,y_center+1) in usedcenter_o) and not((x_center,y_center-1) in usedcenter_o):
            center=(x_center,y_center)
            usedcenter.append(center);usedcenter_o.append(center)        
        else:
            return False
    if enemycolor == "red":
        visited = set()
        for i in range(1,10):
            if dfs(positon,(9,i),visited,neighborhood_c):
                return True
        return False
    
    if enemycolor=="blue":
        visited = set()
        for i in range(1,10):
            if dfs(positon,(1,i),visited,neighborhood_c):
                return True
        return False
def generate_table(wall_a, wall_o,red,blue):
    s = ""
    for i in range(1, 18):  
        ss = ""
        if i % 2 != 0: 
            for n in range(9):
                if ((i+1)/2)==red[0] and n+1==red[1]:
                    if wall_a[(i-1) // 2][n] == "Available":
                        if n!=8:
                            ss += " [red]O[/red] [yellow2]|[/yellow2]"
                        else:
                            ss+=" [red]O[/red] "
                    else:
                        if n!=8:
                            ss += " [red]O[/red] [orange3]|[/orange3]"
                        else:
                            ss +=" [red]O[/red] "
                elif ((i+1)/2)==blue[0] and n+1==blue[1]:
                    if wall_a[(i-1) // 2][n] == "Available":
                        if n!=8:
                            ss += " [blue]O[/blue] [yellow2]|[/yellow2]"
                        else:
                            ss+=" [blue]O[/blue] "
                    else:
                        if n!=8:
                            ss += " [blue]O[/blue] [orange3]|[/orange3]"
                        else:
                            ss +=" [blue]O[/blue] "
                else:
                    if wall_a[(i-1) // 2][n] == "Available":
                        if n!=8:
                            ss += "   [yellow2]|[/yellow2]"
                        else:
                            ss+="   "
                    else:
                        if n!=8:
                            ss += "   [orange3]|[/orange3]"
                        else:
                            ss +="   "
        else: 
            for n in range(9):
                if wall_o[(i - 1) // 2][n] == "Available":
                    if n!=8:  
                        ss += "[yellow2]——-[/yellow2]o"
                    else:
                        ss += "[yellow2]——-[/yellow2]"
                else:
                    if n!=8:
                        ss += "[orange3]——-[/orange3]o"
                    else:
                        ss += "[orange3]——-[/orange3]"  
        s += ss + "\n"
    return s
wall_a = []
wall_o = []
for i in range(9):
    l = []
    for j in range(9):
        l.append("Available")
    wall_a.append(l.copy())
    wall_o.append(l.copy())
red=[1,5]
blue=[9,5]
neighborhood = {}
for i in range(1, 10):
    for j in range(1, 10):
        neighbors = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 1 <= ni <= 9 and 1 <= nj <= 9:
                neighbors.append((ni, nj))
        neighborhood[(i, j)] = neighbors
console.print(generate_table(wall_a, wall_o,red,blue))
redwall=10;bluewall=10;usedcenter_a=[];usedcenter_o=[];usedcenter=[]
run(red,blue,wall_a,wall_o,neighborhood,redwall,bluewall,usedcenter_a,usedcenter_o,usedcenter,start_time)

if red[0]==9:
    print("player1 wins")
    endtime(start_time)





if blue[0]==1:
    print("player2 wins")
    endtime(start_time)
