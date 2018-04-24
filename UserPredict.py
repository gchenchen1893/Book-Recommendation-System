import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import math
def User_Recommendation(us_canada_user_rating,userID):
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
	#       User1 User2 User3 User4 User5
	# book1
	# book2
	# book3
	# book4
	# book5
	book_title = list(us_canada_user_rating_pivot.index)
	users = list(us_canada_user_rating_pivot.columns)
	# find the input user id in current users
	index=-1
	for i in range(0,len(users)):
		if users[i] == userID:
			index=i
	# if it is not existed,report error
	if index==-1:
		print "user ID error or the user has been removed,please check again"
		return

	has_rated=[] 
	#we just need to return books that the input user didn't rate
	user_vec = us_canada_user_rating_pivot.iloc[:,index].values
	for i in range(0,len(user_vec)):
		if user_vec[i]!=0:
			has_rated.append(i)

	# calculate the pearson R coefficience between the input user and other users
	corr_list={}
	for user in range(0,len(users)):
		if user == index:
			continue
		other_user_vec = us_canada_user_rating_pivot.iloc[:,user].values
		user_vec_propress,other_user_vec_propress=helper(user_vec,other_user_vec)
		r,p = pearsonr(user_vec_propress,other_user_vec_propress)
		corr_list[user]=r

	# do the prediction for the input user
	# r_cs = k * sum(sim(cc')*r_c's)
	for book in range(0,len(book_title)):
		if us_canada_user_rating_pivot.iloc[book,index] == 0:
			sum = 0
			for user in range(0,len(users)): 
				if user == index:
					continue
				temp = corr_list[user]*us_canada_user_rating_pivot.iloc[book,user]
				if math.isnan(temp):
					continue
				sum+=temp
			us_canada_user_rating_pivot.iloc[book,index] = 0.1*sum
	# print us_canada_user_rating_pivot.iloc[:,index].values
	# output the predicted top-sorted unrated books
	res=[]
	sort_index=np.argsort(us_canada_user_rating_pivot.iloc[:,index].values)
	for i in sort_index:
		if i in has_rated:
			continue
		res.append(book_title[i])
	print('User-User Collaborative Filtering Recommendations for User {0}:\n'.format(userID))
	temp_res=res[-10:-1]
	for i in range(0,len(temp_res)):
		print str(i+1)+": "+str(res[len(temp_res)-1-i])

def User_Recommendation_Input(us_canada_user_rating,input_vec):
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
	#       User1 User2 User3 User4 User5
	# book1
	# book2
	# book3
	# book4
	# book5
	book_title = list(us_canada_user_rating_pivot.index)
	users = list(us_canada_user_rating_pivot.columns)

	has_rated=[] 
	#we just need to return books that the input user didn't rate
	user_vec = input_vec
	for i in range(0,len(user_vec)):
		if user_vec[i]!=0:
			has_rated.append(i)

	# calculate the pearson R coefficience between the input user and other users
	corr_list={}
	for user in range(0,len(users)):
		other_user_vec = us_canada_user_rating_pivot.iloc[:,user].values
		user_vec_propress,other_user_vec_propress=helper(user_vec,other_user_vec)
		r,p = pearsonr(user_vec_propress,other_user_vec_propress)
		corr_list[user]=r

	# do the prediction for the input user
	# r_cs = k * sum(sim(cc')*r_c's)
	for book in range(0,len(book_title)):
		if input_vec[book] == 0:
		#if us_canada_user_rating_pivot.iloc[book,index] == 0:
			sum = 0
			for user in range(0,len(users)): 
				temp = corr_list[user]*us_canada_user_rating_pivot.iloc[book,user]
				if math.isnan(temp):
					continue
				sum+=temp
			input_vec[book] = 0.1*sum
	# print us_canada_user_rating_pivot.iloc[:,index].values
	# output the predicted top-sorted unrated books
	res=[]
	sort_index=np.argsort(input_vec)
	for i in sort_index:
		if i in has_rated:
			continue
		res.append(book_title[i])
	print('You may also be interested in these books: ')
	temp_res=res[-10:-1]
	for i in range(0,len(temp_res)):
		print str(i+1)+": "+str(res[len(temp_res)-1-i])




def helper(X,Y):
	res_x=[]
	res_y=[]
	for i in range(0,len(X)):
		if X[i]!=0 and Y[i]!=0:
			res_x.append(X[i])
			res_y.append(Y[i])
	return np.asarray(res_x),np.asarray(res_y)

#def User_Recommendation_Input(us_canada_user_rating,input_vec)

def Build_Input_Vec(most_rated_book,us_canada_user_rating):
	us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
	index=[]
	book_title = list(us_canada_user_rating_pivot.index)
	for book in most_rated_book:
		for j in range(0,len(book_title)):
			if book == book_title[j]:
				index.append(j)
	rate_value=[]
	for i in range(0,len(most_rated_book)):
		temp = float(raw_input("Please input your rating for {0}: ".format(most_rated_book[i])))
		rate_value.append(temp)
	vec=[]
	for i in range(0,len(book_title)):
		vec.append(0)
	for i in range(0,len(index)):
		vec[index[i]]=rate_value[i]
	return np.asarray(vec)