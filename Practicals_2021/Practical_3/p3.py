# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
pwm_Accuracy = None # Defined pwm object for the LED accuracy pin
pwm_Buzzer = None   # Defined pwm object for the buzzer pin
guess_counter = 0   #Defined counter variable for the number of guesses made by the user
guess_value = -1    #Defined value variable to store the number given by the user
value = 0           #Variable for the randomly generated number

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        guess_counter = 0
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):#*************************************************************************************
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    
    for j in range(count):
        if j>2:
            break
        score_info = raw_data[slice(j*4, j*4+4)]
        usrname = ''.join(score_info[slice(0,3)])
        c = j+1
        print(str(c)+" - "+usrname+" took "+str(score_info[3])+" guesses")
    # print out the scores in the required format
    pass


# Setup Pins
def setup():
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
#Input setup - Buttons
    GPIO.setup(btn_increase,GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(btn_submit,GPIO.IN), pull_up_down = GPIO.PUD_UP)
#Output setup - Guess value LEDs
    for item in LED_value: GPIO.setup(item,GPIO.OUT)
    for item in LED_value: GPIO.output(item,GPIO.LOW)
#Output setup - Accuracy LED
    GPIO.setup(LED_accuracy,GPIO.OUT)
    GPIO.output(LED_accuracy,GPIO.LOW)
#Output setup - Buzzer
    GPIO.setup(Buzzer,GPIO.OUT)
    GPIO.setup(Buzzer,GPIO.LOW)
    GPIO.setwarnings(False) #*********************************************************************************************
    # Setup PWM channels
    pwm_Accuracy = GPIO.PWM(LED_accuracy, 50) #PWM on accuracy LED pin
    pwm_Accuracy.start(0)
    pwm_Buzzer = GPIO.PWM(Buzzer, 1) #PWM on Buzzer pin
    pwm_Buzzer.start(0)
    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_submit,GPIO.FALLING, callback = btn_guess_pressed, bouncetime = 200)
    GPIO.add_event_detect(btn_increase,GPIO.FALLING, callback = btn_increase_pressed, bouncetime = 200)
    pass


# Load high scores
def fetch_scores():#******************************************************************************************************
    # get however many scores there are
    score_count = None
    # Get the scores
    score_count = eeprom.read_byte(0) # 1st 4 byte for no of scores stored
    scores = eeprom.read_block(1, score_count*4)
    # convert the codes back to ascii
    count = 0
    for i in range(len(scores)):
        count+=1
        if count == 4:
            count = 0
        else:
            scores[i] = chr(scores[i]) 
    # return back the results
    return score_count, scores


# Save high scores
def save_scores(username):#*******************************************************************************************************
    # fetch scores
    score_count = eeprom.read_byte(0)
    scores = eeprom.read_block(1, score_count*4)
    # include new score
    data = []
    #print(scores)
    for i in range(score_count):
        data.append(scores[slice(i*4, i*4+4)])
    #print(data)
    usrnm = list(username)
    usrnm = [ord(i) for i in usrnm]
    usrnm.append(guess)
    data.append(usrnm)
    score_count = score_count+1
    # sort
    #print(data)
    data.sort(key=lambda x: x[3])
    # scores.
    # update total amount of scores
    # write new scores
    data = [b for c in data for b in c]
    #print(data)
    eeprom.write_block(1, data)
    eeprom.write_block(0, [score_count])
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess *****Used this approach
    # or just pull the value off the LEDs when a user makes a guess
# Programming counter to stay within range 0 - 7
    if guess_value == 7: guess_value = 0
    else guess_value += 1
#Setting the value pins to show the number of guesses made (Note Big Endian application. Last array element holds LSB
    if guess_value == 0: {GPIO.output(LED_value[0],GPIO.LOW); GPIO.output(LED_value[1],GPIO.LOW); GPIO.output(LED_value[2],GPIO.LOW)}
    if guess_value == 1: {GPIO.output(LED_value[0],GPIO.LOW); GPIO.output(LED_value[1],GPIO.LOW); GPIO.output(LED_value[2],GPIO.HIGH)}
    if guess_value == 2: {GPIO.output(LED_value[0],GPIO.LOW); GPIO.output(LED_value[1],GPIO.HIGH); GPIO.output(LED_value[2],GPIO.LOW)}
    if guess_value == 3: {GPIO.output(LED_value[0],GPIO.LOW); GPIO.output(LED_value[1],GPIO.HIGH); GPIO.output(LED_value[2],GPIO.HIGH)}
    if guess_value == 4: {GPIO.output(LED_value[0],GPIO.HIGH); GPIO.output(LED_value[1],GPIO.LOW); GPIO.output(LED_value[2],GPIO.LOW)}
    if guess_value == 5: {GPIO.output(LED_value[0],GPIO.HIGH); GPIO.output(LED_value[1],GPIO.LOW); GPIO.output(LED_value[2],GPIO.HIGH)}
    if guess_value == 6: {GPIO.output(LED_value[0],GPIO.HIGH); GPIO.output(LED_value[1],GPIO.HIGH); GPIO.output(LED_value[2],GPIO.LOW)}
    if guess_value == 7: {GPIO.output(LED_value[0],GPIO.HIGH); GPIO.output(LED_value[1],GPIO.HIGH); GPIO.output(LED_value[2],GPIO.HIGH)}
    pass


# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    T_Initial = time.time()
    while GPIO.input(btn_submit)== GPIO.LOW:
       pass
    T_Delay = T_initial - time.time()
    if T_Delay >=2:
       pwm_Accuracy.stop()
       pwm_Buzzer.stop()
       for item in LED_value: GPIO.output(item, GPIO.LOW)
       end_of_game = True
    else
        # Compare the actual value with the user value displayed on the LEDs
# Determined Looped Difference analysis (e.g. if value = 7, and guess_value = 0, the difference is 1 (Not 7))
        Diff = abs(guess_value - value)
        if Diff > (8 - Diff): Diff = 8 - Diff
        # Change the PWM LED
        # if it's close enough, adjust the buzzer
        if Diff > 0:{accuracy_leds(Diff); trigger_buzzer(Diff); guess_counter += 1}
        else    # if it's an exact guess:
            # - Disable LEDs and Buzzer
            pwm_Accuracy.stop()
            pwm_Buzzer.stop()
            for item in LED_value: GPIO.output(item, GPIO.LOW)
            while True:
             name = input("Enter username:")# - tell the user and prompt them for a name
             if len(name)==3:
                end_of_game=True
                save_scores(name)
                break
             print("Enter username of length 3:")
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    pass


# LED Brightness
def accuracy_leds(Diff):
#Included a Diff parameter so as not to repeat Difference calculation between value and guess_value
#See function btn_guess_pressed for difference calculation
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    pwm_Accuracy.ChangeDutyCycle(((value - Diff)/value)*100)   
    pass

# Sound Buzzer
def trigger_buzzer(Diff):
#Included a Diff parameter so as not to repeat Difference calculation between value and guess_value
#See function btn_guess_pressed for difference calculation
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    pwm_Buzzer.stop()
    if Diff == 3: {pwm_Buzzer.ChangeFrequency(1); pwm_Buzzer.start(50)}
    elif Diff == 2: {pwm_Buzzer.ChangeFrequency(2); pwm_Buzzer.start(50)}
    elif Diff == 1: {pwm_Buzzer.ChangeFrequency(4); pwm_Buzzer.start(50)}
    else pwm_Buzzer.start(0)
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        pwm_Accuracy.stop()
        pwm_Buzzer.stop()
        GPIO.cleanup()
