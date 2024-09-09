import pandas as pd
import matplotlib.pyplot as mtp

antibiograma = pd.read_excel('Antibiogramav0.10.xlsx')
antibiograma.head()

### Aquí quitariamos las que no nos sean útiles si quisieramos
antibiograma = antibiograma.drop(columns=["Extracción","Fecha", "Fecha de solicitud", "Fecha de Activación",
                                         "Historia H.Clinico","Fecha Nacimiento", "Tipo de Paciente",
                                          "Prueba", "Muestra", "Nº Cultivo", "Mecanismo Resistencia", "Pool Antibioticos"])

CMIs = []

for i in antibiograma.columns:
    if "CMI" in i:
        CMIs.append(i)
        
antibiograma = antibiograma.drop(columns=CMIs)


sinrepetidos = antibiograma.drop_duplicates(subset=["Número"])

sinrepetidos = sinrepetidos.dropna(subset=["Descripción"])

sinrepetidos = sinrepetidos.reset_index(drop="T")

sinrepetidos["Edad del Paciente"] = sinrepetidos["Edad del Paciente"].str.replace(r"años", "", regex = True)


#sinrepetidos["Fecha de solicitud"] = sinrepetidos["Fecha de solicitud"].str.replace(r"\d{1,2}/\d{1,2}/\d{2} ", "", regex = True) 
#sinrepetidos["Fecha de Activación"] = sinrepetidos["Fecha de Activación"].str.replace(r"\d{1,2}/\d{1,2}/\d{2} ", "", regex = True) 

sinrepetidos.to_csv("sinrepetidos.txt", sep = '\t',index=False)

#sinrepetidos.head(20)
#sinrepetidos.isnull()
#sinrepetidos.shape

#sinrepetidos1 = sinrepetidos.drop(columns=["Mecanismo Resistencia"])
sinrepetidos1 = sinrepetidos.reset_index(drop="T")
 
sinrepetidos1["Edad del Paciente"] = sinrepetidos1["Edad del Paciente"].astype(int)

sinrepetidos1.rename(columns = {'Sexo del Paciente': 'Sexo'}, inplace= True)
sinrepetidos1.rename(columns = {'Edad del Paciente': 'Edad'}, inplace= True)

#sinrepetidos1.head(5)

# Plots of Age x Gender
fig, (ax0, ax1, ax2) = mtp.subplots(nrows=1, ncols=3)
ax0.boxplot([sinrepetidos1[sinrepetidos1['Sexo']=='M']['Edad'] , sinrepetidos1[sinrepetidos1['Sexo']=='F']['Edad']],     
            labels= ['Masculino', 'Femenino'])
ax0.grid(True)
ax0.set_ylabel('Edad')

ax1.violinplot(sinrepetidos1[sinrepetidos1['Sexo']=='M']['Edad'], showmedians=True, showmeans=True)
ax1.set_xticks([1])
ax1.set_xticklabels( ['Masculino',])
ax1.set_yticks([])

ax2.violinplot(sinrepetidos1[sinrepetidos1['Sexo']=='F']['Edad'], showmedians=True, showmeans=True)
ax2.set_xticks([1])
ax2.set_yticks([])
ax2.set_xticklabels( ['Femenino',])

fig.savefig("Box-Violinplot.jpg")

# Plot of infection x Gender

tab = pd.crosstab(
    index= sinrepetidos1['Descripción'],
    columns=sinrepetidos1['Sexo'],
    margins=True
).sort_values('All', ascending=False)

threshold = 5
filtered_tab = tab[tab['All'] >= threshold]

filtered_tab = filtered_tab.drop('All',axis=1)
filtered_tab = filtered_tab.drop('All',axis=0)

mtp.figure(figsize=(10, 6))

ax = filtered_tab.plot(kind='bar', stacked=True)
mtp.xticks(rotation=45, ha='right') 
mtp.tight_layout()

mtp.subplots_adjust(bottom=0.2)

mtp.savefig("DistributionInfectionsSex.jpg", bbox_inches='tight')

# Plot of Servicio x Gender

tab1 = pd.crosstab(
    index= sinrepetidos1['Servicio'],
    columns=sinrepetidos1['Sexo'],
    margins=True
).sort_values('All', ascending=False)
tab1 = tab1.drop('All',axis=1)
tab1 = tab1.drop('All',axis=0)

mtp.figure(figsize=(10, 6))
ax1 = tab1.plot(kind='bar', stacked=True)

mtp.tight_layout()
mtp.savefig("DistributionServiceSex.jpg")


# Plot of Proportions of each gender
gender_counts = sinrepetidos1['Sexo'].value_counts()
gender_proportions = gender_counts / gender_counts.sum()
default_colors = mtp.rcParams['axes.prop_cycle'].by_key()['color']

color_map = {'F': default_colors[0], 'M': default_colors[1]} 

colors = [color_map[gender] for gender in gender_proportions.index]
mtp.figure(figsize=(10,6))
mtp.pie(gender_proportions, labels=gender_proportions.index,colors= colors, autopct='%1.1f%%', startangle=140)
mtp.tight_layout()
mtp.savefig("malesvsfemales.jpg")
