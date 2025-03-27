def map_pov(n):
  if wiimote[n].buttons.button_down(WiimoteButtons.DPadUp):
    vJoy[n].setDigitalPov(0, VJoyPov.Up)
  elif wiimote[n].buttons.button_down(WiimoteButtons.DPadDown):
    vJoy[n].setDigitalPov(0, VJoyPov.Down)
  elif wiimote[n].buttons.button_down(WiimoteButtons.DPadLeft):
    vJoy[n].setDigitalPov(0, VJoyPov.Left)
  elif wiimote[n].buttons.button_down(WiimoteButtons.DPadRight):
    vJoy[n].setDigitalPov(0, VJoyPov.Right)
  else:
    vJoy[n].setDigitalPov(0, VJoyPov.Nil)


def map_nunckuck_joystick(n):
  vJoy[n].x = filters.mapRange(filters.deadband(wiimote[n].nunchuck.stick.x, 5), -95, 95, -vJoy[n + 1].axisMax,
                               vJoy[n + 1].axisMax)
  vJoy[n].y = -filters.mapRange(filters.deadband(wiimote[n].nunchuck.stick.y, 5), -95, 95, -vJoy[n + 1].axisMax,
                                vJoy[n + 1].axisMax)


def map_button(n, wiimote_button, vjoy_button):
  vJoy[n].setButton(vjoy_button, wiimote[n].buttons.button_down(wiimote_button))


def map_nunchuck_button(n, nunchuck_button, vjoy_button):
  vJoy[n].setButton(vjoy_button, wiimote[n].nunchuck.buttons.button_down(nunchuck_button))


def map_buttons(n):
  map_button(n, WiimoteButtons.A, 0)
  map_button(n, WiimoteButtons.B, 1)
  map_button(n, WiimoteButtons.One, 2)
  map_button(n, WiimoteButtons.Two, 3)
  map_button(n, WiimoteButtons.Minus, 4)
  map_button(n, WiimoteButtons.Plus, 5)
  map_button(n, WiimoteButtons.Home, 6)
  map_button(n, WiimoteButtons.DPadUp, 9)
  map_button(n, WiimoteButtons.DPadDown, 10)
  map_button(n, WiimoteButtons.DPadLeft, 11)
  map_button(n, WiimoteButtons.DPadRight, 12)


def map_nunchuck_buttons(n):
  map_nunchuck_button(n, NunchuckButtons.C, 7)
  map_nunchuck_button(n, NunchuckButtons.Z, 8)


def updateWiimote1():
  # Wiimote 1
  map_buttons(0)
  map_pov(0)


def updateNunchuck1():
  map_nunchuck_joystick(0)
  map_nunchuck_buttons(0)


# If we're starting up, then hook up our update function.
if starting:
  wiimote[0].buttons.update += updateWiimote1

  wiimote[0].nunchuck.update += updateNunchuck1
