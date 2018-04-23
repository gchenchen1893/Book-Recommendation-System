import pandas as pd
import numpy as np

def Construct_Utility_Matrix(ratings,books,users):
	# ratings_books:
	# user   ISBN   rating   bookName
	ratings_books = pd.merge(ratings, books, on='ISBN')
	columns = ['yearOfPublication', 'publisher', 'bookAuthor', 'imageUrlS', 'imageUrlM', 'imageUrlL']
	ratings_books = ratings_books.drop(columns, axis=1)
	ratings_books = ratings_books.dropna(axis = 0, subset = ['bookTitle'])

	# book_ratingCount:
	# bookName ratingCount
	book_ratingCount = (ratings_books.
	     groupby(by = ['bookTitle'])['bookRating'].
	     count().
	     reset_index().
	     rename(columns = {'bookRating': 'totalRatingCount'})
	     [['bookTitle', 'totalRatingCount']]
	    )

	# ratings_books_count:
	# user   ISBN   rating   bookName   ratingCount
	ratings_books_count = ratings_books.merge(book_ratingCount, left_on = 'bookTitle', right_on = 'bookTitle', how = 'left')

	# ratings_books_count_overFifty:
	# rating number > 50
	# user   ISBN   rating   bookName ratingCount
	popularity = 50
	ratings_books_count_overFifty = ratings_books_count.query('totalRatingCount >= @popularity')

	# combined:
	# userLocation   Age   user   ISBN   rating   bookName   ratingCount
	combined = ratings_books_count_overFifty.merge(users, left_on = 'userID', right_on = 'userID', how = 'left')

	# us_canada_user_rating:
	# userLocation  user   ISBN   rating   bookName   ratingCount
	# only canada and USA
	us_canada_user_rating = combined[combined['Location'].str.contains("usa|canada")]
	us_canada_user_rating=us_canada_user_rating.drop('Age', axis=1)
	us_canada_user_rating = us_canada_user_rating.drop_duplicates(['userID', 'bookTitle'])
	#       User1 User2 User3 User4 User5
	# book1
	# book2
	# book3
	# book4
	# book5
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
	print "us-canada utility matrix(BookName,User): "+str(us_canada_user_rating_pivot.shape)
	# show the corresponding index and book title
	# helper(us_canada_user_rating_pivot)
	return us_canada_user_rating

def helper(us_canada_user_rating_pivot):
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
	dic={}
	for i in range(0,len(us_canada_user_rating_pivot.index)):
		dic[i]=us_canada_user_rating_pivot.index[i]
		print 'Index of Book: '+str(i)
		print 'Title of Book: '+us_canada_user_rating_pivot.index[i]+'\n'

def KNN_Recommendation_System(us_canada_user_rating,bookName):
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
	book_title = us_canada_user_rating_pivot.index
	book_list = list(book_title)
	bookIndex = book_list.index(bookName)

	from scipy.sparse import csr_matrix
	us_canada_user_rating_matrix = csr_matrix(us_canada_user_rating_pivot.values)

	from sklearn.neighbors import NearestNeighbors
	model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
	model_knn.fit(us_canada_user_rating_matrix)

	query_index = bookIndex
	# pick a book randomly
	distances, indices = model_knn.kneighbors(us_canada_user_rating_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 6)
	# distances: knn distance between target vector
	# indices: index of similar vectors
	for i in range(0, len(distances.flatten())):
	    if i == 0:
	        print('KNN Recommendations for {0}:\n'.format(us_canada_user_rating_pivot.index[query_index]))
	    else:
	        print('{0}: {1}, with distance of {2}:'.format(i, us_canada_user_rating_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
