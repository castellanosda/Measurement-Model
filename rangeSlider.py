"""
  "THE BEER-WARE LICENSE" (Revision 42):
  <shinhalsafar@gmail.com> wrote this file. As long as you retain this notice you
  can do whatever you want with this stuff. If we meet some day, and you think
  this stuff is worth it, you can buy me a beer in return.

	Stephen Damm (shinhalsafar@gmail.com) 
"""


"""
---Change log---
Canvas background color
Show/hide major and minor ticks
Set number of major and minor ticks
Change tick text y padding

"""

import logging
from tkinter import CURRENT, ALL
from tkinter import Canvas


'''
logging.INFO
logging.ERROR
logging.WARN
'''
LOGGING_LEVEL = logging.INFO

'''
logging global
'''
log = logging.getLogger("default")


'''
The view (V in MVC)
'''	
class RangeSlider(Canvas):
	'''
	Fields
	- meaningful names
	'''
	__canvasWidth = 0
	__canvasHeight = 0

	__canvasCenterX = 0
	__canvasCenterY = 0

	__majorTickSpacing = 10
	__minorTickSpacing = 5

	__paintTicks = False
	__minorTicksOn = True
	__majorTicksOn = True
	__tickPadY = 10

	__leftCaretId = 0
	__rightCaretId = 0
	__barId = 0
	__sliderId = 0
	__majorTicks = []
	__minorTicks = []
	__textText = []


	# defaults for widget look`n`feel
	__sliderColor = "gray60"
	__sliderNoFocusColor = "gray60"    #gray80
	__sliderHighlightedColor = "gray40"
	__sliderOutlineColor = "black"
	__sliderNoFocusOutlineColor = "black"     #gray80

	__barColor = "gray85"
	__barNoFocusColor = "gray85"       #gray95
	__barOutlineColor = "black"
	__barNoFocusOutlineColor = "black"    #gray80
	__barWidthPercent = 0.90
	__barHeightPercent = 0.05
	__barBevelWidthPercent = 0.01
	__backgroundColor = "white"
	
	__caretColor = "gray70"
	__caretNoFocusColor = "gray70"     #gray80
	__caretHighlightedColor = "gray40"	
	__caretOutlineColor = "black"
	__caretNoFocusOutlineColor = "black"  #gray80
	__caretWidthPercent = 0.035
	__caretHeightPercent = 1.50
	
	__tickOutlineColor = "black"
	__tickNoFocusOutlineColor = "black"   #gray80
	
	__tickWidthPercent = 0.001
	__majorTickHeightPercent = 0.06
	__minorTickHeightPercent = 0.05
	
	# store values for easy look up of current dimensions
	__barX = 0
	__barY = 0
	__barWidth = 0
	__barHeight = 0
	__caretWidth = 0
	__caretHeight = 0

	__inFocus = False
	__alwaysFocus = True
	__highlightedId = 0
	

	'''
	Constructor
	'''
	def __init__(self, master, **cnf):
		self.mainCanvas = Canvas
		self.mainCanvas.__init__(self, master, highlightthickness=0, background=self.__backgroundColor)

		self.__model = RangeSliderModel()
		self.__controller = RangeSliderController(self.__model, self)
		self.configure(**cnf)

		self.__model.subscribe(self.__controller.update)		
		self.bind("<Configure>", self.__resize)
		self.bind("<Key>", self.__controller.rangeSlider_onKeyPress)
		
		# critical to the focus subsystem!
		self.master.bind("<Button>", self.__focusCheck, add="+")
		self.master.bind("<Key>", self.__focusCheck, add="+")
				

	'''
	Configure
	- pops all the RangeSlider specific variables off the cnf dict
	- uses sane default values if no value is found
	'''
	def configure(self, **cnf):
		try:
			lowerBound = cnf.pop('lowerBound')
			self.__model.setLowerBound(lowerBound)
		except Exception:
			self.__model.setLowerBound(0)

		try:
			upperBound = cnf.pop('upperBound')
			self.__model.setUpperBound(upperBound)
		except Exception:
			self.__model.setUpperBound(100)

		try:
			initialLowerBound = cnf.pop('initialLowerBound')
			self.__model.setLower(initialLowerBound)
		except Exception:
			self.__model.setLower(0)

		try:
			initialUpperBound = cnf.pop('initialUpperBound')
			self.__model.setUpper(initialUpperBound)
		except Exception:
			self.__model.setUpper(100)
			
		try:
			sliderColor = cnf.pop('sliderColor')
			self.__sliderColor = sliderColor
		except Exception:
			None
		try:
			sliderHighlightedColor = cnf.pop('sliderHighlightedColor')
			self.__sliderHighlightedColor = sliderHighlightedColor
		except Exception:
			None
		try:
			sliderNoFocusColor = cnf.pop('sliderNoFocusColor')
			self.__sliderNoFocusColor = sliderNoFocusColor
		except Exception:
			None
		try:
			sliderOutlineColor = cnf.pop('sliderOutlineColor')
			self.__sliderOutlineColor = sliderOutlineColor
		except Exception:
			None
		try:
			sliderNoFocusOutlineColor = cnf.pop('sliderNoFocusOutlineColor')
			self.__sliderNoFocusOutlineColor = sliderNoFocusOutlineColor
		except Exception:
			None			
		try:
			barColor = cnf.pop('barColor')
			self.__barColor = barColor
		except Exception:
			None
		try:
			barHighlightedColor = cnf.pop('barHighlightedColor')
			self.__barHighlightedColor = barHighlightedColor
		except Exception:
			None	
		try:
			barNoFocusColor = cnf.pop('barNoFocusColor')
			self.__barNoFocusColor = barNoFocusColor
		except Exception:
			None
		try:
			barOutlineColor = cnf.pop('barOutlineColor')
			self.__barOutlineColor = barOutlineColor
		except Exception:
			None
		try:
			barNoFocusOutlineColor = cnf.pop('barNoFocusOutlineColor')
			self.__barNoFocusOutlineColor = barNoFocusOutlineColor
		except Exception:
			None			
		try:
			caretColor = cnf.pop('caretColor')
			self.__caretColor = caretColor
		except Exception:
			None
		try:
			caretHighlightedColor = cnf.pop('caretHighlightedColor')
			self.__caretHighlightedColor = caretHighlightedColor
		except Exception:
			None	
		try:
			caretNoFocusColor = cnf.pop('caretNoFocusColor')
			self.__caretNoFocusColor = caretNoFocusColor
		except Exception:
			None
		try:
			caretOutlineColor = cnf.pop('caretOutlineColor')
			self.__caretOutlineColor = caretOutlineColor
		except Exception:
			None
		try:
			caretNoFocusOutlineColor = cnf.pop('caretNoFocusOutlineColor')
			self.__caretNoFocusOutlineColor = caretNoFocusOutlineColor
		except Exception:
			None
		try:
			barWidthPercent = cnf.pop('barWidthPercent')
			self.__barWidthPercent = barWidthPercent
		except Exception:
			None			
		try:
			barHeightPercent = cnf.pop('barHeightPercent')
			self.__barHeightPercent = barHeightPercent
		except Exception:
			None
		try:
			caretWidthPercent = cnf.pop('caretWidthPercent')
			self.__caretWidthPercent = caretWidthPercent
		except Exception:
			None
		try:
			caretHeightPercent = cnf.pop('caretHeightPercent')
			self.__caretHeightPercent = caretHeightPercent
		except Exception:
			None
		try:
			backgroundColor = cnf.pop('background')
			self.__backgroundColor = backgroundColor
			self.mainCanvas.configure(self, background=self.__backgroundColor)
		except Exception:
			None
		try:
			tickColor = cnf.pop('tickColor')
			self.__tickNoFocusOutlineColor = tickColor
			self.__tickOutlineColor = tickColor
			self.redraw()
		except Exception:
			None

	'''
	Subscribe
	- pass along subscribers to the model changer
	'''
	def subscribe(self, func):
		self.__model.subscribe(func)


	'''
	Accessors/Mutators
	'''
	def getUpper(self):
		return self.__model.getUpper()


	def setUpper(self, u):
		self.__model.setUpper(u)


	def getLower(self):
		return self.__model.getLower()


	def setLower(self, l):
		self.__model.setLower(l)


	def getUpperBound(self):	
		return self.__model.getUpperBound()


	def setUpperBound(self, ub):
		self.__model.setUpperBound(ub)
		self.redraw()


	def getLowerBound(self):
		return self.__model.getLowerBound()
	

	def setLowerBound(self, lb):
		self.__model.setLowerBound(lb)
		self.redraw()
		
		
	def getBoundsRange(self):
		return self.__model.getBoundsRange()


	def getRange(self):
		return self.__model.getRange()


	def getMajorTickSpacing(self):
		return self.__majorTickSpacing


	def setMajorTickSpacing(self, majorTS):
		self.__majorTickSpacing = majorTS
		self.redraw()


	def getMinorTickSpacing(self):
		return self.__minorTickSpacing


	def setMinorTickSpacing(self, minorTS):
		self.__minorTickSpacing = minorTS
		self.redraw()


	def getPaintTicks(self):
		return self.__paintTicks


	def setPaintTicks(self, b):
		self.__paintTicks = b
		self.redraw()


	def getSnapToTicks(self):
		return self.__controller.getSnapToTicks()


	def setSnapToTicks(self, b):
		self.__controller.setSnapToTicks(b)


	def getLeftCaretId(self):
		return self.__leftCaretId


	def getRightCaretId(self):
		return self.__rightCaretId


	def getBarId(self):
		return self.__barId


	def getSliderId(self):
		return self.__sliderId

	
	def getCanvasCenterY(self):
		return self.__canvasCenterY

	def getBarX(self):
		return self.__barX
		
	def getBarY(self):
		return self.__barY
		
	def getBarWidth(self):
		return self.__barWidth
		
	def getBarHeight(self):
		return self.__barHeight

	def getCaretHeight(self):
		return self.__caretHeight
		
	def getCaretWidth(self):
		return self.__caretWidth
		
	def getLeftCaretX(self):
		return self.coords(self.__leftCaretId)[0]
		
	def getLeftCaretY(self):
		return self.coords(self.__leftCaretId)[1]
		
	def getRightCaretX(self):
		return self.coords(self.__rightCaretId)[0]
		
	def getRightCaretY(self):
		return self.coords(self.__rightCaretId)[1]		
		
	def getTickWidth(self):
		return self.__canvasWidth * self.__tickWidthPercent
		
	def getHighlightedId(self):
		return self.__highlightedId
    
	def showMinorTicks(self, boolean):
		self.__minorTicksOn = boolean

	def showMajorTicks(self, boolean):
		self.__majorTicksOn = boolean
    
	def setNumberOfMajorTicks(self, number):
		n = str(number)
		if (not n.isdigit()):
			raise TypeError("Number of ticks must be a positive integer")
		if (int(n) == 0):
			self.setMajorTickSpacing(-1)
		else:
			self.setMajorTickSpacing((abs(self.getUpperBound()) + abs(self.getLowerBound()))/int(number))

	def setNumberOfMinorTicks(self, number):
		n = str(number)
		if (not n.isdigit()):
			raise TypeError("Number of ticks must be a positive integer")
		if (int(n) == 0):
			self.setMinorTickSpacing(-1)
		else:
			self.setMinorTickSpacing((abs(self.getUpperBound()) + abs(self.getLowerBound()))/int(number))

	def setTickPadding(self, pady):
		self.__tickPadY = pady
    
		
	
	'''
	Resize Function
	- captures the new canvas dimensions
	- causes a redraw
	'''
	def __resize(self, e):
		log.debug("Resize, New Size -- " + 
				  str(e.width) + " : " + str(e.height))

		self.__canvasWidth = e.width
		self.__canvasHeight = e.height
		self.__canvasCenterX = e.width / 2.0
		self.__canvasCenterY = e.height / 2.0

		self.redraw()

		
	'''
	FullDraw Function
	'''
	def __draw(self,e):
		# only redraw if the canvas is visible still
		if (self.__canvasWidth >= 0 and self.__canvasHeight >= 0):
			log.debug("Doing a fulldraw")
			
			self.__tickText = []
			
			self.__createBar()
			self.__caretWidth = self.__barWidth*self.__caretWidthPercent
			self.__caretHeight = self.__barHeight*self.__caretHeightPercent			
			if (self.__paintTicks):
				if (self.__majorTicksOn):
					self.__createMajorTicks()
				if (self.__minorTicksOn):
					self.__createMinorTicks()
			self.__createSlider()
			self.__createLeftCaret()
			self.__createRightCaret()
			
			if (self.__inFocus == True):
				self.setFocus()							
				self.__changeHighlighted(self.__highlightedId)

	'''
	Draw the bar
	'''
	def __createBar(self):		
		self.__barWidth = self.__canvasWidth * self.__barWidthPercent
		newbarWidth = self.__barWidth + (self.__canvasWidth * self.__tickWidthPercent * 2.0)		
		self.__barHeight = self.__canvasHeight * self.__barHeightPercent
		self.__barX = self.__canvasCenterX - (self.__barWidth / 2)
		newbarX = self.__barX - (self.__canvasWidth * self.__tickWidthPercent)	
		self.__barY = self.__canvasCenterY - (self.__barHeight + (self.__canvasHeight * self.__majorTickHeightPercent)) / 2.0
		self.__barId = self.create_rectangle(newbarX, self.__barY, 
											 newbarX + newbarWidth, 
											 self.__barY + self.__barHeight,
											 outline=self.__barNoFocusOutlineColor, 
											 fill=self.__barNoFocusColor)


	'''
	Draw left caret
	'''
	def __createLeftCaret(self):
		curId = self.__leftCaretId			
		self.__leftCaretId = self.__createCaret(
			self.__caret_onMouseEnter,
			self.__leftCaret_onMouseLeave,
			self.__leftCaret_onMouseClick,
			self.__controller.leftCaret_onMouseMotion)
		if (curId == self.__highlightedId and self.__highlightedId != 0):
			self.__highlightedId = self.__leftCaretId


	'''
	Draw right caret
	'''
	def __createRightCaret(self):
		curId = self.__rightCaretId									  	
		self.__rightCaretId = self.__createCaret(
			self.__caret_onMouseEnter,
			self.__rightCaret_onMouseLeave,
			self.__rightCaret_onMouseClick,
			self.__controller.rightCaret_onMouseMotion)
		if (curId == self.__highlightedId and self.__highlightedId != 0):
			self.__highlightedId = self.__rightCaretId										  			


	'''
	Generic draw caret function Function
	'''
	def __createCaret(self, enterCallback, leaveCallback, clickCallback, motionCallback):									  
		hw = self.__caretWidth / 2.0
		hh = self.__caretHeight / 2.0
		cx = 0 + hw
		cy = 0 + hh
		p1x = cx - hw
		p1y = 0
		p2x = cx+hw
		p2y = 0
		p3x = cx+hw
		p3y = 0 + hh
		p4x = cx
		p4y = cy + hh
		p5x = cx - hw
		p5y = 0+hh
		p6x = cx - hw
		p6y = 0		
		
		newCaret = self.create_polygon(p1x, p1y, 
										p2x, p2y, 
										p3x, p3y, 
										p4x, p4y, 
										p5x, p5y, 	
										p6x, p6y, 										
										  outline=self.__caretNoFocusOutlineColor, 
										  fill=self.__caretNoFocusColor)
		
		self.tag_bind(newCaret, "<Button-1>", 
					  self.__controller.caret_onMouseClick, add="+")
		self.tag_bind(newCaret, "<Button-3>",
					  self.__controller.caret_onMouseClick, add="+")
		self.tag_bind(newCaret, "<B1-Motion>", motionCallback)
		self.tag_bind(newCaret, "<ButtonRelease-1>", 
					  self.__controller.caret_onMouseRelease)
					  
		self.tag_bind(newCaret, "<B1-Motion>", 
					  self.__caret_onMouseEnter, add="+")
		self.tag_bind(newCaret, "<Enter>", enterCallback)					  
		self.tag_bind(newCaret, "<Leave>", leaveCallback)
		self.tag_bind(newCaret,"<Button-1>", clickCallback, add="+")
		self.tag_bind(newCaret,"<Button-3>", clickCallback, add="+")
		return newCaret


	'''
	Draw slider
	'''
	def __createSlider(self):
		curId = self.__sliderId
		self.__sliderId = self.create_rectangle(0, 0, 
												self.__barWidth, self.__barHeight,
												fill=self.__sliderNoFocusColor,
												outline=self.__sliderNoFocusOutlineColor)
		if (curId == self.__highlightedId and self.__highlightedId != 0):
			self.__highlightedId = self.__sliderId
			
		self.tag_bind(self.__sliderId,"<Button-1>",
					  self.__controller.slider_onMouseClick, add="+");
		self.tag_bind(self.__sliderId,"<B1-Motion>",
					  self.__controller.slider_onMouseMotion);
		self.tag_bind(self.__sliderId,"<B1-Motion>", 
					  self.__slider_onMouseEnter,
					  add = "+")
		self.tag_bind(self.__sliderId,"<Enter>", self.__slider_onMouseEnter)
		self.tag_bind(self.__sliderId,"<Leave>", self.__slider_onMouseLeave)
		self.tag_bind(self.__sliderId,"<Button-1>", self.__slider_onMouseClick, add="+")
		self.tag_bind(self.__sliderId,"<Button-3>", self.__slider_onMouseClick, add="+")


	'''
	Draw the major ticks
	'''
	def __createMajorTicks(self):
		self.__majorTicks = []
		self.__createTicks(self.__majorTicks, 
						   self.__canvasWidth * self.__tickWidthPercent,
						   self.__canvasHeight * self.__majorTickHeightPercent,
						   self.getMajorTickSpacing(),
						   True)


	'''
	Draw the minor ticks
	'''
	def __createMinorTicks(self):
		self.__minorTicks = []
		self.__createTicks(self.__minorTicks, 
						   self.__canvasWidth * self.__tickWidthPercent,
						   self.__canvasHeight * self.__minorTickHeightPercent,
						   self.getMinorTickSpacing(),
						   False)


	'''
	Generic draw ticks Function
	'''
	def __createTicks(self, tickArray, width, height, tickSpacing, createText):	
		tickCount = self.__model.getBoundsRange() / tickSpacing
		# zero vision
		if (tickCount == 0):
			return
		
		tickXStart = self.__barX
		tickYStart = self.__barY + (self.__barHeight)	  
		tickInterval = (self.__barWidth) / float(tickCount)

		for i in range(0, int(tickCount)+1):
			tickX = tickXStart + (tickInterval * i) - width / 2.0
			newMajorTick = self.create_rectangle(tickX, 
												 tickYStart, 
												 tickX + width, 
												 tickYStart + height,
												 outline=self.__tickNoFocusOutlineColor)
			if (createText):				
				strVal = self.__model.getLowerBound() + tickSpacing*float(i)
				self.__tickText.append(self.create_text(tickX, 
										tickYStart + height + self.__tickPadY, 
										text=str("%.2f"%(strVal)),
										fill=self.__tickNoFocusOutlineColor,
										font=("Default", "8", "")))

			self.tag_bind(newMajorTick, "<1>", self.__controller.majorTick_onClick)
			self.tag_bind(newMajorTick, "<Enter>", self.__tick_onMouseEnter)
			self.tag_bind(newMajorTick, "<Leave>", self.__tick_onMouseLeave)

			tickArray.append(newMajorTick)


	'''
	Full redraw logic
	Exposed
	'''
	def redraw(self):
		self.delete(ALL)
		self.__draw(None)
		self.__controller.update(None)


	'''
	Helper - Change Highlighted
	- sorts out the logic when user is clicking around the different
	- functional parts of the program.
	'''
	def __changeHighlighted(self, id):
		oldId = self.__highlightedId
		self.__highlightedId = id

		# unhighlight if necessary
		if (oldId != id):		
			if (oldId == self.__sliderId):
				self.__slider_onMouseLeave(None)				
				self.itemconfig(self.__sliderId, fill=self.__sliderColor)
			elif (oldId == self.__leftCaretId):
				self.__leftCaret_onMouseLeave(None)
				self.itemconfig(self.__leftCaretId, fill=self.__caretColor)
			elif (oldId == self.__rightCaretId):
				self.__rightCaret_onMouseLeave(None)
				self.itemconfig(self.__rightCaretId, fill=self.__caretColor)		
			
		# highlight new one if necessary
		if (id == self.__sliderId):
			self.__slider_onMouseEnter(None)
			self.itemconfig(self.__sliderId, fill=self.__sliderHighlightedColor)
		elif (id == self.__leftCaretId):
			self.__caret_onMouseEnter(None)
			self.itemconfig(self.__leftCaretId, fill=self.__caretHighlightedColor)
		elif (id == self.__rightCaretId):
			self.__caret_onMouseEnter(None)
			self.itemconfig(self.__rightCaretId, fill=self.__caretHighlightedColor)
			

	'''
	Event - caretMouseClick
	- cause selection of the caret clicked
	'''
	def __leftCaret_onMouseClick(self, e):
		pass#self.__changeHighlighted(self.__leftCaretId)
	def __rightCaret_onMouseClick(self, e):
		pass#self.__changeHighlighted(self.__rightCaretId)		
		
		
	'''
	Event - caretMouseClick
	- cause selection of the caret clicked
	'''
	def __slider_onMouseClick(self, e):
		pass#self.__changeHighlighted(self.__sliderId)		
				

	'''
	Event - caretMouseEnter
	'''
	def __caret_onMouseEnter(self, e):
		pass#self.master.configure(cursor="hand2")
		#if (self.__inFocus):
		#	self.itemconfig(CURRENT, fill=self.__caretHighlightedColor)


	'''
	Event - caretMouseLeave
	'''
	def __leftCaret_onMouseLeave(self, e):
		pass#self.master.configure(cursor="")		
		#if (self.__inFocus):
		#	if not (self.__highlightedId == self.__leftCaretId):
		#		self.itemconfig(CURRENT, fill=self.__caretColor)			
	def __rightCaret_onMouseLeave(self, e):
		pass#self.master.configure(cursor="")		
		#if (self.__inFocus):
		#	if not (self.__highlightedId == self.__rightCaretId):
		#		self.itemconfig(CURRENT, fill=self.__caretColor)			


	'''
	Event - sliderMouseEnter
	'''
	def __slider_onMouseEnter(self, e):
		pass#self.master.configure(cursor="hand2")
		#if (self.__inFocus):
		#		self.itemconfig(CURRENT, fill=self.__sliderHighlightedColor)


	'''
	Event - sliderMouseLeave
	'''
	def __slider_onMouseLeave(self, e):
		pass#self.master.configure(cursor="")
		#if (self.__inFocus):
		#	if not (self.__highlightedId == self.__sliderId):
		#		self.itemconfig(CURRENT, fill=self.__sliderColor)


	'''
	Event - caretMouseEnter
	'''
	def __tick_onMouseEnter(self, e):
		pass#self.master.configure(cursor="center_ptr")
		

	'''
	Event - caretMouseLeave
	'''
	def __tick_onMouseLeave(self, e):
		pass#self.master.configure(cursor="")


	'''
	Event - handle focus!
	'''
	def __focusCheck(self, e):
		log.debug("FocusCheck...")
		if (e.widget == self and not self.__inFocus):		
			self.setFocus()
		elif (e.widget != self and self.__inFocus):
			self.clearFocus()
			
	
	'''
	Helper - Clear Focus
	- sets the items to be in their non focus state
	'''
	def clearFocus(self):
		self.__inFocus = False
		self.itemconfig(self.__barId, fill=self.__barNoFocusColor, outline=self.__barNoFocusOutlineColor)
		self.itemconfig(self.__sliderId, fill=self.__sliderNoFocusColor, outline=self.__sliderNoFocusOutlineColor)
		self.itemconfig(self.__leftCaretId, fill=self.__caretNoFocusColor, outline=self.__caretNoFocusOutlineColor)
		self.itemconfig(self.__rightCaretId, fill=self.__caretNoFocusColor, outline=self.__caretNoFocusOutlineColor)
	
		for id in self.__majorTicks:
			self.itemconfig(id, outline=self.__tickNoFocusOutlineColor);
		for id in self.__minorTicks:
			self.itemconfig(id, outline=self.__tickNoFocusOutlineColor);	
		for id in self.__tickText:
			self.itemconfig(id, fill=self.__tickNoFocusOutlineColor);	


	'''
	Helper - Set Focus
	- sets the focus colors
	'''
	def setFocus(self):
		self.__inFocus = True
		self.focus_set()
		self.itemconfig(self.__barId, fill=self.__barColor, outline=self.__barOutlineColor)
		self.itemconfig(self.__sliderId, fill=self.__sliderColor, outline=self.__sliderOutlineColor)
		self.itemconfig(self.__leftCaretId, fill=self.__caretColor, outline=self.__caretOutlineColor)
		self.itemconfig(self.__rightCaretId, fill=self.__caretColor, outline=self.__caretOutlineColor)
		
		for id in self.__majorTicks:
			self.itemconfig(id, outline=self.__tickOutlineColor);
		for id in self.__minorTicks:
			self.itemconfig(id, outline=self.__tickOutlineColor);	
		for id in self.__tickText:
			self.itemconfig(id, fill=self.__tickOutlineColor);					
		




