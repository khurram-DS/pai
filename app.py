
import streamlit as st
# Eda packages

import pandas as pd
import numpy as np

#Data viz packages
import xlsxwriter

import matplotlib
matplotlib.use("Agg")
import base64
import io
towrite = io.BytesIO()
import plotly.express as px

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
    
    st.subheader('Public Authority For Industry')
    
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
        if st.checkbox("click to see all the Table's"):
            option = st.selectbox(
                'Select calculation type',
                ('Sum','Mean'))
            st.subheader("Note: You can Download master excel file from the Bottom of this Dashboard")     
    ######################################################################################################        
    #table1        
            ta1=df['الأبواب'].astype(str).str.split('-',expand=True)
            tab1=pd.DataFrame({})
            tab1['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta1=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta1[1].str.replace('\d+','')
            tab1['البيان']=cl.str.strip()
            
            tab1['رأس المال (ألف دينار)']=df['إجمالي حجم رأس المال المستثمر للمنشأة الصناعية - د.ك']
            tab1['المساحة (ألف كيلو متر مربع)']=df['المساحة - متر مربع1']
            tab1['الكود (ISIC 4)']=tab1['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            tab1['البيان']=tab1['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            
            ta1=tab1.groupby(['الكود (ISIC 4)','البيان']).size().reset_index(name='العدد')
            
            if option == 'Sum':
                ta1a=tab1.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','المساحة (ألف كيلو متر مربع)']].sum().round(3)
            elif option == 'Mean':
                ta1a=tab1.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','المساحة (ألف كيلو متر مربع)']].mean().round(3)
                
            ta1a.reset_index(inplace=True)
            ta1=ta1.merge(ta1a, on = ['الكود (ISIC 4)','البيان'])
            ta1.loc['إجمالي عدد المنشآت الصناعية']=ta1.sum(numeric_only=True, axis=0)
            ta1['الكود (ISIC 4)']=ta1['الكود (ISIC 4)'].replace(np.nan,'')
            ta1['البيان']=ta1['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            ta1['العدد']=ta1['العدد'].astype(np.int64,errors='ignore')
                
     
            ta1=ta1.reset_index(drop=True)
            
            def highlight_col(x):
                r = "background-color : #abdbe3"
                
                ta1_df= pd.DataFrame(" ", index= x.index, columns=x.columns)
                
                ta1_df.iloc[-1] = r
                
                return ta1_df
            da1=ta1.style.apply(highlight_col, axis=None)
            
            
            
    #table2
            ta2=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma2=pd.DataFrame({})
            ma2['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta2=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta2[1].str.replace('\d+','')
            ma2['البيان']=cl.str.strip()
            ma2['conti_type']=df['نوع المساهمة']
            ma2['total_vol_invested']=df['إجمالي حجم رأس المال المستثمر للمنشأة الصناعية - د.ك']
            ma2['الكود (ISIC 4)']=ma2['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma2['البيان']=ma2['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
 
            if option == 'Sum':
                ma2=ma2.groupby(['الكود (ISIC 4)', 'البيان', 'conti_type'])[['total_vol_invested']].sum().round(3).reset_index()
            elif option == 'Mean':
                ma2=ma2.groupby(['الكود (ISIC 4)', 'البيان', 'conti_type'])[['total_vol_invested']].mean().round(3).reset_index()
            ma2=ma2.pivot_table('total_vol_invested', ['الكود (ISIC 4)', 'البيان'], 'conti_type').round(3).reset_index()
            ma2=ma2.replace(np.nan, 0)
            ma2['الإجمالي']=ma2['حكومي']+ma2['حكومي و خاص (مشترك)']+ma2['خاص']
            tab2=pd.DataFrame({})
            tab2['الكود (ISIC 4)']=ma2['الكود (ISIC 4)']
            tab2['البيان']=ma2['البيان']
            tab2['حكومي']=ma2['حكومي']
            tab2['حكومي و خاص (مشترك)']=ma2['حكومي و خاص (مشترك)']
            tab2['خاص']=ma2['خاص']
            tab2['الإجمالي']=ma2['الإجمالي']
            tab2.loc['إجمالي المنشآت الصناعية']=tab2.sum(numeric_only=True, axis=0)
            tab2['الكود (ISIC 4)']=tab2['الكود (ISIC 4)'].replace(np.nan,'')
            tab2['البيان']=tab2['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            figu=tab2.copy()
            tab2=tab2.reset_index(drop=True)
            def highlight_col(x):
                r = "background-color : #abdbe3"
                            
                tab2_df= pd.DataFrame(" ", index= x.index, columns=x.columns)
                            
                tab2_df.iloc[-1] = r
                            
                return tab2_df
            da2=tab2.style.apply(highlight_col, axis=None)
    
  #table3
            ta3=pd.DataFrame({})
            ta3['المنطقة الصناعية']=df['موقع المنشأة المنطقة 1'].str.replace('\d+','').str.replace('-','').str.strip()
            tab3=pd.DataFrame({})
            tab3=ta3.groupby(['المنطقة الصناعية']).size().reset_index(name='عدد المنشآت')
            
            tab3['الأهمية النسبية'] = (tab3['عدد المنشآت'] / tab3['عدد المنشآت'].sum()).mul(100).round(1)
            
            tab3.sort_values(by=['عدد المنشآت'],ascending=False,inplace=True)
            tab3.reset_index(inplace = True, drop = True)
            
            tab3.loc['إجمالي عدد المنشآت الصناعية']=tab3.sum(numeric_only=True, axis=0)
            tab3['المنطقة الصناعية']=tab3['المنطقة الصناعية'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab3['عدد المنشآت']=tab3['عدد المنشآت'].astype(np.int64,errors='ignore')
            tab3=tab3.reset_index(drop=True)
            
            def highlight_col(x):
                r = "background-color : #abdbe3"
                            
                tab3_df= pd.DataFrame(" ", index= x.index, columns=x.columns)
                            
                tab3_df.iloc[-1] = r
                            
                return tab3_df
            da3=tab3.style.apply(highlight_col, axis=None)
    #table 4
    
            ta4=pd.DataFrame({})
            ta4['رأس المال (ألف دينار)']=df['إجمالي حجم رأس المال المستثمر للمنشأة الصناعية - د.ك']
            ta4['عدد العاملين الكويتيين']=df['إجمالي-كويتي']
            def get_bucket(x):
                if x <= 250000:
                    return "المنشآت الصناعية الصغيرة"
                elif x > 250000 and x <= 500000:
                    return "المنشآت الصناعية المتوسطة"
                elif x > 500000:
                    return "المنشآت الصناعية الكبيرة"    
                else:
                    return np.NaN
            ta4['البيان']=ta4['رأس المال (ألف دينار)'].apply(lambda x: get_bucket(x))
            ta4['عدد العاملين الكويتيين']=pd.to_numeric(ta4['عدد العاملين الكويتيين'], errors='coerce')
            tab4=pd.DataFrame({})
            tab4=ta4.groupby(['البيان']).size().reset_index(name='عدد المنشآت')
            if option == 'Sum':
                ta4a=ta4.groupby(['البيان'])['رأس المال (ألف دينار)'].sum()
            if option == 'Mean':
                ta4a=ta4.groupby(['البيان'])['رأس المال (ألف دينار)'].mean()
            tab4=tab4.merge(ta4a,on=['البيان'])
            if option == 'Sum':
                ta4b=ta4.groupby(['البيان'])['عدد العاملين الكويتيين'].sum()
            if option == 'Mean':
                ta4b=ta4.groupby(['البيان'])['عدد العاملين الكويتيين'].mean()
            tab4=tab4.merge(ta4b,on=['البيان'])
            tab4['عدد العاملين الكويتيين']=tab4['عدد العاملين الكويتيين'].astype(np.int64,errors='ignore')
            tab4.loc['إجمالي عدد المنشآت الصناعية']=tab4.sum(numeric_only=True, axis=0)
            tab4['البيان']=tab4['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            tab4['عدد العاملين الكويتيين']=tab4['عدد العاملين الكويتيين'].astype(np.int64,errors='ignore')
            tab4['عدد المنشآت']=tab4['عدد المنشآت'].astype(np.int64,errors='ignore')
            tab4.sort_values(by=['عدد المنشآت'],ascending=True,inplace=True)
            tab4=tab4.reset_index(drop=True)
            da4=tab4.style.apply(highlight_col, axis=None)
            
#table 5
            ta5=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma5=pd.DataFrame({})
            ma5['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta5=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta5[1].str.replace('\d+','')
            ma5['البيان']=cl.str.strip()
            ma5['رأس المال (ألف دينار)']=df['إجمالي حجم رأس المال المستثمر للمنشأة الصناعية - د.ك']
            ma5['عدد العاملين الكويتيين']=df['إجمالي-كويتي']
            ma5['عدد العاملين الكويتيين']=pd.to_numeric(ma5['عدد العاملين الكويتيين'], errors='coerce')
            ma5['الكود (ISIC 4)']=ma5['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma5['البيان']=ma5['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
 
            #data below 250k
            ta5=ma5.loc[ma5['رأس المال (ألف دينار)'] <=250000]
            tab5=pd.DataFrame({})
            tab5=ta5.groupby(['الكود (ISIC 4)','البيان']).size().reset_index(name='عدد المنشآت')
            if option == 'Sum':
                ta5a=ta5.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','عدد العاملين الكويتيين']].sum()
            if option =='Mean':
                ta5a=ta5.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','عدد العاملين الكويتيين']].mean()
                
            ta5a.reset_index(inplace=True)
            tab5=tab5.merge(ta5a, on = ['الكود (ISIC 4)','البيان'])
            tab5['عدد العاملين الكويتيين']=tab5['عدد العاملين الكويتيين'].astype(np.int64,errors='ignore')
            tab5.loc['إجمالي عدد المنشآت الصناعية الصغيرة']=tab5.sum(numeric_only=True, axis=0)
            tab5['الكود (ISIC 4)']=tab5['الكود (ISIC 4)'].replace(np.nan,'')
            tab5['البيان']=tab5['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            tab5=tab5.reset_index(drop=True)
            tab5['عدد المنشآت']=tab5['عدد المنشآت'].astype(np.int64,errors='ignore')
            tab5['رأس المال (ألف دينار)']=tab5['رأس المال (ألف دينار)'].astype(np.int64,errors='ignore')
            tab5['عدد العاملين الكويتيين']=tab5['عدد العاملين الكويتيين'].astype(np.int64,errors='ignore')
            tab5=tab5.reset_index(drop=True)
            da5=tab5.style.apply(highlight_col, axis=None)
            
            
    #table 6
            
            ta6=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma6=pd.DataFrame({})
            ma6['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta6=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta6[1].str.replace('\d+','')
            ma6['البيان']=cl.str.strip()
            ma6['رأس المال (ألف دينار)']=df['إجمالي حجم رأس المال المستثمر للمنشأة الصناعية - د.ك']
            ma6['عدد العاملين الكويتيين']=df['إجمالي-كويتي']
            ma6['عدد العاملين الكويتيين']=pd.to_numeric(ma6['عدد العاملين الكويتيين'], errors='coerce')
            ma6['الكود (ISIC 4)']=ma6['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma6['البيان']=ma6['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
 
            #data below 250k
            ta6=ma6.loc[(ma6['رأس المال (ألف دينار)'] > 250000) & (ma6['رأس المال (ألف دينار)'] <=500000)]
            tab6=pd.DataFrame({})
            tab6=ta6.groupby(['الكود (ISIC 4)','البيان']).size().reset_index(name='عدد المنشآت')
            if option == 'Sum':
                ta6a=ta6.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','عدد العاملين الكويتيين']].sum()
            if option == 'Mean':
                ta6a=ta6.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','عدد العاملين الكويتيين']].mean()
                
            ta6a.reset_index(inplace=True)
            tab6=tab6.merge(ta6a, on = ['الكود (ISIC 4)','البيان'])
            tab6['عدد العاملين الكويتيين']=tab6['عدد العاملين الكويتيين'].astype(np.int64,errors='ignore')
            tab6.loc['إجمالي عدد المنشآت الصناعية الصغيرة']=tab6.sum(numeric_only=True, axis=0)
            tab6['الكود (ISIC 4)']=tab6['الكود (ISIC 4)'].replace(np.nan,'')
            tab6['البيان']=tab6['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            tab6=tab6.reset_index(drop=True)
            tab6['عدد المنشآت']=tab6['عدد المنشآت'].astype(np.int64,errors='ignore')
            tab6['رأس المال (ألف دينار)']=tab6['رأس المال (ألف دينار)'].astype(np.int64,errors='ignore')
            tab6['عدد العاملين الكويتيين']=tab6['عدد العاملين الكويتيين'].astype(np.int64,errors='ignore')   
            tab6=tab6.reset_index(drop=True)
            da6=tab6.style.apply(highlight_col, axis=None)
            
            
            
    #table7
    
            ta7=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma7=pd.DataFrame({})
            ma7['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta7=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta7[1].str.replace('\d+','')
            ma7['البيان']=cl.str.strip()
            ma7['رأس المال (ألف دينار)']=df['إجمالي حجم رأس المال المستثمر للمنشأة الصناعية - د.ك']
            ma7['عدد العاملين الكويتيين']=df['إجمالي-كويتي']
            ma7['عدد العاملين الكويتيين']=pd.to_numeric(ma7['عدد العاملين الكويتيين'], errors='coerce')
            ma7['الكود (ISIC 4)']=ma7['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma7['البيان']=ma7['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
 
            #data below 250k
            ta7=ma7.loc[ma7['رأس المال (ألف دينار)'] > 500000]
            tab7=pd.DataFrame({})
            tab7=ta7.groupby(['الكود (ISIC 4)','البيان']).size().reset_index(name='عدد المنشآت')
            if option == 'Sum':
                ta7a=ta7.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','عدد العاملين الكويتيين']].sum()
            if option == 'Mean':
                ta7a=ta7.groupby(['الكود (ISIC 4)','البيان'])[['رأس المال (ألف دينار)','عدد العاملين الكويتيين']].mean()
            ta7a.reset_index(inplace=True)
            tab7=tab7.merge(ta7a, on = ['الكود (ISIC 4)','البيان'])
            tab7.loc['إجمالي عدد المنشآت الصناعية الصغيرة']=tab7.sum(numeric_only=True, axis=0)
            tab7['الكود (ISIC 4)']=tab7['الكود (ISIC 4)'].replace(np.nan,'')
            tab7['البيان']=tab7['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            tab7['عدد العاملين الكويتيين']=tab7['عدد العاملين الكويتيين'].astype(np.int64,errors='ignore')
            tab7=tab7.reset_index(drop=True)
            da7=tab7.style.apply(highlight_col, axis=None)
            
          #table9
            ta9=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma9=pd.DataFrame({})
            ma9['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta9=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta9[1].str.replace('\d+','')
            ma9['البيان']=cl.str.strip()
            ma9['الكود (ISIC 4)']=ma9['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma9['البيان']=ma9['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma9['2017']=df['المخزون من المنتجات النهائية في بداية السنة (الكمية) لعام 2017 للمنتج 1']-df['المخزون من المنتجات النهائية في نهاية السنة (الكمية) لعام 2017 للمنتج 1']
            ma9['2018']=df['المخزون من المنتجات النهائية في بداية السنة (الكمية) لعام 2018 للمنتج 1']-df['المخزون من المنتجات النهائية في نهاية السنة (الكمية) لعام 2018 للمنتج 1']
            ma9['2019']=df['المخزون من المنتجات النهائية في بداية السنة (الكمية) لعام 2019 للمنتج 1']-df['المخزون من المنتجات النهائية في نهاية السنة (الكمية) لعام 2019 للمنتج 1']
            ma9['2020']=df['المخزون من المنتجات النهائية في بداية السنة (الكمية) لعام 2020 للمنتج 1']-df['المخزون من المنتجات النهائية في نهاية السنة (الكمية) لعام 2020 للمنتج 1']
            tab9=pd.DataFrame({})
            if option == 'Sum':
                tab9=ma9.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            elif option == 'Mean':
                tab9=ma9.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab9.reset_index(inplace=True)
            tab9.loc['إجمالي المنشآت الصناعية']=tab9.sum(numeric_only=True, axis=0)
            tab9['الكود (ISIC 4)']=tab9['الكود (ISIC 4)'].replace(np.nan,'')
            tab9['البيان']=tab9['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            tab9=tab9.reset_index(drop=True)
            tab9['2017']=tab9['2017'].astype(np.int64,errors='ignore')
            tab9['2018']=tab9['2018'].astype(np.int64,errors='ignore')
            tab9['2019']=tab9['2019'].astype(np.int64,errors='ignore')
            tab9['2020']=tab9['2020'].astype(np.int64,errors='ignore')
            da9=tab9.style.apply(highlight_col, axis=None)
            #table19
            
            ta19=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma19=pd.DataFrame({})
            ma19['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta19=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta19[1].str.replace('\d+','')
            ma19['البيان']=cl.str.strip()
            ma19['الكود (ISIC 4)']=ma19['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma19['البيان']=ma19['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma19['2017']=df['إجمالي قيمة المواد الأولية (د.ك) لعام 2017']
            ma19['2018']=df['إجمالي قيمة المواد الأولية (د.ك) لعام 2018']
            ma19['2019']=df['إجمالي قيمة المواد الأولية (د.ك) لعام 2019']
            ma19['2020']=df['إجمالي قيمة المواد الأولية (د.ك) لعام 2020']
            tab19=pd.DataFrame({})
            if option == 'Sum':
                tab19=ma19.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab19=ma19.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab19.reset_index(inplace=True)
            tab19.loc['إجمالي المنشآت الصناعية']=tab19.sum(numeric_only=True, axis=0)
            tab19['الكود (ISIC 4)']=tab19['الكود (ISIC 4)'].replace(np.nan,'')
            tab19['البيان']=tab19['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            tab19=tab19.reset_index(drop=True)
            tab19['2017']=tab19['2017'].astype(np.int64,errors='ignore')
            tab19['2018']=tab19['2018'].astype(np.int64,errors='ignore')
            tab19['2019']=tab19['2019'].astype(np.int64,errors='ignore')
            tab19['2020']=tab19['2020'].astype(np.int64,errors='ignore')
            da19=tab19.style.apply(highlight_col, axis=None)
            #table 20
            
            ta20=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma20=pd.DataFrame({})
            ma20['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta20=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta20[1].str.replace('\d+','')
            ma20['البيان']=cl.str.strip()
            ma20['الكود (ISIC 4)']=ma20['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma20['البيان']=ma20['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma20['2017']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في بداية السنة لعام 2017']
            ma20['2018']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في بداية السنة لعام 2018']
            ma20['2019']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في بداية السنة لعام 2019']
            ma20['2020']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في بداية السنة لعام 2020']
            tab20=pd.DataFrame({})
            if option == 'Sum':
                tab20=ma20.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab20=ma20.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
                
            tab20.reset_index(inplace=True)
            tab20.loc['إجمالي المنشآت الصناعية']=tab20.sum(numeric_only=True, axis=0)
            tab20['الكود (ISIC 4)']=tab20['الكود (ISIC 4)'].replace(np.nan,'')
            tab20['البيان']=tab20['البيان'].replace(np.nan,'إجمالي عدد المنشآت الصناعية')
            tab20=tab20.reset_index(drop=True)
            tab20['2017']=tab20['2017'].astype(np.int64,errors='ignore')
            tab20['2018']=tab20['2018'].astype(np.int64,errors='ignore')
            tab20['2019']=tab20['2019'].astype(np.int64,errors='ignore')
            tab20['2020']=tab20['2020'].astype(np.int64,errors='ignore')
            da20=tab20.style.apply(highlight_col, axis=None)
            #table21
            ta21=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma21=pd.DataFrame({})
            ma21['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta21=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta21[1].str.replace('\d+','')
            ma21['البيان']=cl.str.strip()
            ma21['الكود (ISIC 4)']=ma21['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma21['البيان']=ma21['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma21['2017']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في نهاية السنة لعام 2017']
            ma21['2018']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في نهاية السنة لعام 2018']
            ma21['2019']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في نهاية السنة لعام 2019']
            ma21['2020']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في نهاية السنة لعام 2020']
            tab21=pd.DataFrame({})
            if option == 'Sum':
                tab21=ma21.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab21=ma21.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab21.reset_index(inplace=True)
            tab21.loc['إجمالي المنشآت الصناعية']=tab21.sum(numeric_only=True, axis=0)
            tab21['الكود (ISIC 4)']=tab21['الكود (ISIC 4)'].replace(np.nan,'')
            tab21['البيان']=tab21['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab21=tab21.reset_index(drop=True)
            tab21['2017']=tab21['2017'].astype(np.int64,errors='ignore')
            tab21['2018']=tab21['2018'].astype(np.int64,errors='ignore')
            tab21['2019']=tab21['2019'].astype(np.int64,errors='ignore')
            tab21['2020']=tab21['2020'].astype(np.int64,errors='ignore')
            da21=tab21.style.apply(highlight_col, axis=None)
            #table 22
            ta22=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma22=pd.DataFrame({})
            ma22['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta22=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta22[1].str.replace('\d+','')
            ma22['البيان']=cl.str.strip()
            ma22['الكود (ISIC 4)']=ma22['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma22['البيان']=ma22['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma22['2017']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في نهاية السنة لعام 2017']-df['قيمة المخزون السنوي من المواد الأولية (د.ك) في بداية السنة لعام 2017']
            ma22['2018']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في نهاية السنة لعام 2018']-df['قيمة المخزون السنوي من المواد الأولية (د.ك) في بداية السنة لعام 2018']
            ma22['2019']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في نهاية السنة لعام 2019']-df['قيمة المخزون السنوي من المواد الأولية (د.ك) في بداية السنة لعام 2019']
            ma22['2020']=df['قيمة المخزون السنوي من المواد الأولية (د.ك) في نهاية السنة لعام 2020']-df['قيمة المخزون السنوي من المواد الأولية (د.ك) في بداية السنة لعام 2020']
            tab22=pd.DataFrame({})
            if option == 'Sum':
                tab22=ma22.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab22=ma22.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            tab22.reset_index(inplace=True)
            tab22.loc['إجمالي المنشآت الصناعية']=tab22.sum(numeric_only=True, axis=0)
            tab22['الكود (ISIC 4)']=tab22['الكود (ISIC 4)'].replace(np.nan,'')
            tab22['البيان']=tab22['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab22=tab22.reset_index(drop=True)
            tab22['2017']=tab22['2017'].astype(np.int64,errors='ignore')
            tab22['2018']=tab22['2018'].astype(np.int64,errors='ignore')
            tab22['2019']=tab22['2019'].astype(np.int64,errors='ignore')
            tab22['2020']=tab22['2020'].astype(np.int64,errors='ignore')
            da22=tab22.style.apply(highlight_col, axis=None)
            #table 23
            ta23=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma23=pd.DataFrame({})
            ma23['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta23=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta23[1].str.replace('\d+','')
            ma23['البيان']=cl.str.strip()
            ma23['الكود (ISIC 4)']=ma23['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma23['البيان']=ma23['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma23['الكهرباء']=df['قيمة استهلاك كهرباء (د.ك) 2017']
            ma23['المياة العذبة']=df['قيمة استهلاك مياه عذبة (د.ك) 2017']
            ma23['الغاز الطبيعي']=df['قيمة استهلاك غاز طبيعي (د.ك) 2017']
            ma23['البنزين']=df['قيمة استهلاك بنزين (د.ك) 2017']
            ma23['الديزل']=df['قيمة استهلاك ديزل (د.ك) 2017']
            ma23['الزيوت والشحوم']=df['قيمة استهلاك زيوت وشحوم (د.ك) 2017']
            ma23['منافع أخرى']=df['قيمة استهلاك منافع أخرى (د.ك) 2017']
            ma23['الإجمالي']=ma23['الكهرباء']+ma23['المياة العذبة']+ma23['الغاز الطبيعي']+ma23['البنزين']+ma23['الديزل']+ma23['الزيوت والشحوم']+ma23['منافع أخرى']
            tab23=pd.DataFrame({})
            if option == 'Sum':
                tab23=ma23.groupby(['الكود (ISIC 4)','البيان'])[['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab23=ma23.groupby(['الكود (ISIC 4)','البيان'])[['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']].mean()
            tab23.reset_index(inplace=True)
            tab23.loc['إجمالي المنشآت الصناعية']=tab23.sum(numeric_only=True, axis=0)
            tab23['الكود (ISIC 4)']=tab23['الكود (ISIC 4)'].replace(np.nan,'')
            tab23['البيان']=tab23['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab23=tab23.reset_index(drop=True)
            cols=['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']
            tab23[cols]=tab23[cols].astype(np.int64,errors='ignore')
            da23=tab23.style.apply(highlight_col, axis=None)
            #table24
            ta24=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma24=pd.DataFrame({})
            ma24['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta24=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta24[1].str.replace('\d+','')
            ma24['البيان']=cl.str.strip()
            ma24['الكود (ISIC 4)']=ma24['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma24['البيان']=ma24['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma24['الكهرباء']=df['قيمة استهلاك كهرباء (د.ك) 2018']
            ma24['المياة العذبة']=df['قيمة استهلاك مياه عذبة (د.ك) 2018']
            ma24['الغاز الطبيعي']=df['قيمة استهلاك غاز طبيعي (د.ك) 2018']
            ma24['البنزين']=df['قيمة استهلاك بنزين (د.ك) 2018']
            ma24['الديزل']=df['قيمة استهلاك ديزل (د.ك) 2018']
            ma24['الزيوت والشحوم']=df['قيمة استهلاك زيوت وشحوم (د.ك) 2018']
            ma24['منافع أخرى']=df['قيمة استهلاك منافع أخرى (د.ك) 2018']
            ma24['الإجمالي']=ma24['الكهرباء']+ma24['المياة العذبة']+ma24['الغاز الطبيعي']+ma24['البنزين']+ma24['الديزل']+ma24['الزيوت والشحوم']+ma24['منافع أخرى']
            tab24=pd.DataFrame({})
            if option == 'Sum':
                tab24=ma24.groupby(['الكود (ISIC 4)','البيان'])[['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab24=ma24.groupby(['الكود (ISIC 4)','البيان'])[['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']].mean()
            tab24.reset_index(inplace=True)
            tab24.loc['إجمالي المنشآت الصناعية']=tab24.sum(numeric_only=True, axis=0)
            tab24['الكود (ISIC 4)']=tab24['الكود (ISIC 4)'].replace(np.nan,'')
            tab24['البيان']=tab24['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab24=tab24.reset_index(drop=True)
            cols=['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']
            tab24[cols]=tab24[cols].astype(np.int64,errors='ignore')
            da24=tab24.style.apply(highlight_col, axis=None)
            #table 25
            ta25=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma25=pd.DataFrame({})
            ma25['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta25=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta25[1].str.replace('\d+','')
            ma25['البيان']=cl.str.strip()
            ma25['الكود (ISIC 4)']=ma25['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma25['البيان']=ma25['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma25['الكهرباء']=df['قيمة استهلاك كهرباء (د.ك) 2019']
            ma25['المياة العذبة']=df['قيمة استهلاك مياه عذبة (د.ك) 2019']
            ma25['الغاز الطبيعي']=df['قيمة استهلاك غاز طبيعي (د.ك) 2019']
            ma25['البنزين']=df['قيمة استهلاك بنزين (د.ك) 2019']
            ma25['الديزل']=df['قيمة استهلاك ديزل (د.ك) 2019']
            ma25['الزيوت والشحوم']=df['قيمة استهلاك زيوت وشحوم (د.ك) 2019']
            ma25['منافع أخرى']=df['قيمة استهلاك منافع أخرى (د.ك) 2019']
            ma25['الإجمالي']=ma25['الكهرباء']+ma25['المياة العذبة']+ma25['الغاز الطبيعي']+ma25['البنزين']+ma25['الديزل']+ma25['الزيوت والشحوم']+ma25['منافع أخرى']
            tab25=pd.DataFrame({})
            if option == 'Sum':
                tab25=ma25.groupby(['الكود (ISIC 4)','البيان'])[['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab25=ma25.groupby(['الكود (ISIC 4)','البيان'])[['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']].mean()
            tab25.reset_index(inplace=True)
            tab25.loc['إجمالي المنشآت الصناعية']=tab25.sum(numeric_only=True, axis=0)
            tab25['الكود (ISIC 4)']=tab25['الكود (ISIC 4)'].replace(np.nan,'')
            tab25['البيان']=tab25['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab25=tab25.reset_index(drop=True)
            cols=['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']
            tab25[cols]=tab25[cols].astype(np.int64,errors='ignore')
            da25=tab25.style.apply(highlight_col, axis=None)
            #table 26
            ta26=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma26=pd.DataFrame({})
            ma26['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta26=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta26[1].str.replace('\d+','')
            ma26['البيان']=cl.str.strip()
            ma26['الكود (ISIC 4)']=ma26['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma26['البيان']=ma26['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma26['الكهرباء']=df['قيمة استهلاك كهرباء (د.ك) 2020']
            ma26['المياة العذبة']=df['قيمة استهلاك مياه عذبة (د.ك) 2020']
            ma26['الغاز الطبيعي']=df['قيمة استهلاك غاز طبيعي (د.ك) 2020']
            ma26['البنزين']=df['قيمة استهلاك بنزين (د.ك) 2020']
            ma26['الديزل']=df['قيمة استهلاك ديزل (د.ك) 2020']
            ma26['الزيوت والشحوم']=df['قيمة استهلاك زيوت وشحوم (د.ك) 2020']
            ma26['منافع أخرى']=df['قيمة استهلاك منافع أخرى (د.ك) 2020']
            ma26['الإجمالي']=ma26['الكهرباء']+ma26['المياة العذبة']+ma26['الغاز الطبيعي']+ma26['البنزين']+ma26['الديزل']+ma26['الزيوت والشحوم']+ma26['منافع أخرى']
            tab26=pd.DataFrame({})
            if option == 'Sum':
                tab26=ma26.groupby(['الكود (ISIC 4)','البيان'])[['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab26=ma26.groupby(['الكود (ISIC 4)','البيان'])[['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']].mean()
            tab26.reset_index(inplace=True)
            tab26.loc['إجمالي المنشآت الصناعية']=tab26.sum(numeric_only=True, axis=0)
            tab26['الكود (ISIC 4)']=tab26['الكود (ISIC 4)'].replace(np.nan,'')
            tab26['البيان']=tab26['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab26=tab26.reset_index(drop=True)
            cols=['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي']
            tab26[cols]=tab26[cols].astype(np.int64,errors='ignore')
            da26=tab26.style.apply(highlight_col, axis=None)
            # table27
            ta27=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma27=pd.DataFrame({})
            ma27['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta27=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta27[1].str.replace('\d+','')
            ma27['البيان']=cl.str.strip()
            ma27['الكود (ISIC 4)']=ma27['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma27['البيان']=ma27['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma27['2017']=df['الإجمالي (د.ك) لعام 2017']
            ma27['2018']=df['الإجمالي (د.ك) لعام 2018']
            ma27['2019']=df['الإجمالي (د.ك) لعام 2019']
            ma27['2020']=df['الإجمالي (د.ك) لعام 2020']
            tab27=pd.DataFrame({})
            if option == 'Sum':
                tab27=ma27.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab27=ma27.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab27.reset_index(inplace=True)
            tab27.loc['إجمالي المنشآت الصناعية']=tab27.sum(numeric_only=True, axis=0)
            tab27['الكود (ISIC 4)']=tab27['الكود (ISIC 4)'].replace(np.nan,'')
            tab27['البيان']=tab27['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab27=tab27.reset_index(drop=True)
            tab27['2017']=tab27['2017'].astype(np.int64,errors='ignore')
            tab27['2018']=tab27['2018'].astype(np.int64,errors='ignore')
            tab27['2019']=tab27['2019'].astype(np.int64,errors='ignore')
            tab27['2020']=tab27['2020'].astype(np.int64,errors='ignore')
            da27=tab27.style.apply(highlight_col, axis=None)
            #table28
            ta28=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma28=pd.DataFrame({})
            ma28['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta28=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta28[1].str.replace('\d+','')
            ma28['البيان']=cl.str.strip()
            ma28['الكود (ISIC 4)']=ma28['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma28['البيان']=ma28['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma28['الإيجارات']=df['تكاليف المنشأة/ الايجارات (د.ك) 2017']
            ma28['الصيانة وقطع الغيار']=df['تكاليف المنشأة/ صيانة وقطع غيار (د.ك) 2017']
            ma28['التسويق والترويج']=df['تكاليف المنشأة/ تسويق وترويج (د.ك) 2017']
            ma28['تدريب عمالة وطنية']=df['تكاليف المنشأة/ تدريب عمالة وطنية (د.ك) 2017']
            ma28['تدريب عمالة أخرى']=df['تكاليف المنشأة/ تدريب عمالة أخرى (د.ك) 2017']
            ma28['دراسات وبحوث']=df['تكاليف المنشأة/ دراسات وبحوث (د.ك) 2017']
            ma28['مصاريف إدارية']=df['تكاليف المنشأة/ مصاريف إدارية (د.ك) 2017']
            ma28['تكاليف أخرى']=df['تكاليف المنشأة/ تكاليف أخرى (د.ك) 2017']
            col=['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى']
            ma28[col]=ma28[col].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma28['الإجمالي']=ma28['الإيجارات']+ma28['الصيانة وقطع الغيار']+ma28['التسويق والترويج']+ma28['تدريب عمالة وطنية']+ma28['تدريب عمالة أخرى']+ma28['دراسات وبحوث']+ma28['مصاريف إدارية']+ma28['تكاليف أخرى']
            tab28=pd.DataFrame({})
            if option == 'Sum':
                tab28=ma28.groupby(['الكود (ISIC 4)','البيان'])[['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']].sum()
            if option == 'Mean':    
                tab28=ma28.groupby(['الكود (ISIC 4)','البيان'])[['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']].mean()
            tab28.reset_index(inplace=True)
            tab28.loc['إجمالي المنشآت الصناعية']=tab28.sum(numeric_only=True, axis=0)
            tab28['الكود (ISIC 4)']=tab28['الكود (ISIC 4)'].replace(np.nan,'')
            tab28['البيان']=tab28['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab28=tab28.reset_index(drop=True)
            cols=['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']
            tab28[cols]=tab28[cols].astype(np.int64,errors='ignore')
            da28=tab28.style.apply(highlight_col, axis=None)
            #table 29
            ta29=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma29=pd.DataFrame({})
            ma29['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta29=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta29[1].str.replace('\d+','')
            ma29['البيان']=cl.str.strip()
            ma29['الكود (ISIC 4)']=ma29['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma29['البيان']=ma29['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma29['الإيجارات']=df['تكاليف المنشأة/ الايجارات (د.ك) 2018']
            ma29['الصيانة وقطع الغيار']=df['تكاليف المنشأة/ صيانة وقطع غيار (د.ك) 2018']
            ma29['التسويق والترويج']=df['تكاليف المنشأة/ تسويق وترويج (د.ك) 2018']
            ma29['تدريب عمالة وطنية']=df['تكاليف المنشأة/ تدريب عمالة وطنية (د.ك) 2018']
            ma29['تدريب عمالة أخرى']=df['تكاليف المنشأة/ تدريب عمالة أخرى (د.ك) 2018']
            ma29['دراسات وبحوث']=df['تكاليف المنشأة/ دراسات وبحوث (د.ك) 2018']
            ma29['مصاريف إدارية']=df['تكاليف المنشأة/ مصاريف إدارية (د.ك) 2018']
            ma29['تكاليف أخرى']=df['تكاليف المنشأة/ تكاليف أخرى (د.ك) 2018']
            col=['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى']
            ma29[col]=ma29[col].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma29['الإجمالي']=ma29['الإيجارات']+ma29['الصيانة وقطع الغيار']+ma29['التسويق والترويج']+ma29['تدريب عمالة وطنية']+ma29['تدريب عمالة أخرى']+ma29['دراسات وبحوث']+ma29['مصاريف إدارية']+ma29['تكاليف أخرى']
            tab29=pd.DataFrame({})
            if option == 'Sum':
                tab29=ma29.groupby(['الكود (ISIC 4)','البيان'])[['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab29=ma29.groupby(['الكود (ISIC 4)','البيان'])[['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']].mean()
            tab29.reset_index(inplace=True)
            tab29.loc['إجمالي المنشآت الصناعية']=tab29.sum(numeric_only=True, axis=0)
            tab29['الكود (ISIC 4)']=tab29['الكود (ISIC 4)'].replace(np.nan,'')
            tab29['البيان']=tab29['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab29=tab29.reset_index(drop=True)
            cols=['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']
            tab29[cols]=tab29[cols].astype(np.int64,errors='ignore')
            da29=tab29.style.apply(highlight_col, axis=None)
            #table 30
            ta30=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma30=pd.DataFrame({})
            ma30['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta30=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta30[1].str.replace('\d+','')
            ma30['البيان']=cl.str.strip()
            ma30['الكود (ISIC 4)']=ma30['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma30['البيان']=ma30['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma30['الإيجارات']=df['تكاليف المنشأة/ الايجارات (د.ك) 2019']
            ma30['الصيانة وقطع الغيار']=df['تكاليف المنشأة/ صيانة وقطع غيار (د.ك) 2019']
            ma30['التسويق والترويج']=df['تكاليف المنشأة/ تسويق وترويج (د.ك) 2019']
            ma30['تدريب عمالة وطنية']=df['تكاليف المنشأة/ تدريب عمالة وطنية (د.ك) 2019']
            ma30['تدريب عمالة أخرى']=df['تكاليف المنشأة/ تدريب عمالة أخرى (د.ك) 2019']
            ma30['دراسات وبحوث']=df['تكاليف المنشأة/ دراسات وبحوث (د.ك) 2019']
            ma30['مصاريف إدارية']=df['تكاليف المنشأة/ مصاريف إدارية (د.ك) 2019']
            ma30['تكاليف أخرى']=df['تكاليف المنشأة/ تكاليف أخرى (د.ك) 2019']
            col=['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى']
            ma30[col]=ma30[col].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma30['الإجمالي']=ma30['الإيجارات']+ma30['الصيانة وقطع الغيار']+ma30['التسويق والترويج']+ma30['تدريب عمالة وطنية']+ma30['تدريب عمالة أخرى']+ma30['دراسات وبحوث']+ma30['مصاريف إدارية']+ma30['تكاليف أخرى']
            tab30=pd.DataFrame({})
            if option == 'Sum':
                tab30=ma30.groupby(['الكود (ISIC 4)','البيان'])[['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']].sum()
            if option == 'Mean':    
                tab30=ma30.groupby(['الكود (ISIC 4)','البيان'])[['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']].mean()
            tab30.reset_index(inplace=True)
            tab30.loc['إجمالي المنشآت الصناعية']=tab30.sum(numeric_only=True, axis=0)
            tab30['الكود (ISIC 4)']=tab30['الكود (ISIC 4)'].replace(np.nan,'')
            tab30['البيان']=tab30['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab30=tab30.reset_index(drop=True)
            cols=['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']
            tab30[cols]=tab30[cols].astype(np.int64,errors='ignore')
            da30=tab30.style.apply(highlight_col, axis=None)
            # table31
            ta31=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma31=pd.DataFrame({})
            ma31['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta31=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta31[1].str.replace('\d+','')
            ma31['البيان']=cl.str.strip()
            ma31['الكود (ISIC 4)']=ma31['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma31['البيان']=ma31['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma31['الإيجارات']=df['تكاليف المنشأة/ الايجارات (د.ك) 2020']
            ma31['الصيانة وقطع الغيار']=df['تكاليف المنشأة/ صيانة وقطع غيار (د.ك) 2020']
            ma31['التسويق والترويج']=df['تكاليف المنشأة/ تسويق وترويج (د.ك) 2020']
            ma31['تدريب عمالة وطنية']=df['تكاليف المنشأة/ تدريب عمالة وطنية (د.ك) 2020']
            ma31['تدريب عمالة أخرى']=df['تكاليف المنشأة/ تدريب عمالة أخرى (د.ك) 2020']
            ma31['دراسات وبحوث']=df['تكاليف المنشأة/ دراسات وبحوث (د.ك) 2020']
            ma31['مصاريف إدارية']=df['تكاليف المنشأة/ مصاريف إدارية (د.ك) 2020']
            ma31['تكاليف أخرى']=df['تكاليف المنشأة/ تكاليف أخرى (د.ك) 2020']
            col=['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى']
            ma31[col]=ma31[col].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma31['الإجمالي']=ma31['الإيجارات']+ma31['الصيانة وقطع الغيار']+ma31['التسويق والترويج']+ma31['تدريب عمالة وطنية']+ma31['تدريب عمالة أخرى']+ma31['دراسات وبحوث']+ma31['مصاريف إدارية']+ma31['تكاليف أخرى']
            tab31=pd.DataFrame({})
            if option == 'Sum':
                tab31=ma31.groupby(['الكود (ISIC 4)','البيان'])[['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']].sum()
            if option == 'Mean':    
                tab31=ma31.groupby(['الكود (ISIC 4)','البيان'])[['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']].mean()    
            tab31.reset_index(inplace=True)
            tab31.loc['إجمالي المنشآت الصناعية']=tab31.sum(numeric_only=True, axis=0)
            tab31['الكود (ISIC 4)']=tab31['الكود (ISIC 4)'].replace(np.nan,'')
            tab31['البيان']=tab31['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab31=tab31.reset_index(drop=True)
            cols=['الإيجارات','الصيانة وقطع الغيار','التسويق والترويج','تدريب عمالة وطنية','تدريب عمالة أخرى','دراسات وبحوث','مصاريف إدارية','تكاليف أخرى','الإجمالي']
            tab31[cols]=tab31[cols].astype(np.int64,errors='ignore')
            da31=tab31.style.apply(highlight_col, axis=None)
            # table32
            ta32=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma32=pd.DataFrame({})
            ma32['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta32=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta32[1].str.replace('\d+','')
            ma32['البيان']=cl.str.strip()
            ma32['الكود (ISIC 4)']=ma32['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma32['البيان']=ma32['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma32['2017']=df['تكاليف المنشأة/الإجمالي (د.ك) لعام 2017']
            ma32['2018']=df['تكاليف المنشأة/الإجمالي (د.ك) لعام 2018']
            ma32['2019']=df['تكاليف المنشأة/الإجمالي (د.ك) لعام 2019']
            ma32['2020']=df['تكاليف المنشأة/الإجمالي (د.ك) لعام 2020']
            col32=['2017','2018','2019','2020']
            ma32[col32]=ma32[col32].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            tab32=pd.DataFrame({})
            if option == 'Sum':
                tab32=ma32.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab32=ma32.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab32.reset_index(inplace=True)
            tab32.loc['إجمالي المنشآت الصناعية']=tab32.sum(numeric_only=True, axis=0)
            tab32['الكود (ISIC 4)']=tab32['الكود (ISIC 4)'].replace(np.nan,'')
            tab32['البيان']=tab32['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab32=tab32.reset_index(drop=True)
            tab32['2017']=tab32['2017'].astype(np.int64,errors='ignore')
            tab32['2018']=tab32['2018'].astype(np.int64,errors='ignore')
            tab32['2019']=tab32['2019'].astype(np.int64,errors='ignore')
            tab32['2020']=tab32['2020'].astype(np.int64,errors='ignore')
            da32=tab32.style.apply(highlight_col, axis=None)
            # table10
            ta10=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma10=pd.DataFrame({})
            ma10['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta10=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta10[1].str.replace('\d+','')
            ma10['البيان']=cl.str.strip()
            ma10['الكود (ISIC 4)']=ma10['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma10['البيان']=ma10['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma10['2017']=ma19['2017']+ma22['2017']+ma27['2017']+ma32['2017']
            ma10['2018']=ma19['2018']+ma22['2018']+ma27['2018']+ma32['2018']
            ma10['2019']=ma19['2019']+ma22['2019']+ma27['2019']+ma32['2019']
            ma10['2020']=ma19['2020']+ma22['2020']+ma27['2020']+ma32['2020']
            col10=['2017','2018','2019','2020']
            ma10[col10]=ma10[col10].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int,errors='ignore')
            tab10=pd.DataFrame({})
            if option == 'Sum':
                tab10=ma10.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab10=ma10.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab10.reset_index(inplace=True)
            tab10.loc['إجمالي المنشآت الصناعية']=tab10.sum(numeric_only=True, axis=0)
            tab10['الكود (ISIC 4)']=tab10['الكود (ISIC 4)'].replace(np.nan,'')
            tab10['البيان']=tab10['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab10=tab10.reset_index(drop=True)
            tab10['2017']=tab10['2017'].astype(np.int64,errors='ignore')
            tab10['2018']=tab10['2018'].astype(np.int64,errors='ignore')
            tab10['2019']=tab10['2019'].astype(np.int64,errors='ignore')
            tab10['2020']=tab10['2020'].astype(np.int64,errors='ignore')
            da10=tab10.style.apply(highlight_col, axis=None)
            # table 8
            ta8=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma8=pd.DataFrame({})
            ma8['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta8=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta8[1].str.replace('\d+','')
            ma8['البيان']=cl.str.strip()
            ma8['الكود (ISIC 4)']=ma8['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma8['البيان']=ma8['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma8['2017']=ma10['2017']-ma9['2017']
            ma8['2018']=ma10['2018']-ma9['2018']
            ma8['2019']=ma10['2019']-ma9['2019']
            ma8['2020']=ma10['2020']-ma9['2020']
            col8=['2017','2018','2019','2020']
            ma8[col8]=ma8[col8].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int,errors='ignore')
            tab8=pd.DataFrame({})
            if option == 'Sum':
                tab8=ma8.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab8=ma8.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab8.reset_index(inplace=True)
            tab8.loc['إجمالي المنشآت الصناعية']=tab8.sum(numeric_only=True, axis=0)
            tab8['الكود (ISIC 4)']=tab8['الكود (ISIC 4)'].replace(np.nan,'')
            tab8['البيان']=tab8['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab8=tab8.reset_index(drop=True)
            tab8['2017']=tab8['2017'].astype(np.int64,errors='ignore')
            tab8['2018']=tab8['2018'].astype(np.int64,errors='ignore')
            tab8['2019']=tab8['2019'].astype(np.int64,errors='ignore')
            tab8['2020']=tab8['2020'].astype(np.int64,errors='ignore')
            da8=tab8.style.apply(highlight_col, axis=None)
            # table11
            ta11=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma11=pd.DataFrame({})
            ma11['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta11=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta11[1].str.replace('\d+','')
            ma11['البيان']=cl.str.strip()
            ma11['الكود (ISIC 4)']=ma11['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma11['البيان']=ma11['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma11['التسويق المحلي']=df['إجمالي المبيعات لعام 2017 للمنتج 12 د.ك ']
            ma11['التسويق الحكومي']=df['المبيعات المحلية/حكومي لعام 2017 للمنتج 12 د.ك ']
            ma11['التصدير الخليجي']=df['المبيعات الخارجية/خليجي لعام 2017 للمنتج 12 د.ك ']
            ma11['التصدير العربي']=df['المبيعات الخارجية/عربي لعام 2017 للمنتج 12 د.ك ']
            ma11['التصدير الدولي']=df['المبيعات الخارجية/دولي لعام 2017 للمنتج 12 د.ك ']
            col11=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي']
            ma11[col11]=ma11[col11].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma11['الإجمالي']=ma11['التسويق المحلي']+ma11['التسويق الحكومي']+ma11['التصدير الخليجي']+ma11['التصدير العربي']+ma11['التصدير الدولي']
            if option == 'Sum':
                tab11=ma11.groupby(['الكود (ISIC 4)','البيان'])[['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']].sum()
            if option == 'Mean':
                tab11=ma11.groupby(['الكود (ISIC 4)','البيان'])[['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']].mean()
            tab11.reset_index(inplace=True)
            tab11.loc['إجمالي المنشآت الصناعية']=tab11.sum(numeric_only=True, axis=0)
            tab11['الكود (ISIC 4)']=tab11['الكود (ISIC 4)'].replace(np.nan,'')
            tab11['البيان']=tab11['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab11=tab11.reset_index(drop=True)
            col11=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']
            tab11[col11]=tab11[col11].astype(np.int64,errors='ignore')
            da11=tab11.style.apply(highlight_col, axis=None)
            # table12
            ta12=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma12=pd.DataFrame({})
            ma12['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta12=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta12[1].str.replace('\d+','')
            ma12['البيان']=cl.str.strip()
            ma12['الكود (ISIC 4)']=ma12['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma12['البيان']=ma12['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma12['التسويق المحلي']=df['إجمالي المبيعات لعام 2018 للمنتج 12 د.ك ']
            ma12['التسويق الحكومي']=df['المبيعات المحلية/حكومي لعام 2018 للمنتج 12 د.ك ']
            ma12['التصدير الخليجي']=df['المبيعات الخارجية/خليجي لعام 2018 للمنتج 12 د.ك ']
            ma12['التصدير العربي']=df['المبيعات الخارجية/عربي لعام 2018 للمنتج 12 د.ك ']
            ma12['التصدير الدولي']=df['المبيعات الخارجية/دولي لعام 2018 للمنتج 12 د.ك ']
            col12=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي']
            ma12[col12]=ma12[col12].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma12['الإجمالي']=ma12['التسويق المحلي']+ma12['التسويق الحكومي']+ma12['التصدير الخليجي']+ma12['التصدير العربي']+ma12['التصدير الدولي']
            if option == 'Sum':
                tab12=ma12.groupby(['الكود (ISIC 4)','البيان'])[['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']].sum()
            if option == 'Mean':
                tab12=ma12.groupby(['الكود (ISIC 4)','البيان'])[['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']].mean()
            tab12.reset_index(inplace=True)
            tab12.loc['إجمالي المنشآت الصناعية']=tab12.sum(numeric_only=True, axis=0)
            tab12['الكود (ISIC 4)']=tab12['الكود (ISIC 4)'].replace(np.nan,'')
            tab12['البيان']=tab12['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab12=tab12.reset_index(drop=True)
            col12=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']
            tab12[col12]=tab12[col12].astype(np.int64,errors='ignore')
            da12=tab12.style.apply(highlight_col, axis=None)
            # table13
            ta13=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma13=pd.DataFrame({})
            ma13['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta13=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta13[1].str.replace('\d+','')
            ma13['البيان']=cl.str.strip()
            ma13['الكود (ISIC 4)']=ma13['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma13['البيان']=ma13['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma13['التسويق المحلي']=df['إجمالي المبيعات لعام 2019 للمنتج 12 د.ك ']
            ma13['التسويق الحكومي']=df['المبيعات المحلية/حكومي لعام 2019 للمنتج 12 د.ك ']
            ma13['التصدير الخليجي']=df['المبيعات الخارجية/خليجي لعام 2019 للمنتج 12 د.ك ']
            ma13['التصدير العربي']=df['المبيعات الخارجية/عربي لعام 2019 للمنتج 12 د.ك ']
            ma13['التصدير الدولي']=df['المبيعات الخارجية/دولي لعام 2019 للمنتج 12 د.ك ']
            col13=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي']
            ma13[col13]=ma13[col13].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma13['الإجمالي']=ma13['التسويق المحلي']+ma13['التسويق الحكومي']+ma13['التصدير الخليجي']+ma13['التصدير العربي']+ma13['التصدير الدولي']
            if option == 'Sum':
                tab13=ma13.groupby(['الكود (ISIC 4)','البيان'])[['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']].sum()
            if option == 'Mean':    
                tab13=ma13.groupby(['الكود (ISIC 4)','البيان'])[['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']].mean()
            tab13.reset_index(inplace=True)
            tab13.loc['إجمالي المنشآت الصناعية']=tab13.sum(numeric_only=True, axis=0)
            tab13['الكود (ISIC 4)']=tab13['الكود (ISIC 4)'].replace(np.nan,'')
            tab13['البيان']=tab13['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab13=tab13.reset_index(drop=True)
            col13=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']
            tab13[col13]=tab13[col13].astype(np.int64,errors='ignore')
            da13=tab13.style.apply(highlight_col, axis=None)
            # table14
            ta14=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma14=pd.DataFrame({})
            ma14['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta14=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta14[1].str.replace('\d+','')
            ma14['البيان']=cl.str.strip()
            ma14['الكود (ISIC 4)']=ma14['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma14['البيان']=ma14['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma14['التسويق المحلي']=df['إجمالي المبيعات لعام 2020 للمنتج 12 د.ك ']
            ma14['التسويق الحكومي']=df['المبيعات المحلية/حكومي لعام 2020 للمنتج 12 د.ك ']
            ma14['التصدير الخليجي']=df['المبيعات الخارجية/خليجي لعام 2020 للمنتج 12 د.ك ']
            ma14['التصدير العربي']=df['المبيعات الخارجية/عربي لعام 2020 للمنتج 12 د.ك ']
            ma14['التصدير الدولي']=df['المبيعات الخارجية/دولي لعام 2020 للمنتج 12 د.ك ']
            col14=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي']
            ma14[col14]=ma14[col14].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma14['الإجمالي']=ma14['التسويق المحلي']+ma14['التسويق الحكومي']+ma14['التصدير الخليجي']+ma14['التصدير العربي']+ma14['التصدير الدولي']
            if option == 'Sum':
                tab14=ma14.groupby(['الكود (ISIC 4)','البيان'])[['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']].sum()
            if option == 'Mean':    
                tab14=ma14.groupby(['الكود (ISIC 4)','البيان'])[['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']].mean()
            tab14.reset_index(inplace=True)
            tab14.loc['إجمالي المنشآت الصناعية']=tab14.sum(numeric_only=True, axis=0)
            tab14['الكود (ISIC 4)']=tab14['الكود (ISIC 4)'].replace(np.nan,'')
            tab14['البيان']=tab14['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab14=tab14.reset_index(drop=True)
            col14=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي']
            tab14[col14]=tab14[col14].astype(np.int64,errors='ignore')
            da14=tab14.style.apply(highlight_col, axis=None)
            # table15
            ta15=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma15=pd.DataFrame({})
            ma15['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta15=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta15[1].str.replace('\d+','')
            ma15['البيان']=cl.str.strip()
            ma15['الكود (ISIC 4)']=ma15['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma15['البيان']=ma15['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma15['2017']=ma11['الإجمالي']
            ma15['2018']=ma12['الإجمالي']
            ma15['2019']=ma13['الإجمالي']
            ma15['2020']=ma14['الإجمالي']
            col15=['2017','2018','2019','2020']
            ma15[col15]=ma15[col15].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            tab15=pd.DataFrame({})
            if option == 'Sum':
                tab15=ma15.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab15=ma15.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab15.reset_index(inplace=True)
            tab15.loc['إجمالي المنشآت الصناعية']=tab15.sum(numeric_only=True, axis=0)
            tab15['الكود (ISIC 4)']=tab15['الكود (ISIC 4)'].replace(np.nan,'')
            tab15['البيان']=tab15['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab15=tab15.reset_index(drop=True)
            tab15['2017']=tab15['2017'].astype(np.int64,errors='ignore')
            tab15['2018']=tab15['2018'].astype(np.int64,errors='ignore')
            tab15['2019']=tab15['2019'].astype(np.int64,errors='ignore')
            tab15['2020']=tab15['2020'].astype(np.int64,errors='ignore')
            da15=tab15.style.apply(highlight_col, axis=None)
            # table 16
            ta16=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma16=pd.DataFrame({})
            ma16['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta16=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta16[1].str.replace('\d+','')
            ma16['البيان']=cl.str.strip()
            ma16['الكود (ISIC 4)']=ma16['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma16['البيان']=ma16['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma16['مواد خام']=df['مواد خام/قيمة المادة الأولية (د.ك) لعام 2020']
            ma16['مواد نصف مصنعة']=df['مواد نصف مصنعة/قيمة المادة الأولية (د.ك) لعام 2020']
            ma16['مواد مصنعة']=df['مواد مصنعة/قيمة المادة الأولية (د.ك) لعام 2020']
            ma16['مواد تعبئة وتغليف']=df['مواد تعبئة وتغليف/قيمة المادة الأولية (د.ك) لعام 2020']
            col16=['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف']
            ma16[col16]=ma16[col16].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma16['الإجمالي']=ma16['مواد خام']+ma16['مواد نصف مصنعة']+ma16['مواد مصنعة']+ma16['مواد تعبئة وتغليف']
            if option == 'Sum':
                tab16=ma16.groupby(['الكود (ISIC 4)','البيان'])[['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']].sum()
            if option == 'Mean':    
                tab16=ma16.groupby(['الكود (ISIC 4)','البيان'])[['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']].mean()
            tab16.reset_index(inplace=True)
            tab16.loc['إجمالي المنشآت الصناعية']=tab16.sum(numeric_only=True, axis=0)
            tab16['الكود (ISIC 4)']=tab16['الكود (ISIC 4)'].replace(np.nan,'')
            tab16['البيان']=tab16['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab16=tab16.reset_index(drop=True)
            col16=['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']
            tab16[col16]=tab16[col16].astype(np.int64,errors='ignore')
            da16=tab16.style.apply(highlight_col, axis=None)
            #table17
            ta17=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma17=pd.DataFrame({})
            ma17['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta17=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta17[1].str.replace('\d+','')
            ma17['البيان']=cl.str.strip()
            ma17['الكود (ISIC 4)']=ma17['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma17['البيان']=ma17['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma17['مواد خام']=df['مواد خام/منتج كويتي (د.ك) لعام 2020']
            ma17['مواد نصف مصنعة']=df['مواد نصف مصنعة/منتج كويتي (د.ك) لعام 2020']
            ma17['مواد مصنعة']=df['مواد مصنعة/منتج كويتي (د.ك) لعام 2020']
            ma17['مواد تعبئة وتغليف']=df['مواد تعبئة وتغليف/قيمة المادة الأولية (د.ك) لعام 2020']
            col17=['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف']
            ma17[col17]=ma17[col17].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma17['الإجمالي']=ma17['مواد خام']+ma17['مواد نصف مصنعة']+ma17['مواد مصنعة']+ma17['مواد تعبئة وتغليف']
            if option == 'Sum':
                tab17=ma17.groupby(['الكود (ISIC 4)','البيان'])[['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']].sum()
            if option == 'Mean':    
                tab17=ma17.groupby(['الكود (ISIC 4)','البيان'])[['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']].mean()
            tab17.reset_index(inplace=True)
            tab17.loc['إجمالي المنشآت الصناعية']=tab17.sum(numeric_only=True, axis=0)
            tab17['الكود (ISIC 4)']=tab17['الكود (ISIC 4)'].replace(np.nan,'')
            tab17['البيان']=tab17['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab17=tab17.reset_index(drop=True)
            col17=['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']
            tab17[col17]=tab17[col17].astype(np.int64,errors='ignore')
            da17=tab17.style.apply(highlight_col, axis=None)
            # table18
            ta18=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma18=pd.DataFrame({})
            ma18['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta18=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta18[1].str.replace('\d+','')
            ma18['البيان']=cl.str.strip()
            ma18['الكود (ISIC 4)']=ma18['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma18['البيان']=ma18['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma18['مواد خام']=df['مواد خام/منتج مستورد (د.ك) لعام 2020']
            ma18['مواد نصف مصنعة']=df['مواد نصف مصنعة/منتج مستورد (د.ك) لعام 2020']
            ma18['مواد مصنعة']=df['مواد مصنعة/منتج مستورد (د.ك) لعام 2020']
            ma18['مواد تعبئة وتغليف']=df['مواد تعبئة وتغليف/منتج مستورد (د.ك) لعام 2020']
            col18=['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف']
            ma18[col18]=ma18[col18].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma18['الإجمالي']=ma18['مواد خام']+ma18['مواد نصف مصنعة']+ma18['مواد مصنعة']+ma18['مواد تعبئة وتغليف']
            if option == 'Sum':
                tab18=ma18.groupby(['الكود (ISIC 4)','البيان'])[['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']].sum()
            if option == 'Mean':      
                tab18=ma18.groupby(['الكود (ISIC 4)','البيان'])[['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']].mean()
            tab18.reset_index(inplace=True)
            tab18.loc['إجمالي المنشآت الصناعية']=tab18.sum(numeric_only=True, axis=0)
            tab18['الكود (ISIC 4)']=tab18['الكود (ISIC 4)'].replace(np.nan,'')
            tab18['البيان']=tab18['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab18=tab18.reset_index(drop=True)
            col18=['مواد خام','مواد نصف مصنعة','مواد مصنعة','مواد تعبئة وتغليف','الإجمالي']
            tab18[col18]=tab18[col18].astype(np.int64,errors='ignore')
            da18=tab18.style.apply(highlight_col, axis=None)
            # table33
            ta33=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma33=pd.DataFrame({})
            ma33['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta33=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta33[1].str.replace('\d+','')
            ma33['البيان']=cl.str.strip()
            ma33['الكود (ISIC 4)']=ma33['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma33['البيان']=ma33['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma33['المباني']=df['قيمة أصـول المباني (د.ك) لعام 2017']
            ma33['الآلات والمعدات']=df['قيمة أصـول آلات ومعدات (د.ك) لعام 2017']
            ma33['وسائل النقل']=df['قيمة أصـول وسائل نقل (د.ك) لعام 2017']
            ma33['أخرى']=df['قيمة أصـول أخرى (د.ك) لعام 2017']
            col33=['المباني','الآلات والمعدات','وسائل النقل','أخرى']
            ma33[col33]=ma33[col33].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma33['الإجمالي']=ma33['المباني']+ma33['الآلات والمعدات']+ma33['وسائل النقل']+ma33['أخرى']
            if option == 'Sum':
                tab33=ma33.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab33=ma33.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].mean()    
            tab33.reset_index(inplace=True)
            tab33.loc['إجمالي المنشآت الصناعية']=tab33.sum(numeric_only=True, axis=0)
            tab33['الكود (ISIC 4)']=tab33['الكود (ISIC 4)'].replace(np.nan,'')
            tab33['البيان']=tab33['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab33=tab33.reset_index(drop=True)
            col33=['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']
            tab33[col33]=tab33[col33].astype(np.int64,errors='ignore')
            da33=tab33.style.apply(highlight_col, axis=None)
            #table34
            ta34=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma34=pd.DataFrame({})
            ma34['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta34=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta34[1].str.replace('\d+','')
            ma34['البيان']=cl.str.strip()
            ma34['الكود (ISIC 4)']=ma34['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma34['البيان']=ma34['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma34['المباني']=df['قيمة أصـول المباني (د.ك) لعام 2018']
            ma34['الآلات والمعدات']=df['قيمة أصـول آلات ومعدات (د.ك) لعام 2018']
            ma34['وسائل النقل']=df['قيمة أصـول وسائل نقل (د.ك) لعام 2018']
            ma34['أخرى']=df['قيمة أصـول أخرى (د.ك) لعام 2018']
            col34=['المباني','الآلات والمعدات','وسائل النقل','أخرى']
            ma34[col34]=ma34[col34].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma34['الإجمالي']=ma34['المباني']+ma34['الآلات والمعدات']+ma34['وسائل النقل']+ma34['أخرى']
            if option == 'Sum':
                tab34=ma34.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].sum()
            if option == 'Mean':   
                tab34=ma34.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].mean()
            tab34.reset_index(inplace=True)
            tab34.loc['إجمالي المنشآت الصناعية']=tab34.sum(numeric_only=True, axis=0)
            tab34['الكود (ISIC 4)']=tab34['الكود (ISIC 4)'].replace(np.nan,'')
            tab34['البيان']=tab34['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab34=tab34.reset_index(drop=True)
            col34=['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']
            tab34[col34]=tab34[col34].astype(np.int64,errors='ignore')
            da34=tab34.style.apply(highlight_col, axis=None)
            # table35
            ta35=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma35=pd.DataFrame({})
            ma35['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta35=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta35[1].str.replace('\d+','')
            ma35['البيان']=cl.str.strip()
            ma35['الكود (ISIC 4)']=ma35['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma35['البيان']=ma35['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma35['المباني']=df['قيمة أصـول المباني (د.ك) لعام 2019']
            ma35['الآلات والمعدات']=df['قيمة أصـول آلات ومعدات (د.ك) لعام 2019']
            ma35['وسائل النقل']=df['قيمة أصـول وسائل نقل (د.ك) لعام 2019']
            ma35['أخرى']=df['قيمة أصـول أخرى (د.ك) لعام 2019']
            col35=['المباني','الآلات والمعدات','وسائل النقل','أخرى']
            ma35[col35]=ma35[col35].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma35['الإجمالي']=ma35['المباني']+ma35['الآلات والمعدات']+ma35['وسائل النقل']+ma35['أخرى']
            if option == 'Sum':
                tab35=ma35.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].sum()
            if option == 'Mean':    
                tab35=ma35.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].mean()
            tab35.reset_index(inplace=True)
            tab35.loc['إجمالي المنشآت الصناعية']=tab35.sum(numeric_only=True, axis=0)
            tab35['الكود (ISIC 4)']=tab35['الكود (ISIC 4)'].replace(np.nan,'')
            tab35['البيان']=tab35['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab35=tab35.reset_index(drop=True)
            col35=['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']
            tab35[col35]=tab35[col35].astype(np.int64,errors='ignore')
            da35=tab35.style.apply(highlight_col, axis=None)
            #table36
            ta36=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma36=pd.DataFrame({})
            ma36['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta36=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta36[1].str.replace('\d+','')
            ma36['البيان']=cl.str.strip()
            ma36['الكود (ISIC 4)']=ma36['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma36['البيان']=ma36['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma36['المباني']=df['قيمة أصـول المباني (د.ك) لعام 2020']
            ma36['الآلات والمعدات']=df['قيمة أصـول آلات ومعدات (د.ك) لعام 2020']
            ma36['وسائل النقل']=df['قيمة أصـول وسائل نقل (د.ك) لعام 2020']
            ma36['أخرى']=df['قيمة أصـول أخرى (د.ك) لعام 2020']
            col36=['المباني','الآلات والمعدات','وسائل النقل','أخرى']
            ma36[col36]=ma36[col36].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma36['الإجمالي']=ma36['المباني']+ma36['الآلات والمعدات']+ma36['وسائل النقل']+ma36['أخرى']
            if option == 'Sum':
                tab36=ma36.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab36=ma36.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].mean()
            tab36.reset_index(inplace=True)
            tab36.loc['إجمالي المنشآت الصناعية']=tab36.sum(numeric_only=True, axis=0)
            tab36['الكود (ISIC 4)']=tab36['الكود (ISIC 4)'].replace(np.nan,'')
            tab36['البيان']=tab36['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab36=tab36.reset_index(drop=True)
            col36=['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']
            tab36[col36]=tab36[col36].astype(np.int64,errors='ignore')
            da36=tab36.style.apply(highlight_col, axis=None)
            #table 37
            ta37=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma37=pd.DataFrame({})
            ma37['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta37=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta37[1].str.replace('\d+','')
            ma37['البيان']=cl.str.strip()
            ma37['الكود (ISIC 4)']=ma37['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma37['البيان']=ma37['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma37['2017']=ma33['الإجمالي']
            ma37['2018']=ma34['الإجمالي']
            ma37['2019']=ma35['الإجمالي']
            ma37['2020']=ma36['الإجمالي']
            col15=['2017','2018','2019','2020']
            ma37[col15]=ma37[col15].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            tab37=pd.DataFrame({})
            if option == 'Sum':
                tab37=ma37.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab37=ma37.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab37.reset_index(inplace=True)
            tab37.loc['إجمالي المنشآت الصناعية']=tab37.sum(numeric_only=True, axis=0)
            tab37['الكود (ISIC 4)']=tab37['الكود (ISIC 4)'].replace(np.nan,'')
            tab37['البيان']=tab37['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab37=tab37.reset_index(drop=True)
            tab37['2017']=tab37['2017'].astype(np.int64,errors='ignore')
            tab37['2018']=tab37['2018'].astype(np.int64,errors='ignore')
            tab37['2019']=tab37['2019'].astype(np.int64,errors='ignore')
            tab37['2020']=tab37['2020'].astype(np.int64,errors='ignore')
            da37=tab37.style.apply(highlight_col, axis=None)
            # table 38
            ta38=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma38=pd.DataFrame({})
            ma38['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta38=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta38[1].str.replace('\d+','')
            ma38['البيان']=cl.str.strip()
            ma38['الكود (ISIC 4)']=ma38['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma38['البيان']=ma38['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma38['المباني']=df['قيمة الإنفاق على المباني (د.ك) لعام 2017']
            ma38['الآلات والمعدات']=df['قيمة الإنفاق على الآلات ومعدات (د.ك) لعام 2017']
            ma38['وسائل النقل']=df['قيمة الإنفاق على وسائل النقل (د.ك) لعام 2017']
            ma38['أخرى']=df['إنفاقات أخرى لزيادة الإنتاج (د.ك) لعام 2017']
            col38=['المباني','الآلات والمعدات','وسائل النقل','أخرى']
            ma38[col38]=ma38[col38].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma38['الإجمالي']=ma38['المباني']+ma38['الآلات والمعدات']+ma38['وسائل النقل']+ma38['أخرى']
            tab38=pd.DataFrame({})
            if option == 'Sum':
                tab38=ma38.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].sum()
            if option == 'Mean':    
                tab38=ma38.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].mean()
            tab38.reset_index(inplace=True)
            tab38.loc['إجمالي المنشآت الصناعية']=tab38.sum(numeric_only=True, axis=0)
            tab38['الكود (ISIC 4)']=tab38['الكود (ISIC 4)'].replace(np.nan,'')
            tab38['البيان']=tab38['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab38=tab38.reset_index(drop=True)
            col38=['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']
            tab38[col38]=tab38[col38].astype(np.int64,errors='ignore')
            da38=tab38.style.apply(highlight_col, axis=None)
            #table39
            ta39=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma39=pd.DataFrame({})
            ma39['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta39=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta39[1].str.replace('\d+','')
            ma39['البيان']=cl.str.strip()
            ma39['الكود (ISIC 4)']=ma39['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma39['البيان']=ma39['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma39['المباني']=df['قيمة الإنفاق على المباني (د.ك) لعام 2018']
            ma39['الآلات والمعدات']=df['قيمة الإنفاق على الآلات ومعدات (د.ك) لعام 2018']
            ma39['وسائل النقل']=df['قيمة الإنفاق على وسائل النقل (د.ك) لعام 2018']
            ma39['أخرى']=df['إنفاقات أخرى لزيادة الإنتاج (د.ك) لعام 2018']
            col39=['المباني','الآلات والمعدات','وسائل النقل','أخرى']
            ma39[col39]=ma39[col39].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma39['الإجمالي']=ma39['المباني']+ma39['الآلات والمعدات']+ma39['وسائل النقل']+ma39['أخرى']
            tab39=pd.DataFrame({})
            if option == 'Sum':
                tab39=ma39.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab39=ma39.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].mean()
            tab39.reset_index(inplace=True)
            tab39.loc['إجمالي المنشآت الصناعية']=tab39.sum(numeric_only=True, axis=0)
            tab39['الكود (ISIC 4)']=tab39['الكود (ISIC 4)'].replace(np.nan,'')
            tab39['البيان']=tab39['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab39=tab39.reset_index(drop=True)
            col39=['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']
            tab39[col39]=tab39[col39].astype(np.int64,errors='ignore')
            da39=tab39.style.apply(highlight_col, axis=None)
            #table 40
            ta40=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma40=pd.DataFrame({})
            ma40['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta40=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta40[1].str.replace('\d+','')
            ma40['البيان']=cl.str.strip()
            ma40['الكود (ISIC 4)']=ma40['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma40['البيان']=ma40['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma40['المباني']=df['قيمة الإنفاق على المباني (د.ك) لعام 2019']
            ma40['الآلات والمعدات']=df['قيمة الإنفاق على الآلات ومعدات (د.ك) لعام 2019']
            ma40['وسائل النقل']=df['قيمة الإنفاق على وسائل النقل (د.ك) لعام 2019']
            ma40['أخرى']=df['إنفاقات أخرى لزيادة الإنتاج (د.ك) لعام 2019']
            col40=['المباني','الآلات والمعدات','وسائل النقل','أخرى']
            ma40[col40]=ma40[col40].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma40['الإجمالي']=ma40['المباني']+ma40['الآلات والمعدات']+ma40['وسائل النقل']+ma40['أخرى']
            tab40=pd.DataFrame({})
            if option == 'Sum':
                tab40=ma40.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab40=ma40.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].mean()
            tab40.reset_index(inplace=True)
            tab40.loc['إجمالي المنشآت الصناعية']=tab40.sum(numeric_only=True, axis=0)
            tab40['الكود (ISIC 4)']=tab40['الكود (ISIC 4)'].replace(np.nan,'')
            tab40['البيان']=tab40['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab40=tab40.reset_index(drop=True)
            col40=['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']
            tab40[col40]=tab40[col40].astype(np.int64,errors='ignore')
            da40=tab40.style.apply(highlight_col, axis=None)
            # table41
            ta41=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma41=pd.DataFrame({})
            ma41['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta41=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta41[1].str.replace('\d+','')
            ma41['البيان']=cl.str.strip()
            ma41['الكود (ISIC 4)']=ma41['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma41['البيان']=ma41['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma41['المباني']=df['قيمة الإنفاق على المباني (د.ك) لعام 2020']
            ma41['الآلات والمعدات']=df['قيمة الإنفاق على الآلات ومعدات (د.ك) لعام 2020']
            ma41['وسائل النقل']=df['قيمة الإنفاق على وسائل النقل (د.ك) لعام 2020']
            ma41['أخرى']=df['إنفاقات أخرى لزيادة الإنتاج (د.ك) لعام 2020']
            col41=['المباني','الآلات والمعدات','وسائل النقل','أخرى']
            ma41[col41]=ma41[col41].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            ma41['الإجمالي']=ma41['المباني']+ma41['الآلات والمعدات']+ma41['وسائل النقل']+ma41['أخرى']
            tab41=pd.DataFrame({})
            if option == 'Sum':
                tab41=ma41.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].sum()
            if option == 'Mean':
                tab41=ma41.groupby(['الكود (ISIC 4)','البيان'])[['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']].mean()
            tab41.reset_index(inplace=True)
            tab41.loc['إجمالي المنشآت الصناعية']=tab41.sum(numeric_only=True, axis=0)
            tab41['الكود (ISIC 4)']=tab41['الكود (ISIC 4)'].replace(np.nan,'')
            tab41['البيان']=tab41['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab41=tab41.reset_index(drop=True)
            col41=['المباني','الآلات والمعدات','وسائل النقل','أخرى','الإجمالي']
            tab41[col41]=tab41[col41].astype(np.int64,errors='ignore')
            da41=tab41.style.apply(highlight_col, axis=None)
            # table42
            ta42=df['الأبواب'].astype(str).str.split('-',expand=True)
            ma42=pd.DataFrame({})
            ma42['الكود (ISIC 4)'] = df['ISIC4'].astype(str).str[:2]
            ta42=df['الأبواب'].astype(str).str.split('-',expand=True)
            cl=ta42[1].str.replace('\d+','')
            ma42['البيان']=cl.str.strip()
            ma42['الكود (ISIC 4)']=ma42['الكود (ISIC 4)'].replace(['38','43','73','82'],'32')
            ma42['البيان']=ma42['البيان'].replace(['أنشطة جمع النفايات ومعالجتها وتصريفها ، واسترجاع المواد','أنشطة التشييد المتخصصة','أبحاث الإعلان والسوق','الأنشطة الإدارية للمكاتب ، وأنشطة الدعم للمكاتب وغير ذلك من أنشطة الدعم للأعمال'],'الصناعة التحويلية الأخرى')
            ma42['2017']=ma38['الإجمالي']
            ma42['2018']=ma39['الإجمالي']
            ma42['2019']=ma40['الإجمالي']
            ma42['2020']=ma41['الإجمالي']
            col15=['2017','2018','2019','2020']
            ma42[col15]=ma42[col15].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64,errors='ignore')
            tab42=pd.DataFrame({})
            if option == 'Sum':
                tab42=ma42.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].sum()
            if option == 'Mean':
                tab42=ma42.groupby(['الكود (ISIC 4)','البيان'])[['2017','2018','2019','2020']].mean()
            tab42.reset_index(inplace=True)
            tab42.loc['إجمالي المنشآت الصناعية']=tab42.sum(numeric_only=True, axis=0)
            tab42['الكود (ISIC 4)']=tab42['الكود (ISIC 4)'].replace(np.nan,'')
            tab42['البيان']=tab42['البيان'].replace(np.nan,'إجمالي المنشآت الصناعية')
            tab42=tab42.reset_index(drop=True)
            tab42['2017']=tab42['2017'].astype(np.int64,errors='ignore')
            tab42['2018']=tab42['2018'].astype(np.int64,errors='ignore')
            tab42['2019']=tab42['2019'].astype(np.int64,errors='ignore')
            tab42['2020']=tab42['2020'].astype(np.int64,errors='ignore')
            da42=tab42.style.apply(highlight_col, axis=None)
            
            
            
            
  ############################################################################################  
  #table1  
            
            st.subheader('Table 1')
            st.subheader("التوزيع القطاعي للمنشآت الصناعية بحسب التصنيف الصناعي الدولي الموَّحد لجميع الأنشطة الاقتصادية")
            
            
            st.table(ta1.style.apply(highlight_col, axis=None).set_precision(3))
           
            downloaded_file = da1.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_1.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 1 : Bar chart for the total {} based on 'العدد' and based on 'Code (ISIC 4)'**".format(option))
            
            fig1 = px.bar(ta1,  x='الكود (ISIC 4)', y='العدد',color='البيان', title="Total {} based on 'العدد' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig1)
            
            st.markdown("**Figure 2 : Bar chart for the total {} based on 'رأس المال (ألف دينار)' and based on 'Code (ISIC 4)'**".format(option))
            
            fig2 = px.bar(ta1,  x='الكود (ISIC 4)', y='رأس المال (ألف دينار)',color='البيان', title="Total {} based on 'رأس المال (ألف دينار)' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig2)
            
            st.markdown("**Figure 3 : Bar chart for the total {} based on المساحة (ألف كيلو متر مربع) and based on 'Code (ISIC 4)'**".format(option))
            
            fig3 = px.bar(ta1,  x='الكود (ISIC 4)', y='المساحة (ألف كيلو متر مربع)',color='البيان', title="Total {} based on 'المساحة (ألف كيلو متر مربع)' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig3)
               
 #table2           
              
            st.subheader('Table 2')
            st.subheader("التوزيع القطاعي للمنشآت الصناعية بحسب ملكية رأس المال (ألف دينار)")
            
                        
            st.table(tab2.style.apply(highlight_col, axis=None).set_precision(3))
            
            downloaded_file = da2.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_2.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 3 : Bar chart for the total {} based on 'الإجمالي' and based on 'Code (ISIC 4)'**".format(option))
            
            fig3 = px.bar(tab2, x="الكود (ISIC 4)", y="الإجمالي",color="البيان", title="Total {} based on 'الإجمالي' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig3)
            
            
            st.markdown("**Figure 4 : Bar chart for the total {} based on 'الإجمالي' and based on 'نوع المساهمة'**".format(option))
            
            figua=pd.DataFrame(figu.loc['إجمالي المنشآت الصناعية']).reset_index()
            figua=figua.drop(index=[0,1])
            dict = {'index': 'نوع المساهمة',
                            "إجمالي المنشآت الصناعية": 'الإجمالي',
                    }
            figua.rename(columns=dict,
                      inplace=True)
          
            fig4 = px.bar(figua, x='نوع المساهمة', y='الإجمالي',color='نوع المساهمة',title="Total {} based on 'الإجمالي' and based on 'نوع المساهمة'".format(option),width=800, height=500)
            st.write(fig4)
                
            
            st.subheader('Table 3')
            st.subheader("التوزيع الجغرافي للمنشآت الصناعية بحسب المناطق الصناعية")
            st.table(tab3.style.apply(highlight_col, axis=None).set_precision(2))
            
            downloaded_file = da3.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_3.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 5 : Bar chart frequency based on المنطقة الصناعية**")
            
            fig5 = px.bar(tab3, x="المنطقة الصناعية", y="عدد المنشآت",color='المنطقة الصناعية',hover_data=['الأهمية النسبية'], title="Bar chart frequency based on المنطقة الصناعية ",width=800, height=500)
            st.write(fig5)
                
                
            st.subheader('Table 4')
            st.subheader("المنشآت الصناعية بحسب الحجم (صغيرة - متوسطة - كبيرة)")
            st.table(tab4.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da4.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_4.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            st.markdown("**Figure 6 : Bar chart frequency based on البيان**")
            fig6 = px.bar(tab4, x="البيان", y="رأس المال (ألف دينار)",color="البيان",hover_data=['عدد المنشآت','عدد العاملين الكويتيين'], title="Bar chart frequency based on البيان ",width=800, height=500)
            st.write(fig6)
            
            
            st.subheader('Table 5')
            st.subheader("التوزيع القطاعي للمنشآت الصناعية الصغيرة بحسب التصنيف الصناعي الدولي الموَّحد لجميع الأنشطة الاقتصادية ")
            st.table(tab5.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da5.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_5.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            st.markdown("**Figure 7 : Bar chart for the total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'**".format(option))
            
            fig7 = px.bar(tab5,  x='الكود (ISIC 4)', y='عدد العاملين الكويتيين',color='البيان', title="Total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig7)
            
            st.markdown("**Figure 8 : Bar chart for the total {} based on 'رأس المال (ألف دينار)' and based on 'Code (ISIC 4)'**".format(option))
            
            fig8 = px.bar(tab5,  x='الكود (ISIC 4)', y='رأس المال (ألف دينار)',color='البيان', title="Total {} based on 'رأس المال (ألف دينار)' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig8)
            
            st.markdown("**Figure 9 : Bar chart for the total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'**".format(option))
            
            fig9 = px.bar(tab5,  x='الكود (ISIC 4)', y='عدد العاملين الكويتيين',color='البيان', title="Total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig9)
            
           
            st.subheader('Table 6')
            st.subheader("التوزيع القطاعي للمنشآت الصناعية المتوسطة بحسب التصنيف الصناعي الدولي الموَّحد لجميع الأنشطة الاقتصادية ")
            st.table(tab6.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da6.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_6.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            st.markdown("**Figure 10 : Bar chart for the total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'**".format(option))
            
            fig10 = px.bar(tab6,  x='الكود (ISIC 4)', y='عدد العاملين الكويتيين',color='البيان', title="Total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig10)
            
            st.markdown("**Figure 11 : Bar chart for the total {} based on 'رأس المال (ألف دينار)' and based on 'Code (ISIC 4)'**".format(option))
            
            fig11 = px.bar(tab6,  x='الكود (ISIC 4)', y='رأس المال (ألف دينار)',color='البيان', title="Total {} based on 'رأس المال (ألف دينار)' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig11)
            
            st.markdown("**Figure 12 : Bar chart for the total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'**".format(option))
            
            fig12 = px.bar(tab6,  x='الكود (ISIC 4)', y='عدد العاملين الكويتيين',color='البيان', title="Total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig12)
       # table7     
            st.subheader('Table 7')
            st.subheader("التوزيع القطاعي للمنشآت الصناعية الكبيرة بحسب التصنيف الصناعي الدولي الموحَّد لجميع الأنشطة الاقتصادية  ")
            st.table(tab7.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da7.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_7.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            st.markdown("**Figure 13 : Bar chart for the total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'**".format(option))
            
            fig13 = px.bar(tab7,  x='الكود (ISIC 4)', y='عدد العاملين الكويتيين',color='البيان', title="Total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig13)
            
            st.markdown("**Figure 14 : Bar chart for the total {} based on 'رأس المال (ألف دينار)' and based on 'Code (ISIC 4)'**".format(option))
            
            fig14 = px.bar(tab7,  x='الكود (ISIC 4)', y='رأس المال (ألف دينار)',color='البيان', title="Total {} based on 'رأس المال (ألف دينار)' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig14)
            
            st.markdown("**Figure 15 : Bar chart for the total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'**".format(option))
            
            fig15 = px.bar(tab7,  x='الكود (ISIC 4)', y='عدد العاملين الكويتيين',color='البيان', title="Total {} based on 'عدد العاملين الكويتيين' and based on 'Code (ISIC 4)'".format(option),width=800, height=500)
            st.write(fig15)
                
        # table8
            st.subheader('Table 8')
            st.subheader("إجمالي القيمة المضافة للمنشآت الصناعية (ألف دينار) *")
            st.table(tab8.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da8.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_8.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 16 : Bar chart for إجمالي القيمة المضافة للمنشآت الصناعية (ألف دينار) * based on 'Code (ISIC 4)' every year**".format(option))
            
            fig16 = px.bar(tab8, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for إجمالي القيمة المضافة للمنشآت الصناعية (ألف دينار)",width=800, height=700)

            st.write(fig16)
       #table9     
            st.subheader('Table 9')
            st.subheader("إجمالي قيمة الإنتاج للمنشآت الصناعية (ألف دينار) *")
            st.table(tab9.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da9.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_9.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 17 : Bar chart for إجمالي قيمة الإنتاج للمنشآت الصناعية (ألف دينار) * based on 'Code (ISIC 4)' every year**".format(option))
            
            fig17 = px.bar(tab9, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for إجمالي قيمة الإنتاج للمنشآت الصناعية (ألف دينار) *",width=800, height=700)

            st.write(fig17)
      #table10      
            st.subheader('Table 10')
            st.subheader("إجمالي قيمة المدخلات الوسيطة للإنتاج (ألف دينار) للمنشآت الصناعية")
            st.table(tab10.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da10.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_10.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 18 : Bar chart for إجمالي قيمة المدخلات الوسيطة للإنتاج (ألف دينار) للمنشآت الصناعية based on 'Code (ISIC 4)' every year**".format(option))
            
            fig18 = px.bar(tab10, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for إجمالي قيمة المدخلات الوسيطة للإنتاج (ألف دينار) للمنشآت الصناعية",width=800, height=700)

            st.write(fig18)
        #table11      
            st.subheader('Table 11')
            st.subheader("إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2017 (ألف دينار)")
            st.table(tab11.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da11.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_11.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 19 : Bar chart for إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2017 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig19 = px.bar(tab11, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي'], title="Bar chart for إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2017 (ألف دينار)",width=800, height=700)

            st.write(fig19)
        #table12      
            st.subheader('Table 12')
            st.subheader("إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2018 (ألف دينار)")
            st.table(tab12.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da12.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_12.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 20 : Bar chart for إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2018 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig20 = px.bar(tab12, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي'], title="Bar chart for إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2018 (ألف دينار)",width=800, height=700)

            st.write(fig20)
        #table13      
            st.subheader('Table 13')
            st.subheader("إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2019 (ألف دينار)")
            st.table(tab13.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da13.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_13.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 21 : Bar chart for إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2019 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig21 = px.bar(tab13, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي'], title="Bar chart for إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2019 (ألف دينار)",width=800, height=700)

            st.write(fig21)
                
        #table14      
            st.subheader('Table 14')
            st.subheader("إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)")
            st.table(tab14.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da14.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_14.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 22 : Bar chart for إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig22 = px.bar(tab14, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['التسويق المحلي','التسويق الحكومي','التصدير الخليجي','التصدير العربي','التصدير الدولي','الإجمالي'], title="Bar chart for إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)",width=800, height=700)

            st.write(fig22)
        #table15
        
            st.subheader('Table 15')
            st.subheader("إجمالي المبيعات للمنشآت الصناعية (ألف دينار)")
            st.table(tab15.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da15.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_15.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 22 : Bar chart for إجمالي المبيعات للمنشآت الصناعية (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig22 = px.bar(tab15, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for إجمالي المبيعات للمنشآت الصناعية (ألف دينار)",width=800, height=700)

            st.write(fig22)
        #table16
        
            #table16      
            st.subheader('Table 16')
            st.subheader("إجمالي تكلفة المواد الأولية للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)")
            st.table(tab16.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da16.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_16.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 23 : Bar chart for إجمالي تكلفة المواد الأولية للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig23 = px.bar(tab16, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['مواد خام',
 'مواد نصف مصنعة',
 'مواد مصنعة',
 'مواد تعبئة وتغليف',
 'الإجمالي'], title="Bar chart for إجمالي تكلفة المواد الأولية للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)",width=800, height=700)

            st.write(fig23)
        #table17      
            st.subheader('Table 17')
            st.subheader("إجمالي تكلفة المواد الأولية المحلية للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)")
            st.table(tab17.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da17.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_17.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 24 : Bar chart for إجمالي تكلفة المواد الأولية المحلية للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig24 = px.bar(tab17, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['مواد خام',
 'مواد نصف مصنعة',
 'مواد مصنعة',
 'مواد تعبئة وتغليف',
 'الإجمالي'], title="Bar chart for إجمالي تكلفة المواد الأولية المحلية للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)",width=800, height=700)

            st.write(fig24)
            
        #table18
        
            st.subheader('Table 18')
            st.subheader("إجمالي تكلفة المواد الأولية المستوردة للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)")
            st.table(tab18.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da18.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_18.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 25 : Bar chart for إجمالي تكلفة المواد الأولية المستوردة للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig25 = px.bar(tab18, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['مواد خام',
 'مواد نصف مصنعة',
 'مواد مصنعة',
 'مواد تعبئة وتغليف',
 'الإجمالي'], title="Bar chart for إجمالي تكلفة المواد الأولية المستوردة للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)",width=800, height=700)

            st.write(fig25)
        #table19
        
            st.subheader('Table 19')
            st.subheader("إجمالي تكلفة المواد الأولية للمنشآت الصناعية (ألف دينار)")
            st.table(tab19.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da19.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_19.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 26 : Bar chart for إجمالي تكلفة المواد الأولية للمنشآت الصناعية (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig26 = px.bar(tab19, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for إجمالي تكلفة المواد الأولية للمنشآت الصناعية (ألف دينار)",width=800, height=700)

            st.write(fig26)
            
        #table20
             
            st.subheader('Table 20')
            st.subheader("الطباعة واستنساخ وسائط الإعلام")
            st.table(tab20.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da20.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_20.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 27 : Bar chart for الطباعة واستنساخ وسائط الإعلام based on 'Code (ISIC 4)' every year**".format(option))
            
            fig27 = px.bar(tab20, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for الطباعة واستنساخ وسائط الإعلام",width=800, height=700)

            st.write(fig27)
         # table21         
            st.subheader('Table 21')
            st.subheader("قيمة المخزون من المواد الأولية في نهاية العام للمنشآت الصناعية (ألف دينار)")
            st.table(tab21.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da21.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_21.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 28 : Bar chart for قيمة المخزون من المواد الأولية في نهاية العام للمنشآت الصناعية (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig28 = px.bar(tab21, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for قيمة المخزون من المواد الأولية في نهاية العام للمنشآت الصناعية (ألف دينار)",width=800, height=700)

            st.write(fig28)
        # table22         
            st.subheader('Table 22')
            st.subheader("التغير في قيمة المخزون من المواد الأولية للمنشآت الصناعية (ألف دينار)")
            st.table(tab22.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da22.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_22.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 29 : Bar chart for التغير في قيمة المخزون من المواد الأولية للمنشآت الصناعية (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig29 = px.bar(tab22, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for التغير في قيمة المخزون من المواد الأولية للمنشآت الصناعية (ألف دينار)",width=800, height=700)

            st.write(fig29)
        #table23      
            st.subheader('Table 23')
            st.subheader("قيمة الاستهلاك للمنشآت الصناعية في عام 2017 (ألف دينار)")
            st.table(tab23.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da23.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_23.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 30 : Bar chart for قيمة الاستهلاك للمنشآت الصناعية في عام 2017 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig30 = px.bar(tab23, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي'], title="Bar chart for قيمة الاستهلاك للمنشآت الصناعية في عام 2017 (ألف دينار)",width=800, height=700)

            st.write(fig30)
        #table24      
            st.subheader('Table 24')
            st.subheader("قيمة الاستهلاك للمنشآت الصناعية في عام 2018 (ألف دينار)")
            st.table(tab24.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da24.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_24.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 31 : Bar chart for قيمة الاستهلاك للمنشآت الصناعية في عام 2018 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig31 = px.bar(tab24, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي'], title="Bar chart for قيمة الاستهلاك للمنشآت الصناعية في عام 2018 (ألف دينار)",width=800, height=700)

            st.write(fig31)
        #table25      
            st.subheader('Table 25')
            st.subheader("قيمة الاستهلاك للمنشآت الصناعية في عام 2019 (ألف دينار)")
            st.table(tab25.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da25.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_25.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 32 : Bar chart for قيمة الاستهلاك للمنشآت الصناعية في عام 2019 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig32 = px.bar(tab25, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي'], title="Bar chart for قيمة الاستهلاك للمنشآت الصناعية في عام 2019 (ألف دينار)",width=800, height=700)

            st.write(fig32)
        #table26      
            st.subheader('Table 26')
            st.subheader("قيمة الاستهلاك للمنشآت الصناعية في عام 2020 (ألف دينار)")
            st.table(tab26.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da26.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_26.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 33 : Bar chart for قيمة الاستهلاك للمنشآت الصناعية في عام 2020 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig33 = px.bar(tab26, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['الكهرباء','المياة العذبة','الغاز الطبيعي','البنزين','الديزل','الزيوت والشحوم','منافع أخرى','الإجمالي'], title="Bar chart for قيمة الاستهلاك للمنشآت الصناعية في عام 2020 (ألف دينار)",width=800, height=700)

            st.write(fig33)
        # table27         
            st.subheader('Table 27')
            st.subheader("قيمة الاستهلاك للمنشآت الصناعية (ألف دينار)")
            st.table(tab27.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da27.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_27.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 34 : Bar chart for قيمة الاستهلاك للمنشآت الصناعية (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig34 = px.bar(tab27, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for قيمة الاستهلاك للمنشآت الصناعية (ألف دينار)",width=800, height=700)

            st.write(fig34)
        #table28      
            st.subheader('Table 28')
            st.subheader("إجمالي التكاليف للمنشآت الصناعية في عام 2017 (ألف دينار)")
            st.table(tab28.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da28.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_28.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 35 : Bar chart for إجمالي التكاليف للمنشآت الصناعية في عام 2017 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig35 = px.bar(tab28, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['الإيجارات',
 'الصيانة وقطع الغيار',
 'التسويق والترويج',
 'تدريب عمالة وطنية',
 'تدريب عمالة أخرى',
 'دراسات وبحوث',
 'مصاريف إدارية',
 'تكاليف أخرى',
 'الإجمالي'], title="Bar chart for إجمالي التكاليف للمنشآت الصناعية في عام 2017 (ألف دينار)",width=800, height=700)

            st.write(fig35)
            
            #table29      
            st.subheader('Table 29')
            st.subheader("إجمالي التكاليف للمنشآت الصناعية في عام 2018 (ألف دينار)")
            st.table(tab29.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da29.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_29.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 36 : Bar chart for إجمالي التكاليف للمنشآت الصناعية في عام 2018 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig36 = px.bar(tab29, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['الإيجارات',
 'الصيانة وقطع الغيار',
 'التسويق والترويج',
 'تدريب عمالة وطنية',
 'تدريب عمالة أخرى',
 'دراسات وبحوث',
 'مصاريف إدارية',
 'تكاليف أخرى',
 'الإجمالي'], title="Bar chart for إجمالي التكاليف للمنشآت الصناعية في عام 2018 (ألف دينار)",width=800, height=700)

            st.write(fig36)
            
            #table30      
            st.subheader('Table 30')
            st.subheader("إجمالي التكاليف للمنشآت الصناعية في عام 2019 (ألف دينار)")
            st.table(tab30.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da30.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_30.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 37 : Bar chart for إجمالي التكاليف للمنشآت الصناعية في عام 2019 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig37 = px.bar(tab30, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['الإيجارات',
 'الصيانة وقطع الغيار',
 'التسويق والترويج',
 'تدريب عمالة وطنية',
 'تدريب عمالة أخرى',
 'دراسات وبحوث',
 'مصاريف إدارية',
 'تكاليف أخرى',
 'الإجمالي'], title="Bar chart for إجمالي التكاليف للمنشآت الصناعية في عام 2019 (ألف دينار)",width=800, height=700)

            st.write(fig37)
            
            #table31      
            st.subheader('Table 31')
            st.subheader("إجمالي التكاليف للمنشآت الصناعية في عام 2020 (ألف دينار)")
            st.table(tab31.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da31.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_31.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 38 : Bar chart for إجمالي التكاليف للمنشآت الصناعية في عام 2020 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig38 = px.bar(tab31, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['الإيجارات',
 'الصيانة وقطع الغيار',
 'التسويق والترويج',
 'تدريب عمالة وطنية',
 'تدريب عمالة أخرى',
 'دراسات وبحوث',
 'مصاريف إدارية',
 'تكاليف أخرى',
 'الإجمالي'], title="Bar chart for إجمالي التكاليف للمنشآت الصناعية في عام 2020 (ألف دينار)",width=800, height=700)

            st.write(fig38)
            
            # table32         
            st.subheader('Table 32')
            st.subheader("إجمالي التكاليف للمنشآت الصناعية (ألف دينار)")
            st.table(tab32.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da32.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_32.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 39 : Bar chart for إجمالي التكاليف للمنشآت الصناعية (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig39 = px.bar(tab32, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for إجمالي التكاليف للمنشآت الصناعية (ألف دينار)",width=800, height=700)

            st.write(fig39)
            
            #table33      
            st.subheader('Table 33')
            st.subheader("قيمة الأصول غير المالية للمنشآت الصناعية في عام 2017 (ألف دينار)")
            st.table(tab33.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da33.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_33.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 40 : Bar chart for قيمة الأصول غير المالية للمنشآت الصناعية في عام 2017 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig40 = px.bar(tab33, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['المباني',
 'الآلات والمعدات',
 'وسائل النقل',
 'أخرى',
 'الإجمالي'], title="Bar chart for قيمة الأصول غير المالية للمنشآت الصناعية في عام 2017 (ألف دينار)",width=800, height=700)

            st.write(fig40)
        #table34
            st.subheader('Table 34')
            st.subheader("قيمة الأصول غير المالية للمنشآت الصناعية في عام 2018 (ألف دينار)")
            st.table(tab34.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da34.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_34.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 41 : Bar chart for قيمة الأصول غير المالية للمنشآت الصناعية في عام 2018 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig41 = px.bar(tab34, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['المباني',
 'الآلات والمعدات',
 'وسائل النقل',
 'أخرى',
 'الإجمالي'], title="Bar chart for قيمة الأصول غير المالية للمنشآت الصناعية في عام 2018 (ألف دينار)",width=800, height=700)

            st.write(fig41)
            
            #table35      
            st.subheader('Table 35')
            st.subheader("قيمة الأصول غير المالية للمنشآت الصناعية في عام 2019 (ألف دينار)")
            st.table(tab35.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da35.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_35.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 42 : Bar chart for قيمة الأصول غير المالية للمنشآت الصناعية في عام 2019 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig42 = px.bar(tab35, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['المباني',
 'الآلات والمعدات',
 'وسائل النقل',
 'أخرى',
 'الإجمالي'], title="Bar chart for قيمة الأصول غير المالية للمنشآت الصناعية في عام 2019 (ألف دينار)",width=800, height=700)

            st.write(fig42)
            
            #table36      
            st.subheader('Table 36')
            st.subheader("قيمة الأصول غير المالية للمنشآت الصناعية في عام 2020 (ألف دينار)")
            st.table(tab36.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da36.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_36.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 43 : Bar chart for قيمة الأصول غير المالية للمنشآت الصناعية في عام 2020 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig43 = px.bar(tab36, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['المباني',
 'الآلات والمعدات',
 'وسائل النقل',
 'أخرى',
 'الإجمالي'], title="Bar chart for قيمة الأصول غير المالية للمنشآت الصناعية في عام 2020 (ألف دينار)",width=800, height=700)

            st.write(fig43)
            
            # table37         
            st.subheader('Table 37')
            st.subheader("إجمالي قيمة الأصول غير المالية للمنشآت الصناعية (ألف دينار)")
            st.table(tab37.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da37.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_37.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 44 : Bar chart for إجمالي قيمة الأصول غير المالية للمنشآت الصناعية (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig44 = px.bar(tab37, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for إجمالي قيمة الأصول غير المالية للمنشآت الصناعية (ألف دينار)",width=800, height=700)

            st.write(fig44)
            #table38      
            st.subheader('Table 38')
            st.subheader("قيمة الإنفاق للمنشآت الصناعية في عام 2017 (ألف دينار)")
            st.table(tab38.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da38.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_38.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 45 : Bar chart for قيمة الإنفاق للمنشآت الصناعية في عام 2017 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig45 = px.bar(tab38, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['المباني',
 'الآلات والمعدات',
 'وسائل النقل',
 'أخرى',
 'الإجمالي'], title="Bar chart for قيمة الإنفاق للمنشآت الصناعية في عام 2017 (ألف دينار)",width=800, height=700)

            st.write(fig45)
            
            #table39      
            st.subheader('Table 39')
            st.subheader("قيمة الإنفاق للمنشآت الصناعية في عام 2018 (ألف دينار)")
            st.table(tab39.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da39.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_39.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 46 : Bar chart for قيمة الإنفاق للمنشآت الصناعية في عام 2018 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig46 = px.bar(tab39, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['المباني',
 'الآلات والمعدات',
 'وسائل النقل',
 'أخرى',
 'الإجمالي'], title="Bar chart for قيمة الإنفاق للمنشآت الصناعية في عام 2018 (ألف دينار)",width=800, height=700)

            st.write(fig46)
            
            #table40      
            st.subheader('Table 40')
            st.subheader("قيمة الإنفاق للمنشآت الصناعية في عام 2019 (ألف دينار)")
            st.table(tab40.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da40.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_40.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 47 : Bar chart for قيمة الإنفاق للمنشآت الصناعية في عام 2019 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig47 = px.bar(tab40, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['المباني',
 'الآلات والمعدات',
 'وسائل النقل',
 'أخرى',
 'الإجمالي'], title="Bar chart for قيمة الإنفاق للمنشآت الصناعية في عام 2019 (ألف دينار)",width=800, height=700)

            st.write(fig47)
            
            #table41      
            st.subheader('Table 41')
            st.subheader("قيمة الإنفاق للمنشآت الصناعية في عام 2020 (ألف دينار)")
            st.table(tab41.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da41.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_41.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 48 : Bar chart for قيمة الإنفاق للمنشآت الصناعية في عام 2020 (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig48 = px.bar(tab41, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['المباني',
 'الآلات والمعدات',
 'وسائل النقل',
 'أخرى',
 'الإجمالي'], title="Bar chart for قيمة الإنفاق للمنشآت الصناعية في عام 2020 (ألف دينار)",width=800, height=700)

            st.write(fig48)
            
            # table42         
            st.subheader('Table 42')
            st.subheader("إجمالي قيمة الإنفاق الرأسمالي بالمنشآت الصناعية لزيادة الإنتاج (ألف دينار)")
            st.table(tab42.style.apply(highlight_col, axis=None).set_precision(0))
            downloaded_file = da42.to_excel(towrite, encoding='utf-8', index=False, header=True ) # write to BytesIO buffer
            towrite.seek(0)  # reset ponp.int64er
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Table_42.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Figure 49 : Bar chart for إجمالي قيمة الإنفاق الرأسمالي بالمنشآت الصناعية لزيادة الإنتاج (ألف دينار) based on 'Code (ISIC 4)' every year**".format(option))
            
            fig49 = px.bar(tab42, x="البيان", y="الكود (ISIC 4)",color="البيان",hover_data=['2017','2018','2019','2020'], title="Bar chart for إجمالي قيمة الإنفاق الرأسمالي بالمنشآت الصناعية لزيادة الإنتاج (ألف دينار)",width=800, height=700)

            st.write(fig49)
            
        
            
            
            
            
                
                
                
                
                
                
                
                
            
#master excel             
            st.subheader("Download Master Excel File")
            with pd.ExcelWriter(towrite, engine="xlsxwriter") as writer:
                       
                da1.to_excel(writer, sheet_name="1", startrow = 2,index=False)
                da2.to_excel(writer, sheet_name="2",startrow = 2, index=False)
                da3.to_excel(writer, sheet_name="3",startrow = 2, index=False)
                da4.to_excel(writer, sheet_name="4",startrow = 2, index=False)
                da5.to_excel(writer, sheet_name="5",startrow = 2, index=False)
                da6.to_excel(writer, sheet_name="6", startrow = 2,index=False)
                da7.to_excel(writer, sheet_name="7",startrow = 2, index=False)
                da8.to_excel(writer, sheet_name="8",startrow = 2, index=False)
                da9.to_excel(writer, sheet_name="9",startrow = 2, index=False)
                da10.to_excel(writer, sheet_name="10",startrow = 2, index=False)
                da11.to_excel(writer, sheet_name="11",startrow = 2, index=False)
                da12.to_excel(writer, sheet_name="12",startrow = 2, index=False)
                da13.to_excel(writer, sheet_name="13",startrow = 2, index=False)
                da14.to_excel(writer, sheet_name="14",startrow = 2, index=False)
                da15.to_excel(writer, sheet_name="15",startrow = 2, index=False)
                da16.to_excel(writer, sheet_name="16",startrow = 2, index=False)
                da17.to_excel(writer, sheet_name="17",startrow = 2, index=False)
                da18.to_excel(writer, sheet_name="18",startrow = 2, index=False)
                da19.to_excel(writer, sheet_name="19", startrow = 2,index=False)
                da20.to_excel(writer, sheet_name="20",startrow = 2, index=False)
                da21.to_excel(writer, sheet_name="21", startrow = 2,index=False)
                da22.to_excel(writer, sheet_name="22", startrow = 2,index=False)
                da23.to_excel(writer, sheet_name="23", startrow = 2,index=False)
                da24.to_excel(writer, sheet_name="24", startrow = 2,index=False)
                da25.to_excel(writer, sheet_name="25",startrow = 2, index=False)
                da26.to_excel(writer, sheet_name="26",startrow = 2, index=False)
                da27.to_excel(writer, sheet_name="27", startrow = 2,index=False)
                da28.to_excel(writer, sheet_name="28",startrow = 2, index=False)
                da29.to_excel(writer, sheet_name="29", startrow = 2,index=False)
                da30.to_excel(writer, sheet_name="30",startrow = 2, index=False)
                da31.to_excel(writer, sheet_name="31",startrow = 2, index=False)
                da32.to_excel(writer, sheet_name="32",startrow = 2, index=False)
                da33.to_excel(writer, sheet_name="33",startrow = 2, index=False)
                da34.to_excel(writer, sheet_name="34",startrow = 2, index=False)
                da35.to_excel(writer, sheet_name="35",startrow = 2, index=False)
                da36.to_excel(writer, sheet_name="36", startrow = 2,index=False)
                da37.to_excel(writer, sheet_name="37", startrow = 2,index=False)
                da38.to_excel(writer, sheet_name="38", startrow = 2,index=False)
                da39.to_excel(writer, sheet_name="39", startrow = 2,index=False)
                da40.to_excel(writer, sheet_name="40", startrow = 2,index=False)
                da41.to_excel(writer, sheet_name="41", startrow = 2,index=False)
                da42.to_excel(writer, sheet_name="42", startrow = 2,index=False)
                workbook  = writer.book
                worksheet1 = writer.sheets['1']
                worksheet2 = writer.sheets['2']
                worksheet3 = writer.sheets['3']
                worksheet4 = writer.sheets['4']
                worksheet5 = writer.sheets['5']
                worksheet6 = writer.sheets['6']
                worksheet7 = writer.sheets['7']
                worksheet8 = writer.sheets['8']
                worksheet9 = writer.sheets['9']
                worksheet10 = writer.sheets['10']
                worksheet11 = writer.sheets['11']
                worksheet12 = writer.sheets['12']
                worksheet13 = writer.sheets['13']
                worksheet14 = writer.sheets['14']
                worksheet15 = writer.sheets['15']
                worksheet16 = writer.sheets['16']
                worksheet17 = writer.sheets['17']
                worksheet18 = writer.sheets['18']
                worksheet19 = writer.sheets['19']
                worksheet20 = writer.sheets['20']
                worksheet21 = writer.sheets['21']
                worksheet22 = writer.sheets['22']
                worksheet23 = writer.sheets['23']
                worksheet24 = writer.sheets['24']
                worksheet25 = writer.sheets['25']
                worksheet26 = writer.sheets['26']
                worksheet27 = writer.sheets['27']
                worksheet28 = writer.sheets['28']
                worksheet29 = writer.sheets['29']
                worksheet30 = writer.sheets['30']
                worksheet31 = writer.sheets['31']
                worksheet32 = writer.sheets['32']
                worksheet33 = writer.sheets['33']
                worksheet34 = writer.sheets['34']
                worksheet35 = writer.sheets['35']
                worksheet36 = writer.sheets['36']
                worksheet37 = writer.sheets['37']
                worksheet38 = writer.sheets['38']
                worksheet39 = writer.sheets['39']
                worksheet40 = writer.sheets['40']
                worksheet41 = writer.sheets['41']
                worksheet42 = writer.sheets['42']
                
                worksheet1.write(0, 7, 'التوزيع القطاعي للمنشآت الصناعية بحسب التصنيف الصناعي الدولي الموَّحد لجميع الأنشطة الاقتصادية ', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet2.write(0, 5, 'التوزيع القطاعي للمنشآت الصناعية بحسب ملكية رأس المال (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c','size': 11}))
                worksheet3.write(0, 5, 'التوزيع الجغرافي للمنشآت الصناعية بحسب المناطق الصناعية', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet4.write(0, 5, 'المنشآت الصناعية بحسب الحجم (صغيرة - متوسطة - كبيرة)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet5.write(0, 7, 'التوزيع القطاعي للمنشآت الصناعية الصغيرة بحسب التصنيف الصناعي الدولي الموَّحد لجميع الأنشطة الاقتصادية ', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet6.write(0, 7, 'التوزيع القطاعي للمنشآت الصناعية المتوسطة بحسب التصنيف الصناعي الدولي الموَّحد لجميع الأنشطة الاقتصادية ', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet7.write(0, 7, 'التوزيع القطاعي للمنشآت الصناعية الكبيرة بحسب التصنيف الصناعي الدولي الموحَّد لجميع الأنشطة الاقتصادية ', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet8.write(0, 5, 'إجمالي القيمة المضافة للمنشآت الصناعية (ألف دينار) *', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet9.write(0, 5, 'إجمالي قيمة الإنتاج للمنشآت الصناعية (ألف دينار) *', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet10.write(0, 5, 'إجمالي قيمة المدخلات الوسيطة للإنتاج (ألف دينار) للمنشآت الصناعية', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet11.write(0, 7, 'إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2017 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet12.write(0, 7, 'إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2018 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet13.write(0, 7, 'إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2019 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet14.write(0, 7, 'إجمالي المبيعات للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet15.write(0, 5, 'إجمالي المبيعات للمنشآت الصناعية (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet16.write(0, 7, 'إجمالي تكلفة المواد الأولية للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet17.write(0, 7, 'إجمالي تكلفة المواد الأولية المحلية للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet18.write(0, 7, 'إجمالي تكلفة المواد الأولية المستوردة للمنشآت الصناعية بحسب درجة التنصيع لعام 2020 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet19.write(0, 5, 'إجمالي تكلفة المواد الأولية للمنشآت الصناعية (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet20.write(0, 7, 'قيمة المخزون من المواد الأولية في بداية العام للمنشآت الصناعية (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet21.write(0, 7, 'قيمة المخزون من المواد الأولية في نهاية العام للمنشآت الصناعية (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet22.write(0, 7, 'التغير في قيمة المخزون من المواد الأولية للمنشآت الصناعية (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet23.write(0, 5, 'قيمة الاستهلاك للمنشآت الصناعية في عام 2017 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet24.write(0, 5, 'قيمة الاستهلاك للمنشآت الصناعية في عام 2018 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet25.write(0, 5, 'قيمة الاستهلاك للمنشآت الصناعية في عام 2019 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet26.write(0, 5, 'قيمة الاستهلاك للمنشآت الصناعية في عام 2020 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet27.write(0, 5, 'قيمة الاستهلاك للمنشآت الصناعية (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet28.write(0, 5, 'إجمالي التكاليف للمنشآت الصناعية في عام 2017 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet29.write(0, 5, 'إجمالي التكاليف للمنشآت الصناعية في عام 2018 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet30.write(0, 5, 'إجمالي التكاليف للمنشآت الصناعية في عام 2019 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet31.write(0, 5, 'إجمالي التكاليف للمنشآت الصناعية في عام 2020 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet32.write(0, 5, 'إجمالي التكاليف للمنشآت الصناعية (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet33.write(0, 6, 'قيمة الأصول غير المالية للمنشآت الصناعية في عام 2017 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet34.write(0, 6, 'قيمة الأصول غير المالية للمنشآت الصناعية في عام 2018 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet35.write(0, 6, 'قيمة الأصول غير المالية للمنشآت الصناعية في عام 2019 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet36.write(0, 6, 'قيمة الأصول غير المالية للمنشآت الصناعية في عام 2020 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet37.write(0, 5, 'إجمالي قيمة الأصول غير المالية للمنشآت الصناعية (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet38.write(0, 5, 'قيمة الإنفاق للمنشآت الصناعية في عام 2017 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet39.write(0, 5, 'قيمة الإنفاق للمنشآت الصناعية في عام 2018 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet40.write(0, 5, 'قيمة الإنفاق للمنشآت الصناعية في عام 2019 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet41.write(0, 5, 'قيمة الإنفاق للمنشآت الصناعية في عام 2020 (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                worksheet42.write(0, 6, 'إجمالي قيمة الإنفاق الرأسمالي بالمنشآت الصناعية لزيادة الإنتاج (ألف دينار)', workbook.add_format({'bold': True, 'color': '#0d0d0c', 'size': 11}))
                

                
                
                writer.save()
            
                st.download_button(
                    label="Download Master Excel worksheet",
                    data=towrite,
                    file_name="All_tables.xlsx",
                    mime="application/vnd.ms-excel",
                )
            
            
            
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
        
        
