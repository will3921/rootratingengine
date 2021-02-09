import pandas as pd
import geography




#calculates driver class factor
def driverClassFactor(NUMDRIVERS, DRIVERAGE, DRIVERGENDER, DRIVERMARITALSTATUS, df):
    householdoverall = pd.DataFrame()
    
    for x in range(NUMDRIVERS):
        inddriverclassfactor = df[(df.Driver_Age == DRIVERAGE[x]) & (df.Gender == DRIVERGENDER[x]) & (df.Marital_Status == DRIVERMARITALSTATUS[x])]
        householdoverall = householdoverall.append(inddriverclassfactor, ignore_index=True, sort=False)
        
    driverClassFactor = householdoverall.mean()

    return driverClassFactor


#calculates the driver point factor
def pointFactor(NUMDRIVERS, DRIVERPOINTS, df):
    householdoverall = pd.DataFrame()
    
    for x in range(NUMDRIVERS):
        indPoints = df[(df.Points == DRIVERPOINTS[x])]
        householdoverall = householdoverall.append(indPoints, ignore_index=True, sort=False)
    
    pointFactor = householdoverall.mean()
    
    return pointFactor


#calculates the UBI tiers (telematics?)
def UBITier(NUMDRIVERS, DRIVERUBITIERS, df):
    householdoverall = pd.DataFrame()
    
    for x in range(NUMDRIVERS):
        indUBI = df[(df.TIER == DRIVERUBITIERS[x])]
        householdoverall = householdoverall.append(indUBI, ignore_index=True, sort=False)
        
    UBIFactor = householdoverall.mean()
    
    return UBIFactor


#calculates the Base Rate
def baseRate(df):
    baseRate = df.iloc[0]
    return baseRate

#calculates the household structure factor
def householdStructure(NUMDRIVERS, NUMVEHICLES, df):
    if (NUMVEHICLES > 3):
        numVehicles = 4
    else:
        numVehicles = NUMVEHICLES
        
    adjNumDrivers = NUMDRIVERS + 1
    adjNumVehicles = numVehicles - 1
    
    #BI
    BIdf = df[(df.iloc[:,0] == "BI")]
    BI = BIdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #PD
    PDdf = df[(df.iloc[:,0] == "PD")]
    PD = PDdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #COLL
    COLLdf = df[(df.iloc[:,0] == "COLL")]
    COLL = COLLdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #COMP
    COMPdf = df[(df.iloc[:,0] == "COMP")]
    COMP = COMPdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #MEDPAY
    MEDPAYdf = df[(df.iloc[:,0] == "MEDPAY")]
    MEDPAY = MEDPAYdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #PIP
    PIPdf = df[(df.iloc[:,0] == "PIP")]
    PIP = PIPdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #UM/UIM
    UMUIMdf = df[(df.iloc[:,0] == "UMUIM")]
    UMUIM = UMUIMdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #UMPD
    UMPDdf = df[(df.iloc[:,0] == "UMPD")]
    UMPD = UMPDdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #RENT
    RENTdf = df[(df.iloc[:,0] == "RENT")]
    RENT = RENTdf.iloc[adjNumVehicles, adjNumDrivers]
    
    #LOAN
    LOANdf = df[(df.iloc[:,0] == "LOAN")]
    LOAN = LOANdf.iloc[adjNumVehicles, adjNumDrivers]
    
    
    #convert to pandas
    listCoverages = ["BI", "PD", "COLL", "COMP", "MEDPAY", "PIP", "UMUIM", "UMPD", "RENT", "LOAN"]
    listValues = [BI, PD, COLL, COMP, MEDPAY, PIP, UMUIM, UMPD, RENT, LOAN]
    listValues = pd.to_numeric(listValues)
    householdStructureFactor = pd.DataFrame(listValues, index=listCoverages)
    householdStructureFactor = householdStructureFactor.iloc[:,0]
    
    
    return householdStructureFactor


