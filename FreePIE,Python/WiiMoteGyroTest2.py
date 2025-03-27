"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Wiimote & Nunchuck Gyro Aiming Script by Germansani

Inspired mainly by WestleyTwain's Mouse Script (concerning that also thanks to MeteorFalling2, TQwando's Gyro Aiming Left 4 Dead 2 Script).
Also hugely inspired by JibbSmart's / Electronicks' JoyShockMapper (from which I've copied and translated the Smoothing-Part).

Thanks to K_CFG for helping to optimize the code and making it more understandable.

As in WestleyTwain's Script this here is also an amalgamation of often copied code that
I just wouldn't have been able to do on my own (like the corrective Angles for holding the Wiimote not perfectly straight that has been done by lednerg in WestleyTwain's Script)
and self-written code that either is written by myself or is inspired by the named Scripts.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""



"""

			!!!!!!	IMPORTANT	IMPORTANT	IMPORTANT	IMPORTANT	!!!!!!
			!!!!!!	IMPORTANT	IMPORTANT	IMPORTANT	IMPORTANT	!!!!!!
			!!!!!!	IMPORTANT	IMPORTANT	IMPORTANT	IMPORTANT	!!!!!!
			!!!!!!	IMPORTANT	IMPORTANT	IMPORTANT	IMPORTANT	!!!!!!
			!!!!!!	IMPORTANT	IMPORTANT	IMPORTANT	IMPORTANT	!!!!!!
			!!!!!!	IMPORTANT	IMPORTANT	IMPORTANT	IMPORTANT	!!!!!!

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Starting Instructions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When you start the Script, make sure that you leave the Wiimote on a flat surface (buttons facing up) and are holding the Nunchuck vertically (like you'll hold it when playing) for about 5 seconds so that the Calibration
will work correctly.
You know that everything is working when NCRollDeg will show a fluctuating number between 0 and 1 and ~-90 when the Nunchuck is tilted to the left and ~90 when the Nunchuck is tilted to the right and NumOffsetSamples is at 300.

If during gameplay you realise that there's a drift or the tilting / shaking of the Nunchuck doesn't work right anymore press the 1 and 2 Buttons on your Wiimote at the same time, but make sure that your
Wiimote is again on a flat surface and your Nunchuck is hold vertically for about 5 seconds.






~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Button Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The available buttons are as follows:
1. Wiimote + Nunchuck (13 buttons including the DPad)
2. Wiimote Shake (1 button) or Wiimote Tilt (2 buttons)
3. Nunchuck Shake (1 button) or Nunchuck Tilt (2 buttons)
4. Nunchuck-Stick (4-directional (4 buttons) or 8-directional (8 buttons))
5. Outer- and Inner-Ring of the Stick (2 buttons)

Every button can have up to 4 keys mapped to it (except for the Motion-Buttons and Stick-Buttons, here only 2 keys are mappable via the AlternateButton):
1. Normal Tap of a Button
2. Holding a Button
3. Normal Tap of a Button but with an alternate mapping
4. Holding a Button but with an alternate mapping

This script theoretically allows up to 78 keys to be mapped to the Wiimote.
However you'll have to subtract some of them in practice because e.g. the Mouse-Buttons might just be used for themselves (-12 possible keys)

"""

import thread, time, ctypes




"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
									General Options (Thanks to CyberVillain and HarvesteR for their helpful explications in the "Overclock FreePIE!"-Thread)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
#Changing these Values is always at your own risk.
#This normally also only is necessary if you use a Nunchuck together with the Wiimote that's used for controlling the Mouse-Cursor

#This setting let's you decide how fast the script should be processed by the system in milliseconds (ms).
#Lower settings will reduce stuttering and make the GyroMouse much smoother and precise, however this naturally will demand more ressources from your computer / your CPU.
#Standard Value is 2 which is equivalent to 500hz.
#Without the Nunchuck the GyroMouse works much, much better (as it doesn't have to switch between MotionPlus and the Extension continously) and you mostly won't need to set this lower than 2.
global ThreadInterval
ThreadInterval = 2


#If you encounter problems while gaming you can try to change the TimingType.
#ThreadYield = Uses all resources from one core but yields those resources if another program needs them (can lead to problems with games that have a lot of threads)
#ThreadYieldMicroSeconds = Same as ThreadYield but time is measured in microseconds (µs). Don't forget to adapt the ThreadInterval accordingly!
#HighresSystemTimer = Changes the whole system clock as long as the script is running (may lead to problems if a game relies heavily on the normal 64hz clock)
#SystemTimer = Default Timer but can't go lower than 16ms (64hz) which is too low for this script, so I just mention it here.
global TimingType
TimingType = TimingTypes.HighresSystemTimer


#For how long do you need to hold the 1 + 2 keys for a recalibration of the Wiimote and the Nunchuck (important for GyroMouse and Nunchuck-Tilting)
global SecondsBeforeCalibration
SecondsBeforeCalibration = 2


#Activate Checking for Double Assignment of Keys
#This is merely meant to prevent having mapped accidentaly a key twice in either the Normal Mapping or the Mapping when the AlternateButton is pressed.
#The script was tested and showed no bugs if the same key is mapped to different buttons but if you still encounter problems when pressing keys this will most likely solve it (please tell me about the problem so that I can fix it).
global ActivateDoubleCheck
ActivateDoubleCheck = False




"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
																			Wiimote & Nunchuck Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

"""
--------------------------------------------------------------------
General Mouse Settings
--------------------------------------------------------------------
"""

#The higher the number, the faster the speed of the mouse
global MouseSpeed
MouseSpeed = 8


#Same as above but this concerns the speed of the mouse when using the Nunchuck-Stick
global MouseSpeedStick
MouseSpeedStick = 0.1




"""
--------------------------------------------------------------------
Wiimote / MotionPlus Settings
--------------------------------------------------------------------
"""

#By setting this to true you can use the Wiimote's Gyro as a mouse.
#That's the easiest but also most resource-demanding moving mode as the thread Interval needs to be much lower.
global UseGyroMouse
UseGyroMouse = True


#If you want to use the Wiimote horizontally set this to True.
#Only important if you use the GyroMouse.
global WMHorizontal
WMHorizontal = False


#If you're using a Wiimote without the "-TR" in the devicename under "Bluetooth Devices" change TRMoteX to -1 and TRMoteY to 1
#If you're not sure just test which combination works for you
global TRMoteX
TRMoteX = -1
global TRMoteY
TRMoteY = 1


#This modifies the Speed of the cursor by a certain Value ("SpeedBoost") when you move the Wiimote faster than a minimum Speed so that you can e.g. turn around faster in an FPS.
#To prevent too wide movements I've added a maximum Speed as well, so that you won't flip around too much if you move the Wiimote very fast.
#It's best to not choose these values too high but that's up to you.
#If you don't want to use that option simply set SpeedBoost to 1.
global SpeedBoost
SpeedBoost = 3
global SpeedBoostMinimum
SpeedBoostMinimum = 300
global SpeedBoostMaximum
SpeedBoostMaximum = 600


#Use this Option if you want to enable Smoothing for the Gyro-Mouse.
#Enabled this option reduces the shakiness of it however you should set the values for it below quite low to prevent lack of responsiveness.
#Smoothing is best applied to small movements if at all.
global UseSmoothing
UseSmoothing = True


#These values determine at which speed smoothing will have an remarkable effect
#Standard is 2.5 and 5 (its best to have the StartSmoothing-Value at half of the StopSmoothing-Value)
global StartSmoothing, StopSmoothing
StartSmoothing = 2.5
StopSmoothing = 5


#This is used for re-positioning the Wiimote when it feels to far off from the screen.
#When pressing this Button any further input from the Gyro of the Wiimote will be ignored until you release it.
#You can use either NunchuckButtons or WiimoteButtons.
global GyroOff
GyroOff = WiimoteButtons.Home


#This allows to toggle the GyroOff-Button
global GyroOffToggle
GyroOffToggle = True


#By setting "RememberSpeed" to True the Cursor will be applied the last speed of the Gyroscope before pressing the "GyroOff"-Button (will never be applied when using "GyroOffToggle")
#You can also choose from which axes the speed should be remembered.
#When it's set to False the cursor will remain at the same position until you release the "GyroOff"-Button.
#The remembered speed will decrease over time. The seconds until the next decreasing step are indicated by the "SlowingSpeed"-Setting.
#The "SlowFactor" says how much the current speed will be divided by at every step (e.g. with "2" it's 2 --> 1 --> 0.5 --> 0.25 --> ....)
global RememberSpeed
RememberSpeed = False
global RememberXSpeed
RememberXSpeed = True
global RememberYSpeed
RememberYSpeed = True
global SlowingSpeed
SlowingSpeed = 1
global SlowFactor
SlowFactor = 10


#Maps the Wiimote Left / Right tilting to keys.
#If you don't use this, the Shake-Mapping will be used.
global UseWMTiltingForKeys
UseWMTiltingForKeys = False


#Use this option if you'd like to tilt the Wiimote Left / Right for a quick rotation like with a Snap-Stick.
#If you've accidentaly enabled this for both Wiimote and Nunchuck you'll get an error so you can disable one of the methods.
global UseWMTiltingForSnapStick
UseWMTiltingForSnapStick = False


#Use this option if you'd like to tilt the Wiimote Left / Right for a continous rotation that stops when you get in the neutral position again.
#If you've accidentaly enabled this for both Wiimote and Nunchuck you'll get an error so you can disable one of the methods.
global UseWMTiltingForContinousRotation
UseWMTiltingForContinousRotation = False


#How much you have to shake the Wiimote to simulate a Button Press
#If you experience unwanted double presses changing the value can help.
global ShakeIntensityWM
ShakeIntensityWM = 18




"""
--------------------------------------------------------------------
Nunchuck Settings
--------------------------------------------------------------------
"""
#Set this to True if you want to use a Nunchuck that's connected to the Wiimote which is used for the GyroMouse
#ONLY USE EITHER THIS, THE NEXT OPTION OR NONE OF THEM
global UseNunchuck
UseNunchuck = False


#Set this to True if you want to use a Nunchuck that's connected to a second Wiimote
#This makes the GyroMouse much smoother and responsive as switching between MotionPlus and the Nunchuck for the same Wiimote isn't necessary for FreePIE anymore.
global UseNunchuckSecondWiimote
UseNunchuckSecondWiimote = False


#Set this to True if you want to use the Nunchuck-Stick as Mouse (you can use this also together with the GyroMouse)
#If not used as mouse the key-mappings will be used.
#Naturally you will need to have the Nunchuck enabled for this.
global UseStickMouse
UseStickMouse = True


#Set this to True if you want to toggle between using / not-using the Stick as a Mouse.
#If this is set to False you will need to keep the GyroOff-Button pressed to use the stick as a mouse.
global StickMouseToggling
StickMouseToggling = False


#This setting determines how fast the Stick will react (that's to say how far you have to move the stick to have an effect).
#Important for Key-Mappings, the StickMouse and the StickRing.
#Standard is 25
global StickSens
StickSens = 25


#Use this setting if you want to use 8 instead of 4 directions / key mappings for the Nunchuck-Stick.
#Merely meant for having more buttons available if you don't use the stick for moving around as the transition between directions is much more narrow and would prevent a smooth transition.
global UseStickEightDirections
UseStickEightDirections = False


#This simulates the press of a button when you push the Nunchuck-stick over the Outer-Limit (Outer-Ring).
#Or in between the Inner-Limit and Outer-Limit-Values (Inner-Ring).
global UseStickRing
UseStickRing = False


#This sets the limit above which the Inner Stick-Ring-Button should be pressed
#Standard is 50
global StickRingThresholdInner
StickRingThresholdInner = 50


#This sets the limit above which the Outer Stick-Ring-Button should be pressed and the Inner Stick won't be pressed anymore
#Standard is 85
global StickRingThresholdOuter
StickRingThresholdOuter = 85


#Maps the Nunchuck Left / Right tilting to Keys.
global UseNCTiltingForKeys
UseNCTiltingForKeys = False


#Use this option if you'd like to tilt the Nunchuck Left / Right for a quick rotation like with a Snap-Stick.
#If you've accidentaly enabled this for both Wiimote and Nunchuck you'll get an error so you can disable one of the methods.
global UseNCTiltingForSnapStick
UseNCTiltingForSnapStick = False


#Use this option if you'd like to tilt the Nunchuck Left / Right for a continous rotation that stops when you get in the neutral position again.
#If you've accidentaly enabled this for both Wiimote and Nunchuck you'll get an error so you can disable one of the methods.
global UseNCTiltingForContinousRotation
UseNCTiltingForContinousRotation = True


#How much you have to shake the Nunchuck to simulate a Button Press
#If you experience unwanted double presses changing the value can help.
global ShakeIntensityNC
ShakeIntensityNC = 8





"""
--------------------------------------------------------------------
Snap Stick / Continous Rotation Settings
--------------------------------------------------------------------
"""
#Set to True if you want to Toggle if the Mouse can be moved in this mode or not by pressing the GyroOffButton
global ToggleContinousRotation
ToggleContinousRotation = True


#This determines how fast you will turn when you use continous rotation
global ContinousRotationSpeed
ContinousRotationSpeed = 4


#If you want to calculate the AdjustSnapDeg-Value for the Snap-Stick set the following Option to True.
global CalibrateAdjustSnapDeg
CalibrateAdjustSnapDeg = True

#For the Calculation:
#First set the "AdjustSnapDeg"-Value to a number you like so that you won't take forever ingame to complete a turn or won't overturn instantly (that needs experimentation).
#Also make sure to set the same Value for your Ingame-Mouse-Sensitivity for the "InGameSens"-Setting.
#Last for the preparation press at least once on the "GyroOff"-Button to set the Counter for the Turns to 0.

#Secondly look at a specific point with your Camera (e.g. in an FPS) or move the mouse to the left border of the screen (e.g. in a strategy Game or on the Desktop)
#Then tilt the Wiimote / Nunchuck TO THE RIGHT multiple times until you reach the same point (at least approximately) again (when controlling a camera) or the right border of the screen.
#Stop the Script and look in the "Watch"-Tab what value you should put for the AdjustSnapDeg-Setting.
#If you accidentaly moved the mouse in between just press the GyroOff-Button once and start from the beginning.
#Naturally you can also just do an e.g. 90° turn but then you have to multiply the result with 4 by yourself.

#The result is an unique value for each game which is independent from the mouse-sensitivity.
#If you change the sensitivity In-Game you only have to adjust the "InGameSens"-Setting here to the same sensitivity value.

