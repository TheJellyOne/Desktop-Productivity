import pandas as pd
import datetime as dt
import numpy as np
import PIL as pil
from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import seaborn as sns
import math
from bokeh.palettes import Spectral10 as pal

# Changeables
previousDays = 14
previousWeeks = 8
desiredWorkHoursThisWeek = 30
desiredJobSearchHoursThisWeek = 5
desiredExerciseHoursThisWeek = 3
off = False      #toggles input on/off
finishedAdding = False   #toggles week while function on/off
multipliers = {"r":1, "c":1, "p":1, "j":2, "o":1, "e":1.5, "h":1, "g":1}
modifier = 1
modifieri = 1

# FUNCTIONS

def drawText(text,size,rightAlign = False,topMargin = 0, leftBox = True, nextLine = False, colorToFill = (255,255,255,255)):
    global draw
    global text1Line; global text2Line; global title1Line; global marginCount
    global text1; global text2; global title1
    global boxHalf; global textStartHeight; global textStartWidth
    global textSize; global textSize2; global titleSize
    global spacing; global spacing2
    fnt = ImageFont.truetype('C:/Users/Jiali/Desktop/Productivity/Fonts/akrobat/Akrobat-ExtraBold.otf', size)
    
    #Change left and right box
    if leftBox == True:
        leftSide = textStartWidth
        rightSide = boxHalf
    else:
        leftSide = boxHalf
        rightSide = 1910
    
    marginCount += topMargin
    heightValue = textStartHeight + marginCount*textMargin + text1Line*(text1+spacing) + text2Line*(text2+spacing) + title1Line*(title1+spacing2)
    
    if rightAlign == False:
        draw.text((leftSide + textMargin, heightValue),
                  text,
                  font = fnt,
                  fill = colorToFill)
    else: 
        msg = str(text)
        msgW, msgH = draw.textsize(msg)
        draw.text((rightSide-textMargin-msgW, heightValue),
                  msg,
                  font = fnt,
                  fill = colorToFill)
        
    if nextLine == True:
        if size <= text1:
            text1Line += 1
        elif size == text2:
            text2Line += 1
        elif size >= title1:
            title1Line +=1
        
def drawLine(topMargin = False, leftBox = True, colorToFill = (255,255,255,255)):
    global draw
    global text1; global text2; global title1
    global text1Line; global text2Line; global title1Line; global marginCount
    global boxHalf; global textStartHeight; global textStartWidth
    
    marginCount += 1*topMargin
    heightValue = textStartHeight + marginCount*textMargin + text1Line*(text1+spacing) + text2Line*(text2+spacing) + title1Line*(title1+spacing2)
            
    if leftBox == True:
        leftSide = textStartWidth
        rightSide = boxHalf
        leftMargin = 1; rightMargin = 0
    else:
        leftSide = boxHalf
        rightSide = 1915
        leftMargin = 0; rightMargin = 1
        
    draw.line(((leftSide + leftMargin*textMargin, heightValue),
               (rightSide - rightMargin*textMargin,heightValue)),
               fill = colorToFill)

# Importing data
data = pd.DataFrame.from_csv("C:/Users/Jiali/Desktop/Productivity/WorkData.csv",infer_datetime_format=True)
data['Date'] = pd.to_datetime(data['Date'])
weeklyData = pd.DataFrame.from_csv("C:/Users/Jiali/Desktop/Productivity/WeeklyData.csv")
aggregate = pd.DataFrame.from_csv("C:/Users/Jiali/Desktop/Productivity/Aggregate.csv")


def roundup(x):
    return int(math.ceil(x / 4.0)) * 4

# Reference Dictionaries
variables = {"r":"Reading", 
             "c":"Chinese", 
             "p":"Programming", 
             "j":"JobSearch",
             "o":"OnlineCourse",
             "e":"Exercise", 
             "h":"HomeImprovement",
             "g":"GeneralProductivity",
             "l":"Leisure"}
inverseVariables = {"Reading":"Read", 
                    "Chinese":"Chinese", 
                    "Programming":"Prgm", 
                    "JobSearch":"JobS",
                    "OnlineCourse":"OC",
                    "Exercise":"Exrcs", 
                    "HomeImprovement":"HmImpr",
                    "GeneralProductivity":"GenPr",
                    "Leisure":"Leis"}
