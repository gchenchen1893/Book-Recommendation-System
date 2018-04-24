import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import KNN
import MF
import UserPredict

books = pd.read_csv('BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1", low_memory=False)
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
users = pd.read_csv('BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1", low_memory=False)
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1", low_memory=False)
ratings.columns = ['userID', 'ISBN', 'bookRating']

# Data Analysis
def Distribution(ratings):
	# Here, we sorted the books according to their rating counts and show their average ratings
	# But the most popular books does not mean it receives the highest rating
	count_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
	average_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].mean())
	average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
	res = average_rating.sort_values('ratingCount', ascending=False).head(10)

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
	return res

def GenerateRandomRatingBook(ratings,books):
	rating_count = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
	# make a list to store ten books that are rated mostly
	temp = rating_count.sort_values('bookRating', ascending=False).head(10)
	most_rated_ISBN = list(temp.index)
	most_rated_books = pd.DataFrame(most_rated_ISBN, index=np.arange(10), columns = ['ISBN'])
	most_rated_books_summary = pd.merge(most_rated_books, books, on='ISBN')
	res=[]
	for i in list(most_rated_books_summary['bookTitle']):
		res.append(str(i))
	return res

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

# print list(ratings['userID'])
dense_ratings = Similarity(ratings)
us_canada_user_rating = KNN.Construct_Utility_Matrix(dense_ratings,books,users)


##############################################################
# input a user and return recommended books
# input_vec = UserPredict.Build_Input_Vec(most_rated_book,us_canada_user_rating)
# UserPredict.User_Recommendation_Input(us_canada_user_rating,input_vec)
##############################################################


most_rated_book = GenerateRandomRatingBook(ratings,books)
book_name_list = Recommendation_System_BookList(us_canada_user_rating)
valid_id_list = Recommendation_System_userIdList(us_canada_user_rating)
searchResultPairs = []
modeNum = -1

# let user choose to or not to open Distribution function
while True:
	first_option = str(raw_input("Before we go to our book recommendation system, do you want to see some basic analysis results of our dataset? [Y/N]: "))
	if first_option == 'Y' or first_option == 'y':
		Distribution(ratings)
		break
	elif first_option == 'N' or first_option == 'n':
		print "Ok. Let's skip this part. It is not very interesting |-_-|"
		break
	else:
		print "Pardon? Let me repeat the question again. "

# Select the mode of Recommendation between "based on user" or "based on visitor's preferences" or "based on book"
while True:
	print "1. Recommend books for a user-ID typed in or"
	print "2. Recommend books for you according to your rates on ten books listed below or"
	print "3. Recommend books based on a book name "
	while True:
		try:
			modeNum = int(raw_input("Please select recommend mode: 1 or 2 or 3 (Please type in integer 1/2/3): "))
			if modeNum == 1 or modeNum == 2 or modeNum == 3:
				break
			else:
				print "Please type in integer 1 or 2 or 3!"
		except:
			print "Could not convert the input to an integer."

	# User-User Collaborative Filtering Recommendations
	if modeNum == 1:
		while True:
			input_userid = int(raw_input("Please type in the user-ID (between 254 and 278418) you want: "))
			if input_userid in valid_id_list:
				UserPredict.User_Recommendation(us_canada_user_rating,input_userid)
				break
			else:
				print "Non-valid user ID! "
				# give user some help to input valid user id successfully
				get_example = str(raw_input("Do you want to get some valid user ID example? [Y/N]: "))
				if get_example == 'Y' or get_example == 'y':
					sub_valid_id_list = []
					for u in range(100):
						sub_valid_id_list.append(str(valid_id_list[u]))
					sub_valid_id_strlist = ','.join(sub_valid_id_list)
					print sub_valid_id_strlist
				elif get_example == 'N' or get_example == 'n':
					print "Still recommend you to Y because it will save your time. And we are sorry for this not perfect dataset."
				else:
					print "Pardon? Anyway, please try again. "

	# Visitor-friendly Book Recommendations
	if modeNum == 2:
		while True:
			print "Test your preference on top ten books rated by most times in our dataset"
			try:
				input_vec = UserPredict.Build_Input_Vec(most_rated_book,us_canada_user_rating)
			except ValueError:
				print "Please input float number between 0 and 10 for each book listed!"
				continue
			UserPredict.User_Recommendation_Input(us_canada_user_rating,input_vec)
			break

	# Book-Book Collaborative Filtering Recommendations
	if modeNum == 3:
		while True:
		    searchResults = []
		    searchIndex = []
		    titleOfBookSearched = ' '.join(str(raw_input("Please type in (parts of) the name of the book you are interested in: ")).split())
		    searchCandidates = []
		    print "Books that you are most likely to be searching:"
		    for b in book_name_list:
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

	# let user decide whether to leave this system
	y_or_n = str(raw_input("Do you want to try this book recommendation system again? [Y/N]: "))
	if y_or_n == 'N' or y_or_n == 'n':
		print "Thanks for your using."
		break
	elif y_or_n == 'Y' or y_or_n == 'y':
		print "Let's try again!"
	else:
		print "We cannot figure out your input and choice, but we still think you like this system and want to try again |-_-| "