#calculates the limit factor
def limitFactor(limitfactors, df):
    
    #BI
    BIdf = df[(df.Coverage == "BI") & (df.Limit == limitfactors[0])]
    BI = BIdf.iloc[0,2]
    BI = float(BI)
    
    #PD
    PDdf = df[(df.Coverage == "PD") & (df.Limit == limitfactors[1])]
    PD = PDdf.iloc[0,2]
    PD = float(PD)
    
    #MEDPAY
    if (limitfactors[2] == "Not Bought"):
        MEDPAY = 0
    else:
        MEDPAYdf = df[(df.Coverage == "MEDPAY") & (df.Limit == limitfactors[2])]
        MEDPAY = MEDPAYdf.iloc[0,2]
        MEDPAY = float(MEDPAY)
    
    #PIP
    if (limitfactors[3] == "Not Bought"):
        PIP = 0
    else:     
        PIPdf = df[(df.Coverage == "PIP") & (df.Limit == limitfactors[3])]
        PIP = PIPdf.iloc[0,2]
        PIP = float(PIP)
    
    #UMUIM
    if (limitfactors[4] == "Not Bought"):
        UMUIM = 0
    else:
        UMUIMdf = df[(df.Coverage == "UMUIM") & (df.Limit == limitfactors[4])]
        UMUIM = UMUIMdf.iloc[0,2]
        UMUIM = float(UMUIM)
    
    #UMPD
    if (limitfactors[5] == "Not Bought"):
        UMPD = 0
    else:
        UMPDdf = df[(df.Coverage == "UMPD") & (df.Limit == limitfactors[5])]
        UMPD = UMPDdf.iloc[0,2]
        UMPD = float(UMPD)
    
    #RENT
    if (limitfactors[6] == "Not Bought"):
        RENT = 0
    else:
        RENTdf = df[(df.Coverage == "RENT") & (df.Limit == limitfactors[6])]
        RENT = RENTdf.iloc[0,2]
        RENT = float(RENT)
    
    #ACPE
    if (limitfactors[7] == "Not Bought"):
        ACPE = 0
    else:
        ACPEdf = df[(df.Coverage == "ACPE") & (df.Limit == limitfactors[7])]
        ACPE = ACPEdf.iloc[0,2]
        ACPE = float(ACPE)
    
    #convert to series
    listCoverages = ["BI", "PD", "MEDPAY", "PIP", "UMUIM", "UMPD", "RENT", "ACPE"]
    listValues = [BI, PD, MEDPAY, PIP, UMUIM, UMPD, RENT, ACPE]
    listValues = pd.to_numeric(listValues)
    limfactor = pd.DataFrame(listValues, index = listCoverages)
    limfactor = limfactor.iloc[:,0]


    return limfactor

#calculates full coverage factor
def fullCoverage(FULLCOVERAGE, df):
    coverageFactor = df[(df.Full_Coverage == FULLCOVERAGE)]
    coverageFactor = coverageFactor.iloc[0]
    
    return coverageFactor

#calculates vehicle garaging location factor
def vehicleGaraging(ADDRESS, dfZ, dfT):
    coordinates = geography.toCoordinates(ADDRESS)    
    GARAGINGZIP = float(geography.toZIP(coordinates))
    df2 = dfZ[(dfZ.Garaging_ZIP_Code == GARAGINGZIP)]
    
    biFactor = df2.loc[:,"BI"]
    biFactor = int(biFactor.iloc[0])
    bidf2 = dfT[(dfT.Tier == biFactor)]
    biWeight = float(bidf2.loc[:,"BI"])
    
    
    pdFactor = df2.loc[:,"PD"]
    pdFactor = int(pdFactor.iloc[0])
    pddf2 = dfT[(dfT.Tier == pdFactor)]
    pdWeight = float(pddf2.loc[:,"PD"])
    
    medFactor = df2.loc[:,"MEDPAY"]
    medFactor = int(medFactor.iloc[0])
    meddf2 = dfT[(dfT.Tier == medFactor)]
    medWeight = float(meddf2.loc[:,"MEDPAY"])
    
    
    pipFactor = df2.loc[:,"PIP"]
    pipFactor = int(pipFactor.iloc[0])
    pipdf2 = dfT[(dfT.Tier == pipFactor)]
    pipWeight = float(pipdf2.loc[:,"PIP"])
    
    umuimFactor = df2.loc[:,"UMUIM"]
    umuimFactor = int(umuimFactor.iloc[0])
    umuimdf2 = dfT[(dfT.Tier == umuimFactor)]
    umuimWeight = float(umuimdf2.loc[:,"UMUIM"])
    
    umpdFactor = df2.loc[:,"UMPD"]
    umpdFactor = int(umpdFactor.iloc[0])
    umpddf2 = dfT[(dfT.Tier == umpdFactor)]
    umpdWeight = float(umpddf2.loc[:,"UMPD"])
    
    collFactor = df2.loc[:,"COLL"]
    collFactor = int(collFactor.iloc[0])
    colldf2 = dfT[(dfT.Tier == collFactor)]
    collWeight = float(colldf2.loc[:,"COLL"])
    
    compFactor = df2.loc[:,"COMP"]
    compFactor = int(compFactor.iloc[0])
    compdf2 = dfT[(dfT.Tier == compFactor)]
    compWeight = float(compdf2.loc[:,"COMP"])
    
    loanFactor = df2.loc[:,"LOAN"]
    loanFactor = int(loanFactor.iloc[0])
    loandf2 = dfT[(dfT.Tier == loanFactor)]
    loanWeight = float(loandf2.loc[:,"LOAN"])
    
    listLabels = ["BI", "PD", "MEDPAY", "PIP", "UMUIM", "UMPD", "COLL", "COMP", "LOAN"]
    listValues = [biWeight, pdWeight, medWeight, pipWeight, umuimWeight, umpdWeight, collWeight, compWeight, loanWeight]
    listValues = pd.to_numeric(listValues)
    zipFactor = pd.DataFrame(listValues, index = listLabels)
    zipFactor = zipFactor.iloc[:,0]
    return zipFactor

