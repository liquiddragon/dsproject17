import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fuzzywuzzy import process

cluster_column_name_prefix = 'kcat'

def plot_clusters(world, df, pred):
    global cluster_column_name_prefix

    # Name changes taken from gis.py
    change = [{"Bahamas, The": "Bahamas"}, {"Bosnia and Herzegovina": "Bosnia and Herz."},
            {"Brunei Darussalam": "Brunei"}, {"Central African Republic": "Central African Rep."},
            {"Congo, Dem. Rep.": "Dem. Rep. Congo"}, {"Cote d\'Ivoire": "Côte d\'Ivoire"},
            {"Czech Republic": "Czech Rep."}, {"Congo, Rep.": "Congo"},
            {"Egypt, Arab Rep.": "Egypt"}, {'Dominican Republic': 'Dominican Rep.'},
            {"Equatorial Guinea": "Eq. Guinea"}, {'Korea, Rep.': "Korea"},
            {"Gambia, The": "Gambia"}, {'Iran, Islamic Rep.': "Iran"},
            {'Kyrgyz Republic': 'Kyrgyzstan'}, {'Macedonia, FYR': "Macedonia"},
            {'Russian Federation': "Russia"}, {'South Sudan': "S. Sudan"},
            {'Slovak Republic': "Slovakia"}, {'Solomon Islands': "Solomon Is."},
            {'Syrian Arab Republic': "Syria"}, {'Venezuela, RB': "Venezuela"}, {'Yemen, Rep.': "Yemen"}]
    for t in change:
        df.rename(columns=t, inplace=True)

    # Map predictions to countries in a map
    note_displayed = False
    countries = world['name'].tolist()  # World map country names
    for index, cname in enumerate(df.columns):  # Our country names
        candidate = process.extractOne(cname, countries)
        if candidate[1] > 79:
            idx = countries.index(candidate[0])
            for i in range(0, len(pred)):
                col_name = cluster_column_name_prefix + str(i)
                world.loc[idx, col_name] = (pred[i][index] + 1)
        else:
            if not note_displayed:
                print('Following countries are missing from used map file and thus missing from pictures.')
                note_displayed = True
            print('Missing from map: ' + cname)

    # Create plots from predictions
    for i in range(0, len(pred)):
        col_name = cluster_column_name_prefix + str(i)
        # Change coloring by using different value for cmap, see http://matplotlib.org/users/colormaps.html for values
        world.plot(column=col_name, cmap='viridis')
        # Change extension to alter file format, see http://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html#matplotlib.pyplot.savefig
        filename = col_name + '.png'
        # Comment following line (and uncomment show) to display maps instead of saving them to a file
        plt.savefig(filename)
        # Uncomment following to display predictions in addition to saving them to a file
        #plt.show()

# Print predictions
def print_predictions(pred, df):
    year = 2016
    for p in pred:
        print('Year: ' + str(year))
        for idx in range(0, len(df.columns)):
            print('  ' + df.columns[idx] + ': ' + str(p[idx]))
        print()
        year += 1

#
# Main
#
df = pd.read_csv('predictions.csv', index_col=0)

# Create three clusters from each predicted year
pred = []
for i in range(0, len(df)):
    pred.append(KMeans(n_clusters=3, random_state=170).fit_predict(df.iloc[1].values.reshape(-1,1)))

# Load world map and add category columns for year predicted year
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
for i in range(0, len(pred)):
    col_name = cluster_column_name_prefix + str(i)
    world[col_name] = 0

print_predictions(pred, df)
plot_clusters(world, df, pred)