workType = {"Reading":"Learn",
            "Chinese":"Learn",
            "Programming":"Apply",
            "JobSearch":"Reinforce",
            "OnlineCourse":"Learn",
            "Exercise":"WorkOut",
            "HomeImprovement":"WorkOut",
            "GeneralProductivity":"Reinforce",
            "Leisure":"None"}
colors = {"Reading":pal[3],
          "Chinese":pal[6],
          "Programming":pal[0],
          "JobSearch":pal[2],
          "OnlineCourse":pal[9],
          "Exercise":pal[7],
          "HomeImprovement":pal[4],
          "GeneralProductivity":pal[5],
          "Leisure":pal[8],
          "Total":pal[1]
        }


today= dt.datetime.now()




# Creating Missing Data for past weeks: Graph 2

base=today.weekday()
if base>=6:
    modifier = modifier*2
    
thisWeek = today-dt.timedelta(days = base)
thisWeek = thisWeek.strftime("%Y-%m-%d")
previous = 0
while finishedAdding == False:
    theWeek = today-dt.timedelta(days = previous*7+base)
    theWeek = theWeek.strftime("%Y-%m-%d")
    if theWeek in list(weeklyData["Date"]):
        finishedAdding = True
    else: 
        miniDf = pd.DataFrame([[theWeek,0,0,0,0,0,0,0,0,0,0]], 
                              columns=(["Date"] +list(variables.values())+["Total"]))
        weeklyData = weeklyData.append(miniDf,ignore_index=True)
        previous += 1

        
            
        

    
        


# Secondary Data Load
balance = pd.DataFrame.from_csv("C:/Users/Jiali/Desktop/Productivity/Balance.csv")
leisurePoints = balance.iloc[0,0]
spendingMoney = balance.iloc[0,1]



# Help
print('''
              **********************
              r:Reading
              c:Chinese
              p:Programming
              j:JobSearch
              o:OnlineCourse
              e:Exercise
              h:HomeImprovement
              g:GeneralProductivity
              l:Leisure
              t:Transfer Points to Money
              u:Use Money
              i:Input Old Data (Days ago)
              **********************''')

# Data input
now = dt.datetime.now()
todaysDate = str(now.month)+'/'+ str(now.day)+'/'+str(now.year)
while off == False:
    x = input("Name time: ")
    y = x[0]
    if y in variables.keys():
        value = int(x[1:])
        data.loc[len(data)] = [variables[y],value, todaysDate]
        weeklyData.loc[weeklyData["Date"] == thisWeek, [variables[y]]] = weeklyData[weeklyData["Date"] == thisWeek][variables[y]] + value
        aggregate["Total"] = aggregate["Total"] + value
        if y!= "l":
            aggregate[variables[y]] = aggregate[variables[y]] + value
            leisurePoints += value*multipliers[y]*modifier
            weeklyData.loc[weeklyData["Date"] == thisWeek, ["Total"]] = weeklyData[weeklyData["Date"] == thisWeek]["Total"] + value
        else:leisurePoints -= value
    elif y == 'q':
        off = True
    # Transfers leisure points into spending money at rate 100:$1
    elif y == 't':
        value = int(x[1:])
        z = int(round(value/100,2)*100)
        if z<=leisurePoints:
            leisurePoints -= z
            spendingMoney += z/100
        else: print("Insufficient funds")
    elif y == 'u':
        value = float(x[1:])
        spendingMoney -= value
    # Inputs data from z days ago, updates data, weeklyData, aggregate, leisurepoints
    elif y == 'i':         
        z = int(x[1:]) 
        x2 = input("Name Time of Previous: ")
        y2 = x2[0]
        now2 = dt.datetime.now() - dt.timedelta(days = z)
        base2=now2.weekday()
        thisWeek2 = now2-dt.timedelta(days = base2)
        thisWeek2 = thisWeek2.strftime("%Y-%m-%d")
        base=today.weekday()
        if base2>=6:
            modifierThis = modifieri*2
        if y2 in variables.keys():
            value2 = int(x2[1:])
            data.loc[len(data)] = [variables[y2],value2, str(now2.month)+'/'+ str(now2.day)+'/'+str(now2.year)]
            weeklyData.loc[weeklyData["Date"] == thisWeek2, [variables[y2]]] = weeklyData[weeklyData["Date"] == thisWeek2][variables[y2]] + value2
            aggregate["Total"] = aggregate["Total"] + value2
            if y2!= "l":
                aggregate[variables[y2]] = aggregate[variables[y2]] + value2
                leisurePoints += value2*multipliers[y2]*modifierThis
                weeklyData.loc[weeklyData["Date"] == thisWeek2, ["Total"]] = weeklyData[weeklyData["Date"] == thisWeek2]["Total"] + value2
            else:leisurePoints -= value2
    else: continue