#calculates the vehicle age factor
def vehicleAgeFactor(VEHICLEAGE, VEHICLEPRIORINSURANCECLASS, df):
    vehInsClass = VEHICLEPRIORINSURANCECLASS
    if(vehInsClass == "A"):
        df2 = df.filter(["Coverage", "Veh_Age", "Prior Insurance Class = A"])
    elif (vehInsClass == "B"):
        df2 = df.filter(["Coverage", "Veh_Age", "Prior Insurance Class = B"])
    elif (vehInsClass == "C"):
        df2 = df.filter(["Coverage", "Veh_Age", "Prior Insurance Class = C"])
    elif (vehInsClass == "N"):
        df2 = df.filter(["Coverage", "Veh_Age", "Prior Insurance Class = N"])
    #end for loop
    vehAgeFactor = df2[(df2.Veh_Age == VEHICLEAGE)]
    vehAgeFactor = vehAgeFactor.set_index("Coverage")
    vehAgeFactor = vehAgeFactor.iloc[:,1]
    
    vehAgeFactor["UMUIM"] = float("NaN")
    vehAgeFactor["UMPD"] = float("NaN")
    
    return vehAgeFactor

#calculates the vehicle age factor for COLL and COMP coverage
def vehicleAgeDeductible(VEHICLEAGE, VEHDEDUCTNUM, df):

    if(VEHDEDUCTNUM == 100):
        df2 = df.filter(["Coverage", "Vehicle_Age", 100])
    elif (VEHDEDUCTNUM == 250):
        df2 = df.filter(["Coverage", "Vehicle_Age", 250])
    elif (VEHDEDUCTNUM == 500):
        df2 = df.filter(["Coverage", "Vehicle_Age", 500])
    elif (VEHDEDUCTNUM == 1000):
        df2 = df.filter(["Coverage", "Vehicle_Age", 1000])
    #end for loop
    vehAgeDeduct = df2[(df2.Vehicle_Age == VEHICLEAGE)]
    vehAgeDeduct = vehAgeDeduct.set_index("Coverage")
    vehAgeDeduct = vehAgeDeduct.iloc[:,1]
    
    return vehAgeDeduct

#Calculates the VIN Factor
def vinFactor(VIN, df):
    vin = VIN[:8] + "&" + VIN[9]
    df2 = df[(df.Vi == vin)]
    
    if (len(df2) == 1):
        df2 = df2.iloc[0]
        df2["UMUIM"] = float("NaN")
        df2["UMPD"] = float("NaN")
        luxury = df2.iloc[10]
        return df2, luxury
    else:
        return False, False
    #end if

   
