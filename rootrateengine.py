import pandas as pd
import rootcalculate as calculate
import requests
from tkinter import *
import geography
import sys
import os





def read_file(path):
    xls = pd.ExcelFile(path)
    #print(xls.sheet_names)
    for name in xls.sheet_names:
        globals()[f'df_{name}'] = pd.read_excel(xls, name)
        
def resource_path(relative_path):
    #Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

FACTORPATH = resource_path("root_rates.xlsx")
EMPTYRATEPATH = resource_path("emptyratetable.csv")
EMPTYHOUSEHOLDPATH = resource_path("emptyhouseholdriskfactor.csv")

read_file(FACTORPATH)


#%%

#set variables
driverFactors = ["driverAge", "driverGender", "driverMaritalStatus",
             "driverPoints", "driverUBITier"]
vehicleFactors = ["biLimit", "pdLimit", "medLimit", "pipLimit",
            "umuimLimit", "umpdLimit", "rentLimit", "acpeLimit", 
            "fullCoverage", "vehicleAge", "vehiclePriorInsuranceClass",
            "vehDeductible", "roadsideAssistance"]
policyFactors = ["collBought", "compBought", "loanBought", "priorInsurance",
             "paymentMethod", "safe", "accidentFree", "eDelivery", "nafCount",
             "cmpCount", "sr22Status", "cancelMonths", "withPreviousCarrier", "ficoScore", "homeowner"]

numDrivers, numVehicles, numPolicies = 0,0,0
driverAge, driverGender, driverMaritalStatus, driverPoints, driverUBITier = [], [], [], [], []
biLimit, pdLimit, medLimit, pipLimit, umuimLimit, umpdLimit, rentLimit, acpeLimit = [], [], [], [], [], [] ,[], []
fullCoverage, vehicleAge, vehiclePriorInsuranceClass, vehDeductible, vin = [], [], [], [], []
automaticEmergencyBraking, vehicleUse, roadsideAssistance = [], [], []
collBought, compBought, loanBought, address, priorInsurance, paymentMethod, safe = 0,0,0,0,0,0,0
accidentFree, eDelivery, nafCount, cmpCount, sr22Status, cancelMonths, withPreviousCarrier = 0,0,0,0,0,0,0
ficoScore, homeowner = 0,0

numVehiclesLabel, numDriversLabel, newPolicyLabel = 0,0,0


#SET TKINTER
root = Tk()
root.title("Root Rating Engine")   
root.geometry("200x300")






#INPUT FUNCTIONS
def newDriver():
    global driverAge, driverGender, driverMaritalStatus, driverPoints, driverUBITier
    def submitDriver():
        global numDrivers
        x=numDrivers
        #GET INPUTS
        

        driverAge.append(variables[0].get())
        driverGender.append(variables[1].get())
        driverMaritalStatus.append(variables[2].get())
        driverPoints.append(variables[3].get())
        driverUBITier.append(variables[4].get())
        
        driverAge[x] = int(driverAge[x])
        driverPoints[x] = int(driverPoints[x])
        driverUBITier[x] = int(driverUBITier[x])
        
        
        global numDriversLabel
        newDriverScreen.destroy()
        numDrivers = numDrivers+1
        numDriversLabel = Label(root, text="You have inputted " + str(numDrivers) + " Drivers")
        numDriversLabel.grid(column=1,row=7)
        
    newDriverScreen = Toplevel()
    newDriverScreen.title("Add New Driver") 
    newDriverScreen.geometry("300x200")
        

    ageList = (list(range(15,120)))
    genderList = ["F", "M", "X"]
    maritalList = ["M", "S", ]
    pointList = (list(range(0,100)))
    ubiList = (list(range(0,100)))
     
    driverDropdowns = [ageList, genderList, maritalList, pointList, ubiList]
    

    driverLabel, opt, variables = [], [], []
    for x in range(len(driverFactors)):
        y=x+1
        newLabel = Label(newDriverScreen, text=driverFactors[x])
        driverLabel.append(newLabel)
        driverLabel[x].grid(column=0,row=y)

        variable = StringVar(newDriverScreen)
        variable.set(" ")
        variables.append(variable)
        
        
        newDrop = OptionMenu(newDriverScreen, variables[x], *driverDropdowns[x])
        opt.append(newDrop)
        opt[x].config(width=5)
        opt[x].grid(column=1,row=y)
        
        
        
    
    y=y+1
    exitbutton1 = Button(newDriverScreen, text = "Submit Driver", command = submitDriver)
    exitbutton1.grid(column = 1, row = y)
    newDriverScreen.mainloop()