#Set to True this setting will take into account your systems mouse sensitivity which some games use additionaly to their ingame mouse sensitivity settings and cancels it out so you'll still turn around correctly.
#Other games however don't use it and you should put False here for them.
#Unfortunately you have to find out yourself if you have to put "True" or "False" here.
#For Use on Desktop set this to False.
global CounterOSMouseSensitivity
CounterOSMouseSensitivity = False


#Set this to True if you want to turn around instantly instead of seeing the mouse moving in the position.
#Keep in mind that you can't do anything else while turning if you have this disabled as I'm using a while-Loop for this option.
#To make up for that you can always adapt the TurnSpeed with the next setting so that a turn will only last as long as you want it to.
global InstantTurn
InstantTurn = False


#How fast you will turn if you have InstantTurn disabled.
#This setting is in miliseconds, however it doesn't indicate the absolute time a turn will need.
#What it does is taking this time for every full digit from this calculation: (SnapRotationStep * AdjustSnapDeg)/SystemMouseSensivitiy/InGameSens
#So for some games it might be faster with 1.0 as they have a lower result than for others with 0.5 with a higher result in that calculation.
#
#TL:DR:
#Just try out what works best for you.
global TurnSpeed
TurnSpeed = 0.5


#Set this setting to your In-Game Mouse Sensitivity
#For Use on Desktop set this to 1.
global InGameSens
InGameSens = 1.0


#The amount of how much degree a Tilt will move the mouse
global SnapRotationStep
SnapRotationStep = 90.0


#It says to how much a move in the real world will move the camera / the cursor ingame.
#After having calculated it you can naturally still change this setting to get a more precise result as the calculation isn't precise to the degree as it always uses the amount of degrees indicated by the "SnapRotationStep"-Value.
global AdjustSnapDeg
AdjustSnapDeg = 4.25


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
																				Button Mapping Mouse & Scroll Wheel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
#You can put the IgnoreKey here as well if you don't want to use a mouse button
LeftMouse = WiimoteButtons.B
RightMouse = WiimoteButtons.A
MiddleMouse = WiimoteButtons.DPadDown

#The Mouse Wheel is used the following way:
#ONLY WIIMOTE ----> Tilting the Wiimote left / right and pressing the MiddleMouse-Button.
#NUNCHUCK AND WIIMOTE ----> Tilting the Nunchuck up / down and pressing the MiddleMouse-Button.
#
#In a neutral position the MiddleMouse itself will be pressed.
#If this is set to False the MiddleMouse will always be pressed, no matter how you tilt the Nunchuck / Wiimote.
global UseScrollWheel
UseScrollWheel = True

#Setting this Option to True gives you the possibility to use the Alternate-Key-Mappings for the Mouse Buttons as long as you press the Alternate-Button.
#This way you can also use the Alternate Wiimote-Tilt Mappings if you just use the Wiimote as the Scroll Wheel is also disabled as long as you press the Alternate-Button.
global UseAlternateMappingForMouse
UseAlternateMappingForMouse = False




"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
																					Alternate & Hold Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
#Set this to True to use AlternateMapping
global UseAlternateMapping
UseAlternateMapping = True

#Set up a Button that you'd like to use for Alternate Mapping
#It's recommended that, if you use AlternateMapping, you shouldn't map any keys to it. It's possible however.
global AlternateButton
AlternateButton = NunchuckButtons.C

#Set this to True to use 2 additional keys for the same button
#One will be just a click, the other one will be pressed when you keep the button pressed
#"HoldingTime" defines how many seconds are in between the decision of the script if a button is clicked or pressed
#E.g. when setting it to 0.25 you have to press the button for 0.25 seconds for the Hold-Mapping and if you release it earlier you'll have a click
global UseHoldMapping
UseHoldMapping = True
global HoldingTime
HoldingTime = 0.25

#Hold-Mapping can also be used for just certain keys by setting the unwanted Hold-Keys to the IgnoreKey
#(e.g. putting WMPlusHold = IgnoreKey will always immediately press the key you have set for WMPlus)





"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
																						Keyboard Keys Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
#Put in a key you won't use ingame and use that one for every Button you don't want to use
#(e.g. WMA = IgnoreKey when you don't want to use the A-Button for a Keyboard Key or NCShakeVertical = IgnoreKey if you have enabled but don't want to use the Shaking)
global IgnoreKey
IgnoreKey = Key.NumberPad0

#Description:
#No suffix = Key when pressing the Button normally
#Suffix "Hold" = Pressed key when holding the Button
#Suffix "Alt" = Pressed key when holding the AlternateButton
#Suffix "HoldAlt" = Pressed key when holding the button while pressing the AlternateButton

#--------------------------
#Wiimote Button Mapping
#--------------------------
WMOne = IgnoreKey
WMOneHold = IgnoreKey
WMOneAlt = IgnoreKey
WMOneHoldAlt = IgnoreKey

WMTwo = IgnoreKey
WMTwoHold = IgnoreKey
WMTwoAlt = IgnoreKey
WMTwoHoldAlt = IgnoreKey

WMPlus = IgnoreKey
WMPlusHold = IgnoreKey
WMPlusAlt = IgnoreKey
WMPlusHoldAlt = IgnoreKey

WMMinus = IgnoreKey
WMMinusHold = IgnoreKey
WMMinusAlt = IgnoreKey
WMMinusHoldAlt = IgnoreKey

WMHome = IgnoreKey
WMHomeHold = IgnoreKey
WMHomeAlt = IgnoreKey
WMHomeHoldAlt = IgnoreKey

WMA = IgnoreKey
WMAHold = IgnoreKey
WMAAlt = IgnoreKey
WMAHoldAlt = IgnoreKey

WMB = IgnoreKey
WMBHold = IgnoreKey
WMBAlt = IgnoreKey
WMBHoldAlt = IgnoreKey

DPadDown = IgnoreKey
DPadDownHold = IgnoreKey
DPadDownAlt = IgnoreKey
DPadDownHoldAlt = IgnoreKey

DPadUp = IgnoreKey
DPadUpHold = IgnoreKey
DPadUpAlt = IgnoreKey
DPadUpHoldAlt = IgnoreKey

DPadLeft = IgnoreKey
DPadLeftHold = IgnoreKey
DPadLeftAlt = IgnoreKey
DPadLeftHoldAlt = IgnoreKey

DPadRight = IgnoreKey
DPadRightHold = IgnoreKey
DPadRightAlt = IgnoreKey
DPadRightHoldAlt = IgnoreKey


#------------------------
#Nunchuck Button Mapping
#------------------------
NCC = IgnoreKey
NCCHold = IgnoreKey
NCCAlt = IgnoreKey
NCCHoldAlt = IgnoreKey

NCZ = IgnoreKey
NCZHold = IgnoreKey
NCZAlt = IgnoreKey
NCZHoldAlt = IgnoreKey


#-----------------------
#Nunchuck Stick Mapping
#The directions are like on a compass (e.g. N = North = Up, NE = North-East = Upper Right, E = East = Right,...)
#Only N, E, S, W are used for the 4-direction mapping
#-----------------------
NCStickN = Key.W
NCStickNAlt = Key.W

NCStickNE = IgnoreKey
NCStickNEAlt = IgnoreKey

NCStickE = Key.D
NCStickEAlt = Key.D

NCStickSE = IgnoreKey
NCStickSEAlt = IgnoreKey

NCStickS = Key.S
NCStickSAlt = Key.S

NCStickSW = IgnoreKey
NCStickSWAlt = IgnoreKey

NCStickW = Key.A
NCStickWAlt = Key.A

NCStickNW = IgnoreKey
NCStickNWAlt = IgnoreKey

NCStickInnerRing = IgnoreKey
NCStickInnerRingAlt = IgnoreKey

NCStickOuterRing = IgnoreKey
NCStickOuterRingAlt = IgnoreKey



#---------------------------------
#Nunchuck / Wiimote Shake Mapping
#---------------------------------
WMShakeVertical = IgnoreKey
WMShakeVerticalAlt = IgnoreKey

NCShakeVertical = IgnoreKey
NCShakeVerticalAlt = IgnoreKey



#---------------------------------
#Nunchuck Tilt Mapping
#---------------------------------
#Don't shake the Nunchuck too much otherwise you might get the wrong inputs (double presses, the other key will be pressed,..)

#For getting correct results make sure to hold your Nunchuck vertically for at least 5 seconds when launching the script. Otherwise it just won't work correctly!
#You can check in the "Watch"-Tab if everything's alright, if "NCRollDeg" shows numbers between -1 and 1 when holding the Nunchuck vertically.
#This is important because in that time the Accelerometer will determine it's orientation.
#If it feels a bit off during gameplay you can recalibrate together with the Wiimote by holding 1 + 2 for certain seconds.
#(The Seconds are customizable with the setting "SecondsBeforeCalibration" further up)

NCTiltLeft = IgnoreKey
NCTiltLeftAlt = IgnoreKey

NCTiltRight = IgnoreKey
NCTiltRightAlt = IgnoreKey


#---------------------------------
#Wiimote Tilt Mapping
#---------------------------------

WMTiltLeft = IgnoreKey
WMTiltLeftAlt = IgnoreKey

WMTiltRight = IgnoreKey
WMTiltRightAlt = IgnoreKey




"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
#~~~General Gyro-Mouse Function~~~#
def motionplus_update():
	global yawSpeed, pitchSpeed
	
	diagnostics.watch(NumOffsetSamples)
	
	if not WMHorizontal:
		yawSpeed = (wiimote[0].motionplus.yaw_down) - calibratedyaw 
		pitchSpeed = (wiimote[0].motionplus.pitch_left) - calibratedpitch
		
		GyroTightenedInput(-0.5, 0.5, -0.5, 0.5)
		
	elif WMHorizontal:
		yawSpeed = wiimote[0].motionplus.pitch_left - calibratedpitch
		pitchSpeed = wiimote[0].motionplus.roll_left - calibratedyaw
		
		GyroTightenedInput(-1.5, 1.5, -20, 20)
	
	CheckSmoothing()
	
	CheckCurrentWiimoteOrientation()
	
	CheckGyroOffSettings()
    
    
		
		
		
#~~~Sets the tiered limit for minimum Gyro Input~~~#		
def GyroTightenedInput(YawMin, YawMax, PitchMin, PitchMax):
	global yawSpeed, pitchSpeed
		
	if yawSpeed > YawMin and yawSpeed < YawMax:
		YawFraction = (yawSpeed / Fraction)/100
		if yawSpeed < 0:
			yawSpeed = yawSpeed * -YawFraction
		else:
			yawSpeed = yawSpeed * YawFraction
	elif abs(yawSpeed) >= SpeedBoostMinimum and abs(yawSpeed) <= SpeedBoostMaximum:
		yawSpeed = yawSpeed * SpeedBoost
		
	if pitchSpeed > PitchMin and pitchSpeed < PitchMax:
		if WMHorizontal:
			PitchFraction = (pitchSpeed / RFraction)/100
		else:
			PitchFraction = (pitchSpeed / Fraction)/100
			
		if pitchSpeed < 0:
			pitchSpeed = pitchSpeed * -PitchFraction
		else:
			pitchSpeed = pitchSpeed * PitchFraction
	elif abs(pitchSpeed) >= SpeedBoostMinimum and abs(pitchSpeed) <= SpeedBoostMaximum:
		pitchSpeed = pitchSpeed * SpeedBoost
		
		
		
#~~~Checks the current Wiimote Orientation so that all directions in the real world correspond to the same directions on the Computer~~~#		
def CheckCurrentWiimoteOrientation():
	global rollDeg, yawDeg, pitchDeg
	global SpeedX, SpeedY
	
	if not WMHorizontal:
	   	rollDeg = roll*180
	   	yawDeg = yaw*180
	   	pitchDeg = pitch*180
	
		if rollDeg < 0 and rollDeg >= -90:
			XYswap = 1 - filters.ensureMapRange(rollDeg, -90,0, 0, 1)
			RightDown = -1
			TopUp     =  1
		elif rollDeg <= 90 and rollDeg >= 0:
			XYswap = 1 - filters.ensureMapRange(rollDeg, 90,0, 0, 1)
			RightDown =  1
			TopUp     =  1
		elif rollDeg > 90 and rollDeg <= 180:
			XYswap = 1 - filters.ensureMapRange(rollDeg, 90,180, 0, 1)
			RightDown =  1
			TopUp     = -1
		elif rollDeg < -90 and rollDeg >= -180:
			XYswap = 1 - filters.ensureMapRange(rollDeg, -90,-180, 0, 1)
			RightDown = -1
			TopUp     = -1
	
		SpeedX = TopUp *   yawSpeed - ( TopUp *   yawSpeed * XYswap ) + (  RightDown * pitchSpeed * XYswap )
		SpeedY = TopUp * pitchSpeed - ( TopUp * pitchSpeed * XYswap ) + ( -RightDown *   yawSpeed * XYswap )
		
	elif WMHorizontal:
	   	rollDeg = roll*180
	   	yawDeg = yaw*180
	   	pitchDeg = pitch*180
	   	
		SpeedX = yawSpeed
		SpeedY = pitchSpeed
		
#~~~Acceleration Update~~~#
def accel_update():
	global pitch, roll, yaw, NCroll, NCpitch
	
	accl = [wiimote[0].acceleration.x, wiimote[0].acceleration.y, wiimote[0].acceleration.z]
	pitch = pryAngle(accl, 1, 2)		#Pitch uses Y and Z
	roll  = pryAngle(accl, 0, 2)		#Roll  uses X and Z
	yaw   = pryAngle(accl, 1, 0)		#Yaw   uses Y and X
	
	if UseNunchuck:	
		accl = [wiimote[0].nunchuck.acceleration.x, wiimote[0].nunchuck.acceleration.y, wiimote[0].nunchuck.acceleration.z]
		NCroll = pryAngle(accl, 0 ,2)
		NCpitch = pryAngle(accl, 1, 2)
		
	if UseNunchuckSecondWiimote:	
		accl = [wiimote[1].nunchuck.acceleration.x, wiimote[1].nunchuck.acceleration.y, wiimote[1].nunchuck.acceleration.z]
		NCroll = pryAngle(accl, 0 ,2)
		NCpitch = pryAngle(accl, 1, 2)
		
#~~~Reliable Pitch/Roll/Yaw~~~#
def pryAngle(v, a, b):					#range from [0, 2) or (-1, 1] for 1 full rotation
	mag = math.sqrt(v[a]**2 + v[b]**2)
	
	if mag != 0:
		result = math.acos(v[b]/mag) * (1/(math.pi))
		if v[a] >= 0:
			return  result
		else:
			return -result
			
	else:
		return 0
		
		
		
		
		
