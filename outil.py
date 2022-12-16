import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime
from math import exp

pd.set_option('display.max_columns', None)

logo = Image.open("EVOST logo.png")

timestamp = datetime.now()
timestamp = timestamp.strftime("%d-%m-%Y_%H:%M:%S")


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
# c1,c2,c3,c4,c5 = st.columns(5)
# with c1:
#     troom = st.number_input('Reference Air Flow Rate (l/s)',value=26,)
#     if option == 'Option 1 : Outlet Water Temperature':
#         qa = st.number_input('Water Flow rate (l/s)')
# with c2:
#     troom = st.number_input('Reference Air Remperature (°C)',value=26)
#     if option == 'Option 2 : Water flow':
#         st.number_input('Water Flow Rate (l/s)')
#     else: 
#        tgrvalue = st.number_input('Room Temperature Gradient (k/m)', value=0)
# with c3:
#     dtra = st.number_input('Primary Air Temperature (°C)',value=10)
#     twoutvalue = st.number_input('Outlet Water Temperature (°C)',value=17.64)
# with c4:
#     twin = st.number_input('Inlet Water Temperature (°C)',value=15.81)
# with c5:
#     st.write("")
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
    #STEP 2: calculate Dtw and Dtrw
    # st.markdown("**STEP 2: calculate Dtw and Dtrw**")
    dtw_cooling = twout_cooling-twin_cooling
    # st.write('dtw :', dtwvalue)
    dtrw_cooling = troom_cooling - ((twin_cooling+twout_cooling)/2)
    # st.write('dtrw : ',dtrw)
    
    
    #STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
    # PLTtest = Pwtest / dtrwtest
    # st.markdown("**STEP 3 : Specific power PLTtest :**")
    w = 27.67206 * qa + 161.73041
    PLTtest = w / dtrw_cooling
    # st.write('PLT : ', PLTtest)
    
    #STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
    #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
    # st.markdown("**STEP 4 : calculate the power (W) correspondent**")
    eqw_ref = 1.06
    pw1 = (PLTtest*dtrw_cooling)/eqw_ref
    # st.write('pw1 :',pw1)
    
    #STEP 5: calculate the correspondet water flow, using the Dtw calculated
    # st.markdown("**STEP 5: calculate waterflow**")
    qw1 = pw1 / (dtrw_cooling*4200)
    # st.write("qw1 : ", qw1)
    
    def epsilon(x):
        eqw = 0,588878-(1.955)*x+(3140.21)*x**2-(125288)*x**3+exp(2.43832)+6*x^4-exp(2.57437)+(7*x)**5+exp(1.416)+(8*x)**6-exp(3.18428)+(8*x)**7
        return eqw
    
    #STEP 6: check the correction factor correspondent to qw from the graph		
    
    #STEP 7: calculate the new power Pw2
    # st.markdown("**Calculate pw2**")
    if qw1 > 0.08:
        eqw1 = 1.06
    else:
        eqw1 = 2*qw1+0.5 #formule à définir pour l'itération 
        ## IMPORTANT 
    pw2 = pw1 * eqw1
    # st.write("pw2 : ",pw2)		
    
    #STEP 8: calculate the correspondet water flow, using the Dtw calculated and Pw2
    # st.markdown("**Calculate qw2**")
    qw2 = pw2 / (dtw_cooling*4200)
    # st.write("qw2 : ",qw2)
    
    #STEP 9: check the correction factor correspondent to qw from the graph							
    
    #STEP 10: calculate the new power Pw3							
    # st.markdown("**Calculate pw3**")
    if qw2 > 0.08:
        eqw2 = 1.06
    else:
        eqw2 = 2*qw2+0.5 #formule à définir pour l'itération 
    pw3 = pw2 * eqw2
    # st.write("pw3 : ",pw3)   
    
    # STEP 11: calculate the correspondet water flow, using the Dtw calculated and Pw3
    # st.markdown("**Calculate qw3**")
    qw3 = pw3/ (dtw_cooling*4200)
    # st.write("qw3 : ",qw3)
    
    ## IMPORTANT faire une boucle while pour continuer l'itération tant que l'écart entre qwn et qwn-1 est > 0.01
        
    # st.subheader("Outputs")
    # st.markdown("**Difference between water outlet and water inlet**")
    # st.write("dtw : ",dtwvalue)
    # st.markdown("**waterflow rate**")
    # qw3 = round(qw3,1)
    # st.write("qw : ",qw3)
    # st.markdown("**water side capacity**")
    # pw3 = round(pw3,2)
    # st.write("pw : ", pw3)
    # st.markdown("**Air side pressure**")
    pma = 1.2*qa*(troom_cooling+tgr_cooling+(dtrw_cooling/2))
    pma = round(pma,2)
    # st.write("pma : ",pma)
    
    st.markdown('**Tableau récapitulatif**')
    
    recapitulatif = [
        ['Total capacity','', '', '','',''],
        ['Water side capacity','pw','',pw3,'',pw3],
        ['Air side capacity', 'pma','',pma,'',pma],
        ['Reference air temperature','troom', troom_cooling,'',troom_cooling,'']]
    
    df = pd.DataFrame(recapitulatif, columns =['',' ', 'Cooling inputs','Cooling outputs','Heating inputs','Heating outputs'])
    st.write(df)
    
    
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
              'Room Temperature Gradient': tgrvalue_cooling,
              'Inlet Water Temperature': twin,
              "dtw" : dtwvalue,
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
    