def newVehicle():
    global biLimit, pdLimit, medLimit, pipLimit, umuimLimit, umpdLimit, rentLimit, acpeLimit
    global fullCoverage, vehicleAge, vehiclePriorInsuranceClass, vehDeductible
    global vin, automaticEmergencyBraking, vehicleUse, roadsideAssistance
    
    def submitVehicle():
        global numVehicles
        x=numVehicles
        
        try:
            biLimit.append(variables[0].get())
            pdLimit.append(variables[1].get())
            medLimit.append(variables[2].get())
            pipLimit.append(variables[3].get())
            umuimLimit.append(variables[4].get())
            umpdLimit.append(variables[5].get())
            rentLimit.append(variables[6].get())
            acpeLimit.append(variables[7].get())
            fullCoverage.append(variables[8].get())
            vehicleAge.append(variables[9].get())
            vehiclePriorInsuranceClass.append(variables[10].get())
            vehDeductible.append(variables[11].get())
            vin.append(vinInput.get())
            roadsideAssistance.append(variables[12].get())
            
            pdLimit[x] = int(pdLimit[x])
            if(medLimit[x] != "Not Bought"):
                medLimit[x] = int(medLimit[x])
            if(pipLimit[x] != "Not Bought"):
                pipLimit[x] = int(pipLimit[x])
            if(umpdLimit[x] != "Not Bought"):
                umpdLimit[x] = int(umpdLimit[x])
            vehicleAge[x] = int(vehicleAge[x])
            vehDeductible[x] = int(vehDeductible[x])
            
            useless, lux = calculate.vinFactor(vin[x], df_VIN_Factor)
            assert lux in ["L", "N"], "VIN"
        except AssertionError as error:
            
            errortext = "INPUT ERROR: " + str(error)
            yikesLabel = Label(newVehicleScreen, text = errortext)

            z=y+1
            yikesLabel.grid(column=1,row=z)
            del biLimit[x]
            del pdLimit[x]
            del medLimit[x]
            del pipLimit[x]
            del umuimLimit[x]
            del umpdLimit[x]
            del rentLimit[x]
            del acpeLimit[x]
            del fullCoverage[x]
            del vehicleAge[x]
            del vehiclePriorInsuranceClass[x]
            del vehDeductible[x]
            del vin[x]
            del automaticEmergencyBraking[x]
            del vehicleUse[x]
            del roadsideAssistance[x]
            
        else:
            global numVehiclesLabel
            newVehicleScreen.destroy()
            numVehicles = numVehicles+1
            numVehiclesLabel = Label(root, text="You have inputted " + str(numVehicles) + " Vehicles")
            numVehiclesLabel.grid(column=1,row=8)


    newVehicleScreen = Toplevel()
    newVehicleScreen.title("Add New Vehicles")
    newVehicleScreen.geometry("900x550")
    
    parameters = ["Must be one of following: 30/60, 50/100, 100/200, 250/500",
                  "Must be one of following: 25, 50, 100",
                  "Must be one of following: 500, 1000, 2000, 5000, 10000",
                  "Must be one of following: 2500, 5000, 10000",
                  "Must be one of following: 30/60, 50/100, 100/200, 250/500",
                  "Must be one of following: 25, 50, 100",
                  "Must be one of following: 30/900, 40/1200, 50/1500",
                  "Must be one of following: 1_100, 101_200, 201_500, 501_1000, 1001_1500, ..., 3501_4000",
                  "A or S or N", "Must be an integer", "A or B or C or N",
                  "100 or 250 or 500 or 1000", "VIN Number of Car", "Y or N",
                  "Pleasure or Remote 1 or Remote 2 or Commuting or Business or Farm",
                  "Y or N"]
    
    biLimitList = ["30/60", "50/100", "100/200", "250/500"]
    pdLimitList = [25,50,100]
    medLimitList = ["Not Bought", 500, 1000, 2000, 5000, 10000]
    pipLimitList = ["Not Bought", 2500, 5000, 10000]
    umuimLimitList = ["Not Bought", "30/60", "50/100", "100/200", "250/500"]
    umpdLimitList = ["Not Bought", 25, 50, 100]
    rentLimitList = ["Not Bought", "30/900", "40/1200", "50/1500"]
    acpeLimitList = ["Not Bought", "1_100", "101_200", "201_500", "501_1000", "1001_1500", "1501_2000", "2001_2500", "2501_3000", "3001_3500", "3501_4000"]
    fullCoverageList = ["A", "S", "N"]
    vehicleAgeList = list(range(0,40))
    vehiclePriorInsuranceClassList = ["A", "B", "C", "N"]
    vehDeductibleList = [100, 250, 500, 1000]
    roadsideAssistanceList = ["Y", "N"]
    
    vehicleDropdowns = [biLimitList, pdLimitList, medLimitList, pipLimitList, umuimLimitList, umpdLimitList, rentLimitList,
                        acpeLimitList, fullCoverageList, vehicleAgeList, vehiclePriorInsuranceClassList, 
                        vehDeductibleList, roadsideAssistanceList]
    
    
    vehicleLabel, variables, opt= [], [], []
    for x in range(len(vehicleFactors)):
        y=x+1
        newLabel = Label(newVehicleScreen, text=vehicleFactors[x])
        vehicleLabel.append(newLabel)
        vehicleLabel[x].grid(column=0,row=y)
        variable = StringVar(newVehicleScreen)
        variable.set(" ")
        variables.append(variable)
        
        
        newDrop = OptionMenu(newVehicleScreen, variables[x], *vehicleDropdowns[x])
        opt.append(newDrop)
        opt[x].config(width=5)
        opt[x].grid(column=1,row=y)
   
    y=y+1
    vinInput = Entry(newVehicleScreen, width=20)
    vinInput.grid(column=1,row=y)
    vinLabel = Label(newVehicleScreen, text="VIN")
    vinLabel.grid(column=0,row=y)
    y=y+1
    
    exitbutton1 = Button(newVehicleScreen, text="Submit Vehicle", command=submitVehicle)
    exitbutton1.grid(column=1,row=y)
    newVehicleScreen.mainloop()




