import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import pathlib 
import shutil
from PIL import Image
from decimal import Decimal, localcontext


# CONFIGURATIONS

pd.set_option('display.max_columns', None)
logo = Image.open("EVOST logo.png")
machine = Image.open('Image115.png')
st.set_page_config(page_title="EVOST EUROVENT",page_icon=machine,layout="wide")


# STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / 'static'
# CSS_PATH = (STREAMLIT_STATIC_PATH / "assets/css")
# if not CSS_PATH.is_dir():
#     CSS_PATH.mkdir()

# css_file = CSS_PATH / "table_style.css"
# if not css_file.exists():
#     shutil.copy("assets/css/table_style.css", css_file)

# STYLES

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
    
st.markdown("""
         <head>
         <link rel="stylesheet" type="text/css" href=""C:\\Users\\jarosquin\\Documents\\evost\\styles.css"">
         <head>   
         <style>
               .css-18e3th9 {
                    padding-top: 2rem;
                    padding-bottom: 10rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 0.5rem;
                }
                div[class*="stNumberInput"] label {font-size: 12px;}
                input {font-size: 0.66rem !important;}
                div[class*="stRadio"] label {font-size: 12px;}
                input {font-size: 0.66rem !important;}
                options {font-size: 0.66rem !important;}
        </style>
        """, unsafe_allow_html=True)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)        


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

# def cooling_highlight(val):
#     color = '#ACE5EE' if val else 'white'
#     return f'background-color: {color}'



# SIDEBAR

with st.sidebar:    
    st.image(logo)
    st.subheader("")
    st.markdown("**EVOST E1 – 1250 – 4p – L - H**")
    # st.radio("Nozzle : ", ("E1","E1.1"), disabled=True)
    # st.radio("Model", (800, 1150, 1250, 1400, 2600), disabled=True,index=2)
    tubes = st.radio("Tubes",(2,4),index=1,disabled=True)
    # if tubes == 2:
    #     choose = st.radio("",("Cooling","Heating"))
    # elif tubes == 4:
    #     choose = st.radio("",("Cooling","Heating"),disabled=True)
    st.radio("Type : ", ("Horizontal","Vertical"), disabled=True)
    # st.write("Motive pressure – pmot = 350 Pa")
    option = st.radio(
    "Select option",
    ('Option 1 : ∆tw - Calculate water flow from given delta T', 'Option 2 : qw - Calculate delta T from given water flow'))
 
     

#FORMULES 
        
def epsilon_cooling(x):
    eqw = 0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2.43832*(10**6)*(x**4)-2.57437*(10**7)*(x**5)+1.416*(10**8)*(x**6)-3.18428*(10**8)*(x**7)
    return eqw
        
# def epsilon_cooling(x):
#     eqw =0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2438320*(x**4)-25743700*(x**5)+141600000*(x**6)-318428000*(x**7)
#     return eqw

# def epsilon_heating(x):
#     if x<0.134:
#         eqw = (0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2.43832*(10**6)*(x**4)-2.57437*(10**7)*(x**5)+1.416*(10**8)*(x**6)-3.18428*(10**8)*(x**7))*0.66
#     else :
#         eqw = (0.588878-17.955*0.133+3140.21*(0.133**2)-125288*(0.133**3)+2.43832*(10**6)*(0.133**4)-2.57437*(10**7)*(0.133**5)+1.416*(10**8)*(0.133**6)-3.18428*(10**8)*(0.133**7))*0.66
#     return eqw

def epsilon_heating(x):
    if x<=0.132:
        eqw = (0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2.43832*(10**6)*(x**4)-2.57437*(10**7)*(x**5)+1.416*(10**8)*(x**6)-3.18428*(10**8)*(x**7))*0.66
    else :
        eqw = (0.588878-17.955*0.132+3140.21*(0.132**2)-125288*(0.132**3)+2.43832*(10**6)*(0.132**4)-2.57437*(10**7)*(0.132**5)+1.416*(10**8)*(0.132**6)-3.18428*(10**8)*(0.132**7))*0.66
    return eqw
        
# def epsilon_heating(x):
#             eqw =(0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2438320*(x**4)-25743700*(x**5)+141600000*(x**6)-318428000*(x**7))*0.66
#             return eqw
        
def dpw_cooling_formula(x) :
            dpw_c = 1.25-328.673*x+36889*(x**2)-1.601*(10**6)*(x**3)+4.0005*(10**7)*(x**4)-5.50149*(10**8)*(x**5)+3.90377*(10**9)*(x**6)-1.11607*(10**10)*(x**7)
            return dpw_c
    
