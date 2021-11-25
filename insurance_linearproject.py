# -*- coding: utf-8 -*-
"""Insurance LinearProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pNxKDPjcFn4Wl_L9ZSMZLaZf-k-JM5yN
"""

from google.colab import drive
drive.mount('/content/drive')

"""# นำเข้า Library และ Load ข้อมูล"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/K-DAI/ปี 1 เทอม 2/05177001 Linear Algebra for Data Science/PJ_Mid/insurance.csv')
#df=pd.read_csv('insurance.csv')
df.head()

"""## ตรวจสอบค่า Null"""

df.isnull().sum()

df.shape

"""## ตรวจสอบชนิดข้อมูล"""

df.info()

"""## เปลี่ยนข้อมูล categorical  ให้เป็น Dummy"""

df['sex'] = df['sex'].replace('female',0 )
df['sex'] = df['sex'].replace('male',1)
df['smoker'] = df['smoker'].replace('yes', 1)
df['smoker'] = df['smoker'].replace('no', 0)
df['region'] = df['region'].replace('northeast', 0)
df['region'] = df['region'].replace('northwest', 1)
df['region'] = df['region'].replace('southeast', 2)
df['region'] = df['region'].replace('southwest', 3)
print(df)

sns.lmplot(data=df, x='age', y='charges', col='sex', hue='smoker') #scatter + linear plot

"""จากข้อมูลที่ได้มา จะสังเกตว่ายิ่งลูกค้าอายุเพิ่มขึ้นก็มีแนวโน้มที่จะจ่ายค่าเบี้ยประกันแพงขึ้น และ คนที่สูบบุหรี่ ก็มีแนวโน้มที่จะจ่ายเบี้ยประกันแพงกว่าคนที่ไม่สูบบุหรี่ เช่นกัน"""

sns.jointplot(data=df, x='age', y = 'charges', hue='smoker') #ใช้กรณีดู disribution ของข้อมูล

"""จากข้อมูลที่ได้มา กราฟนี้แสดงถึงความหนาแน่นและการทับซ้อนของข้อมูล จะสังเกตว่าทุกช่วงอายุนั้นจำนวนคนที่ ไม่สูบบุหรี่ นั้นมีจำนวนมากกว่า คนที่สูบบุหรี่ และ จำนวนคนที่ไม่สูบบุหรี่นั้นส่วนใหญ่จะมีแนวโน้มกระจุกตัวอยู่ช่วง เบี้ยประกัน 0 - 15000 ดอลลาร์"""

g = sns.pairplot(df)
 g.fig.set_size_inches(9,9)

"""## ดูความสัมพันธ์ของข้อมูล"""

plt.figure(figsize=(15,15))
sns.heatmap(data=df.corr(), annot=True, fmt=".2f")

df.columns

"""## ประกาศตัวแปร x และ y"""

from sklearn.model_selection import train_test_split
x = df.drop(columns=["charges"])
y = df["charges"]

"""## ตรวจสอบ MultiCollinearity ที่มีความสัมพันธ์กันเอง > 0.7"""

thershold = 0.7
corr_mat = x.corr().abs() # ค่าความสัมพันธ์ทางบวก
upper = corr_mat.where(np.triu(np.ones(corr_mat.shape), k=1).astype(np.bool)) # ทำสามเหลี่ยมบน ไม่เอา diagonal
drop = [column for column in upper.columns if any(upper[column] > thershold)] # เก็บค่าที่มากกว่า thershold
print(f"MultiCollinearity {thershold}: {drop}")

"""## แบ่งข้อมูล Train 70% Test 30%  และ fix ค่าแบ่งให้คงที่"""

x_train1, x_test1, y_train1, y_test1 = train_test_split(x, y, test_size=0.3, random_state=100) # train = 70%, test = 30 %, randomstate = fix ค่าตัวแบ่งให้ได้ตัวเดิม

print(x_train1.shape, x_test1.shape, y_train1.shape, y_test1.shape)

