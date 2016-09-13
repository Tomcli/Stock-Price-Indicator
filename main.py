import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeRegressor
from IPython.display import display # Allows the use of display() for DataFrames
import matplotlib.pyplot as plt
import matplotlib

# Show matplotlib plots inline (nicely formatted in the notebook)

def run():
	matplotlib.style.use('ggplot')
	# Load the wholesale customers dataset
	try:
	    data = pd.read_csv("customers.csv")
	    data.drop(['Region', 'Channel'], axis = 1, inplace = True)
	    print "Wholesale customers dataset has {} samples with {} features each.".format(*data.shape)
	except:
	    print "Dataset could not be loaded. Is the dataset missing?"

	# TODO: Select three indices of your choice you wish to sample from the dataset
	indices = [1,2,6]

	# Create a DataFrame of the chosen samples
	samples = pd.DataFrame(data.loc[indices], columns = data.keys()).reset_index(drop = True)
	print "Chosen samples of wholesale customers dataset:"
	display(samples)
	display(data.describe())

	# TODO: Make a copy of the DataFrame, using the 'drop' function to drop the given feature
	new_data = data.drop(['Detergents_Paper'], 1)

	# TODO: Split the data into training and testing sets using the given feature as the target
	X_all = new_data
	y_all = data[['Detergents_Paper']]
	X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.25, random_state=0)

	# TODO: Create a decision tree regressor and fit it to the training set
	regressor = DecisionTreeRegressor(random_state=0)
	regressor.fit(X_train,y_train)

	# TODO: Report the score of the prediction using the testing set
	score = regressor.score(X_test,y_test)
	print "Regressor R2 score: {:.4f}.".format(score)
	pd.scatter_matrix(data, alpha = 0.3, figsize = (14,8), diagonal = 'kde');
	plt.show()

if __name__ == '__main__':
    run()