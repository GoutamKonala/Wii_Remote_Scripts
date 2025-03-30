def pryAngle(v, a, b):  # Gives angle on particular plane based on accelerometer output
  mag = math.sqrt(v[a] ** 2 + v[b] ** 2)

  if mag != 0:
    result = math.acos(v[b] / mag) * (1 / (math.pi))
    if v[a] >= 0:
      return result
    else:
      return -result
  else:
    return 0


def map_Dpad(n):
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


def map_button(n, wiimote_button, vjoy_button):
  vJoy[n].setButton(vjoy_button, wiimote[n].buttons.button_down(wiimote_button))


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


def map_orientation(n):
  accl = [wiimote[n].acceleration.x, wiimote[n].acceleration.y, wiimote[n].acceleration.z]
  pitch = pryAngle(accl, 1, 2)
  roll = pryAngle(accl, 0, 2)
  yaw = pryAngle(accl, 1, 0)

  PitchDeg = pitch * 180 - 90
  RollDeg = roll * 180 - 90
  YawDeg = yaw * 180 - 90

  return PitchDeg, RollDeg, YawDeg


def map_flightstick(n):
  PitchDeg, _, YawDeg = map_orientation(n)
  diagnostics.watch(PitchDeg)
  diagnostics.watch(YawDeg)
  max_angle = 30
  deadzone = 4
  # Left Stick
  vJoy[n].x = filters.mapRange(filters.deadband(YawDeg, deadzone), -max_angle, max_angle, -vJoy[n + 1].axisMax,
                               vJoy[n + 1].axisMax)
  vJoy[n].y = filters.mapRange(filters.deadband(PitchDeg, deadzone), -max_angle, max_angle, -vJoy[n + 1].axisMax,
                               vJoy[n + 1].axisMax)


def map_button(n, wiimote_button, vjoy_button):
  vJoy[n].setButton(vjoy_button, wiimote[n].buttons.button_down(wiimote_button))


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


def updateWiimote1():
  map_buttons(0)
  map_Dpad(0)
  map_flightstick(0)


if starting:
  wiimote[0].buttons.update += updateWiimote1

