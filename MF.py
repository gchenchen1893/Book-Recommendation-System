import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD
import warnings

def MF_Recommendation_System(us_canada_user_rating,bookName):
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'userID', columns = 'bookTitle', values = 'bookRating').fillna(0)
	#us_canada_user_rating_pivot.head()

	# SVD decomposition and reduce dimensions
	SVD = TruncatedSVD(n_components=300,random_state=10)
	matrix=SVD.fit_transform(us_canada_user_rating_pivot.values.T)

	warnings.filterwarnings("ignore",category=RuntimeWarning)
	# Correlation Matrix
	corr=np.corrcoef(matrix)

	book_title = us_canada_user_rating_pivot.columns
	book_list = list(book_title)
	bookIndex = book_list.index(bookName)

	book = us_canada_user_rating_pivot.columns[bookIndex]
	target_index = book_list.index(book)

	print('Matrix Factorization Recommendations for {0}:\n'.format(book))
	temp=list(book_title[(corr[target_index].argsort()[-9:-4])])
	for i in range(0,len(temp)):
	    print str(i+1)+": "+str(temp[len(temp)-1-i])
