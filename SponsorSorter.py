import Image
import math
import csv
import time

#Rescale an image to given width,height
def getImageSize(image,width,height):
    width=int(width)
    height=int(height)
    back = Image.new("RGBA",(width,height),(255,255,255,0))
    OGwidth=width
    OGheight=height
    im=image
    factor=1.0
    if im.size[0]<width and im.size[1]<height:
        print "Picture is not of enough quality"
    if im.size[0]>width-HORIZONTALPADDING:
        factor=(width-HORIZONTALPADDING)/(im.size[0]*1.0)
    if im.size[1]*factor>height-VERTICALPADDING:
        factor*=(height-VERTICALPADDING)/(im.size[1]*factor)
    width=math.floor(im.size[0]*factor)
    height=math.floor(im.size[1]*factor)
    im.thumbnail((width,height),Image.BILINEAR)
    back.paste(im,(int(OGwidth/2-(width/2)),int(OGheight/2-(height/2))))
    return back;

#Translate an image's name to a location
def img(name):
    name.replace(" ","\ ")
    image=Image.open("Logos/"+name+".png");
    image.convert("RGBA");
    return image;

#Generate a "tier" of images
def getTier(tier,slots,slotHeight):
    back = Image.new("RGBA",(WIDTH,HEIGHT),(255,255,255,0))
    curX=0;
    curY=0;
    lastTier=False
    lastTierSize=0
    index=0

    if len(tier)-index<slots:
        lastTier=True
        lastTierSize=len(tier)-index
    for t in tier:
        xOff=0
        if lastTier:
            xOff=int((slots-lastTierSize)*(WIDTH/slots)/2)
        im=getImageSize(img(t),math.floor(WIDTH/slots),slotHeight)
        back.paste(im,(curX*(WIDTH/slots)+xOff,curY*slotHeight))
        curX+=1
        index+=1
        if curX>=slots:
            curX=0
            curY+=1
            if len(tier)-index<slots:
                lastTier=True
                lastTierSize=len(tier)-index
    if curX==0:
        curY-=1
    return back.crop((0,0,WIDTH,curY*slotHeight+slotHeight))

def getTotalHeight():
    curX=0
    curY=0
    height=0
    for i in range(0,len(tier)):
        curX=0
        curY=0
        if len(tier[i])>0:
            curY=1
        for t in tier[i]:
            curX+=1
            if curX>slotNumber[i]:
                curX=0
                curY+=1
        height+=slotHeights[i]*curY
    return height

#Generate all tiers
def makeTiers():
    sizeMult=HEIGHT/getTotalHeight()
    back=Image.new("RGBA",(WIDTH,HEIGHT),(255,255,255,255))
    curY=0;
    for i in range(0,len(tier)):
        img=getTier(tier[i],slotNumber[i],slotHeights[i]*sizeMult)
        back.paste(img,(0,curY),mask=img)
        curY+=img.size[1]
    return back
     
def readTiers(fileName):
    sponsor=[]
    with open(fileName,'rb') as csvfile:
        reader=csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in reader:
            sponsor.append((row[0],int(row[1])))
    tier=[]
    for i in range(0,len(tierBorders)):
        tier.append([])
    print sponsor
    for t in sponsor:
        for i in range(0,len(tierBorders)):
            if t[1]>=tierBorders[i]:
                tier[i].append(t)
                break
    for i in range(0,len(tier)):
            ls=sorted(tier[i],key=lambda x:x[1])[::-1]
            tier[i]=[]
            for t in ls:
                tier[i].append(t[0])
    return tier

# Change these variables for differnt things
tierBorders=[100000,20000,25000,10000,1000,0]
slotNumber=[1,3,1,4,5,6]
slotHeights=[60,40,35,30,30,25]
tier=readTiers("bedragen.csv")    
WIDTH=1920*2
HEIGHT=1080*2
filename="Output/Slide"+time.strftime("%Y-%m-%d %H:%M:%S")+".png"

HORIZONTALPADDING=20*2
VERTICALPADDING=10*2
makeTiers().save(filename,format="PNG");