"""# สร้าง Model 1"""

from sklearn.linear_model import LinearRegression
LR = LinearRegression() # ย่อชื่อ

"""## ป้อน Input Output ให้ model เรียนรู้"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# m1 = LR.fit(x_train1, y_train1) # ป้อน Input Output ให้ model เรียนรู้

print(m1.coef_)
print(m1.intercept_)

list(zip(df.columns, m1.coef_))

df.columns

"""## ทำนายผล y จาก x (train) และ ค่า RMSE"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_train_pred1 = m1.predict(x_train1) # ทำนายผล y_train1 จาก x_train1

from sklearn.metrics import *
from math import sqrt

mse = mean_squared_error(y_train1, y_train_pred1) # ดูค่า Output เทียบกับ ค่า ทำนาย (train)
rmse = sqrt(mse)
print(mse)
print(rmse)

import statsmodels.api as sm
x_train1 = sm.add_constant(x_train1)  # เพิ่ม ค่าคงที่ constant เข้ามา
m1_train = sm.OLS(y_train1, x_train1).fit() 
print(m1_train.summary())

"""## R^2 (train)"""

print(f"R^2 = {m1_train.rsquared*100:.2f} %")
print(f"Adj R^2 = {m1_train.rsquared_adj*100:.2f} %")  # Multiple Linear Regression เน้นดู Adjusted R^2 เป็นหลัก (เพราะเมื่อเพิ่ม feature x เยอะๆ ค่า Adj R^2 จะไม่เพิ่มขึ้นเหมือน R^2)

m1_train.params 
# สูตร  y = -10428.119804 + 259.634761(age) + -0.054324(sex) + 293.390832(bmi) + 467.684029(children) + 24011.169706(smoker) + -499.424941(region)

"""## ทำนายผล y จาก x (test) และ ค่า RMSE"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_test_pred1 = m1.predict(x_test1) # ทำนายผล x_test

mse2 = mean_squared_error(y_test1, y_test_pred1) # ดูค่า Output เทียบกับ ค่า ทำนาย (test)
rmse2 = sqrt(mse2)
print(mse2)
print(rmse2)

import statsmodels.api as sm
x_test1 = sm.add_constant(x_test1)
m1_test = sm.OLS(y_test1, x_test1).fit()
print(m1_test.summary())

"""## R^2 (test)"""

print(f"R^2 = {m1_test.rsquared*100:.2f} %")
print(f"Adj R^2 = {m1_test.rsquared_adj*100:.2f} %")

m1_test.params

"""# สร้าง MODEL 2

##  กำจัด ตัวแปรที่ไม่มีนัยสำคัญเชิงสติถิ และ Normalization
"""

sns.displot(df["bmi"])

df.columns

"""กราฟเบ้ขวา """

sns.boxplot(df["bmi"])

sns.boxplot(df["age"])

sns.boxplot(df["sex"])

sns.boxplot(df["children"])

sns.boxplot(df["smoker"])

sns.boxplot(df["region"])

"""มี Outlier 1.5*IQR  เป็น Outlier อ่อนๆ และสมัยนี้คนน้ำหนักเกินกว่าเกณฑ์กันเป็นจำนวนมากจึงไม่ควรลบทิ้งไป"""

#q3_label_x3 = df["bmi"].quantile(.75)
#q1_label_x3 = df["bmi"].quantile(.25)
#IQR_x3 = q3_label_x3 - q1_label_x3
#thershold_outlier_max_x3 = q3_label_x3 + 1.5*IQR_x3
#thershold_outlier_min_x3 = q1_label_x3 - 1.5*IQR_x3

#print(thershold_outlier_min_x3, thershold_outlier_max_x3)

#df_x_out = df[df["bmi"] <= thershold_outlier_max_x3]

#df_x_out

#df.shape

#sns.boxplot(df_x_out["bmi"])

#sns.displot(df_x_out["bmi"])

"""## Normalization"""

