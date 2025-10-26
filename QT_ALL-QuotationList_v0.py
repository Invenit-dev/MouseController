import pyautogui
import time
import pandas as pd
import glob
import os
import sys
import pyperclip

#pyautogui.FAILSAFE = False
print(f"Posizione attuale del mouse: troia")
try:
    while True:
        delta = 50
        timedelay = 3
        x, y = pyautogui.position()
        #print(f"Posizione attuale del mouse: x={x}, y={y}")
        time.sleep(timedelay)
        """
        pyautogui.moveTo(x+delta, y)
        time.sleep(timedelay)
        pyautogui.moveTo(x+delta , y+delta)
        time.sleep(timedelay)
        pyautogui.moveTo(x, y+delta)
        time.sleep(timedelay)
        pyautogui.moveTo(x , y)
        time.sleep(timedelay)
        """
except KeyboardInterrupt:
    print("Interrotto dall'utente.")

pyautogui.click()  # Click sinistro nella posizione attuale del mouse
pyautogui.click(x=100, y=200)  # Click in una posizione specifica
pyautogui.doubleClick()  # Doppio click
pyautogui.scroll(-500)  # Scrolla verso il basso di 500 unità

"""
# Percorso corrente (compatibile con .exe)
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)
    exe_name = os.path.basename(sys.executable)
else: # Quando il file è eseguito come script .py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    exe_name = os.path.basename(__file__)

# Trova il file da analizzare
file_input = next((f for f in os.listdir(current_dir) if f.startswith("QuotationList_Upload") and f.endswith(".xlsx")), None)
# Carica i dati da Excel
input_df = pd.read_excel(os.path.join(current_dir, file_input), sheet_name=0, engine='openpyxl', header=None)
print("Reading Excel File...")
def FillQuotationList(Internal,Sname,SF,Qname,Ptype,Rtype,Cname,Ddate):
    timedelay = 0.75

    # Add new item
    time.sleep(3)
    pyautogui.click(x=1140, y=1205)

    # Inside Sales
    time.sleep(2)
    pyautogui.click(x=1800, y=1370)
    time.sleep(timedelay)
    pyautogui.write('Quot', interval=0.1)
    time.sleep(timedelay)
    pyautogui.press('enter')

    # Received From Who?
    time.sleep(timedelay)
    if Internal == "yes":
        pyautogui.click(x=1350, y=1470)
        time.sleep(timedelay)
        pyperclip.copy(SF)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(timedelay)
        pyautogui.click(x=1570, y=1470)
        time.sleep(timedelay)
        pyautogui.write(Sname, interval=0.1)
        time.sleep(timedelay)
        pyautogui.press('enter')
    else:
        pyautogui.click(x=2000, y=1370) # Unthick YES button
        time.sleep(timedelay)
        pyautogui.click(x=1800, y=1470)
        time.sleep(timedelay)
        pyautogui.write(Sname, interval=0.1)
        time.sleep(timedelay)
        pyautogui.press('enter')


    # Country
    time.sleep(timedelay)
    pyautogui.click(x=2030, y=1470)
    time.sleep(timedelay)
    pyautogui.write('Ita', interval=0.1)
    time.sleep(timedelay)
    pyautogui.press('enter')

    # Customer
    time.sleep(timedelay)
    pyautogui.click(x=1200, y=1565)
    time.sleep(timedelay)
    pyperclip.copy(Cname)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(timedelay)
    pyautogui.press('enter')

    pyautogui.scroll(-1000)  # Scrolla verso il basso di 500 unità

    # Request Type
    time.sleep(timedelay)
    pyautogui.click(x=1150, y=1390)
    time.sleep(timedelay)
    if Rtype == "DTO":
        pyautogui.click(x=1200, y=1430)
    elif Rtype == "sCTO":
        pyautogui.click(x=1200, y=1460)
    elif Rtype == "aCTO":
        pyautogui.click(x=1200, y=1485)
    elif Rtype == "ETO":
        pyautogui.click(x=1200, y=1515)
    elif Rtype == "BGT":
        pyautogui.click(x=1200, y=1545)

    # Product Type
    time.sleep(timedelay)
    if Ptype == "PDC":
        pyautogui.click(x=1330, y=1392)
    elif Ptype == "ICP":
        pyautogui.click(x=1330, y=1416)
    elif Ptype == "EL":
        pyautogui.click(x=1330, y=1440)
    elif Ptype == "FIRE":
        pyautogui.click(x=1330, y=1465)
    elif Ptype == "MV-COMBINATION":
        pyautogui.click(x=1330, y=1487)
    elif Ptype == "MV-SWITCHGEAR":
        pyautogui.click(x=1330, y=1510)
    elif Ptype == "MV-TRANSFORMER":
        pyautogui.click(x=1330, y=1535)
    elif Ptype == "DPQ":
        pyautogui.click(x=1330, y=1560)
    elif Ptype == "CPS":
        pyautogui.click(x=1330, y=1585)
    elif Ptype == "EVCI":
        pyautogui.click(x=1330, y=1607)
    elif Ptype == "ENERGY STORAGE":
        pyautogui.click(x=1330, y=1630)


    # Quotation Code
    time.sleep(timedelay)
    pyautogui.click(x=1600, y=1390)
    time.sleep(timedelay)
    pyautogui.write('auto', interval=0.1)

    # Quotation Name
    time.sleep(timedelay)
    pyautogui.click(x=1800, y=1390)
    time.sleep(timedelay)
    pyperclip.copy(Qname)
    pyautogui.hotkey('ctrl', 'v')

    # Due Date
    time.sleep(timedelay)
    pyautogui.click(x=1600, y=1270)
    time.sleep(timedelay)
    pyperclip.copy(Ddate)
    pyautogui.hotkey('ctrl', 'v')

    # Save
    time.sleep(timedelay)
    pyautogui.click(x=2200, y=1780)

for index in range(1, len(input_df)):
    if pd.notna(input_df.iloc[index, 0]) and str(input_df.iloc[index, 0]).strip() != "":
        act_row = index

        ReceivedFromInternal = input_df.iloc[act_row, 0] # cell(row, column)
        SaleName = input_df.iloc[act_row, 1]          # cell(row, column)
        SFid = input_df.iloc[act_row, 2]              # cell(row, column)
        QuotName = input_df.iloc[act_row, 3]          # cell(row, column)
        ProductType = input_df.iloc[act_row, 4]       # cell(row, column)
        RequestType = input_df.iloc[act_row, 5]       # cell(row, column)
        CustomerName = input_df.iloc[act_row, 6]      # cell(row, column)
        DueDate = input_df.iloc[act_row, 7]           # cell(row, column)
        
        FillQuotationList(ReceivedFromInternal,SaleName,SFid,QuotName,ProductType,RequestType,CustomerName,DueDate)


"""







