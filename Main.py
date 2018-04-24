import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import KNN
import MF
import UserPredict

books = pd.read_csv('BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
users = pd.read_csv('BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']


# Data Analysis
def Distribution(ratings):
	# Here, we sorted the books according to their rating counts and show their average ratings
	# But the most popular books does not mean it receives the highest rating
	count_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
	average_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].mean())
	average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
	print average_rating.sort_values('ratingCount', ascending=False).head()

	# Plot of Rating Distribution
	subplot=plt.subplot(121)
	plt.rc("font",size=15)
	ratings.bookRating.value_counts(sort=False).plot(kind='bar')
	plt.title('Rating Distribution')
	plt.xlabel('Rating')
	plt.ylabel('Count')

	# Plot of Age Distribution
	subplot=plt.subplot(122)
	users.Age.hist(bins=[0,10,20,30,40,50,100])
	plt.title('Age Distribution')
	plt.xlabel('Age')
	plt.ylabel('Count')
	plt.show()

Distribution(ratings)
def Recommendation_System_BookList(us_canada_user_rating):
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'userID', columns = 'bookTitle', values = 'bookRating').fillna(0)
	# us_canada_user_rating_pivot.head()

	book_title = us_canada_user_rating_pivot.columns
	book_list = list(book_title)
	return book_list

def Recommendation_System_userIdList(us_canada_user_rating):
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'userID', columns = 'bookTitle', values = 'bookRating').fillna(0)
	# us_canada_user_rating_pivot.head()

	user_id = us_canada_user_rating_pivot.index
	id_list = list(user_id)
	return id_list

def Similarity(ratings):
	# users with less than 200 ratings, and books with less than 100 ratings are excluded.
	count_user = ratings['userID'].value_counts()
	ratings = ratings[ratings['userID'].isin(count_user[count_user >= 100].index)]
	count_book = ratings['bookRating'].value_counts()
	ratings = ratings[ratings['bookRating'].isin(count_book[count_book >= 50].index)]

	# Construct pivot table
	# utility_matrix = ratings.pivot(index='userID', columns='ISBN').bookRating
	# print "shape of utility matrix(user,books): "+str(utility_matrix.shape)
	return ratings

#print list(ratings['userID'])
ratings = Similarity(ratings)
us_canada_user_rating=KNN.Construct_Utility_Matrix(ratings,books,users)
bookNameList = Recommendation_System_BookList(us_canada_user_rating)
valid_id_list = Recommendation_System_userIdList(us_canada_user_rating)
searchResultPairs = []
modeNum = -1
# UserPredict.User_Recommendation(us_canada_user_rating,254)

# Select the mode of Recommendation between "based on user" and "based on book"
print "1. Recommend books for a user-ID typed in or"
print "2. Recommend books based on a book name"
while True:
	try:
		modeNum = int(raw_input("Please select recommend mode: 1 or 2 (Please type in integer 1/2): "))
		if modeNum == 1 or modeNum == 2:
			break
		else:
			print "Please type in integer 1 or 2 !"
	except:
		print "Could not convert the input to an integer."

# User-User Collaborative Filtering Recommendations
if modeNum == 1:
	while True:
		try:
			input_userid = int(raw_input("Please type in the user-ID (between 8 and 278854) you want: "))
			if input_userid in valid_id_list:
				UserPredict.User_Recommendation(us_canada_user_rating,input_userid)
				break
			else:
				print "Non-valid user ID! Please try again."
		except ValueError:
			print "Could not convert the input to an integer."

# Book-Book Collaborative Filtering Recommendations
if modeNum == 2:
	while True:
	    searchResults = []
	    searchIndex = []
	    titleOfBookSearched = ' '.join(str(raw_input("Please type in (parts of) the name of the book you are interested in: ")).split())
	    searchCandidates = []
	    print "Books that you are most likely to be searching:"
	    for b in bookNameList:
	        if titleOfBookSearched.lower() in b.lower():
	            searchCandidates.append(b)
	    if len(searchCandidates)>10:
	        print "Your input is not detailed enough, please type in a more specific name of the book you want."
	    elif len(searchCandidates)==0:
	        print "There is no book in the database with a name including: ",titleOfBookSearched
	    else:
	        for name in searchCandidates:
	            searchResults.append(name)
	        for x in range(len(searchResults)):
	            searchIndex.append(x)
	        searchResultPairs = list(zip(searchIndex,searchResults))
	        for p in searchResultPairs:
	            print p[0],". ",p[1]
	        break

	if len(searchResultPairs)==1:
	    bookTitleSelected = searchResultPairs[0][1]
	else:
	    try:
	        indexSelected = int(raw_input("Please type in the index of candidate you want in the list above: "))
	        bookTitleSelected = searchResultPairs[indexSelected][1]
	    except ValueError:
	        print "Could not convert the input to an integer."

	KNN.KNN_Recommendation_System(us_canada_user_rating,bookTitleSelected)
	MF.MF_Recommendation_System(us_canada_user_rating,bookTitleSelected)