from sklearn.model_selection import train_test_split
#x2 = df_x_out.drop(columns=["charges"])
#y2 = df_x_out["charges"]
x2 = df.drop(columns=["charges","sex","region"]) # sex, region ค่า P-value  > 0.05
y2 = df["charges"]

df.columns

from sklearn.preprocessing import StandardScaler 
scale = StandardScaler()
df_outnorm = scale.fit_transform(x2)  # ทำ Z-score
df_outnorm = pd.DataFrame(df_outnorm)
print(df_outnorm)

x2

"""## แบ่งข้อมูล Train 70% Test 30%  และ fix ค่าแบ่งให้คงที่"""

x_train2, x_test2, y_train2, y_test2 = train_test_split(x2, y2, test_size=0.3, random_state=100)

print(x_train2.shape, x_test2.shape, y_train2.shape, y_test2.shape)

from sklearn.linear_model import LinearRegression
LR = LinearRegression()

"""## ป้อน Input Output ให้ model เรียนรู้"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# m2 = LR.fit(x_train2, y_train2) # ป้อน Input Output ให้ model เรียนรู้

print(m2.coef_)
print(m2.intercept_)

list(zip(x2.columns, m2.coef_))

"""## ทำนายผล y จาก x (train) และ ค่า RMSE"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_train_pred2 = m2.predict(x_train2)

from sklearn.metrics import *
from math import sqrt

mse3 = mean_squared_error(y_train2, y_train_pred2)
rmse3 = sqrt(mse3)
print(mse3)
print(rmse3)

import statsmodels.api as sm
x_train2 = sm.add_constant(x_train2)
m2_train = sm.OLS(y_train2, x_train2).fit()
print(m2_train.summary())

"""## R^2 (train)"""

print(f"R^2 = {m2_train.rsquared*100:.2f} %")
print(f"Adj R^2 = {m2_train.rsquared_adj*100:.2f} %")

"""## ทำนายผล y จาก x (test) และ ค่า RMSE"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_test_pred2 = m2.predict(x_test2)

mse4 = mean_squared_error(y_test2, y_test_pred2)
rmse4 = sqrt(mse4)
print(mse4)
print(rmse4)

"""เมื่อทำการลบค่า x ที่ไม่มีนัยสำคัญทางสถิติ sex, region และทำ Standardization เปรียบเทียบค่า Adj R^2  = 78.47 % (RMSE = 5673.73) จาก model 1 และ Adj R^2 = 78.54 % (RMSE = 5650.24) จาก model 2

เปรียบเทียบเวลา Coding ข้อมูล 1338  records 
1.  เวลาที่ใช้ใน Model 1 = 3.86 + 1.99 + 1.96 = 7.81 ms
2.  เวลาที่ใช้ใน Model 2 = 4.25 + 4.42 + 1.83 = 10.5 ms

# สร้าง MODEL 3
"""

df.columns

from sklearn.model_selection import train_test_split

x3 = df.drop(columns=['age', 'sex', 'bmi', 'children', 'region', 'charges']) # smoker มีค่า Correlation สูงที่สุด = 0.79
y3 = df["charges"]

"""## แบ่งข้อมูล Train 70% Test 30%  และ fix ค่าแบ่งให้คงที่"""

x_train3, x_test3, y_train3, y_test3 = train_test_split(x3, y3, test_size=0.3, random_state=100)

print(x_train3.shape, x_test3.shape, y_train3.shape, y_test3.shape)

from sklearn.linear_model import LinearRegression
LR = LinearRegression()

"""## ป้อน Input Output ให้ model เรียนรู้"""

m3 = LR.fit(x_train3, y_train3) # ป้อน Input Output ให้ model เรียนรู้

print(m3.coef_)
print(m3.intercept_)

list(zip(x3.columns, m3.coef_))

