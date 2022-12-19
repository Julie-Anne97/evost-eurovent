import pandas as pd
import streamlit as st
from PIL import Image
from math import exp

pd.set_option('display.max_columns', None)

logo = Image.open("EVOST logo.png")



with st.sidebar:    
    st.image(logo)
    st.container()
    st.radio("Model", (800, 1150, 1250, 1400, 2600), disabled=True,index=2)
    st.radio("Type : ", ("Horizontal","Vertical"), disabled=True)
    st.radio("Nozzle : ", ("E1","E1.1"), disabled=True)
    option = st.radio(
    "Select option",
    ('Option 1 : Outlet Water Temperature', 'Option 2 : Water flow'))




st.title('Software Eurovent')

    
    
#STEP 1: choose one airflow from the table, then define the water temperatures (= enter qa & twin)
        
st.subheader('Select inputs')

col1,col2,col3 = st.columns(3)
with col1:
    qa = st.number_input('Primary air flow rate (l/s)')
 
    
c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.markdown('**Cooling inputs**')
    troom_cooling = st.number_input('Reference Air Remperature (°C)',value=26)
    tgr_cooling = st.number_input('Room Temperature Gradient (k/m)', value=0)
    dtra_cooling = st.number_input('Primary Air Temperature (°C)',value=10)
    twin_cooling = st.number_input('Inlet Water Temperature (°C)',value=15.81)
    if option == 'Option 1 : Outlet Water Temperature':
        twout_cooling = st.number_input('Outlet Water Temperature (°C)',value=17.64)
    else:
        qw_cooling = st.number_input('Water flow rate')
       
with c2:
    st.write('')
with c3:
    st.markdown('**Heating inputs**')
    troom_heating = st.number_input('Reference Air Remperature  (°C)',value=26)
    tgr_heating = st.number_input('Room Temperature Gradient (k/m)  ', value=0)
    dtra_heating = st.number_input('Primary Air Temperature  (°C)',value=10)
    twin_heating = st.number_input('Inlet Water Temperature  (°C)',value=15.81)
    if option == 'Option 1 : Outlet Water Temperature':
        twout_heating = st.number_input('Outlet Water Temperature (°C)  ',value=17.64)
    else:
        qw_heating = st.number_input('Water flow rate  ')
with c4:
    st.write('')
with c5:
    st.write("")

        
