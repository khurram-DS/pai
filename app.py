
import streamlit as st
# Eda packages

import pandas as pd
import numpy as np

#Data viz packages

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

#function

def main():
    
    title_container1 = st.container()
    col1, col2 ,  = st.columns([6,12])
    from PIL import Image
    image = Image.open('static/asia.jpeg')
    with title_container1:
        with col1:
            st.image(image, width=200)
        with col2:
            st.markdown('<h1 style="color: purple;">ASIA Consulting</h1>',
                           unsafe_allow_html=True)
    
    st.subheader('Public Authority For Industry - Validity System For submitted Questionnaire')
    
    st.sidebar.image("static/ind.jpeg", use_column_width=True)
    activites = ["About","PAI Analysis"]
    choice =st.sidebar.selectbox("Select Activity",activites)
    def add_bg_from_url():
        st.markdown(
             f"""
             <style>
             .stApp {{
                 
                
                 
                 background-image: url("https://wallpaperaccess.com/full/1586344.jpg");
                 background-repeat: no-repeat;
                 background-size: cover;
                 background-position: center;
                 background-attachment: fixed;
                 width: 100vw;
                 height: 100vh;
                 
             }}
             </style>
             """,
             unsafe_allow_html=True
         )
    
    add_bg_from_url() 
    
    
    
    
    if choice == "About":
        
        from PIL import Image
        image = Image.open('static/PAI.jpeg')

        st.image(image, caption='Public Autority for Industry',width=600)
        st.text('© ASIA Consulting 2022')
    
    elif choice == "PAI Analysis":
        @st.cache(allow_output_mutation=True)
        def get_df(file):
          # get extension and read file
          extension = file.name.split('.')[1]
          if extension.upper() == 'CSV':
            df = pd.read_csv(file)
          elif extension.upper() == 'XLSX':
            df = pd.read_excel(file)
          
          return df
        file = st.file_uploader("Upload file", type=['csv' 
                                                 ,'xlsx'])
        if not file:
            st.write("Upload a .csv or .xlsx file to get started")
            return
          
        df = get_df(file)
        
        st.write("**Data has been loaded Successfully**")
       
        if st.checkbox('Show Raw Data'):
            st.subheader('Raw Data')
            st.write(df)
        if st.checkbox('Click to see the Table'):
            st.subheader('Table 1')
            st.subheader("التوزيع القطاعي للمنشآت الصناعية بحسب التصنيف الصناعي الدولي الموَّحد لجميع الأنشطة الاقتصادية")
            ta1=df['الأبواب'].astype(str).str.split('-',expand=True)
            tab1=pd.DataFrame({})
            tab1['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta1=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta1[1].str.replace('\d+','')
            tab1['البيان']=cl.str.strip()
            
            tab1['رأس المال (ألف دينار)']=df['إجمالي حجم رأس المال المستثمر للمنشأة الصناعية - د.ك']
            tab1['المساحة (ألف كيلو متر مربع)']=df['المساحة - متر مربع1']
                        
            ta1=tab1.groupby(['الكود (ISIC 4)','البيان']).size().reset_index(name='العدد')
            option = st.selectbox(
            'Select calculation type',
            ('Sum','Mean'))
            if option == 'Sum':
                ta1a=tab1.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','المساحة (ألف كيلو متر مربع)']].sum()
            elif option == 'Mean':
                ta1a=tab1.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','المساحة (ألف كيلو متر مربع)']].mean()
                
            ta1a.reset_index(inplace=True)
            ta1=ta1.merge(ta1a, on = ['الكود (ISIC 4)','البيان'])
            ta1.loc['إجمالي عدد المنشآت الصناعية']=ta1.sum(numeric_only=True, axis=0)
            ta1['الكود (ISIC 4)']=ta1['الكود (ISIC 4)'].replace(np.nan,'')
            ta1['البيان']=ta1['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            ta1['العدد']=ta1['العدد'].astype(int)
            
 
            ta1=ta1.reset_index(drop=True)
            
            def highlight_col(x):
                r = "background-color : #abdbe3"
                
                ta1_df= pd.DataFrame(" ", index= x.index, columns=x.columns)
                
                ta1_df.iloc[-1] = r
                
                return ta1_df
            
            st.table(ta1.style.apply(highlight_col, axis=None))
            da=ta1.style.apply(highlight_col, axis=None)
            import base64
            import io
            towrite = io.BytesIO()
            
            downloaded_file = da.to_excel(towrite, encoding='utf-8', index=False, header=True ,sheet_name='1') # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            st.text(" ")
            st.text(" ")
            st.text(" ")
            st.text(" ")
            
            st.text(" ")
            st.text(" ")
            st.text(" ")
            
            st.text(" ")
            st.text(" ")
            st.text(" ")
            st.text(" ")
            
            st.text(" ")
            st.text(" ")
            st.text(" ")
            st.text('© ASIA Consulting 2022')
                
        
            
            
            
                
            
        
        

    


        
        

if __name__=='__main__':
    main()
        
        
