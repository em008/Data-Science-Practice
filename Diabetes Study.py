"""
Diabetes Study
- Compute mean values and variance for all values
- Plot boxplots for BMI, BP and Y depending on gender
- What is the the distribution of Age, Sex, BMI and Y variables?
- Test the correlation between different variables and disease progression (Y)
- Test the hypothesis that the degree of diabetes progression is different between men and women
- Data: https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html
"""

"""
Getting the Data
Columns: Age, Sex, BMI, BP, S1, S2, S3, S4, S5, S6, Y
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../data/diabetes.tsv",sep='\t')
df.head()

"""
Compute mean values and variance for all values
"""
df.describe()
df.mean()
df.var()

"""
Plot boxplots for BMI, BP and Y depending on gender
"""
for col in ['BMI','BP','Y']:
    df.boxplot(column=col,by='SEX')
plt.show()

"""
What is the the distribution of Age, Sex, BMI and Y variables?
"""
for col in ['AGE','SEX','BMI','Y']:
    df[col].hist()
    plt.show()

# Age - normal
# Sex - uniform
# BMI, Y - skewed left

"""
Test the correlation between different variables and disease progression (Y)
"""
# Correlation matrix would give the most useful information on which values are dependent.
df.corr() 

# The strongest correlation of Y is BMI and S5. 

fig, ax = plt.subplots(1,3,figsize=(10,5))
for i,n in enumerate(['BMI','S5','BP']):
    ax[i].scatter(df['Y'],df[n])
    ax[i].set_title(n)
plt.show()

"""
Test the hypothesis that the degree of diabetes progression is different between men and women
"""
from scipy.stats import ttest_ind

tval, pval = ttest_ind(df.loc[df['SEX']==1,['Y']], df.loc[df['SEX']==2,['Y']],equal_var=False)
print(f"T-value = {tval[0]:.2f}\nP-value: {pval[0]}")

# T-value = -0.90
# P-value: 0.3674449793083975

"""
Conclusion: 
p-value close to 0 would indicate high confidence in our hypothesis. There is no strong evidence that sex affects progression of diabetes.
"""
