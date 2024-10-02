# To read CSV file and return the data as a list of dictionaries
def read_imdb_data(file_path):
    data = []
    
    # Open the file in read mode
    with open(file_path, 'r') as file: # With statement: it will automatically closing the file after the block code is executed
        # Read the first line only
        headers = file.readline().strip().split(',')
        
        # Read each line of the CSV
        for line in file:
            values = line.strip().split(',')    # Split the line by commas and remove extra spacess
            info = dict(zip(headers, values)) # Create a dictionary for each header and its corresponding value
            data.append(info) # Save the info in the list
    
    return data

# Question 1
def top_3_movies_with_highest_ratings_in_2016(data):
    # Filter out the movies that is released in 2016
    movies_in_2016 = [movie for movie in data if movie["Year"] == "2016"]
    # Sort it by unique rating, therefore use set() cuz it will remove duplicate info. and get the top three unique ratings
    sort_by_rating = sorted(set(float(movie["Rating"]) for movie in movies_in_2016), reverse = True)[ : 3]
    # Find the answer
    answer = [movie for movie in movies_in_2016 if float(movie["Rating"]) in sort_by_rating]
    sort_answer = sorted(answer, key = lambda x: float(x["Rating"]), reverse = True)

    return sort_answer

# Question 2
# Find the actor with the highest average revenue per movie 
def actor_with_highest_average_revenue_per_movie(data):
    actor_revenue = {}
    
    # Loop thru each movie
    for movie in data:
        revenue = movie.get('Revenue (Millions)', '')  # Get revenue, if the revenue data is missing, it will be an empty string
        
        # Skip the movie where revenue data is missing
        if not revenue:
            continue
        
        revenue = float(revenue)
        actors = movie['Actors'].split("|")
        
        # Update each actor's revenue and movie count
        for actor in actors:
            actor = actor.strip() # Remove the leading spaces
            if actor not in actor_revenue:
                actor_revenue[actor] = {'Total_revenue': 0, 'Movie_count': 0}
            actor_revenue[actor]['Total_revenue'] += revenue
            actor_revenue[actor]['Movie_count'] += 1
    
    # Calc the average revenue per movie for each actor
    average_revenue = {actor: actor_revenue[actor]['Total_revenue'] / actor_revenue[actor]['Movie_count'] for actor in actor_revenue}
    
    # Find the highest average revenue per movie
    max_average_revenue = max(average_revenue.values())

    answer = {actor: revenue for actor, revenue in average_revenue.items() if revenue == max_average_revenue}
    
    return answer

# Question 3
def average_rating_of_EmmaWatson_movie(data):
    # Filter out the movies that included Emma Watson
    movies = [movie for movie in data if "Emma Watson" in movie["Actors"]]
    # Calc avg rating
    ratings = [float(movie["Rating"]) for movie in movies]
    if ratings:
        answer = sum(ratings) / len(ratings)
    else:
        answer = 0
        
    return answer

# Question 4
def top_3_directors_collaborate_with_most_actors(data):
    directors = {} # Set
    for movie in data:
        director = movie["Director"]
        actors = set(movie["Actors"].split("|"))

        # Remove the leading spaces
        actors = [actor.strip() for actor in actors]

        # If this director haven been recorded yet, then record him/her
        if director not in directors:   # Set is faster in python
            directors[director] = set() # Set will automatically remove those duplicate info.s
        
        directors[director].update(actors)  # Update the collaborated actor to the specific director

    director_actors_count = {director: len(actor) for director, actor in directors.items()}
    top_3_amount_collaborated_actors = sorted(set(director_actors_count.values()), reverse = True)[ : 3]
    answer = [(director, actor_count) for director, actor_count in director_actors_count.items() if actor_count in top_3_amount_collaborated_actors]
    sort_answer = sorted(answer, key = lambda x: x[1], reverse = True)

    return sort_answer

# Question 5
def top_2_actors_playing_most_genres_movies(data):
    actor_genres = {} # Set
    
    for movie in data:
        genres = set(movie["Genre"].split('|'))  
        actors = movie["Actors"].split('|')  
        
        # Save movie genre in each actors if this genre hasn been recorded in those actors respectively
        for actor in actors:
            actor = actor.strip() # Remove the leading spaces
            if actor not in actor_genres:
                actor_genres[actor] = set()
            actor_genres[actor].update(genres)  # Update the set with new genres that the actor participated in
    
    genres_count = {actor: len(genres) for actor, genres in actor_genres.items()}
    top_2_amount_genres_movies = sorted(set(genres_count.values()), reverse = True)[ : 2]
    answer = [(actor, genre_count) for actor, genre_count in genres_count.items() if genre_count in top_2_amount_genres_movies]
    sort_answer = sorted(answer, key = lambda x: x[1], reverse = True)
    
    return sort_answer

