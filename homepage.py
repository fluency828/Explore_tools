import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from matplotlib import rcParams
import plotly.express as px
import numpy as np
mpl.font_manager.fontManager.addfont('字体/SIMSUN.ttf')
import math
config = {
    "font.family":'serif',
    # "font.size": 20,
    "mathtext.fontset":'stix',
    "font.serif": ['SIMSUN'],
}
rcParams.update(config)
plt.rcParams['axes.unicode_minus'] = False


# 上传文件
uploaded_file = st.file_uploader("请选择一个Excel文件", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 获取所有列名
    columns = list(df.columns)

    # time_pn = st.selectbox('请选择时间数据',columns)
    # wtg_pn = st.selectbox('请选择风机名称数据',columns)
    possible_time_list = ['data_time','time','时间']
    for t_pn in possible_time_list:
        if t_pn in columns:
            time_pn = t_pn
            break
    possible_wtg_pn_list= ['风机名称','名称','device_name','device_id',]
    for w_pn in possible_wtg_pn_list:
        if w_pn in columns:
            wtg_pn = w_pn
            break

    df[time_pn] = pd.to_datetime(df[time_pn])
    columns.remove(wtg_pn)
    # 选择框
    x_column = st.selectbox('请选择X轴的数据', columns)
    y_column = st.selectbox('请选择Y轴的数据', columns)
    wind_machine_names = df[wtg_pn].unique()


    if y_column != time_pn:
    # # 根据风机名称，绘制图表
    #     # st.write(wind_machine_names.T)
    #     fig, axs = plt.subplots(math.ceil(len(wind_machine_names)/4), 4, figsize=(30, 5*len(wind_machine_names)//4))

    #     for idx, name in enumerate(wind_machine_names):
    #         data = df[df[wtg_pn] == name].reset_index(drop=True)
    #         axs[idx//4, idx%4].scatter(data[x_column], data[y_column],s=5)
    #         axs[idx//4, idx%4].set_title(name)
    #         axs[idx//4, idx%4].set_xlabel(x_column)
    #         axs[idx//4, idx%4].set_ylabel(y_column)
    #     plt.tight_layout()
        # st.pyplot(fig)

        fig1 = px.scatter(df, x=x_column, y=y_column, title=f'{y_column}-{x_column}',color=wtg_pn)

        st.plotly_chart(fig1)
        wtg_selected = st.selectbox('请选择想要比较的风机',wind_machine_names)
        if x_column == time_pn:
            data = df[[wtg_pn,x_column,y_column]].pivot(index=x_column,columns=wtg_pn,values=y_column)
            # st.write(data)
            rest_list = list(data.columns)
            rest_list.remove(wtg_selected)
            # st.write(wtg_selected)
            # st.write(rest_list)
            data_average = data[rest_list].mean(axis=1)
            # st.write(data_average)
            # st.write(data_average.shape)
            data_selected = data[[wtg_selected]]
            data_selected['average'] = data_average
            # st.write(data_selected)
            # st.write(data_selected.shape)
            data_melted = pd.melt(data_selected.reset_index(),id_vars = x_column,value_name = y_column)
            # st.write(data_melted)
            fig2 = px.scatter(data_melted, x=x_column,y=y_column,title=f'{wtg_selected}与全场其余风机平均值对比',color=wtg_pn)
        else:
            data =df[[wtg_pn,x_column,y_column]]
            data[wtg_pn] = np.where(df[wtg_pn]!=wtg_selected,'F00others',df[wtg_pn])
            data = data.sort_values(by=[wtg_pn])
            # st.write(data)
            fig2 = px.scatter(data, x=x_column,y=y_column,title=f'{wtg_selected}与全场其余风机平均值对比',color=wtg_pn)
        st.plotly_chart(fig2)