#~~~Checks the settings for the GyroOff-Button~~~#	    
def CheckGyroOffSettings():
	global SlowTime, SlowCount
	global CheckGyro, ToggleGyroOn		
	global OldSpeedX, OldSpeedY

	if GyroOffToggle and GyroOffButton:
		if CheckGyro == 0:
			ToggleGyroOn = not ToggleGyroOn
			CheckGyro = 1
	
	if not GyroOffButton and CheckGyro == 1:
		CheckGyro = 0
					
	if not GyroOffButton and not GyroOffToggle:
		mouse.deltaX = TRMoteX*filters.mapRange(SpeedX, 0,100, 0,MouseSpeed)
		mouse.deltaY = TRMoteY*filters.mapRange(SpeedY, 0,100, 0,MouseSpeed)
		OldSpeedX = TRMoteX*filters.mapRange(SpeedX, 0,100, 0,MouseSpeed)
		OldSpeedY = TRMoteY*filters.mapRange(SpeedY, 0,100, 0,MouseSpeed)
		SlowTime = time.time()
		SlowCount = 1
		
	elif GyroOffButton and RememberSpeed:
		if SlowTime + (SlowingSpeed*SlowCount) >= time.time() and RememberXSpeed:
			mouse.deltaX = OldSpeedX
		elif RememberXSpeed:
			SlowCount += 1
			OldSpeedX = OldSpeedX/SlowFactor
			OldSpeedY = OldSpeedY/SlowFactor
			
		if SlowTime + (SlowingSpeed*SlowCount) >= time.time() and RememberYSpeed:
			mouse.deltaY = OldSpeedY
		elif RememberYSpeed:
			SlowCount += 1
			OldSpeedX = OldSpeedX/SlowFactor
			OldSpeedY = OldSpeedY/SlowFactor
		
	elif ToggleGyroOn:
		mouse.deltaX = TRMoteX*filters.mapRange(SpeedX, 0,100, 0,MouseSpeed)
		mouse.deltaY = TRMoteY*filters.mapRange(SpeedY, 0,100, 0,MouseSpeed)
		OldSpeedX = TRMoteX*filters.mapRange(SpeedX, 0,100, 0,MouseSpeed)
		OldSpeedY = TRMoteY*filters.mapRange(SpeedY, 0,100, 0,MouseSpeed)
		SlowTime = time.time()
		SlowCount = 1
	
	
	
	
#~~~Checks the Smoothing settings~~~#	
def CheckSmoothing():
	global yawSpeed, pitchSpeed
	
	if UseSmoothing:
	    YawInput = abs(yawSpeed)
	    PitchInput = abs(pitchSpeed)
	 
	    DirectWeightYaw = (YawInput - StartSmoothing) / (StopSmoothing - StartSmoothing)
	    DirectWeightYaw = clamp(DirectWeightYaw, 0, 1)
	    
	    DirectWeightPitch = (PitchInput - StartSmoothing) / (StopSmoothing - StartSmoothing)
	    DirectWeightPitch = clamp(DirectWeightPitch, 0, 1)
	 
	    yawSpeed = GetDirectInput(yawSpeed * DirectWeightYaw) + GetSmoothedInputYaw(yawSpeed * (1.0 - DirectWeightYaw))
	    pitchSpeed = GetDirectInput(pitchSpeed * DirectWeightPitch) + GetSmoothedInputPitch(pitchSpeed * (1.0 - DirectWeightPitch))
	    
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
   
def GetDirectInput(input):
	return input
	
def GetSmoothedInputYaw(input):
	global inputBuffer, currentInputIndex, average

	currentInputIndex = (currentInputIndex + 1) % 16
	
	inputBuffer[currentInputIndex] = input
	
 	for i in [16]:
 		average = average + inputBuffer[i]
 		
 	average = average / 16
 	
 	return average
	
def GetSmoothedInputPitch(input):
	global inputBuffer, currentInputIndex, averagepitch

	currentInputIndex = (currentInputIndex + 1) % 16
	
	inputBuffer[currentInputIndex] = input
	
 	for i in [16]:
 		averagepitch = averagepitch + inputBuffer[i]
 		
 	averagepitch = averagepitch / 16
 	
 	return averagepitch
 	
 	
 	
 	
#~~~Maps the Wiimote Buttons to Keys~~~#	
def press_button(WButton,BMapping,Click):
	if BMapping == IgnoreKey:
		return
	if wiimote[0].buttons.button_down(WButton):
		keyboard.setKeyDown(BMapping)
	elif Click == True:
		keyboard.setKeyDown(BMapping)
	else:
		keyboard.setKeyUp(BMapping)
		
		
		
		
#~~~Maps the Nunchuck Buttons to Keys~~~#		
def press_button_NC(WButton,BMapping,Click):
	if BMapping == IgnoreKey:
		return
	if wiimote[NunchuckNumber].nunchuck.buttons.button_down(WButton):
		keyboard.setKeyDown(BMapping)
	elif Click == True:
		keyboard.setKeyDown(BMapping)
	else:
		keyboard.setKeyUp(BMapping)
		


		
		
