import media
import my_fresh_tomatoes

#Creating Instances of my movie objects, each variable is an instance of the class Movie
#The class Movie from media takes in the following parameters:
#("Movie Title", "Link to: Movie Poster", "Link to: Movie Trailer")

avengers = media.Movie("The Avengers",
                       "https://upload.wikimedia.org/wikipedia/en/f/f9/TheAvengers2012Poster.jpg",
                       "https://www.youtube.com/watch?v=eOrNdBpGMv8", "PG-13")

spirited_away = media.Movie("Spirited Away",
                            "https://upload.wikimedia.org/wikipedia/en/3/30/Spirited_Away_poster.JPG",
                            "https://www.youtube.com/watch?v=ByXuk9QqQkk", "PG")

bigherosix = media.Movie("Big Hero 6",
                         "https://upload.wikimedia.org/wikipedia/en/4/4b/Big_Hero_6_%28film%29_poster.jpg",
                         "https://www.youtube.com/watch?v=z3biFxZIJOQ", "PG") 

captain_america = media.Movie("Captain America: Civil War",
                              "https://upload.wikimedia.org/wikipedia/en/5/53/Captain_America_Civil_War_poster.jpg",
                              "https://www.youtube.com/watch?v=dKrVegVI0Us", "PG-13")

big_short = media.Movie("The Big Short",
                        "https://upload.wikimedia.org/wikipedia/en/e/e3/The_Big_Short_teaser_poster.jpg",
                        "https://www.youtube.com/watch?v=vgqG3ITMv1Q", "R")

inside_out = media.Movie("Inside Out",
                         "https://upload.wikimedia.org/wikipedia/en/0/0a/Inside_Out_%282015_film%29_poster.jpg",
                         "https://www.youtube.com/watch?v=seMwpP0yeu4", "PG")


#Putting all of the instances into a list

movies = [avengers, spirited_away, bigherosix, captain_america, big_short, inside_out]

#Passing the list of movie objects to the open_movies_page function
#The function is whithin the my_fresh_tomatoes file
#This function creates the webpage by taking in a paramter of one or more movie objects

my_fresh_tomatoes.open_movies_page(movies)