if option == 'Option 1 : Outlet Water Temperature':   
    
    ## COOLING INPUTS 
     
    #STEP 2: calculate Dtw and Dtrw
    dtw_cooling = twout_cooling-twin_cooling
    dtrw_cooling = troom_cooling - ((twin_cooling+twout_cooling)/2)
    
    #STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
    # PLTtest = Pwtest / dtrwtest
    w = 27.67206 * qa + 161.73041
    
    PLTtest_cooling = w / dtrw_cooling
    
    #STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
    #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
    eqw_ref = 1.06
    
    pw1_cooling = (PLTtest_cooling*dtrw_cooling)/eqw_ref
    
    #STEP 5: calculate the correspondet water flow, using the Dtw calculated
    # st.markdown("**STEP 5: calculate waterflow**")
    qw1_cooling = pw1_cooling / (dtrw_cooling*4200)
    
    stop = 0.01
    
    def epsilon(x):
        eqw = 0,588878-(1.955)*x+(3140.21)*x**2-(125288)*x**3+exp(2.43832)+6*x^4-exp(2.57437)+(7*x)**5+exp(1.416)+(8*x)**6-exp(3.18428)+(8*x)**7
        return eqw
    
    #STEP 6: check the correction factor correspondent to qw from the graph		
    
    #STEP 7: calculate the new power Pw2
    if qw1_cooling > 0.08:
        eqw1_cooling = 1.06
    else:
        eqw1_cooling = 2*qw1_cooling+0.5 #formule à définir pour l'itération 
        ## IMPORTANT 
    pw2_cooling = pw1_cooling * eqw1_cooling
    
    #STEP 8: calculate the correspondet water flow, using the Dtw calculated and Pw2
    qw2_cooling = pw2_cooling / (dtw_cooling*4200)
    
    #STEP 9: check the correction factor correspondent to qw from the graph							
    
    #STEP 10: calculate the new power Pw3							
    if qw2_cooling > 0.08:
        eqw2_cooling = 1.06
    else:
        eqw2_cooling = 2*qw2_cooling+0.5 #formule à définir pour l'itération 
    pw3_cooling = pw2_cooling * eqw2_cooling
    # pw3 = round(pw3,2)
    
    # STEP 11: calculate the correspondet water flow, using the Dtw calculated and Pw3
    qw3_cooling = pw3_cooling/ (dtw_cooling*4200)
    
    ## IMPORTANT faire une boucle while pour continuer l'itération tant que l'écart entre qwn et qwn-1 est > 0.01
    
    
    pa_cooling = 1.2*qa*(troom_cooling+tgr_cooling+(dtrw_cooling/2))
    pma_cooling = 35.06543*qa-186.32415
    
    
    ## HEATING INPUTS
    
    #STEP 2: calculate Dtw and Dtrw
    dtra_heating = twout_heating-twin_heating
    dtrw_heating = troom_heating - ((twin_heating+twout_heating)/2)
    
    
    #STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
    # PLTtest = Pwtest / dtrwtest
    w_heating = 27.67206 * qa + 161.73041
    PLTtest_heating = w / dtrw_heating
    
    #STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
    #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
    eqw_ref = 1.06
    pw1_heating = (PLTtest_heating*dtrw_heating)/eqw_ref
    
    #STEP 5: calculate the correspondet water flow, using the Dtw calculated
    qw1_heating = pw1_heating / (dtrw_heating*4200)
    
    stop = 0.01
    
    def epsilon(x):
        eqw = 0,588878-(1.955)*x+(3140.21)*x**2-(125288)*x**3+exp(2.43832)+6*x^4-exp(2.57437)+(7*x)**5+exp(1.416)+(8*x)**6-exp(3.18428)+(8*x)**7
        return eqw
    
    #STEP 6: check the correction factor correspondent to qw from the graph		
    
    #STEP 7: calculate the new power Pw2
    if qw1_heating > 0.08:
        eqw1_heating = 1.06
    else:
        eqw1_heating = 2*qw1_heating+0.5 #formule à définir pour l'itération 
        ## IMPORTANT 
    pw2_heating = pw1_heating * eqw1_heating	
    
    #STEP 8: calculate the correspondet water flow, using the Dtw calculated and Pw2
    qw2_heating = pw2_heating / (dtrw_heating*4200)
    
    #STEP 9: check the correction factor correspondent to qw from the graph							
    
    #STEP 10: calculate the new power Pw3							
    
    if qw2_heating > 0.08:
        eqw2_heating = 1.06
    else:
        eqw2_heating = 2*qw2_heating+0.5 #formule à définir pour l'itération 
        ## IMPORTANT 
    pw3_heating = pw2_heating * eqw2_heating
    
    # STEP 11: calculate the correspondet water flow, using the Dtw calculated and Pw3
    # qw3_heating = pw3_heating (dtrw_heating*4200)
    
    ## IMPORTANT faire une boucle while pour continuer l'itération tant que l'écart entre qwn et qwn-1 est > 0.01
    
    pma = 1.2*qa*(troom_cooling+tgr_cooling+(dtrw_cooling/2))
    
    pa_heating = 1.2*qa*(troom_heating+tgr_heating+(dtrw_heating/2))
    pa_heating = round(pa_heating,2)
    
    float(qa)    
    troom_cooling = round(troom_cooling,2)
    troom_heating = round(troom_heating,2)
    twin_cooling = round(twin_cooling,2)
    twin_heating = round(twin_heating,2)
    twout_cooling = round(twout_heating,2)
    tgr_cooling = round(tgr_cooling,2)
    tgr_heating = round(tgr_heating,2)
    dtra_cooling = round(dtra_cooling,2)
    dtra_heating = round(dtra_heating,2)
    
    
    
    st.markdown('**Tableau récapitulatif**')


    option1 = [
        ['Total capacity','', '', '','',''],
        ['Water side capacity','pw','',pw3_cooling,'',pw3_cooling],
        ['Air side capacity', 'pma','',pma,'',pma],
        ['Reference air temperature','troom', troom_cooling,'',troom_heating,''],
        ['Gradient','',tgr_cooling,'',tgr_heating,''],
        ['Primary air temperature','dtra',dtra_cooling,'',dtra_heating,''],
        ['Inlet water temperature','twi',twin_cooling,'',twin_heating,''],
        ['Outlet water temperature','twout',twout_cooling,'',twin_heating,''],
        ['Diff out-in','dtw','','','',''],
        ['Water flow rate','qw','','','','']]

    df1 = pd.DataFrame(option1, columns =['',' ', 'Cooling inputs','Cooling outputs','Heating inputs','Heating outputs'])
    st.write(df1) 
    
    # submit button
    st.subheader("Add new values to table")
    
    results_option1 = pd.read_csv('results_option1.csv')
    # results_option1
    
    add_ref = results_option1["ref"].max()+1
    
    # d = pd.DataFrame([d],index=[0])
    # d
    #d.to_csv('results_option1.csv')
    
    clickSubmit = st.button('Save values')
    
    if clickSubmit == True: 
         newdata = {'ref' : add_ref,
              'Primary Air Flow Rate': qa, 
              'Primary Air Temperature': dtra,
              'Reference Air Remperature': troom,
              'Room Temperature Gradient': tgrvalue,
              'Inlet Water Temperature': twin,
              "dtw" : dtwvalue,
              "water flow rate" : qw3,
              "water side capacity" : pw3,
              "air side pressure" : pma}
         #st.write(newdata)
         results_option1 = results_option1.append(newdata,ignore_index=True)
         results_option1.to_csv('results_option1.csv',index=False)
         #results_option1 = pd.concat([results_option1,d])
         #open('results_option1.csv','a').write(results_option1.to_csv())
    else :
        st.markdown("Please submit to save")
    
    st.write(results_option1)

    
    
     
    