#~~~General Wiimote Settings (Tilt / Shake / Button-Mapping) but also sets Wiimote or Nunchuck Buttons for the Mouse~~~#
def update_buttons():
	global HoldButtonDPadRight, DPadRightPressed, ClickDPadRight
	global HoldButtonDPadLeft, DPadLeftPressed, ClickDPadLeft
	global HoldButtonDPadUp, DPadUpPressed, ClickDPadUp
	global HoldButtonDPadDown, DPadDownPressed, ClickDPadDown
	global HoldButtonA, APressed, ClickA
	global HoldButtonB, BPressed, ClickB
	global HoldButtonMinus, MinusPressed, ClickMinus
	global HoldButtonHome, HomePressed, ClickHome
	global HoldButtonPlus, PlusPressed, ClickPlus
	global HoldButtonOne, OnePressed, ClickOne
	global HoldButtonTwo, TwoPressed, ClickTwo
	
	global HoldButtonDPadRightAlt, DPadRightPressedAlt, ClickDPadRightAlt
	global HoldButtonDPadLeftAlt, DPadLeftPressedAlt, ClickDPadLeftAlt
	global HoldButtonDPadUpAlt, DPadUpPressedAlt, ClickDPadUpAlt
	global HoldButtonDPadDownAlt, DPadDownPressedAlt, ClickDPadDownAlt
	global HoldButtonAAlt, APressedAlt, ClickAAlt
	global HoldButtonBAlt, BPressedAlt, ClickBAlt
	global HoldButtonMinusAlt, MinusPressedAlt, ClickMinusAlt
	global HoldButtonHomeAlt, HomePressedAlt, ClickHomeAlt
	global HoldButtonPlusAlt, PlusPressedAlt, ClickPlusAlt
	global HoldButtonOneAlt, OnePressedAlt, ClickOneAlt
	global HoldButtonTwoAlt, TwoPressedAlt, ClickTwoAlt
	
	global rollDeg, yawDeg, pitchDeg
	
	diagnostics.watch(wiimote[0].status.batteryPercentage)
	diagnostics.watch(wiimote[1].status.batteryPercentage)
		
	if not UseGyroMouse:
		accel_update()
	   	rollDeg = roll*180
	   	yawDeg = yaw*180
	   	pitchDeg = pitch*180
	   	
	MouseMapping()

	CheckWiimoteTiltingSettings()
			

	if UseHoldMapping and not AlternateMappingKey:
	
	#---------------------DPadRight---------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and DPadRightHold != IgnoreKey:
			if not DPadRightPressed:
				HoldButtonDPadRight = time.time()
				DPadRightPressed = True
			if HoldButtonDPadRight + HoldingTime <= time.time():
				press_button(WiimoteButtons.DPadRight,DPadRightHold,False)
				ClickDPadRight = False
			else:
				ClickDPadRight = True
				
		elif wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and DPadRightHold == IgnoreKey:
			DPadRightPressed = True
			press_button(WiimoteButtons.DPadRight,DPadRight,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and ClickDPadRight:
			press_button(WiimoteButtons.DPadRight,DPadRight,True)
			ClickDPadRight = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and DPadRightPressed:
			DPadRightPressed = False
			press_button(WiimoteButtons.DPadRight,DPadRightHold,False)
			press_button(WiimoteButtons.DPadRight,DPadRight,False)
			
	#---------------------DPadLeft--------------------------------
			
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and DPadLeftHold != IgnoreKey:
			if not DPadLeftPressed:
				HoldButtonDPadLeft = time.time()
				DPadLeftPressed = True
			if HoldButtonDPadLeft + HoldingTime <= time.time():
				press_button(WiimoteButtons.DPadLeft,DPadLeftHold,False)
				ClickDPadLeft = False
			else:
				ClickDPadLeft = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and DPadLeftHold == IgnoreKey:
			DPadLeftPressed = True
			press_button(WiimoteButtons.DPadLeft,DPadLeft,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and ClickDPadLeft:
			press_button(WiimoteButtons.DPadLeft,DPadLeft,True)
			ClickDPadLeft = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and DPadLeftPressed:
			DPadLeftPressed = False
			press_button(WiimoteButtons.DPadLeft,DPadLeftHold,False)
			press_button(WiimoteButtons.DPadLeft,DPadLeft,False)
			
	#---------------------DPadUp--------------------------------
			
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and DPadUpHold != IgnoreKey:
			if not DPadUpPressed:
				HoldButtonDPadUp = time.time()
				DPadUpPressed = True
			if HoldButtonDPadUp + HoldingTime <= time.time():
				press_button(WiimoteButtons.DPadUp,DPadUpHold,False)
				ClickDPadUp = False
			else:
				ClickDPadUp = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and DPadUpHold == IgnoreKey:
			DPadUpPressed = True
			press_button(WiimoteButtons.DPadUp,DPadUp,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and ClickDPadUp:
			press_button(WiimoteButtons.DPadUp,DPadUp,True)
			ClickDPadUp = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and DPadUpPressed:
			DPadUpPressed = False
			press_button(WiimoteButtons.DPadUp,DPadUpHold,False)
			press_button(WiimoteButtons.DPadUp,DPadUp,False)
			
	#---------------------DPadDown--------------------------------
			
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and DPadDownHold != IgnoreKey:
			if not DPadDownPressed:
				HoldButtonDPadDown = time.time()
				DPadDownPressed = True
			if HoldButtonDPadDown + HoldingTime <= time.time():
				press_button(WiimoteButtons.DPadDown,DPadDownHold,False)
				ClickDPadDown = False
			else:
				ClickDPadDown = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and DPadDownHold == IgnoreKey:
			DPadDownPressed = True
			press_button(WiimoteButtons.DPadDown,DPadDown,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and ClickDPadDown:
			press_button(WiimoteButtons.DPadDown,DPadDown,True)
			ClickDPadDown = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and DPadDownPressed:
			DPadDownPressed = False
			press_button(WiimoteButtons.DPadDown,DPadDownHold,False)
			press_button(WiimoteButtons.DPadDown,DPadDown,False)
			
	#---------------------A-Button--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.A) and WMAHold != IgnoreKey:
			if not APressed:
				HoldButtonA = time.time()
				APressed = True
			if HoldButtonA + HoldingTime <= time.time():
				press_button(WiimoteButtons.A,WMAHold,False)
				ClickA = False
			else:
				ClickA = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.A) and WMAHold == IgnoreKey:
			APressed = True
			press_button(WiimoteButtons.A,WMA,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.A) and ClickA:
			press_button(WiimoteButtons.A,WMA,True)
			ClickA = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.A) and APressed:
			APressed = False
			press_button(WiimoteButtons.A,WMAHold,False)
			press_button(WiimoteButtons.A,WMA,False)
			
	#---------------------B-Button--------------------------------
					
		if wiimote[0].buttons.button_down(WiimoteButtons.B) and WMBHold != IgnoreKey:
			if not BPressed:
				HoldButtonB = time.time()
				BPressed = True
			if HoldButtonB + HoldingTime <= time.time():
				press_button(WiimoteButtons.B,WMBHold,False)
				ClickB = False
			else:
				ClickB = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.B) and WMBHold == IgnoreKey:
			BPressed = True
			press_button(WiimoteButtons.B,WMB,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.B) and ClickB:
			press_button(WiimoteButtons.B,WMB,True)
			ClickB = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.B) and BPressed:
			BPressed = False
			press_button(WiimoteButtons.B,WMBHold,False)
			press_button(WiimoteButtons.B,WMB,False)
			
	#---------------------Minus-Button--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Minus) and WMMinusHold != IgnoreKey:
			if not MinusPressed:
				HoldButtonMinus = time.time()
				MinusPressed = True
			if HoldButtonMinus + HoldingTime <= time.time():
				press_button(WiimoteButtons.Minus,WMMinusHold,False)
				ClickMinus = False
			else:
				ClickMinus = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.Minus) and WMMinusHold == IgnoreKey:
			MinusPressed = True
			press_button(WiimoteButtons.Minus,WMMinus,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Minus) and ClickMinus:
			press_button(WiimoteButtons.Minus,WMMinus,True)
			ClickMinus = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Minus) and MinusPressed:
			MinusPressed = False
			press_button(WiimoteButtons.Minus,WMMinusHold,False)
			press_button(WiimoteButtons.Minus,WMMinus,False)
			
	#---------------------Home-Button--------------------------------
			
		if wiimote[0].buttons.button_down(WiimoteButtons.Home) and WMHomeHold != IgnoreKey:
			if not HomePressed:
				HoldButtonHome = time.time()
				HomePressed = True
			if HoldButtonHome + HoldingTime <= time.time():
				press_button(WiimoteButtons.Home,WMHomeHold,False)
				ClickHome = False
			else:
				ClickHome = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.Home) and WMHomeHold == IgnoreKey:
			HomePressed = True
			press_button(WiimoteButtons.Home,WMHome,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Home) and ClickHome:
			press_button(WiimoteButtons.Home,WMHome,True)
			ClickHome = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Home) and HomePressed:
			HomePressed = False
			press_button(WiimoteButtons.Home,WMHomeHold,False)
			press_button(WiimoteButtons.Home,WMHome,False)
			
	#---------------------Plus-Button--------------------------------
			
		if wiimote[0].buttons.button_down(WiimoteButtons.Plus) and WMPlusHold != IgnoreKey:
			if not PlusPressed:
				HoldButtonPlus = time.time()
				PlusPressed = True
			if HoldButtonPlus + HoldingTime <= time.time():
				press_button(WiimoteButtons.Plus,WMPlusHold,False)
				ClickPlus = False
			else:
				ClickPlus = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.Plus) and WMPlusHold == IgnoreKey:
			PlusPressed = True
			press_button(WiimoteButtons.Plus,WMPlus,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Plus) and ClickPlus:
			press_button(WiimoteButtons.Plus,WMPlus,True)
			ClickPlus = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Plus) and PlusPressed:
			PlusPressed = False
			press_button(WiimoteButtons.Plus,WMPlusHold,False)
			press_button(WiimoteButtons.Plus,WMPlus,False)
			
	#---------------------One-Button--------------------------------
			
		if wiimote[0].buttons.button_down(WiimoteButtons.One) and WMOneHold != IgnoreKey:
			if not OnePressed:
				HoldButtonOne = time.time()
				OnePressed = True
			if HoldButtonOne + HoldingTime <= time.time():
				press_button(WiimoteButtons.One,WMOneHold,False)
				ClickOne = False
			else:
				ClickOne = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.One) and WMOneHold == IgnoreKey:
			OnePressed = True
			press_button(WiimoteButtons.One,WMOne,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.One) and ClickOne:
			press_button(WiimoteButtons.One,WMOne,True)
			ClickOne = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.One) and OnePressed:
			OnePressed = False
			press_button(WiimoteButtons.One,WMOneHold,False)
			press_button(WiimoteButtons.One,WMOne,False)
			
	#---------------------Two-Button--------------------------------
			
		if wiimote[0].buttons.button_down(WiimoteButtons.Two) and WMTwoHold != IgnoreKey:
			if not TwoPressed:
				HoldButtonTwo = time.time()
				TwoPressed = True
			if HoldButtonTwo + HoldingTime <= time.time():
				press_button(WiimoteButtons.Two,WMTwoHold,False)
				ClickTwo = False
			else:
				ClickTwo = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.Two) and WMTwoHold == IgnoreKey:
			TwoPressed = True
			press_button(WiimoteButtons.Two,WMTwo,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Two) and ClickTwo:
			press_button(WiimoteButtons.Two,WMTwo,True)
			ClickTwo = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Two) and TwoPressed:
			TwoPressed = False
			press_button(WiimoteButtons.Two,WMTwoHold,False)
			press_button(WiimoteButtons.Two,WMTwo,False)
			
			
		
	elif UseHoldMapping and AlternateMappingKey:
			
			
	#---------------------DPadRightAlt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and DPadRightHoldAlt != IgnoreKey:
			if not DPadRightPressedAlt:
				HoldButtonDPadRightAlt = time.time()
				DPadRightPressedAlt = True
			if HoldButtonDPadRightAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.DPadRight,DPadRightHoldAlt,False)
				ClickDPadRightAlt = False
			else:
				ClickDPadRightAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and DPadRightHoldAlt == IgnoreKey:
			DPadRightPressedAlt = True
			press_button(WiimoteButtons.DPadRight,DPadRightAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and ClickDPadRightAlt:
			press_button(WiimoteButtons.DPadRight,DPadRightAlt,True)
			ClickDPadRightAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and DPadRightPressedAlt:
			DPadRightPressedAlt = False
			press_button(WiimoteButtons.DPadRight,DPadRightHoldAlt,False)
			press_button(WiimoteButtons.DPadRight,DPadRightAlt,False)
			
			
	#---------------------DPadLeftAlt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and DPadLeftHoldAlt != IgnoreKey:
			if not DPadLeftPressedAlt:
				HoldButtonDPadLeftAlt = time.time()
				DPadLeftPressedAlt = True
			if HoldButtonDPadLeftAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.DPadLeft,DPadLeftHoldAlt,False)
				ClickDPadLeftAlt = False
			else:
				ClickDPadLeftAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and DPadLeftHoldAlt == IgnoreKey:
			DPadLeftPressedAlt = True
			press_button(WiimoteButtons.DPadLeft,DPadLeftAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and ClickDPadLeftAlt:
			press_button(WiimoteButtons.DPadLeft,DPadLeftAlt,True)
			ClickDPadLeftAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and DPadLeftPressedAlt:
			DPadLeftPressedAlt = False
			press_button(WiimoteButtons.DPadLeft,DPadLeftHoldAlt,False)
			press_button(WiimoteButtons.DPadLeft,DPadLeftAlt,False)
			
			
	#---------------------DPadUpAlt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and DPadUpHoldAlt != IgnoreKey:
			if not DPadUpPressedAlt:
				HoldButtonDPadUpAlt = time.time()
				DPadUpPressedAlt = True
			if HoldButtonDPadUpAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.DPadUp,DPadUpHoldAlt,False)
				ClickDPadUpAlt = False
			else:
				ClickDPadUpAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and DPadUpHoldAlt == IgnoreKey:
			DPadUpPressedAlt = True
			press_button(WiimoteButtons.DPadUp,DPadUpAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and ClickDPadUpAlt:
			press_button(WiimoteButtons.DPadUp,DPadUpAlt,True)
			ClickDPadUpAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and DPadUpPressedAlt:
			DPadUpPressedAlt = False
			press_button(WiimoteButtons.DPadUp,DPadUpHoldAlt,False)
			press_button(WiimoteButtons.DPadUp,DPadUpAlt,False)
			
					
	#---------------------DPadDownAlt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and DPadDownHoldAlt != IgnoreKey:
			if not DPadDownPressedAlt:
				HoldButtonDPadDownAlt = time.time()
				DPadDownPressedAlt = True
			if HoldButtonDPadDownAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.DPadDown,DPadDownHoldAlt,False)
				ClickDPadDownAlt = False
			else:
				ClickDPadDownAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and DPadDownHoldAlt == IgnoreKey:
			DPadDownPressedAlt = True
			press_button(WiimoteButtons.DPadDown,DPadDownAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and ClickDPadDownAlt:
			press_button(WiimoteButtons.DPadDown,DPadDownAlt,True)
			ClickDPadDownAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and DPadDownPressedAlt:
			DPadDownPressedAlt = False
			press_button(WiimoteButtons.DPadDown,DPadDownHoldAlt,False)
			press_button(WiimoteButtons.DPadDown,DPadDownAlt,False)
	
					
	#---------------------A-Button-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.A) and WMAHoldAlt != IgnoreKey:
			if not APressedAlt:
				HoldButtonAAlt = time.time()
				APressedAlt = True
			if HoldButtonAAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.A,WMAHoldAlt,False)
				ClickAAlt = False
			else:
				ClickAAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.A) and WMAHoldAlt == IgnoreKey:
			APressedAlt = True
			press_button(WiimoteButtons.A,WMAAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.A) and ClickAAlt:
			press_button(WiimoteButtons.A,WMAAlt,True)
			ClickAAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.A) and APressedAlt:
			APressedAlt = False
			press_button(WiimoteButtons.A,WMAHoldAlt,False)
			press_button(WiimoteButtons.A,WMAAlt,False)
					
					
	#---------------------B-Button-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.B) and WMBHoldAlt != IgnoreKey:
			if not BPressedAlt:
				HoldButtonBAlt = time.time()
				BPressedAlt = True
			if HoldButtonBAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.B,WMBHoldAlt,False)
				ClickBAlt = False
			else:
				ClickBAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.B) and WMBHoldAlt == IgnoreKey:
			BPressedAlt = True
			press_button(WiimoteButtons.B,WMBAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.B) and ClickBAlt:
			press_button(WiimoteButtons.B,WMBAlt,True)
			ClickBAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.B) and BPressedAlt:
			BPressedAlt = False
			press_button(WiimoteButtons.B,WMBHoldAlt,False)
			press_button(WiimoteButtons.B,WMBAlt,False)
	
							
	#---------------------Minus-Button-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Minus) and WMMinusHoldAlt != IgnoreKey:
			if not MinusPressedAlt:
				HoldButtonMinusAlt = time.time()
				MinusPressedAlt = True
			if HoldButtonMinusAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.Minus,WMMinusHoldAlt,False)
				ClickMinusAlt = False
			else:
				ClickMinusAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.Minus) and WMMinusHoldAlt == IgnoreKey:
			MinusPressedAlt = True
			press_button(WiimoteButtons.Minus,WMMinusAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Minus) and ClickMinusAlt:
			press_button(WiimoteButtons.Minus,WMMinusAlt,True)
			ClickMinusAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Minus) and MinusPressedAlt:
			MinusPressedAlt = False
			press_button(WiimoteButtons.Minus,WMMinusHoldAlt,False)
			press_button(WiimoteButtons.Minus,WMMinusAlt,False)
			
							
	#---------------------Home-Button-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Home) and WMHomeHoldAlt != IgnoreKey:
			if not HomePressedAlt:
				HoldButtonHomeAlt = time.time()
				HomePressedAlt = True
			if HoldButtonHomeAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.Home,WMHomeHoldAlt,False)
				ClickHomeAlt = False
			else:
				ClickHomeAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.Home) and WMHomeHoldAlt == IgnoreKey:
			HomePressedAlt = True
			press_button(WiimoteButtons.Home,WMHomeAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Home) and ClickHomeAlt:
			press_button(WiimoteButtons.Home,WMHomeAlt,True)
			ClickHomeAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Home) and HomePressedAlt:
			HomePressedAlt = False
			press_button(WiimoteButtons.Home,WMHomeHoldAlt,False)
			press_button(WiimoteButtons.Home,WMHomeAlt,False)
			
							
	#---------------------Plus-Button-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Plus) and WMPlusHoldAlt != IgnoreKey:
			if not PlusPressedAlt:
				HoldButtonPlusAlt = time.time()
				PlusPressedAlt = True
			if HoldButtonPlusAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.Plus,WMPlusHoldAlt,False)
				ClickPlusAlt = False
			else:
				ClickPlusAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.Plus) and WMPlusHoldAlt == IgnoreKey:
			PlusPressedAlt = True
			press_button(WiimoteButtons.Plus,WMPlusAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Plus) and ClickPlusAlt:
			press_button(WiimoteButtons.Plus,WMPlusAlt,True)
			ClickPlusAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Plus) and PlusPressedAlt:
			PlusPressedAlt = False
			press_button(WiimoteButtons.Plus,WMPlusHoldAlt,False)
			press_button(WiimoteButtons.Plus,WMPlusAlt,False)
			
							
	#---------------------One-Button-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.One) and WMOneHoldAlt != IgnoreKey:
			if not OnePressedAlt:
				HoldButtonOneAlt = time.time()
				OnePressedAlt = True
			if HoldButtonOneAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.One,WMOneHoldAlt,False)
				ClickOneAlt = False
			else:
				ClickOneAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.One) and WMOneHoldAlt == IgnoreKey:
			OnePressedAlt = True
			press_button(WiimoteButtons.One,WMOneAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.One) and ClickOneAlt:
			press_button(WiimoteButtons.One,WMOneAlt,True)
			ClickOneAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.One) and OnePressedAlt:
			OnePressedAlt = False
			press_button(WiimoteButtons.One,WMOneHoldAlt,False)
			press_button(WiimoteButtons.One,WMOneAlt,False)
			
							
	#---------------------Two-Button-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Two) and WMTwoHoldAlt != IgnoreKey:
			if not TwoPressedAlt:
				HoldButtonTwoAlt = time.time()
				TwoPressedAlt = True
			if HoldButtonTwoAlt + HoldingTime <= time.time():
				press_button(WiimoteButtons.Two,WMTwoHoldAlt,False)
				ClickTwoAlt = False
			else:
				ClickTwoAlt = True
			
		elif wiimote[0].buttons.button_down(WiimoteButtons.Two) and WMTwoHoldAlt == IgnoreKey:
			TwoPressedAlt = True
			press_button(WiimoteButtons.Two,WMTwoAlt,False)
				
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Two) and ClickTwoAlt:
			press_button(WiimoteButtons.Two,WMTwoAlt,True)
			ClickTwoAlt = False
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Two) and TwoPressedAlt:
			TwoPressedAlt = False
			press_button(WiimoteButtons.Two,WMTwoHoldAlt,False)
			press_button(WiimoteButtons.Two,WMTwoAlt,False)
			
	elif AlternateMappingKey:
	
	#---------------------DPadRight-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadRight):
			DPadRightPressedAlt = True		
			press_button(WiimoteButtons.DPadRight,DPadRightAlt,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and DPadRightPressedAlt:
			DPadRightPressedAlt = False	
			press_button(WiimoteButtons.DPadRight,DPadRightAlt,False)
			
		
	#---------------------DPadLeft-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft):
			DPadLeftPressedAlt = True
			press_button(WiimoteButtons.DPadLeft,DPadLeftAlt,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and DPadLeftPressedAlt:
			DPadLeftPressedAlt = False
			press_button(WiimoteButtons.DPadLeft,DPadLeftAlt,False)
			
		
	#---------------------DPadUp-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadUp):
			DPadUpPressedAlt = True
			press_button(WiimoteButtons.DPadUp,DPadUpAlt,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and DPadUpPressedAlt:
			DPadUpPressedAlt = False
			press_button(WiimoteButtons.DPadUp,DPadUpAlt,False)
			
		
		
	#---------------------DPadDown-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadDown):
			DPadDownPressedAlt = True
			press_button(WiimoteButtons.DPadDown,DPadDownAlt,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and DPadDownPressedAlt:
			DPadDownPressedAlt = False
			press_button(WiimoteButtons.DPadDown,DPadDownAlt,False)
	
	
		
	#---------------------Button A-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.A):
			APressedAlt = True
			press_button(WiimoteButtons.A,WMAAlt,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.A) and APressedAlt:
			APressedAlt = False
			press_button(WiimoteButtons.A,WMAAlt,False)
			
		
	#---------------------Button B-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.B):
			BPressedAlt = True
			press_button(WiimoteButtons.B,WMBAlt,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.B) and BPressedAlt:
			BPressedAlt = False
			press_button(WiimoteButtons.B,WMBAlt,False)
	
		
	#---------------------Button Minus-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Minus):
			MinusPressedAlt = True
			press_button(WiimoteButtons.Minus,WMMinusAlt,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Minus) and MinusPressedAlt:
			MinusPressedAlt = False
			press_button(WiimoteButtons.Minus,WMMinusAlt,False)
			
		
	#---------------------Button Home-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Home):
			HomePressedAlt = True
			press_button(WiimoteButtons.Home,WMHomeAlt,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Home) and HomePressedAlt:
			HomePressedAlt = False
			press_button(WiimoteButtons.Home,WMHomeAlt,False)
			
		
	#---------------------Button Plus-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Plus):
			PlusPressedAlt = True
			press_button(WiimoteButtons.Plus,WMPlusAlt,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Plus) and PlusPressedAlt:
			PlusPressedAlt = False
			press_button(WiimoteButtons.Plus,WMPlusAlt,False)
	
		
	#---------------------Button One-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.One):
			OnePressedAlt = True
			press_button(WiimoteButtons.One,WMOneAlt,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.One) and OnePressedAlt:
			OnePressedAlt = False
			press_button(WiimoteButtons.One,WMOneAlt,False)
		
	#---------------------Button Two-Alt--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Two):
			TwoPressedAlt = True
			press_button(WiimoteButtons.Two,WMTwoAlt,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Two) and TwoPressedAlt:
			TwoPressedAlt = False
			press_button(WiimoteButtons.Two,WMTwoAlt,False)
			
			
			
		
	else:
	
	
	
	#---------------------DPadRight--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadRight):
			DPadRightPressed = True		
			press_button(WiimoteButtons.DPadRight,DPadRight,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadRight) and DPadRightPressed:
			DPadRightPressed = False	
			press_button(WiimoteButtons.DPadRight,DPadRight,False)
			
		
	#---------------------DPadLeft--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft):
			DPadLeftPressed = True
			press_button(WiimoteButtons.DPadLeft,DPadLeft,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadLeft) and DPadLeftPressed:
			DPadLeftPressed = False
			press_button(WiimoteButtons.DPadLeft,DPadLeft,False)
			
		
	#---------------------DPadUp--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadUp):
			DPadUpPressed = True
			press_button(WiimoteButtons.DPadUp,DPadUp,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadUp) and DPadUpPressed:
			DPadUpPressed = False
			press_button(WiimoteButtons.DPadUp,DPadUp,False)
		
		
	#---------------------DPadDown--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.DPadDown):
			DPadDownPressed = True
			press_button(WiimoteButtons.DPadDown,DPadDown,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.DPadDown) and DPadDownPressed:
			DPadDownPressed = False
			press_button(WiimoteButtons.DPadDown,DPadDown,False)
	
	
		
	#---------------------Button A--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.A):
			APressed = True
			press_button(WiimoteButtons.A,WMA,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.A) and APressed:
			APressed = False
			press_button(WiimoteButtons.A,WMA,False)
			
		
	#---------------------Button B--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.B):
			BPressed = True
			press_button(WiimoteButtons.B,WMB,False)
			
		elif not wiimote[0].buttons.button_down(WiimoteButtons.B) and BPressed:
			BPressed = False
			press_button(WiimoteButtons.B,WMB,False)
	
		
	#---------------------Button Minus--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Minus):
			MinusPressed = True
			press_button(WiimoteButtons.Minus,WMMinus,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Minus) and MinusPressed:
			MinusPressed = False
			press_button(WiimoteButtons.Minus,WMMinus,False)
			
		
	#---------------------Button Home--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Home):
			HomePressed = True
			press_button(WiimoteButtons.Home,WMHome,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Home) and HomePressed:
			HomePressed = False
			press_button(WiimoteButtons.Home,WMHome,False)
			
		
	#---------------------Button Plus--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Plus):
			PlusPressed = True
			press_button(WiimoteButtons.Plus,WMPlus,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Plus) and PlusPressed:
			PlusPressed = False
			press_button(WiimoteButtons.Plus,WMPlus,False)
	
		
	#---------------------Button One--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.One):
			OnePressed = True
			press_button(WiimoteButtons.One,WMOne,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.One) and OnePressed:
			OnePressed = False
			press_button(WiimoteButtons.One,WMOne,False)
		
	#---------------------Button Two--------------------------------
	
		if wiimote[0].buttons.button_down(WiimoteButtons.Two):
			TwoPressed = True
			press_button(WiimoteButtons.Two,WMTwo,False)
	
		elif not wiimote[0].buttons.button_down(WiimoteButtons.Two) and TwoPressed:
			TwoPressed = False
			press_button(WiimoteButtons.Two,WMTwo,False)
			
			
			
#~~~Maps Nunchuck / Wiimote Buttons to Keys~~~#
def MouseMapping():	
	global rollDeg, yawDeg, pitchDeg
	global WD, WU, MM	
	
	if LeftMouse != IgnoreKey:
		if not UseAlternateMappingForMouse:
			if LeftMouse == NunchuckButtons.C or LeftMouse == NunchuckButtons.Z:
				mouse.leftButton = wiimote[NunchuckNumber].nunchuck.buttons.button_down(LeftMouse)
			else:
				mouse.leftButton = wiimote[0].buttons.button_down(LeftMouse)
				
		elif UseAlternateMappingForMouse and not AlternateMappingKey:
			if LeftMouse == NunchuckButtons.C or LeftMouse == NunchuckButtons.Z:
				mouse.leftButton = wiimote[NunchuckNumber].nunchuck.buttons.button_down(LeftMouse)
			else:
				mouse.leftButton = wiimote[0].buttons.button_down(LeftMouse)
		
	if RightMouse != IgnoreKey:
		if not UseAlternateMappingForMouse:
			if RightMouse == NunchuckButtons.C or RightMouse == NunchuckButtons.Z:
				mouse.rightButton = wiimote[NunchuckNumber].nunchuck.buttons.button_down(RightMouse)
			else:
				mouse.rightButton = wiimote[0].buttons.button_down(RightMouse)
				
		elif UseAlternateMappingForMouse and not AlternateMappingKey:
			if RightMouse == NunchuckButtons.C or RightMouse == NunchuckButtons.Z:
				mouse.rightButton = wiimote[NunchuckNumber].nunchuck.buttons.button_down(RightMouse)
			else:
				mouse.rightButton = wiimote[0].buttons.button_down(RightMouse)
	
	if MiddleMouse != IgnoreKey:
		Scrolling = rollDeg
		MWDegMin = 30
		MWDegMax = 90
		
		if UseNunchuck or UseNunchuckSecondWiimote:
			Scrolling = NCPitchDeg
			MWDegMin = 15
			MWDegMax = 60
			
		if not UseAlternateMappingForMouse:
			if MiddleMouse == NunchuckButtons.C or MiddleMouse == NunchuckButtons.Z:
				if wiimote[NunchuckNumber].nunchuck.buttons.button_down(MiddleMouse) and UseScrollWheel:
					if Scrolling > MWDegMin and Scrolling <= MWDegMax and not WU:
						mouse.wheelUp = True
						WU = True
					elif Scrolling < -MWDegMin and Scrolling >= -MWDegMax and not WD:
						mouse.wheelDown = True
						WD = True
					elif Scrolling >= -MWDegMin and Scrolling <= MWDegMin and not MM:
						mouse.middleButton = True
						MM = True
				elif wiimote[NunchuckNumber].nunchuck.buttons.button_down(MiddleMouse) and not UseScrollWheel:
					mouse.middleButton = True
				else:
					WU = False
					WD = False
					MM = False
					mouse.middleButton = False
			else:
				if wiimote[0].buttons.button_down(MiddleMouse) and UseScrollWheel:
					if Scrolling > MWDegMin and Scrolling <= MWDegMax and not WU:
						mouse.wheelUp = True
						WU = True
					elif Scrolling < -MWDegMin and Scrolling >= -MWDegMax and not WD:
						mouse.wheelDown = True
						WD = True
					elif Scrolling >= -MWDegMin and Scrolling <= MWDegMin and not MM:
						mouse.middleButton = True
						MM = True
				elif wiimote[0].buttons.button_down(MiddleMouse) and not UseScrollWheel:
					mouse.middleButton = True
				else:
					WU = False
					WD = False
					MM = False
					mouse.middleButton = False
				
		elif UseAlternateMappingForMouse and not AlternateMappingKey:
			if MiddleMouse == NunchuckButtons.C or MiddleMouse == NunchuckButtons.Z:
				if wiimote[NunchuckNumber].nunchuck.buttons.button_down(MiddleMouse) and UseScrollWheel:
					if Scrolling > MWDegMin and Scrolling <= MWDegMax and not WU:
						mouse.wheelUp = True
						WU = True
					elif Scrolling < -MWDegMin and Scrolling >= -MWDegMax and not WD:
						mouse.wheelDown = True
						WD = True
					elif Scrolling >= -MWDegMin and Scrolling <= MWDegMin and not MM:
						mouse.middleButton = True
						MM = True
				elif wiimote[NunchuckNumber].nunchuck.buttons.button_down(MiddleMouse) and not UseScrollWheel:
					mouse.middleButton = True
				else:
					WU = False
					WD = False
					MM = False
					mouse.middleButton = False
			else:
				if wiimote[0].buttons.button_down(MiddleMouse) and UseScrollWheel:
					if Scrolling > MWDegMin and Scrolling <= MWDegMax and not WU:
						mouse.wheelUp = True
						WU = True
					elif Scrolling < -MWDegMin and Scrolling >= -MWDegMax and not WD:
						mouse.wheelDown = True
						WD = True
					elif Scrolling >= -MWDegMin and Scrolling <= MWDegMin and not MM:
						mouse.middleButton = True
						MM = True
				elif wiimote[0].buttons.button_down(MiddleMouse) and not UseScrollWheel:
					mouse.middleButton = True
				else:
					WU = False
					WD = False
					MM = False
					mouse.middleButton = False
					
					

#~~~Checks the Settings for the Tilting of the Wiimote~~~#					
def CheckWiimoteTiltingSettings():
	global WMTiltedLeft, WMTiltedRight, WMTiltedLeftAlt, WMTiltedRightAlt
	global OldTime, OldAccel, NewAccel, Shake
	global rollDeg, yawDeg, pitchDeg

	#Maps Keys to the Tilting of the Wiimote
	if UseWMTiltingForKeys:
		if AlternateMappingKey:	
			if rollDeg < -TiltKeyRollMin and rollDeg > -TiltKeyRollMax and WMTiltLeftAlt != IgnoreKey:
				keyboard.setKeyDown(WMTiltLeftAlt)
				WMTiltedLeftAlt = True
			elif rollDeg > TiltKeyRollMin and rollDeg < TiltKeyRollMax and WMTiltRightAlt != IgnoreKey:
				keyboard.setKeyDown(WMTiltRightAlt)
				WMTiltedRightAlt = True
			elif abs(rollDeg) <= TiltKeyRollMin and abs(rollDeg) >= TiltKeyRollMin-10:
				WMTiltedLeftAlt = True
				WMTiltedRightAlt = True
			elif WMTiltedLeftAlt or WMTiltedRightAlt:
				keyboard.setKeyUp(WMTiltRight)
				keyboard.setKeyUp(WMTiltLeft)
				keyboard.setKeyUp(WMTiltRightAlt)
				keyboard.setKeyUp(WMTiltLeftAlt)
				WMTiltedLeftAlt = False
				WMTiltedRightAlt = False
		
		else:
			if rollDeg < -TiltKeyRollMin and rollDeg > -TiltKeyRollMax and WMTiltLeft != IgnoreKey:
				keyboard.setKeyDown(WMTiltLeft)
				WMTiltedLeft = True
			elif rollDeg > TiltKeyRollMin and rollDeg < TiltKeyRollMax and WMTiltRight != IgnoreKey:
				keyboard.setKeyDown(WMTiltRight)
				WMTiltedRight = True
			elif abs(rollDeg) <= TiltKeyRollMin and abs(rollDeg) >= TiltKeyRollMin-10:
				WMTiltedLeft = True
				WMTiltedRight = True
			elif WMTiltedLeft or WMTiltedRight:
				keyboard.setKeyUp(WMTiltRight)
				keyboard.setKeyUp(WMTiltLeft)
				keyboard.setKeyUp(WMTiltRightAlt)
				keyboard.setKeyUp(WMTiltLeftAlt)
				WMTiltedLeft = False
				WMTiltedRight = False
				
				
	#If Tilting isn't mapped to keys, the Shake Mapping can be used
	if not UseWMTiltingForKeys:
		OldAccel = wiimote[0].acceleration.y
	
		if OldAccel < 0:
			OldAccel = 0
			
		if OldTime + 0.2 <= time.time():
			NewAccel = wiimote[0].acceleration.y
			Shake = False
			if NewAccel < 0:
				NewAccel = 0
			OldTime = time.time()
			
		if (OldAccel - NewAccel) > ShakeIntensityWM and not Shake and WMShakeVertical != IgnoreKey:
			if AlternateMappingKey:
				keyboard.setPressed(WMShakeVerticalAlt)
			else:
				keyboard.setPressed(WMShakeVertical)
			Shake = True
			
			
	#Uses the Tilting to rotate left / right
	if UseWMTiltingForSnapStick:
		SnapStickTurn(rollDeg)
		
	if UseWMTiltingForContinousRotation:
		ContinousRotation(rollDeg)
		

def SnapStickTurn(rollDeg):
	global SnapedLeft, SnapedRight, SnapDeg, SnapAmount, SnapRotations

	if GyroOffButton:
		SnapAmount = 0.0
			
	if round(rollDeg) > 43 and round(rollDeg) < 120 and not SnapedRight:
		SnapedRight = True #Prevents uwanted multiple input with just one tilt
		SnapDeg = SnapRotationStep * AdjustSnapDeg
		SnapX = int(SnapDeg/mousesens/InGameSens)
		CurrentTurnDegRight = 0
		
		if not InstantTurn:
			while CurrentTurnDegRight <= SnapX: #Unfortunately prevents any other input while the loop is active / until the turn has been completed
				if filters.stopWatch(True,TurnSpeed):
					CurrentTurnDegRight = CurrentTurnDegRight + 1
					ctypes.windll.user32.mouse_event(0x0001, 1, 0, 0, 0)
					
		else:
			ctypes.windll.user32.mouse_event(0x0001, SnapX, 0, 0, 0)
			
	elif round(rollDeg) < -43 and round(rollDeg) > -120 and not SnapedLeft:
		SnapedLeft = True
		SnapDeg = SnapRotationStep * AdjustSnapDeg
		SnapX = int(SnapDeg/mousesens/InGameSens)
		CurrentTurnDegLeft = 0
		
		if not InstantTurn:
			while CurrentTurnDegLeft <= SnapX:
				if filters.stopWatch(True,TurnSpeed):
					CurrentTurnDegLeft = CurrentTurnDegLeft + 1
					ctypes.windll.user32.mouse_event(0x0001, -1, 0, 0, 0)
					
		else:
			ctypes.windll.user32.mouse_event(0x0001, -SnapX, 0, 0, 0)
			
	elif abs(rollDeg) > 30 and abs(rollDeg) < 180:
		i = 0
	elif SnapedRight or SnapedLeft:
		if CalibrateAdjustSnapDeg and SnapedRight:
			SnapRotations = 360 / SnapRotationStep
			SnapAmount = SnapAmount + 1
			diagnostics.watch("Use this value for your AdjustSnapDeg-Setting: %f" %(((SnapAmount/SnapRotations)*AdjustSnapDeg)))
		elif CalibrateAdjustSnapDeg and SnapedLeft:
			SnapAmount = SnapAmount - 1
		SnapedLeft = False
		SnapedRight = False
		mouse.deltaX = 0
		mouse.deltaY = 0


def ContinousRotation(rollDeg):
	global ToggleCR, TCCheck
	
	if ToggleContinousRotation and GyroOffButton:
		if TCCheck == 0:
			ToggleCR = not ToggleCR
			TCCheck = 1
			
	if not GyroOffButton and TCCheck == 1:
		TCCheck = 0

	if ToggleCR:
		if round(rollDeg) > 43 and round(rollDeg) < 120:
			ctypes.windll.user32.mouse_event(0x0001, ContinousRotationSpeed, 0, 0, 0)
				
		if round(rollDeg) < -43 and round(rollDeg) > -120:
			ctypes.windll.user32.mouse_event(0x0001, -ContinousRotationSpeed, 0, 0, 0)

	if not ToggleContinousRotation and not ToggleCR:
		if round(rollDeg) > 43 and round(rollDeg) < 120:
			ctypes.windll.user32.mouse_event(0x0001, ContinousRotationSpeed, 0, 0, 0)
				
		if round(rollDeg) < -43 and round(rollDeg) > -120:
			ctypes.windll.user32.mouse_event(0x0001, -ContinousRotationSpeed, 0, 0, 0)
			
			
#~~~Nunchuck~~~#	
def update_buttons_NC():	
	global HoldButtonC, CPressed, ClickC
	global HoldButtonZ, ZPressed, ClickZ
	
	global HoldButtonCAlt, CPressedAlt, ClickCAlt
	global HoldButtonZAlt, ZPressedAlt, ClickZAlt
	
	global NCPitchDeg
	
	NCPitchDeg = NCpitch * 180 #Will be calculated here because a Nunchuck needs to be connected anyway when one wants to scroll when both Wiimote and Nunchuck are used
	
	CheckNunchuckTiltingSettings()
	
	CheckNunchuckStickSettings()

	if UseHoldMapping and not AlternateMappingKey:
		
	#---------------------C-Button-----------------------
	
		if wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.C) and NCCHold != IgnoreKey:
			if not CPressed:
				HoldButtonC = time.time()
				CPressed = True
			if HoldButtonC + HoldingTime <= time.time():
				press_button_NC(NunchuckButtons.C,NCCHold,False)
				ClickC = False
			else:
				ClickC = True
			
		elif wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.C) and NCCHold == IgnoreKey:
			CPressed = True
			press_button_NC(NunchuckButtons.C,NCC,False)
				
		elif not wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.C) and ClickC:
			press_button_NC(NunchuckButtons.C,NCC,True)
			ClickC = False
			
		elif not wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.C) and CPressed:
			CPressed = False
			press_button_NC(NunchuckButtons.C,NCCHold,False)
			press_button_NC(NunchuckButtons.C,NCC,False)
			
				
	#---------------------Z-Button-----------------------
	
		if wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.Z) and NCZHold != IgnoreKey:
			if not ZPressed:
				HoldButtonZ = time.time()
				ZPressed = True
			if HoldButtonZ + HoldingTime <= time.time():
				press_button_NC(NunchuckButtons.Z,NCZHold,False)
				ClickZ = False
			else:
				ClickZ = True
			
		elif wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.Z) and NCZHold == IgnoreKey:
			ZPressed = True
			press_button_NC(NunchuckButtons.Z,NCZ,False)
				
		elif not wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.Z) and ClickZ:
			press_button_NC(NunchuckButtons.Z,NCZ,True)
			ClickZ = False
			
		elif not wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.Z) and ZPressed:
			ZPressed = False
			press_button_NC(NunchuckButtons.Z,NCZHold,False)
			press_button_NC(NunchuckButtons.Z,NCZ,False)
		
	elif UseHoldMapping and AlternateMappingKey:
	
	#---------------------C-Button-Alt-----------------------
	
		if wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.C) and NCCHoldAlt != IgnoreKey:
			if not CPressedAlt:
				HoldButtonCAlt = time.time()
				CPressedAlt = True
			if HoldButtonCAlt + HoldingTime <= time.time():
				press_button_NC(NunchuckButtons.C,NCCHoldAlt,False)
				ClickCAlt = False
			else:
				ClickCAlt = True
			
		elif wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.C) and NCCHoldAlt == IgnoreKey:
			CPressedAlt = True
			press_button_NC(NunchuckButtons.C,NCCAlt,False)
				
		elif not wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.C) and ClickCAlt:
			press_button_NC(NunchuckButtons.C,NCCAlt,True)
			ClickCAlt = False
			
		elif not wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.C) and CPressedAlt:
			CPressedAlt = False
			press_button_NC(NunchuckButtons.C,NCCHoldAlt,False)
			press_button_NC(NunchuckButtons.C,NCCAlt,False)
			
				
	#---------------------Z-Button-Alt-----------------------
	
		if wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.Z) and NCZHoldAlt != IgnoreKey:
			if not ZPressedAlt:
				HoldButtonZAlt = time.time()
				ZPressedAlt = True
			if HoldButtonZAlt + HoldingTime <= time.time():
				press_button_NC(NunchuckButtons.Z,NCZHoldAlt,False)
				ClickZAlt = False
			else:
				ClickZAlt = True
			
		elif wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.Z) and NCZHoldAlt == IgnoreKey:
			ZPressedAlt = True
			press_button_NC(NunchuckButtons.Z,NCZAlt,False)
				
		elif not wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.Z) and ClickZAlt:
			press_button_NC(NunchuckButtons.Z,NCZAlt,True)
			ClickZAlt = False
			
		elif not wiimote[NunchuckNumber].nunchuck.buttons.button_down(NunchuckButtons.Z) and ZPressedAlt:
			ZPressedAlt = False
			press_button_NC(NunchuckButtons.Z,NCZHoldAlt,False)
			press_button_NC(NunchuckButtons.Z,NCZAlt,False)
			
	elif AlternateMappingKey:
			
	#---------------------C Button-Alt-----------------------
	
		if wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.C):
			CPressedAlt = True
			press_button_NC(NunchuckButtons.C,NCCAlt,False)
	
		elif not wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.C) and CPressedAlt:
			CPressedAlt = False
			press_button_NC(NunchuckButtons.C,NCCAlt,False)
			
				
	#---------------------Z Button-Alt-----------------------
	
		if wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.Z):
			ZPressedAlt = True
			press_button_NC(NunchuckButtons.Z,NCZAlt,False)
	
		elif not wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.Z) and ZPressedAlt:
			ZPressedAlt = False
			press_button_NC(NunchuckButtons.Z,NCZAlt,False)
			
	else:
			
	#---------------------C Button-----------------------
	
		if wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.C):
			CPressed = True
			press_button_NC(NunchuckButtons.C,NCC,False)
	
		elif not wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.C) and CPressed:
			CPressed = False
			press_button_NC(NunchuckButtons.C,NCC,False)
			
				
	#---------------------Z Button-----------------------
	
		if wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.Z):
			ZPressed = True
			press_button_NC(NunchuckButtons.Z,NCZ,False)
	
		elif not wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.Z) and ZPressed:
			ZPressed = False
			press_button_NC(NunchuckButtons.Z,NCZ,False)
			
			
