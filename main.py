import streamlit as st
import pandas as pd
import time

def update_log(text,localtime):
    with open('update.log.txt','a+') as f:
        f.write(localtime)
        f.write(':')
        f.write(text)
# from pandas.testing import assert_frame_equal
@st.cache_data
def get_data():
    antibody_df= pd.read_csv('binglab_antibody.v0.0.8.csv',index_col=0)
    return antibody_df
st.header('Antibody')
antibody_df = get_data()
num_row = st.sidebar.selectbox(label='编辑',options=('fixed','dynamic'))
tab1,tab2,tab3 = st.tabs(['查询','抗体详情','统计'])
with tab1:
    name = st.text_input('查询名称')
    if not name:
        st.info('请输入名称, 按enter查询')
        st.stop()
    # st.dataframe(antibody_df[antibody_df.apply(lambda x:True if name.lower() in x.lower() else False,axis=1)])
    name_df = antibody_df[antibody_df.name.map(lambda x: True if str(name).lower() in str(x).lower() else False)]

    for i,row in name_df.iterrows():
        with st.expander(str(row['name'])):
            st.header(row['location'])
            row[name_df.columns]
    with st.expander('表格详情'):
        st.dataframe(name_df)
with tab2:
    data_new=st.data_editor(antibody_df,num_rows=num_row)
    # st.dataframe(data_new.compare(antibody_df))
    st.subheader('修改情况')
    compa = data_new.compare(antibody_df)
    if len(compa) <1:
        st.info('暂无修改')
    else:
        compa
        data_new.loc[compa.index, ['name','location']]
        if st.button('确认修改'):
            passwd = st.text_input('请输入修改密码')
            if passwd == 'bing123456':
                localtime = time.asctime(time.localtime())#
                update_log(str(compa)+'/n'+str(data_new.loc[compa.index, ['name','location']])

                       ,localtime)
            antibody_df.to_csv(f'binglab_antibody.v0.0.8_{localtime}.csv')
            data_new.to_csv('binglab_antibody.v0.0.8.csv')

            st.success('保存成功！')
     
with tab3:
    st.dataframe(antibody_df.describe())
    for col in antibody_df.columns:
        if col not in ['name','catalog','lot']:
            st.header(col)
            st.bar_chart(antibody_df.groupby(col).count()['name'].sort_values(ascending=True)[:50])