# Question 6
def actors_with_largest_movie_gap_year(data):
    actor_years = {}
    
    # Loop thru each movie to find the earliest and the latest year for each actors
    for movie in data:
        year = int(movie["Year"]) 
        actors = movie["Actors"].split('|')  
        
        for actor in actors:
            actor = actor.strip() # Remove the leading spaces
            if actor not in actor_years:
                actor_years[actor] = {"min_year": year, "max_year": year}
            else: # Find out the min. and max. year 
                actor_years[actor]["min_year"] = min(actor_years[actor]["min_year"], year)
                actor_years[actor]["max_year"] = max(actor_years[actor]["max_year"], year)
    
    # Calculate the gap years for each actors
    gap_years = {actor: actor_years[actor]['max_year'] - actor_years[actor]['min_year'] for actor in actor_years}
    
     # Find the maximum gap years
    max_gap_years = max(gap_years.values())
    
    # Find those actors with the maximum gap years
    answer = {actor: gap for actor, gap in gap_years.items() if gap == max_gap_years}
    count = len(answer)
    
    return answer, count

# Question 7
def find_all_actors_collaborate_with_JohnnyDepp_directly_indirectly(data):
    collaborated_actors_directly_indirectly = {}
    
    for movie in data:
        actors = movie['Actors'].split('|')

        # Remove the leading spaces
        actors = [actor.strip() for actor in actors]
        
        # Create edges between all actors in the same movie
        for actor in actors:
            actor = actor.strip()
            if actor not in collaborated_actors_directly_indirectly:
                collaborated_actors_directly_indirectly[actor] = set()
            collaborated_actors_directly_indirectly[actor].update(actors)  # Record all actors in the movie
            collaborated_actors_directly_indirectly[actor].discard(actor)  # Remove itself
    
    # Using BFS 
    answer = set() # Python can run faster in set than in list (set : hash table)
    queue = ["Johnny Depp"]
    
    count = 0
    while queue:
        current_actor = queue.pop(0)
        
        if current_actor not in answer:
            answer.add(current_actor)
            count += 1
            # Add all connected actors into the queue
            queue.extend(collaborated_actors_directly_indirectly.get(current_actor, []))
    
    return answer, count - 1    # Minus 1 cuz need not to count Johnny Depp himself as collaborated actors 

# Read the file
all_data = read_imdb_data('IMDB-Movie-Data.csv')

# Question 1 ans
question_1 = top_3_movies_with_highest_ratings_in_2016(all_data)
print("Question 1: Top-3 movies with the highest ratings in 2016:")
print(f"{"Title":<30}{"Rating":<6}")
print("-" * 36)
for movie in question_1:
    print(f"{movie['Title']:<30}{movie['Rating']:<6}")
print()


# Question 2 ans
question_2 = actor_with_highest_average_revenue_per_movie(all_data)
print("Question 2: The actor generating the highest average revenue?")
print(f"{"Actor":<25}{"Revenue per movie":<17}")
print("-" * 42)
for actor, revenue in question_2.items():
    print(f"{actor:<25}{revenue:<17}")
print()

# Question 3 ans
question_3 = average_rating_of_EmmaWatson_movie(all_data)
print("Question 3: The average rating of Emma Watson's movies?")
print(f"{"Actor":<25}{"Rating":<6}")
print("-" * 31)
print(f"{"Emma Watson":<25}{question_3:<6}")
print()

# Question 4 ans
question_4 = top_3_directors_collaborate_with_most_actors(all_data)
print("Question 4: Top-3 directors who collaborate with the most actors?")
print(f"{"Director":<25}{"Number of collaborated actors":<29}")
print("-" * 54)
for director, actor_count in question_4:
    print(f"{director:<25}{actor_count:<29}")
print()

# Question 5 ans
question_5 = top_2_actors_playing_most_genres_movies(all_data)
print("Question 5: Top-2 actors playing in the most genres of movies?")
print(f"{"Actor":<25}{"Number of movie genres":<22}")
print("-" * 47)
for actor, genre_count in question_5:
    print(f"{actor:<25}{genre_count:<29}")
print()

# Question 6 ans
question_6, question_6_count = actors_with_largest_movie_gap_year(all_data)
print("Question 6: Actors whose movies lead to the largest maximum gap of years?")
print("-" * 60)
print(f"The total number of actors with the largest movie gap years are {question_6_count}.")
print("-" * 60)
print(f"{"Actor":<25}{"Maximum gap years between movies":<32}")
print("-" * 57)
for actor, gap_years in question_6.items():
    print(f"{actor:<25}{gap_years:<32}")
print()

# Question 7 ans
question_7, question_7_count = find_all_actors_collaborate_with_JohnnyDepp_directly_indirectly(all_data)
print("Question 7: Find all actors who collaborate with Johnny Depp in direct and indirect ways:")
print("-" * 60)
print(f"The total number of actors who collaborate with Johnny Depp in direct and indirect ways are {question_7_count}.")
print("-" * 60)
print(question_7)