# Update Balances
balance.iloc[0,0] = leisurePoints
balance.iloc[0,1] = spendingMoney

# Save session data
data['Date'] = pd.to_datetime(data['Date'])
data.to_csv("C:/Users/Jiali/Desktop/Productivity/WorkData.csv")
weeklyData.to_csv("C:/Users/Jiali/Desktop/Productivity/WeeklyData.csv")
balance.to_csv("C:/Users/Jiali/Desktop/Productivity/Balance.csv")
aggregate.to_csv("C:/Users/Jiali/Desktop/Productivity/Aggregate.csv")


# Calculations for graphs

    # Getting Recent Dates: Graph 1
dates = today-data["Date"]
days = []
for i in dates:
    if int(i.days)<previousDays:
        days.append(True)
    else: days.append(False)
recentData = data[days]
recentData['Date'] = pd.to_datetime(recentData['Date'])

    # Filling Data for recent days: Graph 1
recentWorkTotals = {}
recentLeisureTotals = {}
for i in range(previousDays):
    iDaysFromToday = today-dt.timedelta(days = i)
    if len(str(iDaysFromToday.day)) == 1:
        day = "0" + str(iDaysFromToday.day)
    else: day = str(iDaysFromToday.day)
    if len(str(iDaysFromToday.month)) == 1:
        month = "0" + str(iDaysFromToday.month)
    else: month = str(iDaysFromToday.month)
    recentWorkTotals[str(iDaysFromToday.year)+'-'+ month +'-'+ day] = 0
    recentLeisureTotals[str(iDaysFromToday.year)+'-'+ month +'-'+ day] = 0
    
    # Calculating work and leisure hours for recent days
for observation in range(len(recentData)):
    time = recentData["Length"][recentData.index[observation]]
    item = recentData["Item"][recentData.index[observation]]
    date = recentData["Date"][recentData.index[observation]]
    date = str(date.date())
    if item != "Leisure":
        recentWorkTotals[date] = recentWorkTotals[date] + time
    else:
        recentLeisureTotals[date] = recentLeisureTotals[date] + time

    # Create X Y: Graph 1
recentWorkTotals = pd.DataFrame(list(recentWorkTotals.items()), columns=["Date", "Length"])
recentWorkTotals['Date'] = pd.to_datetime(recentWorkTotals['Date'])
recentLeisureTotals = pd.DataFrame(list(recentLeisureTotals.items()),columns=["Date", "Length"])
recentLeisureTotals['Date'] = pd.to_datetime(recentLeisureTotals['Date'])

    #Get 8 week data: Graph 2
weeklyData["Date"] = pd.to_datetime(weeklyData["Date"])
weeklyData = weeklyData[(now.date()-weeklyData["Date"]) <= dt.timedelta(days = 7*previousWeeks)]
    # Generate 7 Day Data  
sevenDays = []
for i in dates:
    if int(i.days)<=7:
        sevenDays.append(True)
    else: sevenDays.append(False)
sevenDayData = data[sevenDays]

    # Generate 7 Day Average Dictionary
sevenDayAverages = {}
for i in variables.values():
    sevenDayAverages[i] = np.round(sum(sevenDayData[sevenDayData["Item"]==i]["Length"])/300,decimals=1)
    
    # Generate 7 day work type
sevenDayWorkType = {"WorkOut":0,"Reinforce":0,"Apply":0,"Learn":0}
for i in sevenDayAverages.keys():
    if i != "Leisure":
        sevenDayWorkType[workType[i]] = sevenDayWorkType[workType[i]] + sevenDayAverages[i]
workTypeLabels = list(sevenDayWorkType.keys())
workTypeValues = list(sevenDayWorkType.values())
workTypeValues = workTypeValues/(sum(workTypeValues))
    

# Graphing
w1,h1 = 500,250
copyWeeklyData = weeklyData
copyWeeklyData["Date"] =  pd.to_datetime(copyWeeklyData['Date'])

# Graph 1 Aesthetic
sns.set()    
sns.set_context("talk",font_scale=.85)
font0 = FontProperties()
font = font0.copy()
font.set_weight('bold')

formatter = mdates.DateFormatter('%m-%d')
fig, ax = plt.subplots()
DPI = 93
ax.xaxis.set_major_formatter(formatter)
fig.set_size_inches(w1/float(DPI),h1/float(DPI))