def CheckNunchuckStickSettings():
	global TiltedN, TiltedNE, TiltedE, TiltedSE, TiltedS, TiltedSW, TiltedW, TiltedNW
	global TiltedNAlt, TiltedNEAlt, TiltedEAlt, TiltedSEAlt, TiltedSAlt, TiltedSWAlt, TiltedWAlt, TiltedNWAlt
	global StickLimit, StickY, StickX, StickDeg, XAxis, YAxis
	
	global StickRingOuter, StickRingOuterAlt, StickRingInner, StickRingInnerAlt	
	
	global ToggleStickMouse, CheckMouse
	
	if not UseStickMouse or not GyroOffButton:
		XAxis = filters.mapRange(filters.deadband(wiimote[NunchuckNumber].nunchuck.stick.x, 0), -95, 95, -95 ,95)
		YAxis = filters.mapRange(filters.deadband(wiimote[NunchuckNumber].nunchuck.stick.y, 0), -95, 95, -95, 95)
		
		CheckMouse = 0
	
	elif UseStickMouse and GyroOffButton and StickMouseToggling:
		if CheckMouse == 0:
			CheckMouse = 1
			ToggleStickMouse = not ToggleStickMouse
			
	elif UseStickMouse and GyroOffButton and not StickMouseToggling:
		mouse.deltaX = (filters.mapRange(filters.deadband(wiimote[NunchuckNumber].nunchuck.stick.x, StickSens), -95, 95, -95 ,95)*MouseSpeedStick)
		mouse.deltaY = (-filters.mapRange(filters.deadband(wiimote[NunchuckNumber].nunchuck.stick.y, StickSens), -95, 95, -95 ,95)*MouseSpeedStick)
		
		XAxis = 0
		YAxis = 0
		
	if ToggleStickMouse:
		mouse.deltaX = (filters.mapRange(filters.deadband(wiimote[NunchuckNumber].nunchuck.stick.x, StickSens), -95, 95, -95 ,95)*MouseSpeedStick)
		mouse.deltaY = (-filters.mapRange(filters.deadband(wiimote[NunchuckNumber].nunchuck.stick.y, StickSens), -95, 95, -95 ,95)*MouseSpeedStick)
		
		XAxis = 0
		YAxis = 0
		
	StickLimit = math.sqrt((XAxis*XAxis)+(YAxis*YAxis))
	
	StickY = math.sqrt((StickLimit*StickLimit)-(YAxis*YAxis))
	StickX = math.sqrt((StickLimit*StickLimit)-(XAxis*XAxis))
	
	if StickLimit == 0:
		StickLimit = 0.001	
	elif StickLimit > 0 and XAxis > 0 and YAxis > 0:
		StickDeg = (StickY/StickLimit)*90
	elif StickLimit > 0 and XAxis > 0 and YAxis < 0:
		StickDeg = (StickX/StickLimit)*90 + 90
	elif StickLimit > 0 and XAxis < 0 and YAxis < 0:
		StickDeg = (StickY/StickLimit)*90 + 180
	elif StickLimit > 0 and XAxis < 0 and YAxis > 0:
		StickDeg = (StickX/StickLimit)*90 + 270		
			

	if not UseStickEightDirections:
		if AlternateMappingKey:	
			if XAxis < -StickSens and NCStickWAlt != IgnoreKey:
				keyboard.setKeyDown(NCStickWAlt)
				TiltedWAlt = True
			elif XAxis > StickSens and NCStickEAlt != IgnoreKey:
				keyboard.setKeyDown(NCStickEAlt)
				TiltedEAlt = True
			elif TiltedWAlt or TiltedEAlt:
				keyboard.setKeyUp(NCStickW)
				keyboard.setKeyUp(NCStickE)
				keyboard.setKeyUp(NCStickWAlt)
				keyboard.setKeyUp(NCStickEAlt)
				TiltedWAlt = False
				TiltedEAlt = False
				
			if YAxis < -StickSens and NCStickSAlt != IgnoreKey:
				keyboard.setKeyDown(NCStickSAlt)
				TiltedSAlt = True
			elif YAxis > StickSens and NCStickNAlt != IgnoreKey:
				keyboard.setKeyDown(NCStickNAlt)
				TiltedNAlt = True
			elif TiltedNAlt or TiltedSAlt:
				keyboard.setKeyUp(NCStickN)
				keyboard.setKeyUp(NCStickS)
				keyboard.setKeyUp(NCStickNAlt)
				keyboard.setKeyUp(NCStickSAlt)
				TiltedNAlt = False
				TiltedSAlt = False
	
		else:
			if XAxis < -StickSens and NCStickW != IgnoreKey:
				keyboard.setKeyDown(NCStickW)
				TiltedW = True
			elif XAxis > StickSens and NCStickE != IgnoreKey:
				keyboard.setKeyDown(NCStickE)
				TiltedE = True
			elif TiltedW or TiltedE:
				keyboard.setKeyUp(NCStickW)
				keyboard.setKeyUp(NCStickE)
				keyboard.setKeyUp(NCStickWAlt)
				keyboard.setKeyUp(NCStickEAlt)
				TiltedW = False
				TiltedE = False
				
			if YAxis < -StickSens and NCStickS != IgnoreKey:
				keyboard.setKeyDown(NCStickS)
				TiltedS = True
			elif YAxis > StickSens and NCStickN != IgnoreKey:
				keyboard.setKeyDown(NCStickN)
				TiltedN = True
			elif TiltedN or TiltedS:
				keyboard.setKeyUp(NCStickN)
				keyboard.setKeyUp(NCStickS)
				keyboard.setKeyUp(NCStickNAlt)
				keyboard.setKeyUp(NCStickSAlt)
				TiltedN = False
				TiltedS = False
				

	elif UseStickEightDirections:
		if AlternateMappingKey:
			if abs(XAxis) > StickSens or abs(YAxis) > StickSens:
				if StickDeg < 292 and StickDeg > 249 and NCStickWAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickWAlt)
					TiltedWAlt = True
				elif StickDeg < 337 and StickDeg > 294 and NCStickNWAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickNWAlt)
					TiltedNWAlt = True
				elif StickDeg > 339 and NCStickNAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickNAlt)
					TiltedNAlt = True
				elif StickDeg < 22 and NCStickNAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickNAlt)
					TiltedNAlt = True
				elif StickDeg > 24 and StickDeg < 67 and NCStickNEAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickNEAlt)
					TiltedNEAlt = True
				elif StickDeg > 69 and StickDeg < 112 and NCStickEAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickEAlt)
					TiltedEAlt = True
				elif StickDeg > 114 and StickDeg < 157 and NCStickSEAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickSEAlt)
					TiltedSEAlt = True
				elif StickDeg > 159 and StickDeg < 202 and NCStickSAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickSAlt)
					TiltedSAlt = True
				elif StickDeg > 204 and StickDeg < 247 and NCStickSWAlt != IgnoreKey:
					keyboard.setKeyDown(NCStickSWAlt)
					TiltedSWAlt = True
				elif TiltedWAlt or TiltedNWAlt or TiltedNAlt or TiltedNEAlt or TiltedEAlt or TiltedSEAlt or TiltedSAlt or TiltedSWAlt:
					keyboard.setKeyUp(NCStickWAlt)
					keyboard.setKeyUp(NCStickNWAlt)
					keyboard.setKeyUp(NCStickNAlt)
					keyboard.setKeyUp(NCStickNEAlt)
					keyboard.setKeyUp(NCStickEAlt)
					keyboard.setKeyUp(NCStickSEAlt)
					keyboard.setKeyUp(NCStickSAlt)
					keyboard.setKeyUp(NCStickSWAlt)
					keyboard.setKeyUp(NCStickW)
					keyboard.setKeyUp(NCStickNW)
					keyboard.setKeyUp(NCStickN)
					keyboard.setKeyUp(NCStickNE)
					keyboard.setKeyUp(NCStickE)
					keyboard.setKeyUp(NCStickSE)
					keyboard.setKeyUp(NCStickS)
					keyboard.setKeyUp(NCStickSW)
					TiltedWAlt = False
					TiltedNWAlt = False
					TiltedNAlt = False
					TiltedNEAlt = False
					TiltedEAlt = False
					TiltedSEAlt = False
					TiltedSAlt = False
					TiltedSWAlt = False
		
		else:
			if abs(XAxis) > StickSens or abs(YAxis) > StickSens:
				if StickDeg < 292 and StickDeg > 249 and NCStickW != IgnoreKey:
					keyboard.setKeyDown(NCStickW)
					TiltedW = True
				elif StickDeg < 337 and StickDeg > 294 and NCStickNW != IgnoreKey:
					keyboard.setKeyDown(NCStickNW)
					TiltedNW = True
				elif StickDeg > 339 and NCStickN != IgnoreKey:
					keyboard.setKeyDown(NCStickN)
					TiltedN = True
				elif StickDeg < 22 and NCStickN != IgnoreKey:
					keyboard.setKeyDown(NCStickN)
					TiltedN = True
				elif StickDeg > 24 and StickDeg < 67 and NCStickNE != IgnoreKey:
					keyboard.setKeyDown(NCStickNE)
					TiltedNE = True
				elif StickDeg > 69 and StickDeg < 112 and NCStickE != IgnoreKey:
					keyboard.setKeyDown(NCStickE)
					TiltedE = True
				elif StickDeg > 114 and StickDeg < 157 and NCStickSE != IgnoreKey:
					keyboard.setKeyDown(NCStickSE)
					TiltedSE = True
				elif StickDeg > 159 and StickDeg < 202 and NCStickS != IgnoreKey:
					keyboard.setKeyDown(NCStickS)
					TiltedS = True
				elif StickDeg > 204 and StickDeg < 247 and NCStickSW != IgnoreKey:
					keyboard.setKeyDown(NCStickSW)
					TiltedSW = True
				elif TiltedW or TiltedNW or TiltedN or TiltedNE or TiltedE or TiltedSE or TiltedS or TiltedSW:
					keyboard.setKeyUp(NCStickWAlt)
					keyboard.setKeyUp(NCStickNWAlt)
					keyboard.setKeyUp(NCStickNAlt)
					keyboard.setKeyUp(NCStickNEAlt)
					keyboard.setKeyUp(NCStickEAlt)
					keyboard.setKeyUp(NCStickSEAlt)
					keyboard.setKeyUp(NCStickSAlt)
					keyboard.setKeyUp(NCStickSWAlt)
					keyboard.setKeyUp(NCStickW)
					keyboard.setKeyUp(NCStickNW)
					keyboard.setKeyUp(NCStickN)
					keyboard.setKeyUp(NCStickNE)
					keyboard.setKeyUp(NCStickE)
					keyboard.setKeyUp(NCStickSE)
					keyboard.setKeyUp(NCStickS)
					keyboard.setKeyUp(NCStickSW)
					TiltedW = False
					TiltedNW = False
					TiltedN = False
					TiltedNE = False
					TiltedE = False
					TiltedSE = False
					TiltedS = False
					TiltedSW = False

	if UseStickRing:
		if AlternateMappingKey:
			if abs(StickLimit) > StickRingThresholdOuter and NCStickOuterRingAlt != IgnoreKey:
				keyboard.setKeyDown(NCStickOuterRingAlt)
				StickRingOuterAlt = True
			elif abs(StickLimit) > StickRingThresholdInner and abs(StickLimit) < StickRingThresholdOuter-3 and NCStickInnerRingAlt != IgnoreKey:
				keyboard.setKeyDown(NCStickInnerRingAlt)
				StickRingInnerAlt = True
			elif StickRingOuterAlt or StickRingInnerAlt:
				keyboard.setKeyUp(NCStickOuterRingAlt)
				keyboard.setKeyUp(NCStickOuterRing)
				keyboard.setKeyUp(NCStickInnerRingAlt)
				keyboard.setKeyUp(NCStickInnerRing)
				StickRingOuterAlt = False
				StickRingInnerAlt = False
				
		else:
			if abs(StickLimit) > StickRingThresholdOuter and NCStickOuterRing != IgnoreKey:
				keyboard.setKeyDown(NCStickOuterRing)
				StickRingOuter = True
			elif abs(StickLimit) > StickRingThresholdInner and abs(StickLimit) < StickRingThresholdOuter-3 and NCStickInnerRing != IgnoreKey:
				keyboard.setKeyDown(NCStickInnerRing)
				StickRingInner = True
			elif StickRingOuter or StickRingInner:
				keyboard.setKeyUp(NCStickOuterRingAlt)
				keyboard.setKeyUp(NCStickOuterRing)
				keyboard.setKeyUp(NCStickInnerRingAlt)
				keyboard.setKeyUp(NCStickInnerRing)
				StickRingOuter = False
				StickRingInner = False
			