def dpw_heating_formula(x):
            dpw_h = 0.2-55*x+6473.81*(x**2)-243790*(x**3)+5.22321*(10**6)*(x**4)-6.2004*(10**7)*(x**5)+3.86905*(10**8)*(x**6)-9.92063*(10**8)*(x**7)
            return dpw_h
        

    
# PRESENTATION ET CALCULS 
  
if option == 'Option 1 : ∆tw - Calculate water flow from given delta T':
    col1,col2,col3 = st.columns([1,1,4])
    ### STEP 1: choose one airflow from the table, then define the water temperatures (= enter qa & twin)
    with col1:
        st.subheader('Select inputs')
        qa = st.number_input('Primary (Motive) air flow rate - qa (l/s)',value=16.0,min_value=7.8,max_value=16.3)

        # measure = st.radio("Unité de mesure",("l/s","m³/h"))
        st.markdown('**Cooling inputs**')
        troom_cooling = st.number_input('Reference Air Temperature - troom (°C)',value=26.0,step=0.1)
        tgr_cooling = st.number_input('Room Temperature Gradient -tgr °C/m)', value=0.0,step=0.1)
        ta_cooling = st.number_input('Primary (Motive) Air Temperature - ta (°C)',value=15.0,step=0.1)
        twin_cooling = st.number_input('Inlet Water Temperature - twin (°C)',value=15.0,min_value=13.0,step=0.1)
        twout_cooling = st.number_input('Outlet Water Temperature - twout (°C)',value=18.0,step=0.1)
                # troom_cooling = st.number_input('Reference Air Temperature - troom (°C)',value=26.0,step=0.1,disabled=True)
                # tgr_cooling = st.number_input('Room Temperature Gradient -tgr °C/m)', value=0.0,step=0.1,disabled=True)
                # ta_cooling = st.number_input('Primary (Motive) Air Temperature - ta (°C)',value=10.0,step=0.1,disabled=True)
                # twin_cooling = st.number_input('Inlet Water Temperature - twin (°C)',value=15.0,min_value=13.0,step=0.1,disabled=True)
                # twout_cooling = st.number_input('Outlet Water Temperature - twout (°C)',value=18.0,step=0.1,disabled=True)   
            
    with col2:
        st.title("")
        st.title("")
        st.title("")
        st.title("")
        st.title("")
        st.write("")
        st.markdown('**Heating inputs**')
        troom_heating = st.number_input('Reference Air Temperature - troom (°C)  ',value=20.0,step=0.1,)
        tgr_heating = st.number_input('Room Temperature Gradient-tgr (°C/m)', value=1.0, step=0.1)
        ta_heating = st.number_input('Primary (Motive) Air Temperature - ta (°C)  ',value=20.0,step=0.1)
        twin_heating = st.number_input('Inlet Water Temperature -twin (°C)',value=55.0,min_value=30.0,step=0.1)
        twout_heating = st.number_input('Outlet Water Temperature (°C) -twout ',value=50.0,step=0.1)
    
    
    with col3: 
        
        # CALCULS ET TABLEAU
        
        ## CALCULS COOLING INPUTS 

        ### STEP 2: calculate Dtw and Dtrw
        
        dtw_cooling = twout_cooling-twin_cooling
        dtrw_cooling = (troom_cooling + tgr_cooling) - ((twin_cooling+twout_cooling)/2)
        
        dtw_cooling = round(dtw_cooling,2)
        # st.write("step 2 dtw_cooling : ",dtw_cooling)
        dtrw_cooling = round(dtrw_cooling,2)
        # st.write("step 2 dtrw_cooling : ", dtrw_cooling)
        
        ### STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
        
        # PLTtest = Pwtest / dtrwtest
        # w = 35.06543 * qa + 186.32415
        # w = -1992.88+734.415*qa-83.8188*(qa**2)+4.29282*(qa**3)-0.0805417*(qa**4)
        w = -1992.88+734.415*qa-83.8188*qa**2+4.29282*qa**3-0.0805417*qa**4
        v = -26.1552+13.5864*qa-1.74758*qa**2+0.0946072*qa**3-0.00185556*qa**4
        PLT_cooling = w / v
        
        w = round(w,2)
        # st.write("step 3 w : ",w)
        v = round(v,2)
        # st.write("step 3 v : ",v)
        PLT_cooling = round(PLT_cooling,2)
        # st.write("step 3 plt_cooling : ",PLT_cooling)
        ###STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
        
        #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
        eqw_ref = 1.06
        pw1_cooling = (PLT_cooling*dtrw_cooling)/eqw_ref
        
        # st.write("step 4 eqw_ref ",eqw_ref)
        pw1_cooling = round(pw1_cooling,2)
        # st.write("step 4 pw1 cooling : ",pw1_cooling)
    
        ###STEP 5: calculate the correspondet water flow, using the Dtw calculated
        
        pw1_cooling = (PLT_cooling*dtrw_cooling)/eqw_ref
        qw1_cooling = pw1_cooling / (dtw_cooling*4200)
        
        pw2_cooling = pw1_cooling*round(epsilon_cooling(qw1_cooling),8)
        qw2_cooling = pw2_cooling / (dtw_cooling*4200)
        
        pw3_cooling = pw1_cooling*round(epsilon_cooling(qw2_cooling),8)
        qw3_cooling = pw3_cooling / (dtw_cooling*4200)
        
        pw4_cooling = pw1_cooling*round(epsilon_cooling(qw3_cooling),8)
        qw4_cooling = pw4_cooling / (dtw_cooling*4200)
        
        pw5_cooling = pw1_cooling*round(epsilon_cooling(qw4_cooling),8)
        qw5_cooling = pw5_cooling / (dtw_cooling*4200)
        
        qw1_cooling = round(qw1_cooling,4)
        pw2_cooling = round(pw2_cooling,2)
        qw2_cooling = round(qw2_cooling,4)
        pw3_cooling = round(pw3_cooling,2)
        qw3_cooling = round(qw3_cooling,4)
        pw4_cooling = round(pw4_cooling,2)
        qw4_cooling = round(qw4_cooling,4)
        pw5_cooling = round(pw5_cooling,2)
        qw5_cooling = round(qw5_cooling,4)
    
        ## HEATING INPUTS
     
        ### STEP 2: calculate Dtw and Dtrw
        
        dtw_heating = - twout_heating + twin_heating
        dtrw_heating = - (troom_heating+tgr_heating) + ((twin_heating +twout_heating)/2)
        
        dtw_heating = round(dtw_heating,2)
        dtrw_heating = round(dtrw_heating,2)
        # st.write("step 2 dt_heating : ",dtw_heating)
        # st.write("step 2 dtrw_heating",dtrw_heating)
    
        ### STEP 3: read the data from the table correspondent to the airflow selected and calculate the specific power PLT (W/K)
        
        # PLTtest = Pwtest / dtrwtest
        # w = 35.06543 * qa + 186.32415
        # v = -26.1552+13.5864*qa-1.74758*qa**2+0.0946072*qa**3-0.00185556*qa**4
        # PLT_heating = w / v 
        
        w = 2159.35-710.505*qa+100.656*(qa**2)-5.75702*(qa**3)+0.120588*(qa**4)
        
        # PLT_heating = w / dtrw_heating
        
        PLT_heating = w / 20

        
        w = round(w,2)
        PLT_heating = round(PLT_heating,2)
        # st.write("step 3 w heating", w)
        # st.write("step 3 plt heating",PLT_heating)
        
    
        ### STEP 4: calculate the power (W) correspondent to correction factor equal to 1, using the Dtrw calculated
        
        #Pw1 = (PLTtest * dtrw)/Eqw0.08ls
        eqw_ref = 0.7
        # pw1_heating = (PLT_heating*dtrw_heating)/eqw_ref
    
        ### STEP 5: calculate the correspondet water flow, using the Dtw calculated
        
        pw1_heating = PLT_heating*(dtrw_heating/eqw_ref)
        pw1_heating = round(pw1_heating,2)
        # st.write("step 3 pw1_heating",pw1_heating)
        qw1_heating = pw1_heating / (dtw_heating*4200)
        qw1_heating = round(qw1_heating,4)
        # st.write("step 3 qw1 heating", qw1_heating)
        
        pw2_heating = pw1_heating*epsilon_heating(qw1_heating)
        # st.write("epsilon pw2 heating", epsilon_heating(qw1_heating))
        pw2_heating = round(pw2_heating,2)
        # st.write("step 3 pw2 heating",pw2_heating)
        qw2_heating = pw2_heating / (dtw_heating*4200)
        qw2_heating = round(qw2_heating,4)
        # st.write("step qw2 heating",qw2_heating)
        
        pw3_heating = pw1_heating*epsilon_heating(qw2_heating)
        pw3_heating = round(pw3_heating)
        # st.write("step 3 pw3 heating",pw3_heating)
        qw3_heating = pw3_heating / (dtw_heating*4200)
        qw3_heating  = round(qw3_heating,4)
        # st.write("step 3 qw3 heating", qw3_heating)


        pw4_heating = pw1_heating*epsilon_heating(qw3_heating)
        pw4_heating = round(pw4_heating,2)
        # st.write("step 3 pw4 heating",pw4_heating)
        qw4_heating = pw4_heating / (dtw_heating*4200)
        qw4_heating = round(qw4_heating,4)
        # st.write("qw4 heating", qw4_heating)
        
        pw5_heating = pw1_heating*epsilon_heating(qw4_heating)
        # st.write("epsilon pw5 heating", epsilon_heating(qw4_heating))
        pw5_heating = round(pw5_heating,2)
        # st.write("pw5 heating", pw5_heating)
        qw5_heating = pw5_heating / (dtw_heating*4200)
        qw5_heating = round(qw5_heating,4)
        # st.write("qw5 heating", qw5_heating)
        
        
        
        
        
        ## AUTRES CALCULS
        
        # dtra_cooling = troom_cooling+tgr_cooling-ta_cooling
        # dtra_heating = -(troom_heating+tgr_heating-ta_heating)
        dtra_cooling = troom_cooling-ta_cooling
        dtra_heating = -(troom_heating-ta_heating)
        dtra_cooling = round(dtra_cooling,2)
        dtra_heating = round(dtra_heating,2)

        pma = 2131.77-589.557*qa+62.2699*(qa**2)-2.75638*(qa**3)+0.0463111*(qa**4)
        pma = round(pma,2)
        pa_cooling=1.2*qa*dtra_cooling
        pa_heating=1.2*qa*dtra_heating
        pa_cooling = round(pa_cooling,2)
        pa_heating = round(pa_heating,2)
        
        # pa_heating = 1.2*qa*(troom_heating+tgr_heating+(dtrw_heating/2))
        # pa_heating = round(pa_heating,2)
        
        ptot_cooling = round(pw5_cooling + pa_cooling,2)
        ptot_heating = round(pw5_heating + pa_heating,2)
        
        dpw_cooling = dpw_cooling_formula(qw5_cooling)
        dpw_heating = dpw_heating_formula(qw5_heating)
    

    
        qa=round(qa,2)
        qa = str(qa)
        # troom_cooling = round(troom_cooling,2)
        # troom_heating = round(troom_heating,2)
        # tgr_cooling = round(tgr_cooling,2)
        # tgr_heating = round(tgr_heating,2)
        # twin_cooling = round(twin_cooling,2)
        # twin_heating = round(twout_heating,2)
        # twout_heating = round(twout_heating,2)
        # twout_cooling = round(twout_cooling,2)
        # dtw_cooling = round(dtw_cooling,2)
        
        
      
        ## TABLEAU RECAPITULATIF
        
        st.subheader("Results")
     
        
        # if qw5_heating<0.025:
        #     st.error("Water flow rate in cooling circuit is below the minimum permitted qwmin = 0.025 l/s", icon="🚨")
            
        if qw5_cooling<0.025:
            st.error("Water flow rate in cooling circuit is below the minimum permitted qwmin = 0.025 l/s", icon="🚨")
        
        if qw5_heating<0.038:
            st.error("Water flow rate in heating circuit is below the minimum permitted qwmin = 0.038 l/s", icon="🚨")
            
        # if qw_heating<0.025:
        #     st.error("Water flow rate in heating circuit is below the minimum permitted qwmin = 0.025 l/s",icon="🚨")
        
        # if qw5_heating>1.0:
        #     st.error("Water flow rate in cooling circuit is above the minimum permitted qwmin = 1.0 l/s",icon="🚨")
        
        if qw5_cooling>0.1:
            st.error("Water flow rate in cooling circuit is above the maximum permitted qwmin = 0.1 l/s",icon="🚨")
        
        if qw5_heating>0.1:
            st.error("Water flow rate in heating circuit is above the maximum permitted qwmin = 0.1 l/s",icon="🚨")
        
        # if qw_heating>1.0:
        #     st.error("Water flow rate in heating circuit is above the minimum permitted qwmin = 1.0 l/s",icon="🚨")
        
        if qw5_cooling>0.133 :
            st.error("Water flow rate in cooling circuit is above the maximum permitted qwmin = 0.133 l/s",icon="🚨")
        elif qw5_heating>0.133:
            st.error("Water flow rate in heating circuit is above the maximum permitted qwmin = 0.133 l/s",icon="🚨")
        else:
             option1 = [
            ['qa',qa,'',qa,'','(l/s)'],
            ['troom', round(troom_cooling,2),'',round(troom_heating,2),'', '(°C)'],
            ['ta',ta_cooling,'',ta_heating,'','(°C)'],
            ['tgr',round(tgr_cooling,2),'',round(tgr_heating,2),'',''],
            ['twi',round(twin_cooling,2),'',round(twin_heating,2),'','(°C)'],
            ['twout',round(twout_cooling,2),'',round(twout_heating,2),'','(°C) '],
            ['dtw','',round(abs(dtw_cooling),2),'',round(abs(dtw_heating),2), '(°C)'],
            ['dtrw','',round(dtrw_cooling,2),'',round(dtrw_heating,2),'(K)'],
            ['qw','',round(qw5_cooling,4),'',round(qw5_heating,4),'(l/s)'],
            [ 'pma', '', round(pma,2), '', round(pma,2),'(Pa)'],
            ['pw','',round(pw5_cooling,2),'',round(pw5_heating,2),'(W)'],
            ['dtra',"",round(dtra_cooling,2),"",round(dtra_heating,2), '(°C)'],
            [ 'pa','',round(pa_cooling,2),'',round(pa_heating,2), '(W)'],
            ['ptot', '', round(ptot_cooling,2),'',round(ptot_heating,2), '(W)'],
            ['DPw','',round(dpw_cooling,2),'',round(dpw_heating,2), '(kPa)']
            ]
             df1 = pd.DataFrame(option1, 
                           index = pd.Index(['Primary (Motive) air flow rate',
                                             'Reference air temperature',
                                             'Primary (Motive) air température',
                                             'Room temperature gradient',
                                             'Inlet water temperature',
                                             'Outlet water temperature',
                                             'Water temperature difference in out',
                                             'Temp. diff. room air and mean water temp ',
                                             'Water flow rate',
                                             'Motive air pressure' ,
                                             'Water side capacity',
                                             'Temp. diff. room air and primary air temp',
                                             'Air side capacity',
                                             'Total capacity',
                                             'Water pressure drop'
                                             
                                             ]),
                           columns =[' ', 'Cooling inputs','Cooling outputs','Heating inputs','Heating outputs','',])
             def highlight_col(x):
                blue = 'background-color: lightblue '
                red = 'background-color: #ffcccb'
                df2 = pd.DataFrame('', index=x.index, columns=x.columns)
                df2.iloc[:, 1:3] = blue
                df2.iloc[:, 3:5] = red
                return df2.where(df1.ne(''))
             st.dataframe(df1,
                    #  .style.apply(highlight_col,axis=None)
                    #  .format_index(axis=0),
                
                    #  .format(precision=2), 
                        #  formatter={('Reference air temperature') :"{:.2f}" },
                        # .set_table_attributes()
                    #  .format(precision=4)
                     width=1300,height=560)
        
    
    # st.write('pwtest : ',w)
    # st.write('plttest : ',PLT_cooling)
    
    # # submit button
    # st.subheader("Add new values to table")
    
    # results_option1 = pd.read_csv('results_option1.csv')
    # results_option1
    
    
    # results_option1["ref"][-1] = results_option1.max()+1
    
    # add_ref = results_option1["ref"].max()+1
    
    # add_ref = int(add_ref)
    
    # clickSubmit = st.button('Save the calculation in summmary table')
    
   
    # newdata = {'ref' : add_ref,
    #          'Primary (Motive) Air Flow Rate': qa,
    #          'Reference air temperature cooling' : troom_cooling,
    #          'Reference air temperature heating' : troom_heating,
    #          'Gradient cooling' : tgr_cooling,
    #          'Gradient heating' : tgr_heating,
    #          'Primary (Motive) Air Temperature Cooling' : dtra_cooling,
    #          'Primary (Motive) Air Temperature Heating' : dtra_heating,
    #          'Primary (Motive) Air Temperature cooling' : ta_cooling,
    #          'Primary (Motive) Air Temperature Heating' : ta_heating,
    #          'Inlet water temperature cooling' : twin_cooling,
    #          'Inlet water temperature heating' : twin_heating,
    #          'Outlet Water Temperature cooling': twout_cooling,
    #          'Outlet Water Temperature heating' : twout_heating,
    #          'Water temperature difference in out cooling' : dtw_cooling,
    #          'Water temperature difference in out heating' : dtw_heating,
    #          'Temp. diff. room air and mean water temp cooling' : dtrw_cooling,
    #          'Temp. diff. room air and mean water temp cooling' : dtrw_heating,
    #          'Water flow rate cooling' : qw5_cooling,
    #          'Water flow rate heating' : qw5_heating,
    #          'Motive air side pressure' : pma, 
    #          'Water side capacity cooling': pw5_cooling,
    #          'Water side capacity heating' : pw5_heating,
    #          'Air side capacity cooling': pa_cooling,
    #          'Air side capacity heating' : pa_heating,
    #          'Total capacity cooling' : ptot_cooling,
    #          'Total capacity heating' : ptot_heating,
    #          'Water pressure drop cooling' : dpw_cooling,
    #          'Water pressure drop heating' : dpw_heating
    #           }
         
    # d = pd.DataFrame([newdata])
    # # d
    # # d.to_csv('C:\\Users\\jarosquin\\Documents\\evost\\results_option1.csv',index=False)
         
    # results_option1 = results_option1.append(d,ignore_index=True)
    # results_option1.to_csv('results_option1.csv',index=True)
         #results_option1 = pd.concat([results_option1,d])
         #open('results_option1.csv','a').write(results_option1.to_csv())
    # else :
    #     st.markdown("Please submit to save")
    
    # st.dataframe(results_option1)
    
    # @st.cache
    # def convert_df(results_option1):
    # # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #     return results_option1.to_csv().encode('utf-8')

    # csv = convert_df(results_option1)
    
    # st.download_button(
    # label="Download data as CSV",
    # data=csv,
    # file_name='results_evost_option1.csv',
    # mime='text/csv')


    