# Graphing 1
plt.plot(recentWorkTotals["Date"],
         recentWorkTotals["Length"]/60, 
         label ="Work",
         color = colors["Total"],
         linewidth = 4)
plt.plot(recentLeisureTotals["Date"], 
         recentLeisureTotals["Length"]/60,
         label ="Leisure",
         color = colors["Leisure"],
         linewidth = 4)
plt.xticks(rotation=0, fontproperties=font)
plt.yticks(fontproperties=font)
plt.legend(frameon = True,
           prop = {"weight":"bold"})
plt.tight_layout()
plt.savefig("C:/Users/Jiali/Desktop/Productivity/Plots/plot1.png",
            dpi=DPI)
plt.close(fig)

# Graph 2 Aesthetic
formatter = mdates.DateFormatter('%m-%d')
fig, ax = plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.set_xticks(list(copyWeeklyData["Date"]))
fig.set_size_inches(w1/float(DPI),h1/float(DPI))

# Graphing 2
for i in variables.values():
    if i!="Leisure":
        a = "dashdot"
    else: a = "solid"
    plt.plot(copyWeeklyData["Date"], 
             copyWeeklyData[i]/60, 
             label = inverseVariables[i],
             ls = a,
             color = colors[i],
             linewidth = 4)
plt.plot(copyWeeklyData["Date"],
         copyWeeklyData["Total"]/60,
         label = "Total",
         color= colors["Total"],
         linewidth = 4)
plt.legend(loc="upper left",
           frameon=True, 
           ncol=3,
           prop={"weight":"bold","size":8})
plt.xticks(rotation=0, fontproperties=font)
plt.yticks(fontproperties=font)
plt.tight_layout()
plt.savefig("C:/Users/Jiali/Desktop/Productivity/Plots/plot2.png",
            dpi=DPI)
plt.close(fig)

# Bar graphs
    
    # Bar 1: Work hours/goal per week
w2,h2=100,100
targetHours = desiredWorkHoursThisWeek
finishedHoursThisWeek = float(weeklyData[weeklyData["Date"]==thisWeek]["Total"]/60)
fig,x = plt.subplots()
small = max(finishedHoursThisWeek,targetHours/10)
plt.bar(1,targetHours, color="gray")
plt.bar(1,small, color=colors["Total"])
x.xaxis.set_visible(False)
x.yaxis.set_visible(False)
fig.set_size_inches(w2/float(DPI),h2/float(DPI))
plt.text(1,
         targetHours/2,
         str(int(float(finishedHoursThisWeek/targetHours)*100))+"%", 
         horizontalalignment='center',
        verticalalignment='center', 
        fontproperties=font)
plt.savefig("C:/Users/Jiali/Desktop/Productivity/Plots/bar1.png",
            dpi=DPI,
            bbox_inches='tight',
            pad_inches = -.04)
plt.close(fig)

    # Bar 2: Job search hours/ goal per week
targetHours = desiredJobSearchHoursThisWeek
finishedHoursThisWeek = float(weeklyData[weeklyData["Date"]==thisWeek]["JobSearch"]/60)
small = max(finishedHoursThisWeek,targetHours/10)
fig,x = plt.subplots()
plt.bar(1,targetHours, color="gray")
plt.bar(1,small, color=colors["JobSearch"])
x.xaxis.set_visible(False)
x.yaxis.set_visible(False)
fig.set_size_inches(w2/float(DPI),h2/float(DPI))
plt.text(1,
         targetHours/2,
         str(int(float(finishedHoursThisWeek/targetHours)*100))+"%", 
         horizontalalignment='center',
        verticalalignment='center', 
        fontproperties=font)
plt.savefig("C:/Users/Jiali/Desktop/Productivity/Plots/bar2.png",
            dpi=DPI,
            bbox_inches='tight',
            pad_inches = -.04)
plt.close(fig)



    # Bar 3: Work vs Leisure
targetHours = desiredExerciseHoursThisWeek
finishedHoursThisWeek = float(weeklyData[weeklyData["Date"]==thisWeek]["Exercise"]/60)
small = max(finishedHoursThisWeek,targetHours/10)
fig,x = plt.subplots()
plt.bar(1,targetHours, color="gray")
plt.bar(1,small, color=colors["Exercise"])
x.xaxis.set_visible(False)
x.yaxis.set_visible(False)
fig.set_size_inches(w2/float(DPI),h2/float(DPI))
plt.text(1,
         max(targetHours, finishedHoursThisWeek)/2,
         str(int(float(finishedHoursThisWeek/targetHours)*100))+"%", 
         horizontalalignment='center',
        verticalalignment='center', 
        fontproperties=font)
