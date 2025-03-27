
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
    
    
def map_orientation(n):
  accl = [wiimote[n].acceleration.x, wiimote[n].acceleration.y, wiimote[n].acceleration.z]
  pitch = pryAngle(accl, 1, 2)
  roll = pryAngle(accl, 0, 2)
  yaw = pryAngle(accl, 1, 0)

  PitchDeg = pitch * 180 - 90
  RollDeg = roll * 180 - 90
  YawDeg = yaw * 180 - 90

  return PitchDeg, RollDeg, YawDeg
  
  
def map_nunchuck_orientation(n):
  accl = [wiimote[n].nunchuck.acceleration.x, wiimote[n].nunchuck.acceleration.y, wiimote[n].nunchuck.acceleration.z]
  NCroll = pryAngle(accl, 0, 2)
  NCpitch = pryAngle(accl, 1, 2)
  NCyaw = pryAngle(accl, 1, 0)

  NCRollDeg = NCroll * 180
  NCPitchDeg = NCpitch * 180
  NCYawDeg = NCyaw * 180

  return NCRollDeg, NCPitchDeg, NCYawDeg