def CheckNunchuckTiltingSettings():
	global NCRollDeg
	global NCTiltedLeft, NCTiltedLeftAlt, NCTiltedRight, NCTiltedRightAlt
	global OldTimeNC, OldAccelNC, NewAccelNC, ShakeNC

	NCRollDeg = NCroll * 180
	
	diagnostics.watch(NCRollDeg)
	
	if UseNCTiltingForKeys:
		if AlternateMappingKey:	
			if NCRollDeg < -TiltKeyRollMin and NCRollDeg > -TiltKeyRollMax and NCTiltLeftAlt != IgnoreKey:
				keyboard.setKeyDown(NCTiltLeftAlt)
				NCTiltedLeftAlt = True
			elif NCRollDeg > TiltKeyRollMin and NCRollDeg < TiltKeyRollMax and NCTiltRightAlt != IgnoreKey:
				keyboard.setKeyDown(NCTiltRightAlt)
				NCTiltedRightAlt = True
			elif abs(NCRollDeg) <= TiltKeyRollMin and abs(NCRollDeg) >= TiltKeyRollMin-10:
				NCTiltedLeftAlt = True
				NCTiltedRightAlt = True
			elif NCTiltedLeftAlt or NCTiltedRightAlt:
				keyboard.setKeyUp(NCTiltRight)
				keyboard.setKeyUp(NCTiltLeft)
				keyboard.setKeyUp(NCTiltRightAlt)
				keyboard.setKeyUp(NCTiltLeftAlt)
				NCTiltedLeftAlt = False
				NCTiltedRightAlt = False
		
		else:
			if NCRollDeg < -TiltKeyRollMin and NCRollDeg > -TiltKeyRollMax and NCTiltLeft != IgnoreKey:
				keyboard.setKeyDown(NCTiltLeft)
				NCTiltedLeft = True
			elif NCRollDeg > TiltKeyRollMin and NCRollDeg < TiltKeyRollMax and NCTiltRight != IgnoreKey:
				keyboard.setKeyDown(NCTiltRight)
				NCTiltedRight = True
			elif abs(NCRollDeg) <= TiltKeyRollMin and abs(NCRollDeg) >= TiltKeyRollMin-10:
				NCTiltedLeft = True
				NCTiltedRight = True
			elif NCTiltedLeft or NCTiltedRight:
				keyboard.setKeyUp(NCTiltRight)
				keyboard.setKeyUp(NCTiltLeft)
				keyboard.setKeyUp(NCTiltRightAlt)
				keyboard.setKeyUp(NCTiltLeftAlt)
				NCTiltedLeft = False
				NCTiltedRight = False
				
	if not UseNCTiltingForKeys:		
		OldAccelNC = wiimote[NunchuckNumber].nunchuck.acceleration.y
	
		if OldAccelNC < 0:
			OldAccelNC = 0
			
		if OldTimeNC + 0.05 <= time.time():
			NewAccelNC = wiimote[NunchuckNumber].nunchuck.acceleration.y
			ShakeNC = False
			if NewAccelNC < 0:
				NewAccelNC = 0
			OldTimeNC = time.time()
			
		if (OldAccelNC - NewAccelNC) > ShakeIntensityNC and not ShakeNC and NCShakeVertical != IgnoreKey:
			if AlternateMappingKey:
				keyboard.setPressed(NCShakeVerticalAlt)
			else:
				keyboard.setPressed(NCShakeVertical)
			ShakeNC = True
					
	if UseNCTiltingForSnapStick:
		SnapStickTurn(NCRollDeg)
		
	if UseNCTiltingForContinousRotation:
		ContinousRotation(NCRollDeg)
		

	