'''
the controller (C in MVC)
'''
class RangeSliderController():
	'''
	Fields
	'''
	__model = None
	__view = None

	__lastMouseX = 0
	
	__snapToTicks = False


	'''
	Constructor
	'''
	def __init__(self, rs_model, rs_view):
		self.__model = rs_model
		self.__view = rs_view


	'''
	Accessors/Mutators
	'''		
	def getSnapToTicks(self):
		return self.__snapToTicks


	def setSnapToTicks(self, b):
		self.__snapToTicks = b


	'''
	Event - on Key press
	- handles key presses directed at the canvas
	'''
	def rangeSlider_onKeyPress(self, e):
		pass
		"""
		# unit step	
		lowerstep = 0
		upperstep = 0
	
		# get direction
		direction = 0
		if (e.keysym == "Left"):
			direction = -1
		elif (e.keysym == "Right"):
			direction = 1		
		else:
			return
			
		#if (direction == -1 and self.__model.getLower() <= self.__model.getLowerBound()):
		#	return
		#elif (direction == 1 and self.__model.getUpper() >= self.__model.getUpperBound()):
		#	return
	
		bRoundUp = False
		if (direction == 1):
			bRoundUp = True
					
		step = self.__model.getBoundsRange() / self.__view.getBarWidth()	
		step *= direction
		if (self.__view.getHighlightedId() == self.__view.getLeftCaretId()):
			if (direction == 1 and self.__view.getLower() >= self.__view.getUpper()):
				self.__view.setLower(self.__view.getUpper())
				return	
		
			if (self.__snapToTicks):
				step += self.__model.getLower()
				step = self.barRoundValue(step, self.__view.getMinorTickSpacing(), bRoundUp)
				step -= self.__model.getLower()

			self.__model.setLower(self.__model.getLower() + step)
			return
		elif (self.__view.getHighlightedId() == self.__view.getRightCaretId()):
			if (self.__snapToTicks):
				step += self.__model.getUpper()
				step = self.barRoundValue(step, self.__view.getMinorTickSpacing(), bRoundUp)
				step -= self.__model.getUpper()

			self.__model.setUpper(self.__model.getUpper() + step)		
			return
		elif (self.__view.getHighlightedId() == self.__view.getSliderId()):
			# prevent 0 division
			if (self.__model.getBoundsRange() <= 0):
				return				
			
			if not (self.__snapToTicks):
				step = self.__model.getBoundsRange() / self.__view.getBarWidth()
				step *= direction
				
				lowerstep = step
				upperstep = step
			else:		
				step = self.__model.getBoundsRange() / self.__view.getBarWidth()
				step *= direction
				lowerstep = (self.__model.getLower()+step) 
				upperstep = (self.__model.getUpper()+step)

				lowerstep = self.barRoundValue(lowerstep, self.__view.getMinorTickSpacing(), bRoundUp)
				lowerstep -= self.__model.getLower()
				upperstep = self.barRoundValue(upperstep, self.__view.getMinorTickSpacing(), bRoundUp)
				upperstep -= self.__model.getUpper()			
				
			# move the range 1 unit to the direction pressed
			self.__model.setLower(self.__model.getLower() + lowerstep)
			self.__model.setUpper(self.__model.getUpper() + upperstep)
		"""			
		
			
	'''
	Helper - Round to snap
	'''
	def barRoundValue(self, value, roundToNearest, bRoundUp):
		tmpVal = (value / roundToNearest) + (-0.5 + int(bRoundUp))
		tmp = int(tmpVal)
		tmpVal = round((tmpVal - tmp) * pow(10, 0))
		nValue = tmp + tmpVal / pow(10, 0)
		roundedValue = nValue * roundToNearest
		
		return roundedValue
		

	'''
	Event - Caret On Mouse Click event
	- nothing
	'''
	def caret_onMouseClick(self, e):
		log.debug("Button " + str(e.num) + " @ " + 
				  str(e.x) + " : " + str(e.y))

		self.__lastMouseX = e.x


	'''
	Event - Caret on mouse release
	'''
	def caret_onMouseRelease(self, e):
		return

		
	'''
	Event - Caret OnMouseMotion
	- moves the caret that fired the event
	- the amount moved is a delta between cur caret bar pos
	- and the amount moved in canvas coords
	'''
	def leftCaret_onMouseMotion(self, e):
		pass
		"""
		log.debug(str(self.__view.canvasx(e.x)) + " : " + 
				  str(self.__view.canvasy(e.y)))		
		
		# leave early if the mouse is not aligned with the caret anymore
		rightCaretX = self.__view.getRightCaretX() + (self.__view.getCaretWidth())
		if (self.__view.canvasx(e.x) < self.__view.getBarX()):			
			self.__model.setLower(self.__model.getLowerBound())			
		# edge case, inside right caret
		elif (self.__view.canvasx(e.x) > rightCaretX):
			self.__model.setLower(self.__model.getUpper())
			self.__lastMouseX = e.x
		else:					
			if (self.__snapToTicks):
				newLower = self.__snapCanvasXToSliderValue(e.x)
			else:
				# determine how much to move
				barDistance = self.__mouseMotionToBarDistance(self.__lastMouseX, e.x)
				newLower = self.__model.getLower() + barDistance

			self.__model.setLower(newLower)
			self.__lastMouseX = e.x
		
		# raise the caret to the top
		if (self.__model.getUpper() == self.__model.getLowerBound()):
			self.__view.tag_raise(self.__view.getRightCaretId())				
		else:
			self.__view.tag_raise(self.__view.getLeftCaretId())
		"""

	def rightCaret_onMouseMotion(self, e):
		pass
		"""
		log.debug(str(self.__view.canvasx(e.x)) + " : " + 
				  str(self.__view.canvasy(e.y)))
			
		# leave early if the mouse is not aligned with the caret anymore
		leftCaretX = self.__view.getLeftCaretX() + (self.__view.getCaretWidth())
		if (self.__view.canvasx(e.x) > (self.__view.getBarX() + self.__view.getBarWidth())):			
			self.__model.setUpper(self.__model.getUpperBound())
		# edge case, inside right caret
		elif (self.__view.canvasx(e.x) < leftCaretX):
			if (self.__model.getLower() <= self.__model.getUpperBound()):
				self.__model.setUpper(self.__model.getLower())

			self.__lastMouseX = e.x
		else:
			if (self.__snapToTicks):
				newUpper = self.__snapCanvasXToSliderValue(e.x)
			else:
				# determine how much to move
				barDistance = self.__mouseMotionToBarDistance(self.__lastMouseX, e.x)
				newUpper = self.__model.getUpper() + barDistance

			self.__model.setUpper(newUpper)
			self.__lastMouseX = e.x
			
		# raise the caret to the top
		if (self.__model.getLower() >= self.__model.getUpperBound()):
			self.__view.tag_raise(self.__view.getLeftCaretId())				
		else:
			self.__view.tag_raise(self.__view.getRightCaretId())
		"""		

	'''
	Event - Major Tick onClick
	- Snaps the approriate caret to the position represented by the tick
	- Note: the tick canvas x is converted to bar x
	'''
	def majorTick_onClick(self, e):
		pass
		"""
		w = CURRENT
		tickCoords = self.__view.coords(w)
		tickWidth = tickCoords[2] - tickCoords[0]
		barX = self.__canvasXToBarX(tickCoords[0] + tickWidth / 2.0)
		
		
		
		if (barX < self.__model.getLower()):
			self.__model.setLower(barX)
		elif (barX > self.__model.getUpper()):
			self.__model.setUpper(barX)
		"""

	'''
	Event - Slider onClick
	- save the slider position
	'''
	def slider_onMouseClick(self, e):
		self.__lastMouseX = e.x
		

	'''
	Event - Slider onMouseMotion
	- allows user to slide the slider by clicking the range inbetween
	'''
	def slider_onMouseMotion(self, e):
		pass
		"""
		log.debug(str(self.__view.canvasx(e.x)) + " : " + 
				  str(self.__view.canvasy(e.y)))
		
		# leave early if the mouse is not aligned with the slider anymore
		if (self.__view.canvasx(e.x) < self.__view.getBarX()):
			return		
		elif (self.__view.canvasx(e.x) > self.__view.getBarX() + self.__view.getBarWidth()):			
			return	
		
		# determine how much to move
		barDistance = 0
		lowerAdjust = 0
		upperAdjust = 0
		if (self.__snapToTicks):	
			step = self.__mouseMotionToBarDistance(self.__view.canvasx(self.__lastMouseX), self.__view.canvasx(e.x)) / 2.0			
			tmp = self.__view.getMinorTickSpacing() / 3.0
			if (abs(step) >= tmp):				
				lowerstep = (self.__model.getLower()+step) 
				upperstep = (self.__model.getUpper()+step)
				bRoundUp = False
				if (step >= 0):
					bRoundUp = True
				
				lowerAdjust = self.barRoundValue(lowerstep, self.__view.getMinorTickSpacing(), bRoundUp)
				lowerAdjust -= self.__model.getLower()
				upperAdjust = self.barRoundValue(upperstep, self.__view.getMinorTickSpacing(), bRoundUp)
				upperAdjust -= self.__model.getUpper()	
					
				# bounds check
				if (lowerAdjust+self.__model.getLower() < self.__model.getLowerBound()):
					upperAdjust = 0
				if (upperAdjust+self.__model.getUpper() > self.__model.getUpperBound()):
					lowerAdjust = 0					
					
				if (upperAdjust != 0 or lowerAdjust != 0):
					self.__lastMouseX = e.x					
		else:
			barDistance = self.__mouseMotionToBarDistance(self.__view.canvasx(self.__lastMouseX), self.__view.canvasx(e.x))
			
			# detect bounds collision
			if self.__model.getLower()+barDistance <= self.__model.getLowerBound():
				barDistance = self.__model.getLowerBound() - self.__model.getLower()
			elif (self.__model.getUpper()+barDistance >=  self.__model.getUpperBound()):
				barDistance = self.__model.getUpperBound() - self.__model.getUpper()
										
			lowerAdjust = barDistance
			upperAdjust = barDistance
		
			if (barDistance != 0.0):
					self.__lastMouseX = e.x			

		# adjust slider
		self.__model.setLower(self.__model.getLower() + lowerAdjust)
		self.__model.setUpper(self.__model.getUpper() + upperAdjust)
		"""


	'''
	Update Logic
	- allows for a full update of all positions
	- left exposed for manual calling
	'''
	def update(self, e):
		log.debug("Performing RePositioning...")
								 
		# position left caret
		lower = self.__model.getLower()
		if (lower > self.__model.getUpper()):
			lower = self.__model.getUpper()
		if (self.__view.getLeftCaretId() > 0):	
			self.__positionCaret(self.__view.getLeftCaretId(), 
								 lower)

		# position right caret
		if (self.__view.getRightCaretId() > 0):
			self.__positionCaret(self.__view.getRightCaretId(), 
								 self.__model.getUpper())
			
		# position slider
		if (self.__view.getSliderId() > 0):
			self.__updateSlider()


	'''
	PositionCaret helper function
	- performs the simple task of positioning a caret at a point on the bar
	- sliderValue is intended to be in bar coords
	'''
	def __positionCaret(self, caretId, sliderValue):
		caretCoords = self.__view.coords(caretId)
		barY = self.__view.getBarY()
		barYCenter = barY + (self.__view.getBarHeight() / 2.0)
		caretY = self.__view.getCaretHeight() / 2.0
		caretHalfWidth = self.__view.getCaretWidth() / 2.0

		canvasX = self.__barXToCanvasX(sliderValue)
		if (canvasX > self.__view.getBarX() + self.__view.getBarWidth()):
			canvasX = self.__view.getBarX() + self.__view.getBarWidth()
		canvasX = canvasX - caretHalfWidth
		canvasY = barYCenter - caretCoords[1] - caretY
		log.debug("Moving caret to: (slider=%f) %d,%d", 
				  sliderValue,
				  canvasX, canvasY)
				  
		if (self.__model.getUpperBound() < self.__model.getLowerBound()):
			self.__view.itemconfig(caretId, state="hidden")
		else:
			self.__view.itemconfig(caretId, state="normal")
			
		if (canvasX < self.__view.getBarX()-caretHalfWidth):
			self.__view.itemconfig(caretId, state="hidden")
		else:
			self.__view.itemconfig(caretId, state="normal")		
				  
		self.__view.move(caretId,
						 canvasX - caretCoords[0],
						 canvasY)


	'''
	updateSlider helper function
	- positions the slider at its correct point
	- we convert the distance on the bar into canvas coords
	'''
	def __updateSlider(self):
		sliderId = self.__view.getSliderId()		
		sliderCoords = self.__view.coords(self.__view.getSliderId())
		sliderX = self.__view.getLeftCaretX() + (self.__view.getCaretWidth() / 2.0)
		sliderY =  self.__view.getBarY()
		sliderHeight = sliderCoords[3] - sliderCoords[1]
		sliderWidth = 0
		if (self.__model.getRange() > 0):
			sliderWidth = self.__barRangeToCanvasDistance(self.__model.getRange())
			
		if (self.__model.getBoundsRange() < 0):			
			sliderX = 0
			sliderWidth = 0
			sliderHeight = 0
			sliderY = 0
		else:
			if (sliderWidth <= 0):
				sliderWidth = 0
			elif (sliderWidth + sliderX > self.__view.getRightCaretX() + (self.__view.getCaretWidth() / 2.0)):
				sliderWidth = (self.__view.getRightCaretX() + (self.__view.getCaretWidth() / 2.0)) - sliderX
			
		# bounds check
		self.__view.coords(sliderId, 
						   sliderX, sliderY, 
						   sliderX + sliderWidth, sliderY + sliderHeight)

	
	'''
	Helper - BarPointX To CanvasPointX
	- converts a value from the model into a point on the bar
	- then converts that bar point to an x value on the canvas
	'''
	def __barXToCanvasX(self, point):
		barLength = self.__view.getBarWidth()

		canvasX = 0

		# prevent trying to draw carets at invalid range
		# this is user problem
		if (self.__model.getBoundsRange() > 0):
			unitPoint = barLength / (self.__model.getBoundsRange())
			translatedBarPoint = (point - self.__model.getLowerBound())
			canvasX = self.__view.getBarX() + (unitPoint * translatedBarPoint)

		return canvasX


	'''
	Helper - BarRange to CanvasDistance
	- this will convert the range on our slider bar to a distance
	- in canvas coords.
	- Note: if the bar length is 0 or the range is 0 this returns 0
	'''
	def __barRangeToCanvasDistance(self, range):
		barLength = self.__view.getBarWidth()
		if (self.__model.getBoundsRange() > 0):
			return barLength * (float(range) / self.__model.getBoundsRange())
		else:
			return 0

	
	'''
	Helper - CanvasX to BarX
	- Converts an X coordinate in canvas coords to bar coords
	'''
	def __canvasXToBarX(self, canvasX):
		barLength = float(self.__view.getBarWidth())
		unitStep = float(self.__model.getBoundsRange()) / barLength

		# check bounds
		return self.__model.getLowerBound() + (unitStep *
											   (canvasX - self.__view.getBarX()))


	'''
	Helper - MouseMotionToBarDistance
	- calculate the distance the mouse has moved in canvas coords
	- converts it to bar distance
	'''
	def __mouseMotionToBarDistance(self, lastX, newX):
		barLastMouseX = self.__canvasXToBarX(lastX)
		barNewMouseX = self.__canvasXToBarX(newX)

		return barNewMouseX - barLastMouseX	


	'''
	Helper - Snap CanvasX Slider Value
	'''
	def __snapCanvasXToSliderValue(self, canvasX):
		# find nearest tick to mouse pos
		barPointX = self.__canvasXToBarX(canvasX)
		clickPointRounded = round(barPointX / self.__view.getMinorTickSpacing())
		snapX = clickPointRounded * self.__view.getMinorTickSpacing()

		return snapX

		
	
		


