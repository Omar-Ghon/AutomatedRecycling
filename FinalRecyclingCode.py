ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B'
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()

def spawn_container(spawn_num_list):#Spawns a container given a list of spawn numbers
  spawn_num = random.choice(spawn_num_list)
  spawn_num_list.remove(spawn_num) #removes the chosen spawn num from the list
  arm.spawn_cage(spawn_num)
  return spawn_num, spawn_num_list #returns the spawn num chosen and the new spawn list


def identify_container(spawn_num):#Use if statements to determine the size and colour of the container based on the spawn number
  if spawn_num < 4: 
    size = 'small'
  else:
    size = 'large'

  if spawn_num == 1 or spawn_num == 4:
    colour = 'red'

  if spawn_num == 2 or spawn_num == 5:
    colour = 'green'

  if spawn_num == 3 or spawn_num == 6:
    colour = 'blue'

  return size, colour


def return_home(): #Decativates autoclaves and returns to home position
  arm.deactivate_autoclaves()
  arm.home()


def pick_up(): #picks up container at the pick up location
  arm.move_arm(0.6, 0.05, 0.01)
  time.sleep(1)
  arm.control_gripper(40)
  time.sleep(1)
  arm.move_arm(0.406, 0.0, 0.483)


def rotate_base_potentiometer(colour): # Rotates base based on potentiometer reading
  right_poteniometer_initial = 0.5 
  right_potentiometer_final = potentiometer.right()
  check = True
  while check == True:
      right_potientiometer_final = potentiometer.right()
      diff = right_potientiometer_final-right_poteniometer_initial #constantly checks difference between initial and final potentiometer readings
      deg = int(diff*350)
      if deg >= 175: #Since arm can't rotate more than +/- 175 degrees, this just sets any degrees above/below +/- 175 degress to +/-175 degrees
        deg = 175
      if deg <= -175:
        deg = -175
      qarm.rotate_base(arm, deg)
      right_poteniometer_initial = right_potientiometer_final #Resets the initial potentiometer reading 
      if arm.check_autoclave(colour) == True: #Uses the built-in function of checking the colour of the autoclave and container to see if the arm is in range
        check = False
     
def reset_potentiometer(): #Functions forces user to go to 0.5 for each potentiometer for each iteration
  check = False
  while check == False:
    if potentiometer.left() == 0.5 and potentiometer.right() == 0.5: #Program won't continue unless both potentiometers are 0.5 
      check = True


  
def drop_off(size, colour): #uses left potentiometer readings to drop off container depending on size
  check = False
  arm.activate_autoclaves() #Acticates Autoclave
  while check == False:
    if potentiometer.left() < 0.5 and size == 'small': #Uses both the left potentiometer and the size variable to determine where to drop off the container. The drop off won't happen unless both the left potentiometer and the size of the container don't match
        drop_off_small(colour)
        check = True
    elif potentiometer.left() > 0.5 and size == 'large':
        drop_off_big(colour)
        check = True
        
  time.sleep(3)
  

def drop_off_small(colour): #This function is used for small containers
  if colour == 'red': #Tells the arm where to move according to colour
    arm.move_arm(-0.025, 0.62, 0.286)

  elif colour == 'green':
    arm.move_arm(-0.644, 0.234, 0.29)

  elif colour == 'blue':
    arm.move_arm(-0.025, -0.62, 0.286)

  time.sleep(1)  
  arm.control_gripper(-40) #Closes gripper. The time sleep is used so the move_arm doesn't interfere with the control_gripper


def drop_off_big(colour): #This function is used for large containers
  arm.open_autoclave(colour) #Opens autoclave

  if colour == 'red': #Tells the arm where to move according to colour
    arm.move_arm(0.029, 0.411, 0.221)

  elif colour == 'green':
    arm.move_arm(-0.423, 0.151, 0.143)

  elif colour == 'blue':
    arm.move_arm(0.029, -0.411, 0.221)
 
  time.sleep(1)
  arm.control_gripper(-40) #Closes gripper. The time sleep is used so the move_arm doesn't interfere with the control_gripper
  time.sleep(3)
  arm.open_autoclave(colour, False) #Closes autoclave. The time sleep allows the container to fully enter the autoclave without there being interference with the closing of the autoclave.


def main():  
  spawn_num_list = [1, 2, 3, 4, 5, 6]
  for i in range(len(spawn_num_list)):
    spawn_num, new_spawn_list = spawn_container(spawn_num_list)
    size, colour = identify_container(spawn_num)
    pick_up()
    rotate_base_potentiometer(colour)
    drop_off(size, colour)
    spawn_num_list = new_spawn_list
    reset_potentiometer()
    return_home()

main()
  

  

