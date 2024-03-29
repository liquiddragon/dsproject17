import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est > 0) & (world.name != "Antarctica")]

df = pd.read_csv("dsproject17/presentation/predictions.csv")

remove = ["Aruba", "Bahrain", "Barbados", "Cabo Verde", "Comoros", "Curacao", 'French Polynesia', 'Grenada',
          'Guam', 'Hong Kong SAR, China', 'Macao SAR, China', 'Maldives', 'Malta', 'Mauritius', 'Micronesia, Fed. Sts.',
          'Sao Tome and Principe', 'Samoa', 'Singapore', 'St. Lucia', 'St. Vincent and the Grenadines', 'Tonga',
          'Virgin Islands (U.S.)']
for t in remove:
    df.drop(t, axis=1, inplace=True)

change = [{"Bahamas, The": "Bahamas"},
          {"Bosnia and Herzegovina": "Bosnia and Herz."}, {"Brunei Darussalam": "Brunei"},
          {"Central African Republic": "Central African Rep."}, {"Congo, Dem. Rep.": "Dem. Rep. Congo"},
          {"Cote d\'Ivoire": "Côte d\'Ivoire"}, {"Czech Republic": "Czech Rep."}, {"Congo, Rep.": "Congo"},
          {"Egypt, Arab Rep.": "Egypt"}, {'Dominican Republic': 'Dominican Rep.'}, {"Equatorial Guinea": "Eq. Guinea"},
          {'Korea, Rep.': "Korea"}, {"Gambia, The": "Gambia"}, {'Iran, Islamic Rep.': "Iran"},
          {'Kyrgyz Republic': 'Kyrgyzstan'}, {'Macedonia, FYR': "Macedonia"}, {'Russian Federation': "Russia"},
          {'South Sudan': "S. Sudan"}, {'Slovak Republic': "Slovakia"}, {'Solomon Islands': "Solomon Is."},
          {'Syrian Arab Republic': "Syria"}, {'Venezuela, RB': "Venezuela"}, {'Yemen, Rep.': "Yemen"}]
for t in change:
    df.rename(columns=t, inplace=True)

missing = ['Falkland Is.', 'Dem. Rep. Korea', 'Fr. S. Antarctic Lands', 'Greenland', 'Kosovo', 'N. Cyprus',
           'New Caledonia', 'Palestine', "Somaliland", "Taiwan", "Yemen"]
for t in missing:
    df[t] = np.zeros(15)

df2 = df.drop("Unnamed: 0", axis=1)
df2 = df2[world.name]

# gdp images
plt.ioff()
for i in range(15):
    fig, ax = plt.subplots()
    ax.set_title("{0}".format(2016 + i))
    plt.axis("off")
    world['gdp_per_cap'] = np.asarray(df2.loc[i])
    vmin, vmax = 0, 7
    t = world.plot(ax=ax, column='gdp_per_cap', scheme='quantiles', vmin=vmin, vmax=vmax, cmap="cool")

    fig = t.get_figure()
    cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    sm = plt.cm.ScalarMappable(cmap='cool', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    fig.colorbar(sm, cax=cax)
    plt.savefig("dsproject17/presentation/images/{0}.png".format(i))

# top/bottom performers separate images
path = "dsproject17/presentation/"
files = ["bottom_performers_high_income.csv", "bottom_performers_low_income.csv",
         "top_performers_low_income.csv", "top_performers_high_income.csv"]
for f in files:
    df = pd.read_csv(path + f)
    for c in change:
        df.replace(c, inplace=True)
        df = df[~df[df.columns[0]].isin(remove)]
    plt.ioff()
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
    base = world.plot(color='white', edgecolor='black')
    plt.axis("off")
    world = world[world.name.isin(np.asarray(df[df.columns[0]]))]
    vmin, vmax = int(np.min(df[df.columns[1]])), int(np.max(df[df.columns[1]]))
    t = world.plot(ax=base, color="r")
    plt.savefig("dsproject17/presentation/{0}.png".format(f[:-3]))

# top/bottom performers
path = "dsproject17/presentation/"
files = ["top_performers_high_income.csv", "top_performers_low_income.csv",
         "bottom_performers_high_income.csv", "bottom_performers_low_income.csv"]
countries = []
for f in files:
    df = pd.read_csv(path + f)
    for c in change:
        df.replace(c, inplace=True)
        df = df[~df[df.columns[0]].isin(remove)]
    countries.append(df)
plt.ioff()
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
base = world.plot(color='white', edgecolor='black')
plt.axis("off")
colors = ["darkorange", "peachpuff", "b", "lightskyblue"]
labels = [f[:-4].replace("_", " ").capitalize() for f in files]
for i in range(len(countries)):
    c = countries[i]
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
    world = world[world.name.isin(np.asarray(c[c.columns[0]]))]
    t = world.plot(ax=base, color=colors[i], label=labels[i], legend=True)
    plt.legend(loc="upper right")

patch = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, labels)]
plt.legend(handles=patch, bbox_to_anchor=(-0.1, 1.02, 1.1, .102), loc=3, ncol=2, mode="expand")
plt.savefig("dsproject17/presentation/all.png")


# gdp differences between years 2000, 2015
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
df1 = pd.read_csv("dsproject17/data/processed/gdp_per_capita_current_usd.csv")
gdp = pd.DataFrame((df1.iloc[55] - df1.iloc[55-15])/df1.iloc[55-15]).transpose()
for t in remove:
    gdp.drop(t, axis=1, inplace=True)
for t in change:
    gdp.rename(columns=t, inplace=True)
for t in missing:
    gdp[t] = np.zeros(1)

gdp = gdp.drop("Unnamed: 0", axis=1)
gdp = gdp[world.name]

vmax, vmin = int(gdp.iloc[0].max()), int(gdp.iloc[0].min())
fig, ax = plt.subplots()
ax.set_title("2015")
plt.axis("off")
world['gdp_per_cap'] = np.nan_to_num(np.asarray(gdp.iloc[0]))
t = world.plot(ax=ax, column='gdp_per_cap', vmin=vmin, vmax=vmax, cmap="cool")
fig = t.get_figure()
cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
sm = plt.cm.ScalarMappable(cmap='cool', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
fig.colorbar(sm, cax=cax)
plt.savefig("dsproject17/presentation/2015.png")