#Calculates the average age factor    
def avgVehicleAgeFactor(VEHICLEAGE, VEHICLEPRIORINSURANCECLASS, df):
    vehInsClass = VEHICLEPRIORINSURANCECLASS
    if(vehInsClass == "A"):
        df2 = df.filter(["Coverage", "Veh_Age", "Prior Insurance Class = A"])
    elif (vehInsClass == "B"):
        df2 = df.filter(["Coverage", "Veh_Age", "Prior Insurance Class = B"])
    elif (vehInsClass == "C"):
        df2 = df.filter(["Coverage", "Veh_Age", "Prior Insurance Class = C"])
    elif (vehInsClass == "N"):
        df2 = df.filter(["Coverage", "Veh_Age", "Prior Insurance Class = N"])
    #end for loop
    vehAgeFactor = df2[(df2.Veh_Age == VEHICLEAGE)]
    vehAgeFactor = vehAgeFactor.set_index("Coverage")
    vehAgeFactor = vehAgeFactor.iloc[:,1]
    vehAgeFactor["BI"] = float("NaN")
    vehAgeFactor["PD"] = float("NaN")
    vehAgeFactor["MEDPAY"] = float("NaN")
    vehAgeFactor["PIP"] = float("NaN")
    vehAgeFactor["RENT"] = float("NaN")
    vehAgeFactor["LOAN"] = float("NaN")
    
    return vehAgeFactor


#calculates the average VIN factor
def avgVIN(VIN, df):
    vin = VIN
    vin = vin[:8] + "&" + vin[9]
    df2 = df[(df.Vi == vin)]
    
    if (len(df2) == 1):
        df2 = df2.iloc[0]
        df2["BI"] = float("NaN")
        df2["PD"] = float("NaN")
        df2["MEDPAY"] = float("NaN")
        df2["PIP"] = float("NaN")
        df2["COLL"] = float("NaN")
        df2["COMP"] = float("NaN")
        df2["LOAN"] = float("NaN")
        return df2
    else:
        return False
    #end if
    
#calculates luxury vehicle factor
def luxuryFactor(luxury, pniAge, numVehicles, df):
    if(numVehicles > 1):
        numVehicles = "2...9"
    
    df2 = df[(df.Luxury_Status_Indicator == luxury) & (df.Number_of_Vehicles == numVehicles)
             & (df.PNI_Age == pniAge)]
    return df2.iloc[0]
        

#calculates prior insurance factor
def priorInsurance(PRIORINSURANCE, df):
    df2 = df[(df.Prior_Insurance_Coverage == PRIORINSURANCE)]
    priorInsuranceFactor = df2.iloc[0]
    return priorInsuranceFactor


#calculates cancellation months factor
def cancelFactor(cancelMonths, df):
    df2 = df[(df.Months == cancelMonths)]
    cancelMonthsFactor = df2.iloc[0]
    return cancelMonthsFactor
    
#Calculates previous carrier factor
def previousCarrierFactor(previousCarrier, df):
    df2 = df[(df.Months == previousCarrier)]
    previousCarrierFactor = df2.iloc[0]
    return previousCarrierFactor
    
#Calculates payment discount
def paymentDiscount(PAYMENTMETHOD, df):
    df2 = df[(df.Payment_Method == PAYMENTMETHOD)]
    paymentDiscountFactor = df2.iloc[0]
    return paymentDiscountFactor

#Calculates safe driver discount
def safeDriverDiscount(SAFE, df):
    df2 = df[(df.Safe == SAFE)]
    safeDiscount = df2.iloc[0]
    return safeDiscount

#calculates 5 year accident free discount
def accidentFreeDiscount(ACCIDENTFREE, df):
    df2 = df[(df.Accident_Free == ACCIDENTFREE)]
    accidentDiscount = df2.iloc[0]
    return accidentDiscount

#calculates edelivery discount
def eDelivery(EDELIVERY, df):
    df2 = df[(df.e_delivery == EDELIVERY)]
    eDeliveryDiscount = df2.iloc[0]
    return eDeliveryDiscount


#calculates not at fault count
def nafFactor(NAFCOUNT, df):
    df2 = df[(df.NAF_Count == NAFCOUNT)]
    nafRate = df2.iloc[0]
    return nafRate


#calculates cmp factor
def cmpFactor(CMPCOUNT, df):
    df2 = df[(df.CMP == CMPCOUNT)]
    cmpRate = df2.iloc[0]
    return cmpRate

def sr22Penalty(SR22STATUS, df):
    df2 = df[(df.sr22 == SR22STATUS)]
    sr22Factor = df2.iloc[0]
    return sr22Factor


def creditFactor(ficoScore, dfFico, dfTier):
    df2 = dfFico[(dfFico.FICO_Score == ficoScore)]
    tier = df2.iloc[0,1]
    df3 = dfTier[(dfTier.Financial_Responsibility_Tier == tier)]
    factor = df3.iloc[0]
    return factor

def homeownerFactor(homeowner, df):
    df2 = df[(df.Homeowner == homeowner)]
    df2 = df2.iloc[0]
    return df2
    
    
    
    






















