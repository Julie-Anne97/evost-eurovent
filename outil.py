import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime

pd.set_option('display.max_columns', None)

logo = Image.open("EVOST logo.png")

timestamp = datetime.now()
timestamp = timestamp.strftime("%d-%m-%Y_%H:%M:%S")


with st.sidebar:    
    st.image(logo)
    option = st.radio(
    "Select option",
    ('Option 1 : Outlet Water Temperature', 'Option 2 : Water flow'))
    
    if option == 'Option 1 : Outlet Water Temperature':
        twoutvalue = st.number_input('Outlet Water Temperature',value=17.64)
    elif option == 'Option 2 : Water flow':
        qwvalue = st.number_input('Water flow',value=0.080)  


st.title('Software Eurovent')


if option == 'Option 1 : Outlet Water Temperature':
    #STEP 1: choose one airflow from the table, then define the water temperatures (= enter qa & twin)
    st.markdown("**STEP 1: choose one airflow from the table, then define the water temperatures (= enter qa & twin)**")
    st.subheader('Select inputs')
    col1,col2 = st.columns(2)
    with col1: 
        qavalue = st.number_input('Primary Air Flow Rate',value = 59)
        travalue = st.number_input('Primary Air Temperature',value=10)
        trvalue = st.number_input('Reference Air Remperature',value=26)
    with col2:
        tgrvalue = st.number_input('Room Temperature Gradient', value=0)
        twinvalue = st.number_input('Inlet Water Temperature',value=15.81)
    #STEP 2: calculate Dtw and Dtrw
    st.markdown("**STEP 2: calculate Dtw and Dtrw**")
    dtwvalue = twoutvalue-twinvalue
    st.write('dtw :', dtwvalue)
    dtrw = trvalue - ((twinvalue+twoutvalue)/2)
    st.write('dtrw : ',dtrw)
    
    #STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
    # PLTtest = Pwtest / dtrwtest
    st.markdown("**STEP 3 : Specific power PLTtest :**")
    w = 27.67206 * qavalue + 161.73041
    PLTtest = w / dtrw
    st.write('PLT : ', PLTtest)
    
    #STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
    #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
    st.markdown("**STEP 4 : calculate the power (W) correspondent**")
    eqw = 1.06
    pw1 = (PLTtest*dtrw)/eqw
    st.write('pw1 :',pw1)
    
    #STEP 5: calculate the correspondet water flow, using the Dtw calculated
    st.markdown("**STEP 5: calculate waterflow**")
    qw1 = pw1 / (dtwvalue*4200)
    st.write("qw1 : ", qw1)
    
    #STEP 6: check the correction factor correspondent to qw from the graph		
    
    #STEP 7: calculate the new power Pw2
    st.markdown("**Calculate pw2**")
    if qw1 > 0.08:
        eqw1 = 1.06
    else:
        eqw1 = 2*qw1+0.5 #formule à définir pour l'itération 
        ## IMPORTANT 
    pw2 = pw1 * eqw1
    st.write("pw2 : ",pw2)		
    
    #STEP 8: calculate the correspondet water flow, using the Dtw calculated and Pw2
    st.markdown("**Calculate qw2**")
    qw2 = pw2/ (dtwvalue*4200)
    st.write("qw2 : ",qw2)
    
    #STEP 9: check the correction factor correspondent to qw from the graph							
    
    #STEP 10: calculate the new power Pw3							
    st.markdown("**Calculate pw3**")
    if qw2 > 0.08:
        eqw2 = 1.06
    else:
        eqw2 = 2*qw2+0.5 #formule à définir pour l'itération 
    pw3 = pw2 * eqw2
    st.write("pw3 : ",pw3)   
    
    # STEP 11: calculate the correspondet water flow, using the Dtw calculated and Pw3
    st.markdown("**Calculate qw3**")
    qw3 = pw3/ (dtwvalue*4200)
    st.write("qw3 : ",qw3)
    
    ## IMPORTANT faire une boucle while pour continuer l'itération tant que l'écart entre qwn et qwn-1 est > 0.01
        
    st.subheader("Outputs")
    st.markdown("**Difference between water outlet and water inlet**")
    st.write("dtw : ",dtwvalue)
    st.markdown("**waterflow rate**")
    qw3 = round(qw3,1)
    st.write("qw : ",qw3)
    st.markdown("**water side capacity**")
    pw3 = round(pw3,2)
    st.write("pw : ", pw3)
    st.markdown("**Air side pressure**")
    pma = 1.2*qavalue*(trvalue+tgrvalue+(dtwvalue/2))
    pma = round(pma,2)
    st.write("pma : ",pma)
    
    # submit button
    st.subheader("Add new values to table")
    
    results_option1 = pd.read_csv('results_option1.csv')
    results_option1
    
    add_ref = results_option1["ref"].max()+1
    
    # d = pd.DataFrame([d],index=[0])
    # d
    #d.to_csv('results_option1.csv')
    
    clickSubmit = st.button('Save values')
    
    if clickSubmit == True: 
         newdata = {'ref' : add_ref,
              'Primary Air Flow Rate': qavalue, 
              'Primary Air Temperature': travalue,
              'Reference Air Remperature': trvalue,
              'Room Temperature Gradient': tgrvalue,
              'Inlet Water Temperature': twinvalue,
              "dtw" : dtwvalue,
              "water flow rate" : qw3,
              "water side capacity" : pw3,
              "air side pressure" : pma}
         st.write(newdata)
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
    col1,col2 = st.columns(2)
    with col1: 
        qavalue = st.number_input('Primary Air Flow Rate',value = 59)
        travalue = st.number_input('Primary Air Temperature',value=10)
        trvalue = st.number_input('Reference Air Remperature',value=26)
    with col2:
        tgrvalue = st.number_input('Room Temperature Gradient', value=0)
        twinvalue = st.number_input('Inlet Water Temperature',value=15.81)
    
    
    #STEP 2: define the Dtrw for the calculation
    st.markdown("**STEP 2: define the Dtrw for the calculation**")
    dtrw = 10
    st.write("dtrw : ",dtrw)
    
    #STEP 3: read the data from the table correspondent to the airflow selected 
    # and calculate the specific power PLT (W/K)
    
    st.markdown("**STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)**")							
    w = 27.67206 * qavalue + 161.73041
    PLTtest = w / dtrw
    st.write('PLT : ', PLTtest)
    
    #STEP 4: check the correction factor correspondent to qw from the graph
    st.markdown("**STEP 4: check the correction factor correspondent to qw from the graph**")
    st.write("?")
    
    #STEP 5: calculate the power (W) correspondent to waterflow desired, using the Dtrw chosen							
    st.markdown("**STEP 5: calculate the power (W) correspondent to waterflow desired, using the Dtrw chosen**")
    
