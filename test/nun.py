from nunchuck import nunchuck

wii = nunchuck()

while True:
    joyx = wii.joystick_x()
    joyy = wii.joystick_y()
    butc = wii.button_c()
    butz = wii.button_z()
    print("x: {}  y: {} button c: {}  button z: {}".format(joyx,joyy,butc,butz))
    