elif option == 'Option 2 : qw - Calculate delta T from given water flow':
    
    col1,col2,col3 = st.columns([1,1,4])
    
    ### STEP 1: choose one airflow from the table, then define the water temperatures (= enter qa & twin)
    
    with col1:
        st.subheader('Select inputs')
        qa = st.number_input('Primary (Motive) air flow rate - qa (l/s)',value=16.3,min_value=7.8,max_value=16.3)
        st.markdown('**Cooling inputs**')
        troom_cooling = st.number_input('Reference Air Temperature - troom (°C)',value=26.0,step=0.1)
        tgr_cooling = st.number_input('Room Temperature Gradient -tgr °C/m)', value=0.0,step=0.1)
        ta_cooling = st.number_input('Primary (Motive) Air Temperature - ta (°C)',value=15.0,step=0.1)
        twin_cooling = st.number_input('Inlet Water Temperature - twin (°C)',value=15.0,min_value=13.0,step=0.1)
        qw_cooling = st.number_input('Water flow rate - qw (l/s)',value=0.08,step=0.01,min_value=0.038,max_value=0.1)
    with col2:
        st.title("")
        st.title("")
        st.title("")
        st.title("")
        st.title("")
        st.write("")
        st.markdown('**Heating inputs**')
        troom_heating = st.number_input('Reference Air Temperature - troom (°C)  ',value=20.0,step=0.1)
        tgr_heating = st.number_input('Room Temperature Gradient-tgr (°C/m)', value=1.0, step=0.1)
        ta_heating = st.number_input('Primary (Motive) Air Temperature - ta (°C)  ',value=20.0,step=0.1)
        twin_heating = st.number_input('Inlet Water Temperature -twin (°C)',value=55.0,min_value=30.0,step=0.1)
        qw_heating = st.number_input('Water flow rate  -qw (l/s)',value=0.08,step=0.01,max_value=0.1,min_value=0.038)
    
    
    with col3: 
        
        # CALCULS ET TABLEAU
        
        ## FORMULES
        
        # def epsilon(x):
        #     eqw = 0.588878-17.955*x+3140.21*(x**2)-125288*(x**3)+2.43832*(10**6)*(x**4)-2.57437*(10**7)*(x**5)+1.416*(10**8)*(x**6)-3.18428*(10**8)*(x**7)
        #     return eqw
        
        # def dpw_cooling_formula(x) :
        #     dpw_c = 1.25-328.673*x+36889*(x**2)-1.601*(10**6)*(x**3)+4.0005*(10**7)*(x**4)-5.50149*(10**8)*(x**5)+3.90377*(10**9)*(x**6)-1.11607*(10**10)*(x**7)
        #     return dpw_c
        
        # def dpw_heating_formula(x):
        #     dpw_h = 0.2-55*x+6473.81*(x**2)-243790*(x**3)+5.22321*(10**6)*(x**4)-6.2004*(10**7)*(x**5)+3.86905*(10**8)*(x**6)-9.92063*(10**8)*(x**7)
        #     return dpw_h
        
        ## COOLING INPUTS
        
        ### STEP 2 : Calculate Dtrw
    
        dtrw1_cooling = 8

        w = -1992.88+734.415*qa-83.8188*qa**2+4.29282*qa**3-0.0805417*qa**4
        v = -26.1552+13.5864*qa-1.74758*qa**2+0.0946072*qa**3-0.00185556*qa**4

        PLT_cooling = w / v
        eqw_ref = epsilon_cooling(qw_cooling)
    

        pw1_cooling = PLT_cooling*(dtrw1_cooling*eqw_ref/1.06)
        dtw1_cooling = pw1_cooling / (qw_cooling *4200)
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
        
        
        dtrw1_heating = 20

        # w = -1992.88+734.415*qa-83.8188*qa**2+4.29282*qa**3-0.0805417*qa**4
        
        # w = (-13224.5+4748.29*qa-612.369*(qa**2)+34.7311*(qa**3)-0.728535*(qa**4))/1.06
        
        w = 2159.35-710.505*qa+100.656*(qa**2)-5.75702*(qa**3)+0.120588*(qa**4)

        PLT_heating = w / dtrw1_heating

        eqw_ref = epsilon_heating(qw_heating)


        pw1_heating = PLT_heating*(dtrw1_heating*eqw_ref/0.7)
        dtw1_heating = pw1_heating / (qw_heating *4200)
        twout1_heating = dtw1_heating + twin_heating
        
        dtrw2_heating = troom_heating - (twin_heating + twout1_heating)/2
        pw2_heating = PLT_heating*(dtrw2_heating*eqw_ref/0.7)
        dtw2_heating = pw2_heating / (qw_heating *4200)
        twout2_heating = dtw2_heating + twin_heating

        dtrw3_heating = troom_heating - (twin_heating + twout2_heating)/2
        pw3_heating = PLT_heating*(dtrw3_heating*eqw_ref/0.7)
        dtw3_heating = pw3_heating / (qw_heating *4200)
        twout3_heating = dtw3_heating + twin_heating

        dtrw4_heating = troom_heating - (twin_heating + twout3_heating)/2
        pw4_heating = PLT_heating*(dtrw4_heating*eqw_ref/0.7)
        dtrw4_heating = pw4_heating / (qw_heating *4200)
        twout4_heating = dtrw4_heating + twin_heating

        dtrw5_heating = troom_heating - (twin_heating + twout4_heating)/2
        pw5_heating = PLT_heating*(dtrw5_heating*eqw_ref/0.7)
        dtw5_heating = pw5_heating / (qw_heating *4200)
        twout5_heating = dtw5_heating + twin_heating


        #Autres formules
        
        # dtra_cooling = (troom_cooling + tgr_cooling - ta_cooling)
        # dtra_heating = -(troom_heating + tgr_heating - ta_heating)
        dtra_cooling = (troom_cooling  - ta_cooling)
        dtra_heating = -(troom_heating  - ta_heating)
        dtra_cooling = round(dtra_cooling,2)
        dtra_heating = round(dtra_heating,2)

        dpw_cooling = dpw_cooling_formula(qw_cooling)
        dpw_heating = dpw_heating_formula(qw_heating)

        pma = 2131.77-589.557*qa+62.2699*(qa**2)-2.75638*(qa**3)+0.0463111*(qa**4)

        # pa_cooling = 1.2*qa*(troom_cooling+tgr_cooling+(dtrw5_cooling/2))
        
        pa_cooling = 1.2*qa*dtra_cooling
        pa_cooling = round(pa_cooling,2)

        pa_heating = 1.2*qa*dtra_heating
        pa_heating = round(pa_heating,2)

        ptot_cooling = pw5_cooling + pa_cooling
        ptot_heating = -pw5_heating + pa_heating
    
        qa = str(qa)
        
        st.subheader("Results")
        
        if qw_cooling<0.025:
            st.error("Water flow rate in cooling circuit is below the minimum permitted qwmin = 0.025 l/s", icon="🚨")
            
        if qw_heating<0.038:
            st.error("Water flow rate in heating circuit is below the minimum permitted qwmin = 0.025 l/s",icon="🚨")
        
        if qw_cooling>1.0:
            st.error("Water flow rate in cooling circuit is above the maximum permitted qwmin = 1.0 l/s",icon="🚨")
        
        if qw_heating>1.0:
            st.error("Water flow rate in heating circuit is above the maximum permitted qwmin = 1.0 l/s",icon="🚨")
        
        if qw_cooling>0.133 :
            st.error("Water flow rate in cooling circuit is above the maximum permitted qwmin = 0.133 l/s",icon="🚨")
        elif qw_heating>0.133:
            st.error("Water flow rate in heating circuit is above the maximum permitted qwmin = 0.133 l/s",icon="🚨")
        else:
            option2 = [
            ['qa',qa,'',qa,'', '(l/s)'],
            ['troom', round(troom_cooling,2),'',round(troom_heating,2),'', '(°C)'],
            ['ta',ta_cooling,'',ta_heating,'','(°C)'],
            ['tgr',round(tgr_cooling,2),'',round(tgr_heating,2),'',''],
            ['qw',round(qw_cooling,4),'',round(qw_heating,4),'', '(l/s)'],
            ['twi',round(twin_cooling,2),'',round(twin_heating,2),'', '(°C)'],
            ['twout','',round(twout5_cooling,2),'',round(twout5_heating,2), '(°C) '],
            ['dtw','',round(abs(dtw5_cooling),2),'',round(abs(dtw5_heating),2), '(°C)'],
            ['dtrw','',round(abs(dtrw5_cooling),2),'',round(abs(-dtrw5_heating),2),'(°C)'],
            [ 'pma', '', round(pma,2), '', round(pma,2), '(Pa)'],
            ['pw','',round(pw5_cooling,2),'',round(-pw5_heating,2), '(W)'],
            ['dtra',"",round(dtra_cooling,2),"",round(dtra_heating,2), '(°C)'],
            [ 'pa','',round(pa_cooling,2),'',round(pa_heating,2), '(W)'],
            ['ptot', '', round(ptot_cooling,2),'',round(ptot_heating,2), '(W)'],
            ['DPw','',round(dpw_cooling,2),'',round(dpw_heating,2), '(kPa)']]
            df3 = pd.DataFrame(option2, 
                           index = pd.Index(['Primary (Motive) air flow rate',
                                             'Reference air temperature',
                                             "Primary (Motive) air temperature",
                                             'Room temperature gradient',
                                             'Water flow rate',
                                             'Inlet water temperature',
                                             'Outlet water temperature',
                                             'Water temperature difference in out',
                                             'Temp. diff. room air and min water temp.',
                                             'Motive air pressure',
                                             'Water side capacity',
                                             'Temp.diff.,room air and primary air temp.',
                                             'Air side capacity',
                                             'Total capacity',
                                             'Water pressure drop']),
                           columns =[' ', 'Cooling inputs','Cooling outputs','Heating inputs','Heating outputs','     '])
            def highlight_col(x):
                blue = 'background-color: lightblue '
                red = 'background-color: #ffcccb'
                df4 = pd.DataFrame('', index=x.index, columns=x.columns)
                df4.iloc[:, 1:3] = blue
                df4.iloc[:, 3:5] = red
                return df4.where(df3.ne(''))
            st.dataframe(df3
                    #  .style.apply(highlight_col,axis=None)
                    #  .format(precision=2)
                     ,height=560,width=1300)
        
    
    
    # d = {'ref' : 1,
    #     'Water flow' : qw_cooling,
    #           'Primary Air Flow Rate': qa, 
    #           'Primary Air Temperature': dtra_cooling,
    #           'Reference Air Remperature': troom_cooling,
    #           'Room Temperature Gradient': tgrvalue_cooling,
    #           "Specific power" : PLTtest}
    
    
    # d = pd.DataFrame([d],index=[0])
    # d
    # d.to_csv('results_option2.csv')
    
    # results_option2 = pd.read_csv('results_option2.csv')
    # results_option2
    
    # add_ref = int(results_option2["ref"].max()+1)
    
    # clickSubmit = st.button('Save the calculation in summary table')
    
    # if clickSubmit == True: 
    #      newdata = {'ref' : add_ref,
    #           'Primary Air Flow Rate': qa, 
    #           'Primary Air Temperature': dtra_cooling,
    #           'Reference Air Remperature': troom_cooling,
    #           'Room Temperature Gradient': tgr_cooling,
    #           'Inlet Water Temperature': twin_cooling,
    #           "dtw" : dtw_cooling,
    #           "water flow rate" : qw3,
    #           "water side capacity" : pw3,
    #           "air side pressure" : pma}
    #      st.write(newdata)
    #      results_option2 = results_option2.append(newdata,ignore_index=True)
    #      results_option2.to_csv('results_option2.csv',index=False)
    #      #results_option1 = pd.concat([results_option1,d])
    #      #open('results_option1.csv','a').write(results_option1.to_csv())
    # else :
    #     st.markdown("Please submit to save")
    
    # st.write(results_option2)