def newPolicy():
    
    def submitPolicy():
        try:
            global collBought, compBought, loanBought, address, priorInsurance, paymentMethod
            global safe, accidentFree, eDelivery, nafCount, cmpCount, sr22Status, cancelMonths, withPreviousCarrier
            global ficoScore, homeowner
            collBought = variables[0].get()
            compBought = variables[1].get()
            loanBought = variables[2].get()
            address = addressInput.get()
            priorInsurance = variables[3].get()
            paymentMethod = variables[4].get()
            safe = variables[5].get()
            accidentFree = variables[6].get()
            eDelivery = variables[7].get()
            nafCount = variables[8].get()
            cmpCount = variables[9].get()
            sr22Status = variables[10].get()
            cancelMonths = variables[11].get()
            withPreviousCarrier = variables[12].get()
            ficoScore = variables[13].get()
            homeowner = variables[14].get()

                
            nafCount = int(nafCount)
            cmpCount = int(cmpCount)

            
            assert geography.checkAddressTX(address) == True
            
        except:
            yikesLabel = Label(newPolicyScreen, text = "INPUT ERROR: ADDRESS")
            z=y+1
            yikesLabel.grid(column=1,row=z)
        else:
            global newPolicyLabel
            newPolicyScreen.destroy()
            newPolicyLabel = Label(root, text="You have inputted a Policy")
            newPolicyLabel.grid(column=1,row=9)
            
            
            

    newPolicyScreen = Toplevel()
    newPolicyScreen.title("Add Policy Inputs")
    newPolicyScreen.geometry("550x500")
    
    parameters = ["True or False", "True or False", "True or False", "Full Address",
                  "A or B or C or N", "Pay_in_Full or Installments", "Yes or No",
                  "Y or N", "Y or N", "Must be an Integer", "Must be an Integer",
                  "Y or N", "0_11, 12_23, 24_35, 36_", "0_17, 18_35, 36_"]
    
    collBoughtList = ["True", "False"]
    compBoughtList = ["True", "False"]
    loanBoughtList = ["True", "False"]
    priorInsuranceList = ["A", "B", "C", "N"]
    paymentMethodList = ["Pay_in_Full", "Installments"]
    safeList = ["Yes", "No"]
    accidentFreeList = ["Y", "N"]
    eDeliveryList = ["Y", "N"]
    nafCountList = list(range(0,6))
    cmpCountList = list(range(0,6))
    sr22StatusList = ["Y", "N"]
    cancelMonthsList = ["0_11", "12_23", "24_35", "36_"]
    withPreviousCarrierList = ["0_11", "12_23", "24_35", "36_"]
    ficoList = ["516 and below", "517-533", "534-547", "548-557", "558-567", "568-575", "576-584", "585-591",
                "592-597", "598-604", "605-610", "611-616", "617-621", "622-626", "627-631", "632-636", "637-640",
                "641-645", "646-649", "650-653", "654-657", "658-660", "661-664", "665-667", "668-671", "672-675",
                "676-679", "680-683", "684-686", "687-690", "691-693", "694-697", "698-701", "702-704", "705-708",
                "709-712", "713-716", "717-720", "721-724", "725-729", "730-733", "734-737", "738-741", "742-745",
                "746-749", "750-753", "754-759", "760-764", "765-769", "770 and above", "No_hit", "No_score"]
    homeownerList = ["Yes", "No"]
    
    policyDropdowns = [collBoughtList, compBoughtList, loanBoughtList, priorInsuranceList,
                       paymentMethodList, safeList, accidentFreeList, eDeliveryList, nafCountList,
                       cmpCountList, sr22StatusList, cancelMonthsList, withPreviousCarrierList, ficoList, homeownerList]
    
    policyLabel, variables, opt = [], [], []
    for x in range(len(policyFactors)):
        y=x+1
        newLabel = Label(newPolicyScreen, text=policyFactors[x])
        policyLabel.append(newLabel)
        policyLabel[x].grid(column=0,row=y)
        variable = StringVar(newPolicyScreen)
        variable.set(" ")
        variables.append(variable)
        
        
        newDrop = OptionMenu(newPolicyScreen, variables[x], *policyDropdowns[x])
        opt.append(newDrop)
        opt[x].config(width=5)
        opt[x].grid(column=1,row=y)
    y=y+1
    addressInput = Entry(newPolicyScreen, width=20)
    addressInput.grid(column=1,row=y)
    addressLabel = Label(newPolicyScreen, text="Address")
    addressLabel.grid(column=0,row=y)
    y=y+1
    exitbutton1 = Button(newPolicyScreen, text = "Submit Policy", command = submitPolicy)
    exitbutton1.grid(column=1,row=y)
    newPolicyScreen.mainloop()
        














