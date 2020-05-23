import sqlite3
from recommender import recommend
import datetime

connection = sqlite3.connect('Movielist.db')
cursor = connection.cursor()

time = datetime.datetime.now()


class Theatre:

    def __init__(self, name):
        self.name = name
        

    def DisplayMovies(self):
        print('WE HAVE FOLLOWING MOVIES IN OUR SHOWBOX :- \n')
        cursor.execute("SELECT _id, name FROM movie;")
        for row in cursor:
            print('{}. {}'.format(row[0], row[1]))
        connection.commit()

    def LendMovie(self, movieid, moviename, user):
        cursor.execute('SELECT _id FROM movie WHERE _id="{}";'.format(movieid))
        check = cursor.execute('SELECT _id FROM entries WHERE _id="{}";'.format(movieid)).fetchone()
        
        if check!=None:
            print("Movie already in use.\n")
            cursor.execute("SELECT _id, movie_name, user_name, trans_time FROM entries;")
            for row in cursor:
                print('{} | {} | {} | {}'.format(row[0], row[1], row[2], row[3]))
            connection.commit()


        else:            
            cursor.execute('INSERT INTO entries VALUES({}, "{}", "{}", "{}");'.format(movieid, moviename, user, time))
            print('\nLENDER-MOVIE DATABASE HAS BEEN SUCCESSFULLY UPDATED. YOU CAN TAKE YOUR MOVIE NOW.\n ')
            cursor.execute("SELECT _id, movie_name, user_name, trans_time FROM entries;")
            for row in cursor:
                print('{} | {} | {} | {}'.format(row[0], row[1], row[2],row[3]))
            connection.commit()


    def ReturnMovie(self, movieid):
        cursor.execute("SELECT user_name FROM entries WHERE _id={};".format(movieid))
        for val in cursor:
            person = val[0]
        print("MOVIE SUCCESSFULLY RETURNED TO SHOWBOX by user : {}.".format(person))
        cursor.execute("DELETE FROM entries WHERE _id LIKE {}".format(movieid))
        print()
        cursor.execute("SELECT _id, movie_name, user_name, trans_time FROM entries;")
        for row in cursor:
            print('{} | {} | {} | {}'.format(row[0], row[1], row[2], row[3]))
        connection.commit()



if __name__ == '__main__':
    movieBase = Theatre("SHOWBOX")
    print('\n'+'*'*50+f'  WELCOME TO {movieBase.name}  '+'*'*50+'\n')
    print("Here you can rent movies of your wish!")
    while(True):
        
        print('Enter your choice to continue...\n')
        print('1. Display movies')
        print('2. Lend a movie')
        print('3. Return a movie\n')
        
        user_choice = int(input('Enter Choice : '))

        if user_choice == 1:
            movieBase.DisplayMovies()

        elif user_choice == 2:
            movieid = int(input('Enter the id of movie which you want to lend : '))
            moviename = input('Enter the name of movie which you want to lend : ')

            user = input('Enter your Name : ')
            movieBase.LendMovie(movieid, moviename, user)
            print("\nYou may also like : ")
            recommend(moviename, movieid)


        elif user_choice == 3:
            movieid = int(input('Enter the movie-id which you want to return : '))
            movieBase.ReturnMovie(movieid)
        else:
            print('INVALID OPERATION')

        user_choice2=''
        
        while(user_choice2!='q' and user_choice2!='c'):
            print('\nEnter q to quit and c to continue...')
            user_choice2 = input()
            if user_choice2 == 'q':
                exit()
            elif user_choice2 == 'c':
                continue
            else:
                print("INVALID OPERATION... Try again")
cursor.close()
