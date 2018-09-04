#预处理数据，将数据更改为含有临近指标的数据，并分为测试集和训练集

import pandas as pd
import numpy as np

def main():
    #读入数据
    background = pd.read_csv('background.csv')
    signal = pd.read_csv('signal.csv')
    frames = [background, signal]

    #合并与排序
    total = pd.concat(frames)
    newtotal = total.reset_index(drop=True)
    newtotal.rename(columns={'0':'EventID', '1':'Layer', '2':'Wire', '3':'Rawtime', '4':'ADC', '5':'t0', '6':'isSignal'}, inplace=True)

    #构建neighbor集
    ext = pd.DataFrame(columns=['nRt', 'nRA', 'nLt', 'nLA'])
    for i, row in enumerate(newtotal.itertuples()):
        for row2 in newtotal.itertuples():
            if row2.Layer == row.Layer:
                if row2.Wire == row.Wire+1:
                    ext.loc[i, 'nRt'] = row2.Rawtime
                    ext.loc[i, 'nRA'] = row2.ADC
                if row2.Wire == row.Wire-1:
                    ext.loc[i, 'nLt'] = row2.Rawtime
                    ext.loc[i, 'nLA'] = row2.ADC

    ext.to_csv('ext.csv')
    result=pd.concat([newtotal, ext], axis=1)
    result.fillna(-1)
    result.to_csv('result.csv')


if __name__ == '__main__':
    main()
