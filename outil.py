import pandas as pd
import streamlit as st
from PIL import Image
from math import exp
from datetime import date
import os

pd.set_option('display.max_columns', None)
st.set_page_config(layout="wide")

today = date.today()
logo = Image.open("EVOST logo.png")


with st.sidebar:    
    st.image(logo)
    st.subheader("")
    st.markdown("**EVOST E1 – 1250 – 4p – L - H**")
    st.container()
    # st.radio("Nozzle : ", ("E1","E1.1"), disabled=True)
    # st.radio("Model", (800, 1150, 1250, 1400, 2600), disabled=True,index=2)
    st.radio("Tubes",(2,4),index=1)
    st.radio("Type : ", ("Horizontal","Vertical"), disabled=True)
    # st.write("Motive pressure – pmot = 350 Pa")
    option = st.radio(
    "Select option",
    ('Option 1 : Outlet Water Temperature', 'Option 2 : Water flow'))
    
    
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 1rem;
                    padding-bottom: 10rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
                div[class*="stNumberInput"] label {font-size: 12px;}
                input {font-size: 0.66rem !important;}
        </style>
        """, unsafe_allow_html=True)

# style
th_props = [
  ('font-size', '8px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7ffff')
  ]
                               
td_props = [
  ('font-size', '12px')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]

    
#STEP 1: choose one airflow from the table, then define the water temperatures (= enter qa & twin)

st.subheader('Select inputs')



col1,col2,col3 = st.columns(3)
with col1:
    qa = st.number_input('Motive (Primary) air flow rate - qa (l/s)',value=16.0,min_value=6.2)
 
      
if option == 'Option 1 : Outlet Water Temperature':
    
    st.markdown('**Cooling inputs**')
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        troom_cooling = st.number_input('Reference Air Temperature - troom (°C)',value=26)
    with c2:
        tgr_cooling = st.number_input('Room Temperature Gradient -tgr (°C/m)', value=0)
    with c3:
        ta_cooling = st.number_input('Primary Air Temperature - ta (°C)',value=10)
    with c4 :
        twin_cooling = st.number_input('Inlet Water Temperature - twin (°C)',value=15.0,min_value=13.0)
    with c5:
        twout_cooling = st.number_input('Outlet Water Temperature - twout (°C)',value=18)
    
    st.markdown('**Heating inputs**')
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        troom_heating = st.number_input('Reference Air Temperature - troom (°C)  ',value=26)
    with c2:
        tgr_heating = st.number_input('Room Temperature Gradient - tgr (°C/m)  ', value=0)
    with c3:
        ta_heating = st.number_input('Primary Air Temperature - ta (°C)  ',value=10)
    with c4 :
        twin_heating = st.number_input('Inlet Water Temperature -twin (°C)',value=15.0,min_value=13.0)
    with c5:
        twout_heating = st.number_input('Outlet Water Temperature (°C) -twout ',value=17.64)
    
    
    ## COOLING INPUTS 

    @st.cache
    def epsilon(x):
        eqw = 0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2.43832*(10**6)*(x**4)-2.57437*(10**7)*(x**5)+1.416*(10**8)*(x**6)-3.18428*(10**8)*(x**7)
        return eqw
    
    @st.cache
    def dpw_cooling_formula(x) :
        dpw_c = 1.25-328.673*x+36889*(x**2)-1.601*(10**6)*(x**3)+4.0005*(10**7)*(x**4)-5.50149*(10**8)*(x**5)+3.90377*(10**9)*(x**6)-1.11607*(10**10)*(x**7)
        return dpw_c
    
    @st.cache
    def dpw_heating_formula(x):
        dpw_h = 0.2-55*x+6473.81*(x**2)-243790*(x**3)+5.22321*(10**6)*(x**4)-6.2004*(10**7)*(x**5)+3.86905*(10**8)*(x**6)-9.92063*(10**8)*(x**7)
        return dpw_h
    

    #STEP 2: calculate Dtw and Dtrw
    dtw_cooling = twout_cooling-twin_cooling
    dtrw_cooling = (troom_cooling + tgr_cooling) - ((twin_cooling+twout_cooling)/2)
    
    #STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
    # PLTtest = Pwtest / dtrwtest
    # w = 35.06543 * qa + 186.32415
    # w = -1992.88+734.415*qa-83.8188*(qa**2)+4.29282*(qa**3)-0.0805417*(qa**4)
    
    w = -1992.88+734.415*qa-83.8188*qa**2+4.29282*qa**3-0.0805417*qa**4
    v = -26.1552+13.5864*qa-1.74758*qa**2+0.0946072*qa**3-0.00185556*qa**4
    PLT_cooling = w / v
    
    #STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
    #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
    
    eqw_ref = 1.06
    
    pw1_cooling = (PLT_cooling*dtrw_cooling)/eqw_ref
    
    #STEP 5: calculate the correspondet water flow, using the Dtw calculated
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
    
    
    
    ## HEATING INPUTS
    
    
    
    #STEP 2: calculate Dtw and Dtrw
    dtw_heating = twout_heating -twin_heating
    dtrw_heating = (troom_heating+tgr_heating) - ((twin_heating +twout_heating)/2)
    
    
    #STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
    # PLTtest = Pwtest / dtrwtest
    w = 35.06543 * qa + 186.32415
    v = -26.1552+13.5864*qa-1.74758*qa**2+0.0946072*qa**3-0.00185556*qa**4
    PLT_heating = w / v 
    
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
    
    dtra_cooling = troom_cooling+tgr_cooling-ta_cooling
    dtra_heating = troom_heating+tgr_heating-ta_heating

    pma = 2131.77-589.557*qa+62.2699*(qa**2)-2.75638*(qa**3)+0.0463111*(qa**4)
    pa_cooling=1.2*qa*dtra_cooling
    pa_heating=1.2*qa*dtra_heating
    
    
    pa_heating = 1.2*qa*(troom_heating+tgr_heating+(dtrw_heating/2))
    pa_heating = round(pa_heating,2)
    
    ptot_cooling = round(pw5_cooling + pa_cooling,2)
    ptot_heating = round(pw5_heating + pa_heating,2)
    
    dpw_cooling = dpw_cooling_formula(qw5_cooling)
    dpw_heating = dpw_heating_formula(qw5_heating)
    

    
    qa=round(qa,2)
    qa = str(qa)
    
    troom_cooling = round(troom_cooling,2)
    troom_heating = round(troom_heating,2)
    twin_cooling = round(twin_cooling,2)
    twin_heating = round(twin_heating,2)
    twout_cooling = round(twout_cooling,2)
    twout_heating = round(twout_heating,2)
    tgr_cooling = round(tgr_cooling,2)
    tgr_heating = round(tgr_heating,2)
    dtra_cooling = round(dtra_cooling,2)
    dtra_heating = round(dtra_heating,2)
    dtw_cooling = round(dtw_cooling,2)
    dtw_heating = round(dtw_heating,2)
    qw5_cooling = round (qw5_cooling,4)
    qw5_heating = round(qw5_heating,4)
    dpw_cooling = round(dpw_cooling,2)
    dpw_heating = round(dpw_heating,2)
    pma = round(pma,2)
    pw5_cooling = round(pw5_cooling,2)
    pw5_heating = round(pw5_heating,2)
    qw5_cooling = round(qw5_cooling,2)
    qw5_heating = round(qw5_heating)

        
    
    st.subheader("Results")
    st.write('pwtest : ',w)
    st.write('plttest : ',PLT_cooling)
    
    

    option1 = [
        ['Motive (Primary) air flow rate' ,'(l/s)','qa',qa,'',qa,''],
        ['Reference air temperature', '(°C)','troom', troom_cooling,'',troom_heating,''],
        ['Room temperature gradient','','tgr',tgr_cooling,'',tgr_heating,''],
        ['Primary (Motive) air temperature', '(°C)','dtra',dtra_cooling,"",dtra_heating,""],
        ['Inlet water temperature','(°C)','twi',twin_cooling,'',twin_heating,''],
        ['Outlet water temperature','(°C) ','twout',twout_cooling,'',twout_heating,''],
        ['Water temperature difference in out', '(°C)','dtw','',dtw_cooling,'',dtw_heating],
        ['Temp. diff. room air and mean water temp ','(K)','dtrw','','','',''],
        ['Water flow rate','(l/s)','qw','',qw5_cooling,'',qw5_heating],
        ['Motive air pressure' ,'(W)', 'pma', '', pma, '', pma],
        ['Water side capacity','(W)','pw','',pw5_cooling,'',pw5_cooling],
        ['Air side capacity', '(W)', 'pa','',pa_cooling,'',pa_heating],
        ['Total capacity', '(W)','ptot', '', ptot_cooling,'',ptot_heating],
        ['Water pressure drop', '(kPa)','DPw','',dpw_cooling,'',dpw_heating]
        ]

    df1 = pd.DataFrame(option1, columns =['   ',' ','', 'Cooling inputs','Cooling outputs','Heating inputs','Heating outputs'])
    
    df1 = df1.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    
    
    st.dataframe(df1,height=530)
    
    # submit button
    st.subheader("Add new values to table")
    
    results_option1 = pd.read_csv('results_option1.csv')
    # results_option1
    
    
    # results_option1["ref"][-1] = results_option1.max()+1
    
    add_ref = results_option1["ref"].max()+1
    
    add_ref = int(add_ref)
    
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
         
        #  d = pd.DataFrame([newdata])
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
    
    def epsilon(x):
        eqw = 0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2.43832*(10**6)*(x**4)-2.57437*(10**7)*(x**5)+1.416*(10**8)*(x**6)-3.18428*(10**8)*(x**7)
        return eqw
    
    def dpw_cooling_formula(x) :
        dpw_c = 1.25-328.673*x+36889*(x**2)-1.601*(10**6)*(x**3)+4.0005*(10**7)*(x**4)-5.50149*(10**8)*(x**5)+3.90377*(10**9)*(x**6)-1.11607*(10**10)*(x**7)
        return dpw_c
    
    def dpw_heating_formula(x):
        dpw_h = 0.2-55*x+6473.81*(x**2)-243790*(x**3)+5.22321*(10**6)*(x**4)-6.2004*(10**7)*(x**5)+3.86905*(10**8)*(x**6)-9.92063*(10**8)*(x**7)
        return dpw_h
    
    dtrw1_cooling = 8

    w = -1992.88+734.415*qa-83.8188*qa**2+4.29282*qa**3-0.0805417*qa**4
    
    v = -26.1552+13.5864*qa-1.74758*qa**2+0.0946072*qa**3-0.00185556*qa**4

    PLT_cooling = w / v
    
    PLT_cooling

    eqw_ref = epsilon(qw_cooling)
    
    eqw_ref

    

    pw1_cooling = PLT_cooling*(dtrw1_cooling*eqw_ref/1.06)
    
    pw1_cooling

    dtw1_cooling = pw1_cooling / (qw_cooling *4200)
    
    dtw1_cooling

    twout1_cooling = dtw1_cooling + twin_cooling

    dtrw2_cooling = troom_cooling - (twin_cooling + twout1_cooling)/2

    pw2_cooling = PLT_cooling*(dtrw2_cooling*eqw_ref/1.06)

    dtw2_cooling = pw2_cooling / (qw_cooling *4200)

    twout2_cooling = dtw2_cooling + twin_cooling

    dtrw3_cooling = troom_cooling - (twin_cooling + twout2_cooling)/2

    pw3_cooling = PLT_cooling*(dtrw3_cooling*eqw_ref/1.06)

    dtw3_cooling = pw3_cooling / (qw_cooling *4200)

    twout3_cooling = dtw3_cooling + twin_cooling

    dtrw4_cooling = troom_cooling - (twin_cooling + twout3_cooling)/2

    pw4_cooling = PLT_cooling*(dtrw4_cooling*eqw_ref/1.06)

    dtw4_cooling = pw4_cooling / (qw_cooling *4200)

    twout4_cooling = dtw4_cooling + twin_cooling

    dtrw5_cooling = troom_cooling - (twin_cooling + twout4_cooling)/2

    pw5_cooling = PLT_cooling*(dtrw5_cooling*eqw_ref/1.06)

    dtw5_cooling = pw5_cooling / (qw_cooling *4200)

    twout5_cooling = dtw5_cooling + twin_cooling
    

    #HEATING INPUTS
    
    
    dtrw1_heating = 8

    w = -1992.88+734.415*qa-83.8188*qa**2+4.29282*qa**3-0.0805417*qa**4

    PLT_heating = w / dtrw1_heating

    eqw_ref = epsilon(qw_heating)

    

    pw1_heating = PLT_heating*(dtrw1_heating*eqw_ref/1.06)

    dtw1_heating = pw1_heating / (qw_heating *4200)

    twout1_heating = dtw1_heating + twin_heating

    dtrw2_heating = troom_heating - (twin_heating + twout1_heating)/2

    pw2_heating = PLT_heating*(dtrw2_heating*eqw_ref/1.06)

    dtw2_heating = pw2_heating / (qw_heating *4200)

    twout2_heating = dtw2_heating + twin_heating

    dtrw3_heating = troom_heating - (twin_heating + twout2_heating)/2

    pw3_heating = PLT_heating*(dtrw3_heating*eqw_ref/1.06)

    dtw3_heating = pw3_heating / (qw_heating *4200)

    twout3_heating = dtw3_heating + twin_heating

    dtrw4_heating = troom_heating - (twin_heating + twout3_heating)/2

    pw4_heating = PLT_heating*(dtrw4_heating*eqw_ref/1.06)

    dtrw4_heating = pw4_heating / (qw_heating *4200)

    twout4_heating = dtrw4_heating + twin_heating

    dtrw5_heating = troom_heating - (twin_heating + twout4_heating)/2

    pw5_heating = PLT_heating*(dtrw5_heating*eqw_ref/1.06)

    dtw5_heating = pw5_heating / (qw_cooling *4200)

    twout5_heating = dtw5_heating + twin_heating








    #Autres formules
    
    dtra_cooling = troom_cooling + tgr_cooling - ta_cooling
    dtra_heating = troom_heating + tgr_heating - ta_heating

    dpw_cooling = dpw_cooling_formula(qw_cooling)

    dpw_heating = dpw_heating_formula(qw_heating)

    

    pma = 2131.77-589.557*qa+62.2699*(qa**2)-2.75638*(qa**3)+0.0463111*(qa**4)
    
    

    # pa_cooling = 1.2*qa*(troom_cooling+tgr_cooling+(dtrw5_cooling/2))
    
    pa_cooling = 1.2*qa*dtra_cooling
    pa_cooling = round(pa_cooling,2)

    

    pa_heating = 1.2*qa*dtra_heating

    pa_heating = round(pa_heating,2)

    

    ptot_cooling = pw5_cooling + pa_cooling

    ptot_heating = pw5_heating + pa_heating
    
    qa = str(qa)
    
    st.write('plt : ',PLT_cooling)
    
    option2 = [
        ['Primary (Motive) air flow rate', '(l/s)','qa',qa,'',qa,''],
        ['Reference air temperature', '(°C)','troom', troom_cooling,'',troom_heating,''],
        ['Room temperature gradient','','tgr',tgr_cooling,'',tgr_heating,''],
        ['Primary (Motive) air temperature', '(°C)','dtra',dtra_cooling,'',dtra_heating,''],
        ['Water flow rate', '(l/s)','qw',qw_cooling,'',qw_heating,''],
        ['Inlet water temperature', '(°C)','twi',twin_cooling,'',twin_heating,''],
        ['Outlet water temperature', '(°C) ','twout','',twout5_cooling,'',twout5_heating],
        ['Water temperature difference in out', '(°C)','dtw','',dtw5_cooling,'',dtw5_heating],
        ['Temp. diff. room air and min water temp.','(°C)','dtrw','',dtrw5_cooling,'',dtrw5_heating],
        ['Motive air pressure', '(W)', 'pma', '', pma, '', pma],
        ['Water side capacity', '(W)','pw','',pw5_cooling,'',pw5_cooling],
        ['Air side capacity', '(W)', 'pa','',pa_cooling,'',pa_heating],
        ['Total capacity', '(W)','ptot', '', ptot_cooling,'',ptot_heating],
        ['Water pressure drop', '(kPa)','DPw','',dpw_cooling,'',dpw_heating]]
    
    df2 = pd.DataFrame(option2, columns =['   ',' ','', 'Cooling inputs','Cooling outputs','Heating inputs','Heating outputs'])
    st.dataframe(df2,height=530)
    
    
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
    
