# -*- coding: utf-8 -*-
"""Customer_Shopping_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RJpR7VGWRch-LYJmGtiDnoG37kW9Ny_6
"""

import numpy as n
import pandas as p
import datetime
from matplotlib import pyplot as plt 
import seaborn as sns

from google.colab import drive
drive.mount('/content/gdrive')

d=p.read_csv("/content/gdrive/My Drive/Data_Mining_Project/marketing_campaign.csv",sep='\t')
d.info()

d.head(20).T

print("Total Missing values in all Columns!!!")
d.isnull().sum()

print("Replacing Null Values!!!")
d.fillna(d['Income'].mean())

print("Birth Year Status!!!\n",d['Year_Birth'].value_counts(),'\n')

print("Education Status!!!\n",d['Education'].value_counts(),'\n')

print("Marital Status!!!\n",d['Marital_Status'].value_counts())

x=d['Education']
y=d['Year_Birth']
plt.bar(x,y)
plt.xlabel('Education')
plt.ylabel("Year_Birth")

plt.ylim(d['Year_Birth'].min(),d['Year_Birth'].max(),10)
plt.show()

x=d['Education']
y=d['Marital_Status']
plt.bar(x,y)
plt.xlabel('Education')
plt.ylabel("Marital_Status")


plt.show()

d1=d.copy()

d1=d1.dropna()

d1.isna().sum().sum()

d1["Dt_Customer"]=p.to_datetime(d1["Dt_Customer"])

d1.describe()

d1.head(10)

d2=d1.copy()

d2["Age"]=2022-d1["Year_Birth"]

d2["Kids"]=d2["Kidhome"]+d2["Teenhome"]
d2["Kids"].head(10)

d2["TotalAmount"]=d2["MntWines"]+d2["MntFruits"]+d2["MntGoldProds"]+d2["MntFishProducts"]+d2["MntSweetProducts"]+d2["MntMeatProducts"]

d2["TotalAmount"].head(10)

d2["TotalPurchases"]=d2["NumWebPurchases"]+d2["NumCatalogPurchases"]+d2["NumStorePurchases"]
d2["TotalPurchases"].head(10)

d2.drop(["Z_CostContact","Z_Revenue","Year_Birth","Kidhome","Teenhome","ID"],axis=1,inplace=True)

d2.describe()

sns.countplot(x=d2["Education"],data=d2)

sns.countplot(x=d2["Marital_Status"],data=d2)

sns.boxplot(x=d2["Income"])

f=plt.figure(figsize=(6,6))
x=d2["Education"].value_counts().sort_values()
plt.pie(x=x, labels=['2n Cycle', 'Basic', 'Master', 'PhD', 'Graduation'],autopct='%1.1F%%')

plt.figure(figsize=(5,5))
x = d2['Marital_Status'].value_counts().sort_values()
plt.pie(x=x, labels=['YoLo', 'Absurd','Alone', 'Window', 'Divorced', 'Single', 'Together','Married'],
        autopct = '%1.1f%%', )
plt.axis('equal')

d2 = d2.drop(d2.loc[d2['Income'] > 600000].index)
d2 = d2.drop(d2.loc[d2['Age'] > 100].index)

d2['Have_Children'] = n.where(d2.Kids > 0, 1, 0)
d2.head()

pairplot = d2.loc[:, ['Income', 'Age', 'TotalAmount', 'Have_Children']]

sns.pairplot(pairplot, hue='Have_Children', palette='Set2',size=3)

a=[0,10,20,30,40,50,60,70,80,90,100]
age_group=p.cut(d2['Age'],bins=a)
print(age_group.value_counts())

plt.figure(figsize=(10,5))
sns.countplot(y=age_group,palette='Set1')
plt.title=('Count of AgeGroups')

sns.boxplot(x=age_group, y=d2['TotalAmount'], palette='Set3')

sns.boxplot(x=d2['Education'], y=d2['TotalAmount'], palette='Set2')

sns.barplot(x= 'Marital_Status',y='TotalAmount',hue='Education',data=d2, ci=1, palette='Set3')

sns.regplot(y='TotalAmount', x='Income', data=d2, color='g')

sns.histplot(d2['NumWebVisitsMonth'], bins=50, kde=True, color='b')

sns.histplot(data=d2,x='NumWebPurchases')