elif option == 'Option 2 : Water flow':
    
    #COOLING INPUTS
    
    #STEP 1: choose one airflow from the table, then define the waterflow
    st.markdown("**STEP 1: choose one airflow from the table, then define the waterflow**")
    
    st.subheader('Select inputs')
    
    
    
    #STEP 2: define the Dtrw for the calculation
    st.markdown("**STEP 2: define the Dtrw for the calculation**")
    st.write("tr - (dtw/2)")
    st.write("dtrw : ",dtrw) 
    
    #STEP 3: read the data from the table correspondent to the airflow selected 
    # and calculate the specific power PLT (W/K)
    
    st.markdown("**STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)**")							
    w = 27.67206 * qa + 161.73041
    PLTtest = w / dtrw
    st.write('PLT : ', PLTtest)
    
    #STEP 4: check the correction factor correspondent to qw from the graph
    st.markdown("**STEP 4: check the correction factor correspondent to qw from the graph**")
    st.write("water flow rate : ", qwvalue)
    st.write("Eqw = qwvalue * a + b  --> fonction à définir")

    
    #STEP 5: calculate the power (W) correspondent to waterflow desired, using the Dtrw chosen							
    st.markdown("**STEP 5: calculate the power (W) correspondent to waterflow desired, using the Dtrw chosen**")
    st.write("Pw1 = PLT * dtrw *(Eqw / 1,06)")
    st.write("pw1 = ",PLTtest," * ",dtrw,"(Eqw / 1,06)")
    
    
    d = {'ref' : 1,
        'Water flow' : qw_cooling,
              'Primary Air Flow Rate': qa, 
              'Primary Air Temperature': dtra_cooling,
              'Reference Air Remperature': troom_cooling,
              'Room Temperature Gradient': tgrvalue_cooling,
              "Specific power" : PLTtest}
    
    
    d = pd.DataFrame([d],index=[0])
    d
    d.to_csv('results_option2.csv')
    
    results_option2 = pd.read_csv('results_option2.csv')
    results_option2
    
    add_ref = results_option2["ref"].max()+1
    
    clickSubmit = st.button('Save values')
    
    if clickSubmit == True: 
         newdata = {'ref' : add_ref,
              'Primary Air Flow Rate': qa, 
              'Primary Air Temperature': dtra_cooling,
              'Reference Air Remperature': troom_cooling,
              'Room Temperature Gradient': tgr_cooling,
              'Inlet Water Temperature': twin_cooling,
              "dtw" : dtw_cooling,
              "water flow rate" : qw3,
              "water side capacity" : pw3,
              "air side pressure" : pma}
         st.write(newdata)
         results_option2 = results_option2.append(newdata,ignore_index=True)
         results_option2.to_csv('results_option2.csv',index=False)
         #results_option1 = pd.concat([results_option1,d])
         #open('results_option1.csv','a').write(results_option1.to_csv())
    else :
        st.markdown("Please submit to save")
    
    st.write(results_option2)
    
