import pandas as pd
import streamlit as st
from PIL import Image
from math import exp
from datetime import date

pd.set_option('display.max_columns', None)

today = date.today()

logo = Image.open("EVOST logo.png")



with st.sidebar:    
    st.image(logo)
    st.container()
    st.radio("Nozzle : ", ("E1","E1.1"), disabled=True)
    st.radio("Model", (800, 1150, 1250, 1400, 2600), disabled=True,index=2)
    st.radio("Tubes",(2,4),disabled=True,index=1)
    st.radio("Type : ", ("Horizontal","Vertical"), disabled=True)




st.title('Software Eurovent')

    
    
#STEP 1: choose one airflow from the table, then define the water temperatures (= enter qa & twin)

option = st.radio(
    "Select option",
    ('Option 1 : Outlet Water Temperature', 'Option 2 : Water flow'))

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
    
    def epsilon(x):
        eqw = 0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2.43832*(10**6)*(x**4)-2.57437*(10**7)*(x**5)+1.416*(10**8)*(x**6)-3.18428*(10**8)*(x**7)
        return eqw
    
    def dpw_cooling_formula(x) :
        dpw_c = 1.25-328.673*x+36889*(x**2)-1.601e+06*(x**3)+4.0005*(10**7)*(x**4)-5.50149*(10**8)*(x**5)+3.90377*(10**9)*(x**6)-1.11607*(10**10)*(x**7)
        return dpw_c
     
    #STEP 2: calculate Dtw and Dtrw
    dtw_cooling = twout_cooling-twin_cooling
    dtrw_cooling = troom_cooling - ((twin_cooling+twout_cooling)/2)
    
    #STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
    # PLTtest = Pwtest / dtrwtest
    w = 35.06543 * qa + 186.32415
    
    PLT_cooling = w / dtrw_cooling
    
    #STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
    #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
    eqw_ref = 1.06
    
    pw1_cooling = (PLT_cooling*dtrw_cooling)/eqw_ref
    
    #STEP 5: calculate the correspondet water flow, using the Dtw calculated
    # st.markdown("**STEP 5: calculate waterflow**")
    pw1_cooling = (PLT_cooling*dtrw_cooling)/eqw_ref
    qw1_cooling = pw1_cooling / (dtw_cooling*4200)
    
    pw2_cooling = pw1_cooling*epsilon(qw1_cooling)
    qw2_cooling = pw2_cooling / (dtw_cooling*4200)
    
    pw3_cooling = pw1_cooling*epsilon(qw2_cooling)
    qw3_cooling = pw3_cooling / (dtw_cooling*4200)
    
    pw4_cooling = pw1_cooling*epsilon(qw3_cooling)
    qw4_cooling = pw4_cooling / (dtw_cooling*4200)
    
    pw5_cooling = pw1_cooling*epsilon(qw4_cooling)
    qw5_cooling = pw5_cooling / (dtw_cooling*4200)
    
    #STEP 6: check the correction factor correspondent to qw from the graph		
    
    # #STEP 7: calculate the new power Pw2
    # if qw1_cooling > 0.08:
    #     eqw1_cooling = 1.06
    # else:
    #     eqw1_cooling = 2*qw1_cooling+0.5 #formule à définir pour l'itération 
    #     ## IMPORTANT 
    # pw2_cooling = pw1_cooling * eqw1_cooling
    
    # #STEP 8: calculate the correspondet water flow, using the Dtw calculated and Pw2
    # qw2_cooling = pw2_cooling / (dtw_cooling*4200)
    
    # #STEP 9: check the correction factor correspondent to qw from the graph							
    
    # #STEP 10: calculate the new power Pw3							
    # if qw2_cooling > 0.08:
    #     eqw2_cooling = 1.06
    # else:
    #     eqw2_cooling = 2*qw2_cooling+0.5 #formule à définir pour l'itération 
    # pw3_cooling = pw2_cooling * eqw2_cooling
    # # pw3 = round(pw3,2)
    
    # # STEP 11: calculate the correspondet water flow, using the Dtw calculated and Pw3
    # qw3_cooling = pw3_cooling/ (dtw_cooling*4200)
    
    ## IMPORTANT faire une boucle while pour continuer l'itération tant que l'écart entre qwn et qwn-1 est > 0.01
    
    
    pa_cooling = 1.2*qa*(troom_cooling+tgr_cooling+(dtrw_cooling/2))
    pma_cooling = 35.06543*qa-186.32415
    
    
    ## HEATING INPUTS
    
    #STEP 2: calculate Dtw and Dtrw
    dtw_heating = twout_heating -twin_heating
    dtrw_heating = troom_heating - ((twin_heating +twout_heating)/2)
    
    
    #STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
    # PLTtest = Pwtest / dtrwtest
    w = 35.06543 * qa + 186.32415
    PLT_heating = w / dtrw_heating
    
    #STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
    #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
    eqw_ref = 1.06
    pw1_heating = (PLT_heating*dtrw_heating)/eqw_ref
    
    #STEP 5: calculate the correspondet water flow, using the Dtw calculated
    pw1_heating = (PLT_heating*dtrw_heating)/eqw_ref
    qw1_heating = pw1_heating / (dtw_heating*4200)
    
    pw2_heating = pw1_heating*epsilon(qw1_heating)
    qw2_heating = pw2_heating / (dtw_heating*4200)
    
    pw3_heating = pw1_heating*epsilon(qw2_heating)
    qw3_heating = pw3_heating / (dtw_heating*4200)
    
    pw4_heating = pw1_heating*epsilon(qw3_heating)
    qw4_heating = pw4_heating / (dtw_heating*4200)
    
    pw5_heating = pw1_heating*epsilon(qw4_heating)
    qw5_heating = pw5_heating / (dtw_heating*4200)
    
    
    pma = 1.2*qa*(troom_cooling+tgr_cooling+(dtrw_cooling/2))
    
    pa_heating = 1.2*qa*(troom_heating+tgr_heating+(dtrw_heating/2))
    pa_heating = round(pa_heating,2)
    
    qa = str(qa)
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
        ['Primary air flow rate','qa',qa,'',qa,''],
        ['Motive air side pressure', 'pma', '', pma_cooling, '', pma],
        ['Water side capacity','pw','',pw5_cooling,'',pw5_cooling],
        ['Air side capacity', 'pma','',pa_cooling,'',pa_heating],
        ['Total capacity','', '', '','',''],
        ['Reference air temperature','troom', troom_cooling,'',troom_heating,''],
        ['Gradient','',tgr_cooling,'',tgr_heating,''],
        ['Primary air temperature','dtra',dtra_cooling,'',dtra_heating,''],
        ['Inlet water temperature','twi',twin_cooling,'',twin_heating,''],
        ['Outlet water temperature','twout',twout_cooling,'',twout_heating,''],
        ['Diff out-in','dtw','',dtw_cooling,'',dtw_heating],
        ['Water flow rate','qw','',qw5_cooling,'',qw5_heating]]

    df1 = pd.DataFrame(option1, columns =['',' ', 'Cooling inputs','Cooling outputs','Heating inputs','Heating outputs'])
    st.write(df1) 
    
    # submit button
    st.subheader("Add new values to table")
    
    results_option1 = pd.read_csv('results_option1.csv')
    results_option1
    
    # results_option1["ref"][-1] = results_option1.max()+1
    
    add_ref = results_option1["ref"].max()+1
    
    clickSubmit = st.button('Save values')
    
    if clickSubmit == True: 
         newdata = {'ref' : add_ref,
             'Primary Air Flow Rate': qa,
              'Motive air side pressure cooling' : pma, 
              'Water side capacity cooling': pw5_cooling,
              'Water side capacity heating' : pw5_heating,
              'Air side capacity cooling': pa_cooling,
              'Air side capacity heating' : pa_heating,
              'Reference air temperature cooling' : troom_cooling,
              'Reference air temperature heating' : troom_heating,
              'Gradient cooling' : tgr_cooling,
              'Gradient heating' : tgr_heating,
              'Primary air temperature cooling' : tgr_cooling,
              'Primary air temperature heating' : tgr_heating,
              'Inlet water temperature cooling' : twin_cooling,
              'Inlet water temperature heating' : twin_heating,
              'Outlet Water Temperature cooling': twout_cooling,
              'Outlet Water Temperature heating' : twin_heating
              }
         
        #  d = pd.DataFrame([newdata],index=[0])
        #  d
        #  d.to_csv('C:\\Users\\jarosquin\\Documents\\evost\\results_option1.csv',index=False)
         
         results_option1 = results_option1.append(newdata,ignore_index=True)
         results_option1.to_csv('results_option1.csv',index=False)
         #results_option1 = pd.concat([results_option1,d])
         #open('results_option1.csv','a').write(results_option1.to_csv())
    else :
        st.markdown("Please submit to save")
    
    st.write(results_option1)
    
    @st.cache
    def convert_df(results_option1):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return results_option1.to_csv().encode('utf-8')

    csv = convert_df(results_option1)
    
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='results_evost_option1.csv',
    mime='text/csv',
)





    
elif option == 'Option 2 : Water flow':
    
    #COOLING INPUTS
    
    #STEP 1: choose one airflow from the table, then define the waterflow
    st.markdown("**STEP 1: choose one airflow from the table, then define the waterflow**")
    
    st.subheader('Select inputs')
    
    
    
    #STEP 2: define the Dtrw for the calculation
    st.markdown("**STEP 2: define the Dtrw for the calculation**")
    st.write("tr - (dtw/2)")
    st.write("dtrw : ",dtrw_cooling) 
    
    #STEP 3: read the data from the table correspondent to the airflow selected 
    # and calculate the specific power PLT (W/K)
    
    st.markdown("**STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)**")							
    w = 27.67206 * qa + 161.73041
    PLTtest = w / dtrw_cooling
    st.write('PLT : ', PLTtest)
    
    #STEP 4: check the correction factor correspondent to qw from the graph
    st.markdown("**STEP 4: check the correction factor correspondent to qw from the graph**")
    st.write("water flow rate : ", qw3_cooling)
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
    
    add_ref = int(results_option2["ref"].max()+1)
    
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
    