plt.savefig("C:/Users/Jiali/Desktop/Productivity/Plots/bar3.png",
            dpi=DPI,
            bbox_inches='tight',
            pad_inches = -.04)
plt.close(fig)

 # Bar 4: Work vs Leisure
leisureHours = float(weeklyData[weeklyData["Date"]==thisWeek]["Leisure"])
workHours = float(weeklyData[weeklyData["Date"]==thisWeek]["Total"])
maxOf = max((workHours+leisureHours), 1)
ratio = workHours/(maxOf)
fig,x = plt.subplots()
plt.barh(1,1, color=colors["Leisure"])
plt.barh(1,ratio, color=colors["Total"])
x.xaxis.set_visible(False)
x.yaxis.set_visible(False)
fig.set_size_inches(w2/float(DPI),h2/float(DPI))
plt.text(1/2,
         1,
         str(int(float(ratio)*100))+"%", 
         horizontalalignment='center',
        verticalalignment='center', 
        fontproperties=font)
plt.savefig("C:/Users/Jiali/Desktop/Productivity/Plots/bar4.png",
            dpi=DPI,
            bbox_inches='tight',
            pad_inches = -.04)


# Radar Chart
w3,h3=120,120
font2 = font0.copy()
font2.set_weight('bold')
font2.set_size(9)

categories = list(aggregate)
categories = categories[:-1]
categories2=[]
for i in categories:
    categories2.append(inverseVariables[i])
N = len(categories)

totals=aggregate.loc[0].values.flatten().tolist()
totals = totals[:-1]
totals += totals[:1]     # closes loop
totals = [x / 60 for x in totals]
maxOf = roundup(max(totals))
maxOver4 = int(maxOf/4)

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]
fig.set_size_inches(w3/float(DPI),h3/float(DPI),DPI)
ax = plt.subplot(111, polar=True)
plt.xticks(angles[:-1], 
           categories2, 
           color='black',
           fontproperties=font2)
ax.set_rlabel_position(0)
plt.yticks([maxOver4,maxOver4*2,maxOver4*3],
           [str(maxOver4),str(maxOver4*2),str(maxOver4*3)], 
           color="grey", 
           size=9)
plt.ylim(0,maxOf)
 
ax.plot(angles, 
        totals, 
        linewidth=3, 
        linestyle='solid')
ax.fill(angles,
        totals, 
        'b', 
        alpha=0.1)
plt.savefig("C:/Users/Jiali/Desktop/Productivity/Plots/radar1.png",
            dpi=DPI, 
            bbox_inches = "tight",
            pad_inches = 0)
plt.close(fig)

# Pie Chart
w4,h4 = 200,200
fig, ax = plt.subplots()
fig.set_size_inches(w4/float(DPI),h4/float(DPI),DPI)
patches, texts = plt.pie(workTypeValues, startangle=90)
plt.legend(patches, 
           workTypeLabels, 
           loc="lower left",
           frameon=True,
           prop = {"weight":"bold", "size" :9})
ax.axis("equal")
plt.savefig("C:/Users/Jiali/Desktop/Productivity/Plots/pie1.png", 
            dpi = DPI,bbox_inches = "tight", 
            pad_inches = -0.05)
plt.close(fig)


# Manipulate Desktop Image

# Changeables
startWidth = 1092
startHeight = 523
margins = 10
barMargins = 12


# Uploading Images
plot1 = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Plots/plot1.png")
plot2 = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Plots/plot2.png")
bar1 = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Plots/bar1.png")
bar2 = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Plots/bar2.png")
bar3 = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Plots/bar3.png")
bar4 = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Plots/bar4.png")
radar1 = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Plots/radar1.png")
pie1 = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Plots/pie1.png")

width1, height1 = plot1.size
width3, height3 = bar1.size
width4, height4 = radar1.size
width5, height5 = pie1.size

desktop = pil.Image.open("C:/Users/Jiali/Desktop/Productivity/Core/1.jpg")

draw = pil.ImageDraw.Draw(desktop,"RGBA")
draw.rectangle([(startWidth - margins,
                 startHeight - margins),
                 (1920,1080)], 
                 fill = (0,0,0,128))

# Paste Images
desktop.paste(plot1, (startWidth,
                      startHeight))