def getRate():
    global driverAge, driverGender, driverMaritalStatus, driverPoints, driverUBITier
    global biLimit, pdLimit, medLimit, pipLimit, umuimLimit, umpdLimit, rentLimit, acpeLimit
    global fullCoverage, vehicleAge, vehiclePriorInsuranceClass, vehDeductible
    global vin, automaticEmergencyBraking, vehicleUse, roadsideAssistance
    global collBought, compBought, loanBought, address, priorInsurance, paymentMethod
    global safe, accidentFree, eDelivery, nafCount, cmpCount, sr22Status, cancelMonths, withPreviousCarrier
    global numDrivers, numVehicles, ficoScore, homeowner
    
        #process driverage
    for x in range(len(driverAge)):
        if(driverAge[x] < 17):
            driverAge[x] = "16 or younger"
        elif(driverAge[x] > 90):
            driverAge[x] = "91 or older"
    
    #process vehicle age
    for x in range(len(vehicleAge)):
        if(vehicleAge[x] < 0):
            vehicleAge[x] = 0
        elif(vehicleAge[x] > 19):
            vehicleAge[x] = "20_"
            
            
    def getRateTable(x):
        rateTable = pd.read_csv(EMPTYRATEPATH)
        householdFactorTable = pd.read_csv(EMPTYHOUSEHOLDPATH)
        
        rateTable.set_index("Factor", inplace=True)
        householdFactorTable.set_index("Factor", inplace=True)
        
        Driver_Class_Factors = calculate.driverClassFactor(numDrivers, driverAge, driverGender, driverMaritalStatus, df_Driver_Class_Factors)
        Point_Factors = calculate.pointFactor(numDrivers, driverPoints, df_Violation_Point_Factors)
        UBI_Underwriting_Tier = calculate.UBITier(numDrivers, driverUBITier, df_UBI_Underwriting_Tier)
        
        #write factors to df
        householdFactorTable.loc["Driver_Class_Factors"] = Driver_Class_Factors
        householdFactorTable.loc["Point_Factors"] = Point_Factors
        householdFactorTable.loc["UBI_Underwriting_Tier"] = UBI_Underwriting_Tier
        Developed_Household_Risk_Factor = pd.DataFrame.product(householdFactorTable)
        rateTable.loc["Developed_Household_Risk_Factor"] = Developed_Household_Risk_Factor
        
        #--------------------------------------------------------------------
        Base_Rate = calculate.baseRate(df_Base_Rates_for_Coverages)
        rateTable.loc["Base_Rate"] = Base_Rate
        
        #Household Structure Calculation
        Household_Structure = calculate.householdStructure(numDrivers, numVehicles, df_Household_Factors_by_Coverages)
        rateTable.loc["Household_Structure"] = Household_Structure
        
        #Limit Factor Calculation
        coverageLimits = [biLimit[x], pdLimit[x], medLimit[x], pipLimit[x], umuimLimit[x], umpdLimit[x], rentLimit[x], acpeLimit[x]]
        Limit_Factor = calculate.limitFactor(coverageLimits, df_Limit_Factors_for_Coverages)
        rateTable.loc["Limit_Factor"] = Limit_Factor
        
        #Full Coverage Factor Calculation
        Full_Coverage_Factor = calculate.fullCoverage(fullCoverage[x], df_Full_Coverage_Factor)
        rateTable.loc["Full_Coverage_Factor"] = Full_Coverage_Factor
        
        #Vehicle Garaging Location Factor Calculation
        Vehicle_Garaging_Location_Factor = calculate.vehicleGaraging(address, df_Zip_to_Territory,
                                                                     df_Zip_Territory_Factors)
        rateTable.loc["Vehicle_Garaging_Location_Factor"] = Vehicle_Garaging_Location_Factor
        
        #Calculates Vehicle Age Factor
        Vehicle_Age = calculate.vehicleAgeFactor(vehicleAge[x], vehiclePriorInsuranceClass[x], df_Vehicle_Age_Factors)
        rateTable.loc["Vehicle_Age"] = Vehicle_Age
        
        #Calculates Deductible by Vehicle Age Factor
        Deductible_by_Vehicle_Age = calculate.vehicleAgeDeductible(vehicleAge[x], vehDeductible[x], df_Deductible_By_Vehicle_Age_Facto)
        rateTable.loc["Deductible_by_Vehicle_Age"] = Deductible_by_Vehicle_Age
        
        #Calculates the VIN Factor
        VIN_Vehicle_Factor, luxury = calculate.vinFactor(vin[x], df_VIN_Factor)
        rateTable.loc["VIN_Vehicle_Factor"] = VIN_Vehicle_Factor
        
        #Calculates the average vehicle age factor
        vehicleAgedf = pd.DataFrame()
        for x in range(numVehicles):
            indVehAgeFactor = calculate.avgVehicleAgeFactor(vehicleAge[x], vehiclePriorInsuranceClass[x], df_Vehicle_Age_Factors)
            #indVehAgeFactor = pd.Series.to_frame(indVehAgeFactor)
            vehicleAgedf = vehicleAgedf.append(indVehAgeFactor, ignore_index=True, sort=False)
        #end loop
        Average_Vehicle_Age = vehicleAgedf.mean()
        rateTable.loc["Average_Vehicle_Age"] = Average_Vehicle_Age
        
        #Calculates the average VIN factor
        vindf = pd.DataFrame()
        for x in range(numVehicles):
            indVINFactor = calculate.avgVIN(vin[x], df_VIN_Factor)
            vindf = vindf.append(indVINFactor, ignore_index=True, sort=False)
        #end loop
        Average_VIN_Vehicle_Factor = vindf.mean()
        rateTable.loc["Average_VIN_Vehicle_Factor"] = Average_VIN_Vehicle_Factor
        
        pniAge = driverAge[0]
        Luxury_Factor = calculate.luxuryFactor(luxury, pniAge, numVehicles, df_Luxury_Status)
        rateTable.loc["Luxury"] = Luxury_Factor
        
        #Calculates the prior insurance factor
        Prior_Insurance = calculate.priorInsurance(priorInsurance, df_Prior_Insurance_Factor)
        rateTable.loc["Prior_Insurance"] = Prior_Insurance
        
        #Calculates the cancel months factor
        Cancellation_Months = calculate.cancelFactor(cancelMonths, df_Cancel_Months_Factor)
        rateTable.loc["Cancellation_Months"] = Cancellation_Months
        
        #Calculates the previous carrier factor
        With_Previous_Carrier = calculate.previousCarrierFactor(withPreviousCarrier, df_With_Previous_Carrier_Factor)
        rateTable.loc["With_Previous_Carrier"] = With_Previous_Carrier
            
        #Calculates paid in full discount
        Paid_In_Full_Discount = calculate.paymentDiscount(paymentMethod, df_Paid_in_Full_Discount)
        rateTable.loc["Paid_In_Full_Discount"] = Paid_In_Full_Discount
        
        #Calculates safe driver discount
        Three_Year_Safe_Driver_Discount = calculate.safeDriverDiscount(safe, df_Safe_Driver_Discount)
        rateTable.loc["3_Year_Safe_Driver_Discount"] = Three_Year_Safe_Driver_Discount
        
        #Calculates 5 year accident free discount
        Five_Year_Accident_Free_Discount = calculate.accidentFreeDiscount(accidentFree, df_Accident_Free_Discount)
        rateTable.loc["5_Year_Accident_Free_Discount"] = Five_Year_Accident_Free_Discount
        
        #Evaluate collbought, compbought, and loanbought
        
        
        
        #Calculates e delivery discount
        EDelivery_Discount = calculate.eDelivery(eDelivery, df_E_Delivery_Discount)
        rateTable.loc["E-Delivery_Discount"] = EDelivery_Discount
        
        #Calculates the NAF Count
        NAF_Count = calculate.nafFactor(nafCount, df_Paid_Not_At_Fault_Count_Factor)
        rateTable.loc["NAF_Count"] = NAF_Count
        
        #Calculates CMP factor
        CMP_Count = calculate.cmpFactor(cmpCount, df_Paid_CMP_Count_Comprehensive)
        rateTable.loc["CMP_Count"] = CMP_Count
        
        #calculates sr22 penalty
        SR22_Penalty = calculate.sr22Penalty(sr22Status, df_SR22_Status)
        rateTable.loc["SR-22"] = SR22_Penalty
        
        #calculates credit score penalty
        Financial_Responsibility_Tier = calculate.creditFactor(ficoScore, df_FICO_Score, df_Financial_Responsibility_Tier)
        rateTable.loc["Financial_Responsibility_Tier"] = Financial_Responsibility_Tier
        
        #calculates homeowner tier
        Homeowner_Factor = calculate.homeownerFactor(homeowner, df_Homeowner_Factor)
        rateTable.loc["Homeowner"] = Homeowner_Factor
        
        if(collBought == "False"):
            rateTable = rateTable.drop(columns=["COLL"])
            
        if(compBought == "False"):
            rateTable = rateTable.drop(columns=["COMP"])
            
        if(loanBought == "False"):
            rateTable = rateTable.drop(columns=["LOAN"])
        
        return rateTable
    #returns a series of the total cost of each coverage
    def getCoverageCosts(rateTable):
        #calculates the premium series
        premiumS = pd.DataFrame.product(rateTable)
        
        return premiumS
    #returns a single number, the total premium
    def getPremiums(rateTable):
        #calculates the premium series
        premiumS = getCoverageCosts(rateTable)
        
        #adds all coverages for total premium
        premium = pd.Series.sum(premiumS)
        
        for x in range(numVehicles):
            if(roadsideAssistance[x] == "Y"):
                premium = premium + 8


        return premium

    def getPremium(premiums):
        return sum(premiums)
    global rateTable
    rateTable = [pd.DataFrame]
    for x in range(numVehicles):
        rateTable[x] = getRateTable(x)
        
        
    premiumSer = [pd.Series]
    for x in range(numVehicles):
        y = getCoverageCosts(rateTable[x])
        premiumSer[x] = y
    
    premiums = [0]
    for x in range(numVehicles):
        premiums[x] = getPremiums(rateTable[x])
        
    premium = getPremium(premiums)
    premium = round(premium, 2)
    
    premiumLabelText = "6 Month Premium is: $" + str(premium)
    premiumLabel = Label(root, text = premiumLabelText)
    premiumLabel.grid(column=1,row=15)