"""## ทำนายผล y จาก x (train) และ ค่า RMSE"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_train_pred3 = m3.predict(x_train3)

from sklearn.metrics import *
from math import sqrt

mse5 = mean_squared_error(y_train2, y_train_pred2)
rmse5 = sqrt(mse5)
print(mse5)
print(rmse5)

import statsmodels.api as sm
x_train3 = sm.add_constant(x_train3)
m3_train = sm.OLS(y_train3, x_train3).fit()
print(m3_train.summary())

"""## R^2 (train)"""

print(f"R^2 = {m3_train.rsquared*100:.2f} %")
print(f"Adj R^2 = {m3_train.rsquared_adj*100:.2f} %")

"""## ทำนายผล y จาก x (test) และ ค่า RMSE"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_test_pred3 = m3.predict(x_test3)

mse6 = mean_squared_error(y_test3, y_test_pred3)
rmse6 = sqrt(mse6)
print(mse6)
print(rmse6)

"""# L1 - Lasso Regularization

feture selection จะตัดตัวแปรที่ไม่สำคัญออกไป สามารถกำหนด ให้ค่า ส.ป.ส. หน้า feature เป็น 0 ได้
"""

from sklearn.linear_model import Lasso

LR_L1 = Lasso() # default alpha = 1

# Commented out IPython magic to ensure Python compatibility.
# %%time
# m4 = LR_L1.fit(x_train2, y_train2)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_test_pred3 = LR_L1.predict(x_test2)

from sklearn.metrics import *
from math import sqrt

mse3 = mean_squared_error(y_test2, y_test_pred3)
rmse3 = sqrt(mse3)
print(mse3)
print(rmse3)

print(m4.intercept_)

list(zip(x2.columns, m4.coef_))

r2 = m4.score(x_test2,y_test2)
print(f"R^2 = {r2*100:.2f} %")

"""ข้อมูล model 2 จะได้ RMSE 5650.156471593312 R^2 = 78.01 %

ข้อมูล model 1 จะได้ RMSE 5673.529598758564 R^2 = 77.83 %

# L2 - Ridge Regularization

feture selection จะตัดตัวแปรที่ไม่สำคัญออกไป สามารถกำหนด ให้ค่า ส.ป.ส. หน้า feature เป็น 0 ไม่ได้ แต่ใกล้เคียงได้
"""

from sklearn.linear_model import Ridge

LR_L2 = Ridge() # alpha = 1

# Commented out IPython magic to ensure Python compatibility.
# %%time
# m5 = LR_L2.fit(x_train2, y_train2)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_test_pred4 = LR_L2.predict(x_test2)

from sklearn.metrics import *
from math import sqrt

mse4 = mean_squared_error(y_test2, y_test_pred4)
rmse4 = sqrt(mse4)
print(mse4)
print(rmse4)

print(m5.intercept_)

list(zip(x2.columns, m5.coef_))

r3 = m5.score(x_test2,y_test2)
print(f"R^2 = {r3*100:.2f} %")

"""ข้อมูล model 2 จะได้ RMSE 5647.745411401587 R^2 = 78.03 %

ข้อมูล model 1 จะได้ RMSE 5670.70832725905 R^2 = 77.85 %

## Elastic Net (L1+L2)
"""

from sklearn.linear_model import ElasticNet

LR_L1_L2 = ElasticNet(l1_ratio = 1) # alpha = 1

# Commented out IPython magic to ensure Python compatibility.
# %%time
# m6 = LR_L1_L2.fit(x_train2, y_train2)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_test_pred5 = LR_L1_L2.predict(x_test2)

from sklearn.metrics import *
from math import sqrt

mse5 = mean_squared_error(y_test2, y_test_pred5)
rmse5 = sqrt(mse5)
print(mse5)
print(rmse5)

r4 = m6.score(x_test2,y_test2)
print(f"R^2 = {r4*100:.2f} %")

print(m6.intercept_)

list(zip(x2.columns, m6.coef_))

"""ข้อมูล model 2 จะได้ RMSE 5650.156471593312 R^2 = 78.01 %

ข้อมูล model 1 จะได้ RMSE 5673.529598758564 R^2 = 77.83 %
"""