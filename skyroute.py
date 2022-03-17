# imports
from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

landmark_string = ""
stations_under_construction = []
# creates a string that joins all landmarks together with it's corresponding letter of the alphabet
for letter, landmark in landmark_choices.items():
    landmark_string += "{0} - {1}\n".format(letter, landmark)


# function greet
def greet():
    print("Hi there and welcome to SkyRoute!")
    print("We'll help you find the shortest route between the following Vancouver landmarks:\n" + landmark_string)

# this function takes two parameters (start_point, end_point). This will handle setting the selected origin and destination points
def set_start_and_end(start_point, end_point):
    if start_point is not None:
        change_point = input("What would you like to change? you can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both': ")
        # Change both
        if change_point == 'b':
            start_point = get_start()
            end_point = get_end()
        # change the origin
        elif change_point == 'o':
            start_point = get_start()
        # change the destination
        elif change_point == 'd':
            end_point = get_end()
        else:
            # this else hits if user enters invalid selection
            print("Oops, that isn't 'o', 'd', or 'b'...")
            set_start_and_end(start_point, end_point)
    else:
        # if there is no start_point then we must set both of them start and end
        start_point = get_start()
        end_point = get_end()

    return start_point, end_point

# Takes no parameters. This function will be used to request an origin from the user for a starting point
def get_start():
    start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
    
    if start_point_letter in landmark_choices:
        start_point = landmark_choices[start_point_letter]
        return start_point
    else:
        print("Sorry, that's not a landmark we have data on. Let's try this again...")
        get_start()

# Takes no parameters. This function will be used to request an end location from the user ending location
def get_end():
    end_point_letter = input("Where are you headed? Type in the corresponding letter: ")
    
    if end_point_letter in landmark_choices:
        end_point = landmark_choices[end_point_letter]
        return end_point
    else:
        print("Sorry, that's not a landmark we have data on. Let's try this again...")
        get_end()

# Takes two parameters start_point end_point. This function will get and set the origin and destination and call search to get the recommended route, and also allow users
# to search for another route
def new_route(start_point = None, end_point = None):
    # the reason that we set start_point and end_point with None becuase both me need to be defined for the first time or redefined upon subsequent
    # new_route calls
    start_point , end_point = set_start_and_end(start_point, end_point)
    shortest_route = get_route(start_point, end_point)
    if shortest_route:
        shortest_route_string = '\n'.join(shortest_route)
        print("The shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
    
    else:
        print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))


    again = input("Would you like to see another route? Enter y/n: ")

    if again == 'y':
        show_landmarks()
        new_route(start_point, end_point)

def show_landmarks():
    see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n: ")

    if see_landmarks == 'y':
        print(landmark_string)
   

def get_route(start_point, end_point):
    # this grabs a set of at least one metro station for the starting
    start_stations = vc_landmarks[start_point]
    # this grabs a set of at least one metro station for the ending
    end_stations = vc_landmarks[end_point]

    # we set routes as an empty list to hold routes that we find. So we can compare later whats the shortest route
    routes = []
    
    # to get each combination we loop through each start stations and inside loop through end stations
    for start_station in start_stations:
        for end_station in end_stations:
            metro_system = get_active_stations() if stations_under_construction else vc_metro
            if stations_under_construction:
                possible_route = dfs(metro_system, start_station, end_station)
                if not possible_route:
                    return None
            route = bfs(metro_system, start_station, end_station)
            if route:
                routes.append(route)

    shortest_route = min(routes, key=len)
    return shortest_route

def goodbye():
    print("Thanks for using SkyRoute!")

def get_active_stations():
    updated_metro = vc_metro
    
    for station_under_construction in stations_under_construction:
        for current_station, neighboring_stations in vc_metro.items():
            if current_station != station_under_construction:
                updated_metro[current_station] -= set(stations_under_construction)
            else:
                updated_metro[current_station] = set([])

    return updated_metro

# skyroute function

def skyroute():
    greet()
    new_route(None, None)
    goodbye()

if __name__ == '__main__':

    skyroute()
