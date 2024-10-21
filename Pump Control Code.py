# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 11:50:21 2022
@author: cukelarter




Script for initiating multi-step run on Chemyx Syringe Pump.
"""




#Uncomment when not testing




global n
n = 1
from core import connect
import time
# get open port info
portinfo = connect.getOpenPorts()




# MUST set baudrate in pump "System Settings", and MUST match this rate:
baudrate=9600
# initiate Connection object with first open port
conn = connect.Connection(port=str(portinfo[0]),baudrate=baudrate, x=0, mode=0)








def go():
    print("Starting the pump...")
    conn.startPump()
    print("Pump started:")
   




# Function to stop the pump
def stop():
    print("Stopping the pump...")
    conn.stopPump()
    print("Pump stopped:")








def dispense_volume(volume, flow_rate):

    n = 0
    try:
        # Convert volume and flow_rate to floats (allow decimals)
        vol = float(volume)
        flow = float(flow_rate)

        conn.setRate(flow)
        print(f"Flow rate set to: {flow} mL/min")

        conn.startPump()
        print("Pump started.")

        # Calculate the time required to dispense the volume

        time_required = vol / flow  # Time in minutes, no adjustment
        print(f"Time required to dispense {vol} mL: {time_required} minutes.")

        # Sleep for the calculated time (convert minutes to seconds)
        time.sleep(time_required * 60)
        print(f"{vol} mL dispensed.")

        # Stop the pump after dispensing the volume
        conn.stopPump()
        print("Pump stopped.")
       
    except ValueError:
        print("Invalid input. Please enter numeric values for volume and flow rate.")

    # Stop the pump after dispensing the volume
    conn.stopPump()
    n = 1
    print("Pump stopped.")    
   
# Function to ask for commands
def askCommand():
    while True:
        print("Options: go, stop, dispense volume(dv), control, exit")
        command = input("Command here: ").strip().lower()
        if command == "go":
            go()
        elif command == "stop":
            stop()
        elif command == "exit":
            print("Exiting program.")
            on = False
            break
           
        elif command =="dv":
            try:
                specify_volume = float(input("What volume are you dispensing? (in mL): "))
                specify_flow = float(input("What is the flow rate? (in mL/min): "))
                dispense_volume(specify_volume, specify_flow)
            except ValueError:
                print("Invalid input. Please enter valid numbers for volume and flow rate.")
        else:
            print("Invalid command. Please try again.")


if __name__ == '__main__':

    on = True
    # Open Connection to pump
    conn.openConnection()

    # Default setup
    units = 'mL/min'            # OPTIONS: 'mL/min','mL/hr','μL/min','μL/hr'
    diameter = 4.78           # 4.78mm diameter
    volume = 1                # 1 ml
    delay = 0                # 30 second delay

    # Communicate parameters to pump
    conn.setUnits(units)
    conn.setDiameter(diameter)  
    conn.setVolume(volume)      

    # Start command prompt for user input
    while on:
        if n == 1:
            askCommand()
    # Close the connection when done