#~~~Gets the Systems Mouse Sensitivity~~~#
def get_current_speed():
    get_mouse_speed = 112   # 0x0070 for SPI_GETMOUSESPEED
    speed = ctypes.c_int()
    ctypes.windll.user32.SystemParametersInfoA(get_mouse_speed, 0, ctypes.byref(speed), 0)

    return speed.value
			
			
			
#~~~Checks for double mappings~~~#	
def checkdouble():
	i = 0
	Count = 0
	Failure = False
	
	WMButtons.append(DPadUp)
	WMButtons.append(DPadRight)
	WMButtons.append(DPadLeft)
	WMButtons.append(DPadDown)
	WMButtons.append(WMA)
	WMButtons.append(WMB)
	WMButtons.append(WMMinus)
	WMButtons.append(WMPlus)
	WMButtons.append(WMHome)
	WMButtons.append(WMOne)
	WMButtons.append(WMTwo)
	WMButtons.append(NCC)
	WMButtons.append(NCZ)
	WMButtons.append(NCStickN)
	WMButtons.append(NCStickNE)
	WMButtons.append(NCStickE)
	WMButtons.append(NCStickSE)
	WMButtons.append(NCStickS)
	WMButtons.append(NCStickSW)
	WMButtons.append(NCStickW)
	WMButtons.append(NCStickNW)
	WMButtons.append(NCStickInnerRing)
	WMButtons.append(NCStickOuterRing)
	WMButtons.append(NCTiltLeft)
	WMButtons.append(NCTiltRight)
	WMButtons.append(WMTiltLeft)
	WMButtons.append(WMTiltRight)
	WMButtons.append(NCShakeVertical)
	WMButtons.append(WMShakeVertical)
	WMButtons.append(DPadUpHold)
	WMButtons.append(DPadRightHold)
	WMButtons.append(DPadLeftHold)
	WMButtons.append(DPadDownHold)
	WMButtons.append(WMAHold)
	WMButtons.append(WMBHold)
	WMButtons.append(WMMinusHold)
	WMButtons.append(WMPlusHold)
	WMButtons.append(WMHomeHold)
	WMButtons.append(WMOneHold)
	WMButtons.append(WMTwoHold)
	WMButtons.append(NCCHold)
	WMButtons.append(NCZHold)
	
	WMStrings.append("DPadUp")
	WMStrings.append("DPadRight")
	WMStrings.append("DPadLeft")
	WMStrings.append("DPadDown")
	WMStrings.append("WMA")
	WMStrings.append("WMB")
	WMStrings.append("WMMinus")
	WMStrings.append("WMPlus")
	WMStrings.append("WMHome")
	WMStrings.append("WMOne")
	WMStrings.append("WMTwo")
	WMStrings.append("NCC")
	WMStrings.append("NCZ")
	WMStrings.append("NCStickN")
	WMStrings.append("NCStickNE")
	WMStrings.append("NCStickE")
	WMStrings.append("NCStickSE")
	WMStrings.append("NCStickS")
	WMStrings.append("NCStickSW")
	WMStrings.append("NCStickW")
	WMStrings.append("NCStickNW")
	WMStrings.append("NCStickInnerRing")
	WMStrings.append("NCStickOuterRing")
	WMStrings.append("NCTiltLeft")
	WMStrings.append("NCTiltRight")
	WMStrings.append("WMTiltLeft")
	WMStrings.append("WMTiltRight")
	WMStrings.append("NCShakeVertical")
	WMStrings.append("WMShakeVertical")
	WMStrings.append("DPadUpHold")
	WMStrings.append("DPadRightHold")
	WMStrings.append("DPadLeftHold")
	WMStrings.append("DPadDownHold")
	WMStrings.append("WMAHold")
	WMStrings.append("WMBHold")
	WMStrings.append("WMMinusHold")
	WMStrings.append("WMPlusHold")
	WMStrings.append("WMHomeHold")
	WMStrings.append("WMOneHold")
	WMStrings.append("WMTwoHold")
	WMStrings.append("NCCHold")
	WMStrings.append("NCZHold")
	

	
	for item in WMButtons:
		if not WMButtons[i] == IgnoreKey:
	
			for item in WMButtons:
				if	WMButtons[i] == WMButtons[Count] and i != Count:
					diagnostics.notify("%s and %s are both mapped to %s. Please change the mapping of these keys." %(WMStrings[i], WMStrings[Count], WMButtons[i]))
					keyboard.setPressed(Key.LeftShift)
					keyboard.setPressed(Key.F5)
					Failure = True
					break
				Count += 1
			
		if Failure:
			break
			
		i += 1
		Count = 0