accepted = d2[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']]
accepted = accepted.apply(p.DataFrame.sum)

print(accepted)

plt.figure(figsize=(12,6))
sns.barplot(x=accepted.index, y=accepted, palette='Set2')

Date = d2.set_index('Dt_Customer')
Date = Date.resample('Y').count()

plt.figure(figsize=(11,6))
Date.NumWebPurchases.plot()

Date = d2.set_index('Dt_Customer')
Date = Date.resample('M').count()

plt.figure(figsize=(14,4))
Date.NumWebPurchases.plot()

Date = d2.set_index('Dt_Customer')
Date = Date.resample('Y').count()

plt.figure(figsize=(12,4))
Date.NumStorePurchases.plot()

Date = d2.set_index('Dt_Customer')
Date = Date.resample('M').count()

plt.figure(figsize=(10,5))
Date.NumStorePurchases.plot()

Date = d2.set_index('Dt_Customer')
Date = Date.resample('M').count()

plt.figure(figsize=(12,5))
Date.TotalAmount.plot()

from sklearn.preprocessing import LabelEncoder
s = (d2.dtypes == 'object')
cols = list(s[s].index)
for i in cols:
    d2[i]=d2[[i]].apply(LabelEncoder().fit_transform)

plt.figure(figsize = (20, 20))
data1 = d2.iloc[:, 1:-1]
sns.heatmap(data1.corr(), annot=True, cmap='Set3')

d3 = d2.copy()
cols_del = [ 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1','AcceptedCmp2', 
            'Complain', 'Response', 'Have_Children', 'Dt_Customer',  'Kids']
d3 = d3.drop(cols_del, axis=1)
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
s = StandardScaler()
s.fit(d3)
scaled_data = p.DataFrame(s.transform(d3),columns= d3.columns )
pca = PCA(n_components=5)
pca.fit(scaled_data)
PCA_ds = p.DataFrame(pca.transform(scaled_data), columns=(["col1","col2", "col3","col4","col5"]))
PCA_ds.describe().T

from sklearn.cluster import KMeans
l=[]
for i in range(1,7):
  kmeans=KMeans(n_clusters=i,init='k-means++',random_state=100)
  kmeans.fit(d3)
  l.append(kmeans.inertia_)
plt.figure(figsize=(10,5))
plt.plot(range(1,7),l, 'bx-')
plt.xlabel('Number of clusters')
plt.ylabel('sum of squared distance ')
plt.show()

from yellowbrick.cluster import KElbowVisualizer
e=KElbowVisualizer(KMeans(),k=6)
e.fit(PCA_ds)
e.show()

from sklearn.cluster import AgglomerativeClustering
AC=AgglomerativeClustering(n_clusters=6)
a=AC.fit_predict(PCA_ds)
PCA_ds["Clusters"]=a
d3["Clusters"]=a

x =PCA_ds["col1"]
y =PCA_ds["col2"]
z =PCA_ds["col3"]
plt.figure(figsize=(5,5))
axs=plt.subplot(111, projection='3d', label="bla")
axs.scatter(x, y, z, s=50, c=PCA_ds["Clusters"], marker='o', cmap = 'Set1' )
axs.set_title("The Plot Of The Clusters")
plt.show()

plt.figure(figsize=(10,4))
a=sns.countplot(x=d3["Clusters"],palette="Set1")
a.set_title("Cluster Distribution")
plt.show()

plt.figure(figsize=(10,5))
b=sns.scatterplot(data=d3,x=d3["TotalAmount"],y=d3["Income"],hue=d3["Clusters"])
b.set_title("Clusters based on Income and Spent")
plt.legend()
plt.show()

plt.figure(figsize=(10,5))
b=sns.scatterplot(data=d3,x=d3["TotalAmount"],y=d3["Income"],hue=d3['Education'],palette='Set2')
b.set_title("Education based on Income and Spent")
plt.legend()
plt.show()

plt.figure(figsize=(10,5))
sns.swarmplot(x=d3["Clusters"], y=d3["TotalAmount"], alpha=1.0, palette= 'Set1' )

plt.figure(figsize=(10,5))
sns.swarmplot(x=d3["Clusters"], y=d3["NumWebPurchases"], alpha=0.9, palette= 'Set3' )

plt.figure(figsize=(10,5))
sns.swarmplot(x=d3["Clusters"], y=d3["NumStorePurchases"], alpha=0.6, palette= 'Set2' )

plt.figure(figsize=(15,5))
pl = sns.countplot(x=d3["TotalPurchases"],hue=d3["Clusters"], palette= 'Set3')
pl.set_title("Total Count Of Purchases")
pl.set_xlabel("Number Of Total Purchases")
plt.show()

d3["TotalAcceptedCamp"]=d1['AcceptedCmp1']+d1['AcceptedCmp2']+d1['AcceptedCmp3']+d1['AcceptedCmp4']+d1['AcceptedCmp5']
plt.figure(figsize=(15,5))
pl = sns.countplot(x=d3["TotalAcceptedCamp"],hue=d3["Clusters"], palette = 'Set1')
pl.set_title("Total Count Of Accepted Campaigns")
pl.set_xlabel("Number Of Campaigns")
plt.show()

plt.figure(figsize=(12,6))
sns.swarmplot(x=d3["Clusters"], y=d3["TotalAcceptedCamp"], alpha=1, palette= 'Set2' )

plt.figure(figsize=(10,5))
b=sns.scatterplot(data=d3,x=d3["Income"],y=d3["TotalAcceptedCamp"],hue=d3['Clusters'],palette='Set1')
b.set_title("Clusters based on Income and Accepted Campaigns")
plt.legend()
plt.show()

