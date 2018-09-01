from reportlab.pdfgen import canvas
 
from reportlab.lib.colors import yellow, red, black,white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

from math import pi

import sys

# Done Vertical tape should wrap on 3/4



# Config
tapeHeight = 6.7*mm
turretDiameter = 27*mm
turretClicks = 60
turretClicksPerMoa = 4

turretDiameterMargin = 0.0*mm
overscanWidth = 0*mm
centerLineHeight = tapeHeight
moaLineHeight = 1.5*mm
labelY = 3.5*mm
labelLineHeight = 3.0*mm

labelFontSize = 8
titleFontSize = 12

verticalLables = [
    (120, 3),
    (140, 7),
    (160, 12),
    (180, 18),
    (200, 24),
    (220, 32),
    (240, 40),
    (260, 49)
]

horizontalLabels = [

]

baseX = 5*mm
baseY = 250*mm


# Subcalc
clickSpacing = ((turretDiameter + turretDiameterMargin) * pi) / turretClicks
moaSpacing = clickSpacing * 4

tapeWidth = (turretDiameter + turretDiameterMargin) * pi + overscanWidth * 2


# Pdf
c = canvas.Canvas("cds.pdf", pagesize=A4)
c.saveState()


## Move elements
c.translate(baseX, baseY)

# Title
c.drawString(0, 0,"CCI 17HMR GamePoint")

## Vertical turret
c.translate(0, -10*mm)
c.setFillColor(black)
c.rect(0,0,tapeWidth,tapeHeight, stroke=0, fill=1)

# Center line
clX = tapeWidth*3/4.0
c.setStrokeColor(yellow)
c.setLineWidth(2)
c.line(clX, 0, clX, 0 + centerLineHeight)

# Moa lines
c.setStrokeColor(yellow)
c.setLineWidth(2)
xd = 0
for m in range(0,int(turretClicks/turretClicksPerMoa)):
    xd = xd + moaSpacing
    if xd > tapeWidth * 0.25:
        xd = xd - tapeWidth
    c.line(clX + xd, 0, clX + xd, moaLineHeight)


# Meter lables
c.setFillColor(yellow)
c.setStrokeColor(yellow)
c.setLineWidth(1)
c.setFont("Helvetica", 8)
for l in verticalLables:
    lClick = l[1]
    if lClick > turretClicks*3/4:
        lClick = lClick - turretClicks
    lX = 0 + tapeWidth*3/4.0 - lClick*clickSpacing
    c.line(lX, 0, lX, 0 + labelLineHeight)
    c.drawCentredString(lX, 0 + labelY, str(l[0]))


## Horizontal turret
c.translate(0, -10*mm)
c.setFillColor(black)
c.rect(0,0,tapeWidth,tapeHeight, stroke=0, fill=1)

# Center line
clX = 0 + tapeWidth*2/4.0
c.setStrokeColor(yellow)
c.setLineWidth(2)
c.line(clX, 0, clX, 0 + centerLineHeight)




# Moa lines
c.setStrokeColor(yellow)
c.setFillColor(yellow)
c.setLineWidth(2)
xd = 0
for m in range(1,int(turretClicks/(2*turretClicksPerMoa))+1):
    xd = xd + moaSpacing
    c.line(clX + xd, 0, clX + xd, 0 + moaLineHeight)
    c.line(clX - xd, 0, clX - xd, 0 + moaLineHeight)

    c.saveState()
    c.translate(clX - xd + labelFontSize/4, labelY)
    c.rotate(90)
    c.drawCentredString(0, 0, str(m))
    c.restoreState()
    c.saveState()
    c.translate(clX + xd + labelFontSize/4, labelY)
    c.rotate(90)
    c.drawCentredString(0, 0, str(-m))
    c.restoreState()
    #c.drawCentredString(clX + xd, labelY, str(-m))
    #c.drawCentredString(baseY + labelY, -(clX - xd)-1*mm, str(m))
    #c.drawCentredString(baseY + labelY, -(clX + xd)-1*mm, str(-m))
    #c.rotate(-90)

c.restoreState()

c.save()
sys.exit(0)
