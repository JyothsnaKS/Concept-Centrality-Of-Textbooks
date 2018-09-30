#!/usr/bin/python
# -*- coding: utf-8 -*-
from ete3 import Tree, TreeStyle, TextFace, NodeStyle
from ebook2 import scores, title

def size_internal(node):
    if not node.is_leaf():
        node.img_style["size"] = 10

def unit(scores, i, curr_level):
    newt=""
    header=scores[i]
    j=i+1
    excond=False
    if i+1<len(scores):
        d=scores[j]
        it_no=1
        while d[0]!=1 and not excond:
            if it_no==1:
                newt=newt+"("
            else:
                newt=newt+", "
            it_no+=1
            newt=newt+d[1]
            j=j+1
            if j<len(scores):
                d=scores[j]
            else:
                excond=True
        if it_no!=1:
            newt=newt+")"+header[1]
        else:
            newt=newt+header[1]
    else:
        newt=newt+header[1]
    return newt, j

def conv(title, scores):

    i=0
    op=""
    it_no=1
    while i<len(scores):
        newt, j=unit(scores, i, 1)
        if it_no==1:
            op="("+newt
        else:
            op=op+", "+newt
        it_no+=1
        i=j
    op=op+")"+title+";"
    return op

#order is 'level', 'name', 'centrality percentage'

for i in range(0,len(scores)):
    scores[i][1]= (scores[i][1].replace(':','')).replace(',','')
    scores[i][1] = scores[i][1].replace('(','')
    scores[i][1] = scores[i][1].replace(')','')



i_no=0
j_no=0

for score in scores:
    if score[0]==2:
        j_no+=1
    elif score[0]==1:
        i_no+=1
        j_no=0
    score[1]=str(i_no)+"."+str(j_no)+"__"+score[1]

nf=conv(title, scores)
t2 = Tree(nf, format=1)

cent={}
lev={}

for score in scores:
    cent[score[1]]=score[2]
    lev[score[1]]=score[0]
cent[title]=100
lev[title]=0

for leaf in t2:
    leaf.add_features(c=cent.get(leaf.name, "none"))
for leaf in t2.traverse():
    if not leaf.is_leaf():
        leaf.add_features(buff="------------", level=lev.get(leaf.name, "none"))

c_sum=0
for leaf in t2:
    #print leaf.c
    if leaf.c:
        c_sum+=leaf.c

#print c_sum

percs={}
percstr={}
for leaf in t2:
    percs[leaf.name]=float("{0:.2f}".format((leaf.c * 100)/c_sum))
    percstr[leaf.name]="{0:.2f}".format((leaf.c * 100)/c_sum)+"%"

for leaf in t2:
    leaf.add_features(perc=percs.get(leaf.name, "none"), percstring=percstr.get(leaf.name, "none"))

for node in t2.traverse():
    if not node.is_leaf() and node.level==1:
        sum_parent=0
        for child in node.children:
            sum_parent+=child.perc
        percs[node.name]=sum_parent
        percstr[node.name]=str(sum_parent)+"%"

for node in t2.traverse():
    if not node.is_leaf() and node.level==1:
        node.add_features(perc=percs.get(node.name, "none"), percstring=percstr.get(node.name, "none"))

sum_title=0
for child in t2.children:
    sum_title+=child.perc
sum_title=round(sum_title,2)
for node in t2.traverse():
    if node.name==title:
        node.add_features(perc=sum_title, percstring=str(sum_title)+"%")
    
print t2.get_ascii(attributes=["name", "percstring", "buff"])

ts = TreeStyle()
# provide a list of layout functions, instead of a single one
ts.layout_fn = [size_internal]

ts.show_leaf_name = False

ts.branch_vertical_margin=10
ts.title.add_face(TextFace("Graphical Representation of "+title, fsize=20), column=0)

ns=NodeStyle()
ns["shape"]="sphere"
ns["size"]=1
ns["fgcolor"] = "darkred"

ns["hz_line_color"]="#cccccc"
for n in t2.traverse():
    n.set_style(ns)

for node in t2.traverse():
    stri=node.name+" "+node.percstring
    node.add_face(TextFace(stri), column=0, position="branch-right")


t2.render("a7.png", w=400, units="mm", tree_style=ts)

 