desktop.paste(plot2, (startWidth,
                      startHeight+height1+margins))
desktop.paste(bar1, (startWidth+width1 + margins+2, 
                     startHeight))
desktop.paste(bar2, (startWidth+width1 + margins + barMargins + width3+1, 
                     startHeight))
desktop.paste(bar3, (startWidth+width1 + margins + barMargins*2 + width3*2,
                     startHeight))
desktop.paste(bar4, (startWidth+width1 + margins + barMargins*3 + width3*3 -2,
                     startHeight))
desktop.paste(radar1, (startWidth+width1 + margins, 
                       startHeight+2*height1+margins-height4))
desktop.paste(pie1, (startWidth+width1 + 2*margins + width4,
                     startHeight+2*height1+margins-height4))





#Write information
text1 = 14
text2 = 18
title1 = 25

spacing = 2
spacing2 = 4

textStartWidth = startWidth+width1 + margins
textStartHeight = startHeight+2*margins+height4+height3
textMargin = 5
boxHalf = 1920-(1920 - textStartWidth)/2


textStartWidth = startWidth+width1 + margins
textStartHeight = startHeight + margins + height3
textMargin = 5
boxHalf = 1920-(1920 - textStartWidth)/2

# Draw Text Box + Text Half
draw.rectangle([(textStartWidth,textStartHeight),
                 (1915,startHeight+2*height1-height4)], 
                 fill = (0,0,0,192))

draw.line(((boxHalf,textStartHeight + textMargin),(boxHalf,startHeight+2*height1-height4-textMargin)),fill = (255,255,255,255))

# Left Text
text1Line = 0
text2Line = 0
title1Line = 0
marginCount = 0
    # Left Title
drawText("7 Day Average",title1,topMargin = 1, nextLine = True)
    # Item Averages
for i,j in sorted(sevenDayAverages.items(), key=lambda x: x[1], reverse=True):
    drawText(i,text1,topMargin = False)
    drawText(j,text1,rightAlign = True,topMargin = False, nextLine = True)

    # Hours Logged Per Day
drawLine(topMargin = True)
drawText("Daily logged hours", text1, topMargin = 1)
drawText(str(sum(sevenDayAverages.values())), text1, rightAlign = True, nextLine = True)
drawText("Work Per Day", text1)
drawText(str(sum(sevenDayAverages.values())-sevenDayAverages["Leisure"]), text1, rightAlign = True, nextLine = True)

    #Total work hours per week
    

# Right Text/ Reset line values
text1Line = 0
text2Line = 0
title1Line = 0
marginCount = 0

    # Leisure Point value
drawText("Leisure Points:",text2, topMargin = 1, leftBox = False)
drawText(str(int(leisurePoints)), text2, leftBox = False, rightAlign =True, nextLine = True)
    # Spendable Money Value
drawText("Money:", text2, leftBox = False)
drawText("$" + str(spendingMoney), text2,leftBox = False, rightAlign = True, nextLine = True)

drawLine(topMargin = True, leftBox = False)
    # Recent Entries
drawText("Recent Entries", text2, leftBox = False, topMargin = 1, nextLine = True)
toPrint = 0
lineNumber = 0
ii = len(data)-1
while lineNumber<=10:
    get = data.loc[ii]["Date"]
    get = get.strftime("%m-%d")
    if get != toPrint:
        if lineNumber <= 9:
            drawText(str(get), 13, leftBox = False, nextLine = True, topMargin = True,colorToFill = (255-lineNumber*15,255-lineNumber*15,255-lineNumber*15,255-lineNumber*15))
            toPrint = get
            lineNumber+=1
        else: lineNumber+=1
    else:
        drawText("    " + str(data.loc[ii]["Item"]), 14, leftBox = False,colorToFill = (255-lineNumber*15,255-lineNumber*15,255-lineNumber*15,255-lineNumber*15))
        drawText(str(data.loc[ii]["Length"]), 13, leftBox = False, rightAlign = True, nextLine = True, colorToFill = (255-lineNumber*15,255-lineNumber*15,255-lineNumber*15,255-lineNumber*15))
        ii -= 1
        lineNumber+=1
    
    
        
    



desktop.save("C:/Users/Jiali/Desktop/Productivity/Desktop/1.png",
             subsampling=0, 
             quality=100)
desktop.save("C:/Users/Jiali/Desktop/Productivity/Desktop/2.png", 
             subsampling=0, 
             quality=100)

print("Finished")