def checkdoubleAlt():
	i = 0
	Count = 0
	Failure = False
	
	WMButtonsAlt.append(DPadUpAlt)
	WMButtonsAlt.append(DPadRightAlt)
	WMButtonsAlt.append(DPadLeftAlt)
	WMButtonsAlt.append(DPadDownAlt)
	WMButtonsAlt.append(WMAAlt)
	WMButtonsAlt.append(WMBAlt)
	WMButtonsAlt.append(WMMinusAlt)
	WMButtonsAlt.append(WMPlusAlt)
	WMButtonsAlt.append(WMHomeAlt)
	WMButtonsAlt.append(WMOneAlt)
	WMButtonsAlt.append(WMTwoAlt)
	WMButtonsAlt.append(NCCAlt)
	WMButtonsAlt.append(NCZAlt)
	WMButtonsAlt.append(NCStickNAlt)
	WMButtonsAlt.append(NCStickNEAlt)
	WMButtonsAlt.append(NCStickEAlt)
	WMButtonsAlt.append(NCStickSEAlt)
	WMButtonsAlt.append(NCStickSAlt)
	WMButtonsAlt.append(NCStickSWAlt)
	WMButtonsAlt.append(NCStickWAlt)
	WMButtonsAlt.append(NCStickNWAlt)
	WMButtonsAlt.append(NCStickInnerRingAlt)
	WMButtonsAlt.append(NCStickOuterRingAlt)
	WMButtonsAlt.append(NCTiltLeftAlt)
	WMButtonsAlt.append(NCTiltRightAlt)
	WMButtonsAlt.append(WMTiltLeftAlt)
	WMButtonsAlt.append(WMTiltRightAlt)
	WMButtonsAlt.append(NCShakeVerticalAlt)
	WMButtonsAlt.append(WMShakeVerticalAlt)
	WMButtonsAlt.append(DPadUpHoldAlt)
	WMButtonsAlt.append(DPadRightHoldAlt)
	WMButtonsAlt.append(DPadLeftHoldAlt)
	WMButtonsAlt.append(DPadDownHoldAlt)
	WMButtonsAlt.append(WMAHoldAlt)
	WMButtonsAlt.append(WMBHoldAlt)
	WMButtonsAlt.append(WMMinusHoldAlt)
	WMButtonsAlt.append(WMPlusHoldAlt)
	WMButtonsAlt.append(WMHomeHoldAlt)
	WMButtonsAlt.append(WMOneHoldAlt)
	WMButtonsAlt.append(WMTwoHoldAlt)
	WMButtonsAlt.append(NCCHoldAlt)
	WMButtonsAlt.append(NCZHoldAlt)
	
	WMStringsAlt.append("DPadUpAlt")
	WMStringsAlt.append("DPadRightAlt")
	WMStringsAlt.append("DPadLeftAlt")
	WMStringsAlt.append("DPadDownAlt")
	WMStringsAlt.append("WMAAlt")
	WMStringsAlt.append("WMBAlt")
	WMStringsAlt.append("WMMinusAlt")
	WMStringsAlt.append("WMPlusAlt")
	WMStringsAlt.append("WMHomeAlt")
	WMStringsAlt.append("WMOneAlt")
	WMStringsAlt.append("WMTwoAlt")
	WMStringsAlt.append("NCCAlt")
	WMStringsAlt.append("NCZAlt")
	WMStringsAlt.append("NCStickNAlt")
	WMStringsAlt.append("NCStickNEAlt")
	WMStringsAlt.append("NCStickEAlt")
	WMStringsAlt.append("NCStickSEAlt")
	WMStringsAlt.append("NCStickSAlt")
	WMStringsAlt.append("NCStickSWAlt")
	WMStringsAlt.append("NCStickWAlt")
	WMStringsAlt.append("NCStickNWAlt")
	WMStringsAlt.append("NCStickInnerRingAlt")
	WMStringsAlt.append("NCStickOuterRingAlt")
	WMStringsAlt.append("NCTiltLeftAlt")
	WMStringsAlt.append("NCTiltRightAlt")
	WMStringsAlt.append("WMTiltLeftAlt")
	WMStringsAlt.append("WMTiltRightAlt")
	WMStringsAlt.append("NCShakeVerticalAlt")
	WMStringsAlt.append("WMShakeVerticalAlt")
	WMStringsAlt.append("DPadUpHoldAlt")
	WMStringsAlt.append("DPadRightHoldAlt")
	WMStringsAlt.append("DPadLeftHoldAlt")
	WMStringsAlt.append("DPadDownHoldAlt")
	WMStringsAlt.append("WMAHoldAlt")
	WMStringsAlt.append("WMBHoldAlt")
	WMStringsAlt.append("WMMinusHoldAlt")
	WMStringsAlt.append("WMPlusHoldAlt")
	WMStringsAlt.append("WMHomeHoldAlt")
	WMStringsAlt.append("WMOneHoldAlt")
	WMStringsAlt.append("WMTwoHoldAlt")
	WMStringsAlt.append("NCCHoldAlt")
	WMStringsAlt.append("NCZHoldAlt")
	

	
	for item in WMButtonsAlt:
		if not WMButtonsAlt[i] == IgnoreKey:
	
			for item in WMButtonsAlt:
				if	WMButtonsAlt[i] == WMButtonsAlt[Count] and i != Count:
					diagnostics.notify("%s and %s are both mapped to %s. Please change the mapping of these keys." %(WMStringsAlt[i], WMStringsAlt[Count], WMButtonsAlt[i]))
					keyboard.setPressed(Key.LeftShift)
					keyboard.setPressed(Key.F5)
					Failure = True
					break
				Count += 1
			
		if Failure:
			break
			
		i += 1
		Count = 0
    
if starting:
	system.setThreadTiming(TimingType)
	system.threadExecutionInterval = ThreadInterval
	
	SnapedRight = False
	SnapedLeft = False
	SnapDeg = 0
	SnapRotations = 0
	SnapAmount = 0.0
	
	Fraction = 0.5/100
	RFraction = 20.0/100
	YawFraction = 0
	PitchFraction = 0
	
	if CounterOSMouseSensitivity:
		mousesens = get_current_speed()
	else:
		mousesens = 1
	
	TiltKeyRollMin = 40
	TiltKeyRollMax = 120
	
	ToggleStickMouse = False
	CheckMouse = 0
	
	ToggleCR = False
	TCCheck = 0
	
	ToggleGyroOn = True
	CheckGyro = 0
	
	DPadRightPressed = False
	ClickDPadRight = False
	
	DPadLeftPressed = False
	ClickDPadLeft = False
	
	DPadUpPressed = False
	ClickDPadUp = False
	
	DPadDownPressed = False
	ClickDPadDown = False
	
	APressed = False
	ClickA = False
	
	BPressed = False
	ClickB = False	
	
	MinusPressed = False
	ClickMinus = False
	
	HomePressed = False
	ClickHome = False
	
	PlusPressed = False
	ClickPlus = False
	
	OnePressed = False
	ClickOne = False
	
	TwoPressed = False
	ClickTwo = False
	
	CPressed = False
	ClickC = False
	
	ZPressed = False
	ClickZ = False
	
	DPadRightPressedAlt = False
	ClickDPadRightAlt = False
	
	DPadLeftPressedAlt = False
	ClickDPadLeftAlt = False
	
	DPadUpPressedAlt = False
	ClickDPadUpAlt = False
	
	DPadDownPressedAlt = False
	ClickDPadDownAlt = False
	
	APressedAlt = False
	ClickAAlt = False
	
	BPressedAlt = False
	ClickBAlt = False	
	
	MinusPressedAlt = False
	ClickMinusAlt = False
	
	HomePressedAlt = False
	ClickHomeAlt = False
	
	PlusPressedAlt = False
	ClickPlusAlt = False
	
	OnePressedAlt = False
	ClickOneAlt = False
	
	TwoPressedAlt = False
	ClickTwoAlt = False
	
	CPressedAlt = False
	ClickCAlt = False
	
	ZPressedAlt = False
	ClickZAlt = False
	
	WMTiltedLeft = False
	WMTiltedRight = False
	WMTiltedLeftAlt = False
	WMTiltedRightAlt = False
	
	NCTiltedLeft = False
	NCTiltedRight = False
	NCTiltedLeftAlt = False
	NCTiltedRightAlt = False
	
	NCTiltedUp = False
	NCTiltedDown = False
	NCTiltedUpAlt = False
	NCTiltedDownAlt = False
	
	StickRingOuter = False
	StickRingOuterAlt = False
	StickRingInner = False
	StickRingInnerAlt = False
	
	TiltedN = False
	TiltedNE = False
	TiltedE = False
	TiltedSE = False
	TiltedS = False
	TiltedSW = False
	TiltedW = False
	TiltedNW = False	
	TiltedNAlt = False
	TiltedNEAlt = False
	TiltedEAlt = False
	TiltedSEAlt = False
	TiltedSAlt = False
	TiltedSWAlt = False
	TiltedWAlt = False
	TiltedNWAlt = False
	
	OldTime = time.time()
	OldAccel = 0
	NewAccel = 0
	Shake = True
	
	OldTimeNC = time.time()
	OldAccelNC = 0
	NewAccelNC = 0
	ShakeNC = True
	
	StickDeg = 0
	
	WD = False
	WU = False
	MM = False
	
	currentInputIndex = 0
	inputBuffer = [0]*17
	average = 0.0
	averagepitch = 0.0
	
	rollDeg = 0
	pitchDeg = 0
	NCRollDeg = 0
	NCPitchDeg = 0
	
	if ActivateDoubleCheck:
		WMButtons = []
		WMStrings = []
		WMButtonsAlt = []
		WMStringsAlt = []
		checkdouble()
		checkdoubleAlt()
	
	calibrated = False
	Cd = False
	Countdown = 0
	NumOffsetSamples = 0
	Offsets = 300
	calibratedyaw = wiimote[0].motionplus.yaw_down
	calibratedpitch = wiimote[0].motionplus.pitch_left
	
	NunchuckNumber = 0
		
	wiimote[0].acceleration.update += accel_update
	
	if UseGyroMouse and not UseNunchuck:
		wiimote[0].motionplus.update += motionplus_update
		wiimote[0].enable(WiimoteCapabilities.MotionPlus)
	elif UseGyroMouse and UseNunchuck:
		wiimote[0].motionplus.update += motionplus_update
		wiimote[0].enable(WiimoteCapabilities.MotionPlus | WiimoteCapabilities.Extension)
	elif not UseGyroMouse and UseNunchuck:
		wiimote[0].enable(WiimoteCapabilities.Extension)
		
	wiimote[0].buttons.update += update_buttons
	
	if UseNunchuck and UseNunchuckSecondWiimote:
		keyboard.setPressed(Key.LeftShift)
		keyboard.setPressed(Key.F5)
		diagnostics.notify("Too many Nunchucks", "You have enabled Nunchucks for Wiimote 1 and 2. Please just enable one of them.")
		diagnostics.debug("You have enabled Nunchucks for Wiimote 1 and 2. Please just enable one of them.")
	
	if UseNCTiltingForSnapStick and UseWMTiltingForSnapStick:
		keyboard.setPressed(Key.LeftShift)
		keyboard.setPressed(Key.F5)
		diagnostics.notify("Too many Snap-Sticks", "You have enabled both the Wiimote and Nunchuck for the SnapStick. Please just enable one of them.")
		diagnostics.debug("You have enabled both the Wiimote and Nunchuck for the SnapStick. Please just enable one of them.")
	
	if UseNCTiltingForContinousRotation and UseWMTiltingForContinousRotation:
		keyboard.setPressed(Key.LeftShift)
		keyboard.setPressed(Key.F5)
		diagnostics.notify("Too many Continous Rotation Modes", "You have enabled both the Wiimote and Nunchuck for the Continous Rotation Mode. Please just enable one of them.")
		diagnostics.debug("You have enabled both the Wiimote and Nunchuck for the Continous Rotation Mode. Please just enable one of them.")
	
	if UseNCTiltingForSnapStick and UseNCTiltingForContinousRotation:
		keyboard.setPressed(Key.LeftShift)
		keyboard.setPressed(Key.F5)
		diagnostics.notify("Snap-Stick and Continous Rotation Overlap", "You have enabled Snap-Stick and Continous Rotation for the Nunchuck. Please just enable one of these methods.")
		diagnostics.debug("You have enabled Snap-Stick and Continous Rotation for the Nunchuck. Please just enable one of these methods.")
	
	if UseWMTiltingForSnapStick and UseWMTiltingForContinousRotation:
		keyboard.setPressed(Key.LeftShift)
		keyboard.setPressed(Key.F5)
		diagnostics.notify("Snap-Stick and Continous Rotation Overlap", "You have enabled Snap-Stick and Continous Rotation for the Wiimote. Please just enable one of these methods.")
		diagnostics.debug("You have enabled Snap-Stick and Continous Rotation for the Wiimote. Please just enable one of these methods.")
			
	if UseNunchuck:
		wiimote[0].nunchuck.update += update_buttons_NC
		
	if UseNunchuckSecondWiimote:
		wiimote[1].nunchuck.update += update_buttons_NC
		NunchuckNumber = 1
	
if UseGyroMouse and WMHorizontal:
	if NumOffsetSamples < Offsets and wiimote[0].motionplus.roll_left != 0 and wiimote[0].motionplus.pitch_left != 0:
		NumOffsetSamples += 1
		calibratedyaw += wiimote[0].motionplus.roll_left
		calibratedpitch += wiimote[0].motionplus.pitch_left
		
	if not calibrated and NumOffsetSamples == Offsets:
		calibrated = True
		calibratedyaw = calibratedyaw / NumOffsetSamples
		calibratedpitch = calibratedpitch / NumOffsetSamples
		
			
		#~~~Recalibration if necessary~~~#
	if calibrated and wiimote[0].buttons.button_down(WiimoteButtons.One) and wiimote[0].buttons.button_down(WiimoteButtons.Two):
		if not Cd:
			Countdown = time.time()
			Cd = True
		
		if Countdown + SecondsBeforeCalibration <= time.time():
			calibrated = False
			Cd = False
			NumOffsetSamples = 0
			calibratedyaw = 0
			calibratedpitch = 0
			
	else:
		Cd = False
		
elif UseGyroMouse and not WMHorizontal:
	if NumOffsetSamples < Offsets and wiimote[0].motionplus.yaw_down != 0 and wiimote[0].motionplus.pitch_left != 0:
		NumOffsetSamples += 1
		calibratedyaw += wiimote[0].motionplus.yaw_down
		calibratedpitch += wiimote[0].motionplus.pitch_left
		
	if not calibrated and NumOffsetSamples == Offsets:
		calibrated = True
		calibratedyaw = calibratedyaw / NumOffsetSamples
		calibratedpitch = calibratedpitch / NumOffsetSamples
		
			
		#~~~Recalibration if necessary~~~#
	if calibrated and wiimote[0].buttons.button_down(WiimoteButtons.One) and wiimote[0].buttons.button_down(WiimoteButtons.Two):
		if not Cd:
			Countdown = time.time()
			Cd = True
		
		if Countdown + SecondsBeforeCalibration <= time.time():
			calibrated = False
			Cd = False
			NumOffsetSamples = 0
			calibratedyaw = 0
			calibratedpitch = 0
			
	else:
		Cd = False
		
if UseAlternateMapping:
	if AlternateButton == NunchuckButtons.C or AlternateButton == NunchuckButtons.Z:
		AlternateMappingKey = wiimote[NunchuckNumber].nunchuck.buttons.button_down(AlternateButton)
	else:
		AlternateMappingKey = wiimote[0].buttons.button_down(AlternateButton)
else:
	AlternateMappingKey = False
	
if GyroOff == NunchuckButtons.C or GyroOff == NunchuckButtons.Z:
	GyroOffButton = wiimote[NunchuckNumber].nunchuck.buttons.button_down(GyroOff)
else:
	GyroOffButton = wiimote[0].buttons.button_down(GyroOff)