def resetInputs():
    global numDrivers, numVehicles, numPolicies
    global driverAge, driverGender, driverMaritalStatus, driverPoints, driverUBITier
    global biLimit, pdLimit, medLimit, pipLimit, umuimLimit, umpdLimit, rentLimit, acpeLimit
    global fullCoverage, vehicleAge, vehiclePriorInsuranceClass, vehDeductible, vin
    global automaticEmergencyBraking, vehicleUse, roadsideAssistance 
    global collBought, compBought, loanBought, address, priorInsurance, paymentMethod, safe
    global accidentFree, eDelivery, nafCount, cmpCount, sr22Status, cancelMonths, withPreviousCarrier
    
    
    
    
    
    
    numDrivers, numVehicles, numPolicies = 0,0,0
    driverAge, driverGender, driverMaritalStatus, driverPoints, driverUBITier = [], [], [], [], []
    biLimit, pdLimit, medLimit, pipLimit, umuimLimit, umpdLimit, rentLimit, acpeLimit = [], [], [], [], [], [] ,[], []
    fullCoverage, vehicleAge, vehiclePriorInsuranceClass, vehDeductible, vin = [], [], [], [], []
    automaticEmergencyBraking, vehicleUse, roadsideAssistance = [], [], []
    collBought, compBought, loanBought, address, priorInsurance, paymentMethod, safe = 0,0,0,0,0,0,0
    accidentFree, eDelivery, nafCount, cmpCount, sr22Status, cancelMonths, withPreviousCarrier = 0,0,0,0,0,0,0
    ficoScore, homeowner = 0,0
    
    numDriversLabel.destroy()
    numVehiclesLabel.destroy()
    newPolicyLabel.destroy()
        



#MAINSCREEN FUNCTIONS


def mainScreen():
    driverButton = Button(root, text = "Add New Driver", command=newDriver)
    driverButton.grid(column=1, row=3)
    vehicleButton = Button(root, text = "Add New Vehicle", command=newVehicle)
    vehicleButton.grid(column=1,row=4)
    policyButton = Button(root, text = "Add New Policy", command=newPolicy)
    policyButton.grid(column=1,row=5)
    resetButton = Button(root, text="Reset Inputs", command=resetInputs)
    resetButton.grid(column=1,row=10)
    calculateButton = Button(root, text = "Calculate Rate", command=getRate)
    calculateButton.grid(column=1,row=11)

#MAINSCREEN
titleText = Label(root, text="Root Rating Engine")
titleText.grid(column=1,row=0)


mainScreen()



root.mainloop()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    