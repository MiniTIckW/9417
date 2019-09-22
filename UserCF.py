from math import *
import random
import numpy as np

class Mermory_Based_CF:

    def __init__(self, movies, ratings, k=5, n=10):
        self.movies = movies
        self.ratings = ratings
        # the number of neighbors
        self.k = k
        # the number of recommend
        self.n = n
        # the ratings of one movie by one user
        # {'UserID:':[MoiveID,Rating]}
        self.userDict = {}
        # User item
        self.ItemUser = {}
        # the info of neighbors
        self.neighbors = []
        # recoomandList 
        self.recommandList = []
        self.cost = 0.0
        self.accurracy = 0

    # User-based recommend 
    def recommendByUser(self, userId):
        # turn ratings to 
        self.formatRate()
        # n = len of UserDict[userId]
        self.n = len(self.userDict[userId])
        temp_neighbors = []
        self.neighbors = []

        # find these users 
        for e in self.userDict[userId]:
            for j in self.ItemUser[e[0]]:
                if(j != userId):
                    if(j not in temp_neighbors):
                        temp_neighbors.append(j)
        # compute the simulation between this user and other users and sort 
        for i in temp_neighbors:
            dist = self.Cos_sim(userId, i)
            #dist = self.Distance_sim(userId, i)
            self.neighbors.append([dist, i])
        # decrease sort 
        self.neighbors.sort(reverse=True)
        self.neighbors = self.neighbors[:self.k]

        # get the recommand list 
        self.recommandList = []
        # create the directory of recommand
        recommandDict = {}
        for neighbor in self.neighbors:
            movies = self.userDict[neighbor[1]]
            for movie in movies:
                if(movie[0] in recommandDict):
                    recommandDict[movie[0]] += neighbor[0]
                else:
                    recommandDict[movie[0]] = neighbor[0]

        # create the recommandList
        for key in recommandDict:
            self.recommandList.append([recommandDict[key], key])
        self.recommandList.sort(reverse=True)
        self.recommandList = self.recommandList[:self.n]
        # determine the evaluation of the user
        self.evaluation(userId)

    # turn ratings to userDict and ItemUser
    def formatRate(self):
        self.userDict = {}
        self.ItemUser = {}
        for i in self.ratings:
            temp = (i[1], float(i[2]) / 5)
            # {'1':[(1,5),(2,5)...],'2':[...]...}
            if(i[0] in self.userDict):
                self.userDict[i[0]].append(temp)
            else:
                self.userDict[i[0]] = [temp]
            # 计算ItemUser {'1',[1,2,3..],...}
            if(i[1] in self.ItemUser):
                self.ItemUser[i[1]].append(i[0])
            else:
                self.ItemUser[i[1]] = [i[0]]

    # formate the Userdict
    def formatuserDict(self, userId, l):
        user = {}
        for i in self.userDict[userId]:
            user[i[0]] = [i[1], 0]
        for j in self.userDict[l]:
            if(j[0] not in user):
                user[j[0]] = [0, j[1]]
            else:
                user[j[0]][1] = j[1]
        return user

    # compute the cosine of the angle between the two users’ vectors
    def Cos_sim(self, userId, l):
        # get the Uion of UserId and movies
        # {"MoviesID":[userID's rating, the rating of l]} 
        # if no ratings then the rating of l is 0
        user = self.formatuserDict(userId, l)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0]) * float(v[0])
            y += float(v[1]) * float(v[1])
            z += float(v[0]) * float(v[1])
        if(z == 0.0):
            return 0
        return z / sqrt(x * y)

    def Distance_sim(self,userId,l):
        data = self.formatuserDict(userId, l)
        distance = 0
        for key in data:
            distance += pow(float(data[key][0])-float(data[key][1]),2)
        return 1/(1+sqrt(distance))

    # the evaltion by Precision
    def evaluation(self, userId):
        user = []
        for e in self.userDict[userId]:
            user.append(e[0])
        recommand = []
        for e in self.recommandList:
            recommand.append(e[1])
        count = 0.0
        
        for i in recommand:
            if(i in user):
                count += 1.0
        self.cost = count / len(recommand)


    def show(self):
        ls = []        
        for e in self.neighbors:
            ls.append(int(e[1]))
        print("-------the MoiveID show below---------")
        print(ls)
        _len = len(self.ratings)
        self.accurracy = round(self.cost * 100,2)
        print("--------------result------------------")
        print("The total acount of data is {}".format(_len))
        print("The accurracy is ： {} %".format(self.accurracy))

# read the file 
def readRatingFile(filename):
    files = open(filename, "r", encoding="iso-8859-15")
    ratings = []
    for line in files.readlines():
        item = line.strip().split()
        ratings.append(item)
    return ratings

def readMoviesFile(filename):
    files = open(filename, "r", encoding="iso-8859-15")
    movies = []
    for line in files.readlines():
        item = line.strip().split("|")
        movies.append(item)
    return movies

# main function
ratings = readRatingFile("u2.base")
movies = readMoviesFile("u.item")
demo = Mermory_Based_CF(movies, ratings, k=10, n=10)
ls = []

# for UserId in range(1,944):
#     demo.recommendByUser(str(UserId))
#     accurracy = round(demo.cost * 100,2)
#     ls.append(accurracy)
# ave_accurracy = round(np.mean(ls),2)
# print("The average accurracy is {}%".format(ave_accurracy))

Rand_userID = random.randint(1,943)
demo.recommendByUser(str(Rand_userID))
print("the recommand list of {} is:".format(Rand_userID))
demo.show()