'''
The model (M in MVC)
'''	
class RangeSliderModel():
	'''
	Fields
	'''
	__callbacks = []

	__lower = 0
	__lowerBound = 0
	__upper = 0
	__upperBound = 0
	

	''' 
	Constructor
	'''
	def __init__(self, init_color = "black"):
		self.__stroke_color = init_color

	'''
	Callback subsystem
	'''
	def subscribe(self, callback):
		self.__callbacks.append(callback)


	'''
	Notify all subscribers of a change
	'''	
	def __notify(self, **state):
		for call in self.__callbacks:
			call(state)


	'''
	Accessor/Mutator
	'''
	def getLower(self):
		return self.__lower


	def setLower(self, l):
		if (l < self.__lowerBound):
			l = self.__lowerBound

		self.__lower = l
		self.__notify()


	def getUpper(self):
		return self.__upper


	def setUpper(self, u):
		if (u > self.__upperBound):			
			u = self.__upperBound
		elif (u < self.__lower):
			u = self.__lower
			
		self.__upper = u
		self.__notify()


	def getLowerBound(self):
		return self.__lowerBound


	def setLowerBound(self, lb):
		self.__lowerBound = lb
		self.__notify()


	def getUpperBound(self):
		return self.__upperBound


	def setUpperBound(self, ub):
		self.__upperBound = ub
		self.__notify()


	def getRange(self):
		return self.__upper - self.__lower


	def getBoundsRange(self):
		return self.__upperBound - self.__lowerBound
'''
END MEGAWIDGETS
'''