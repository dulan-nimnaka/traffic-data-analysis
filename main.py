#Author: E. A. Dulan Nimnaka
#Date: 11/12/2024

import csv
from datetime import datetime
import tkinter as tk

# Task A: Input Validation

def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    
    #asking for input until a valid date is provided
    while True:
        try:
            while True: 
                try:
                    day = int(input("Please enter the day of the survey in the format DD: ")) #ask user to enter the date
                    if 1 <= day <= 31:   #Check if day is within the valid range
                        break  #exit loop if valid
                    else:
                        print("Out of range - values must be between 1 and 31.")    #if the value is out of range
                except ValueError:
                    print("Integer required! Please enter valid numbers.")          #if input is not an integer

            while True:
                try:
                    month = int(input("Please enter the month of the survey in the format MM: "))  #ask user to enter the month
                    if 1 <= month <= 12:  #Check if month is within the valid range
                        break  #exit loop if valid
                    else:
                        print("Out of range - values must be between 1 and 12.")    #if the value is out of range
                except ValueError:
                    print("Integer required! Please enter valid numbers.")          #if input is not an integer

            while True:
                try:
                    year = int(input("Please enter the year of the survey in the format YYYY: "))   #ask user to enter the year
                    if 2000 <= year <= 2024:     #Check if day is within the valid range
                        break  #exit loop if valid
                    else:
                        print("Out of range - year must be between 2000 and 2024.")   #if the value is out of range
                except ValueError:
                    print("Integer required! Please enter valid numbers.")            #if input is not an integer
                    
            # Validate the full date
            try:
                date = datetime(year, month, day)  #validate if the full date exists
                return f"{day:02d}-{month:02d}-{year}"  #format the date and return
            except ValueError:
                print(f"Invalid date {day:02d}-{month:02d}-{year}. Please try again.")     #if date is invalid

        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")     #unexpected errors

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    
    #loop until valid input is given
    while True:
        user_input = input("Do you want to load another dataset? (Y/N): ").upper()       #Ask user if they want to continue and convert input to uppercase
        if user_input in ["Y", "N"]:          # Check input
            return user_input == "Y"          # Return True for 'Y' and False for 'N'.
        else:   
            print("INVALID input. Please enter 'Y' or 'N'.")     #invalid input

def define_file_path(date):
    
    #create a file path based on the validated date.
    day, month, year = date.split("-")                #Split the date string into day, month, and year
    return f"traffic_data{day}{month}{year}.csv"      #Return the file path string in day, month, year format

# Task B: Process CSV Data

def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    
    try:
        # Initialize variables for metrics
        total_vehicles = 0            # Total vehicles for the date
        total_trucks = 0              # Total trucks
        total_electric_vehicles = 0   # Electric vehicles
        two_wheeled_vehicles = 0      # Two-wheeled vehicles (bikes, scooters, motorcycles)
        busses_leaving_north = 0      # Buses leaving Elm Avenue heading North
        vehicles_no_turns = 0         # Vehicles going straight
        vehicles_over_speed = 0       # Vehicles exceeding speed limit
        vehicles_elm_rabbit = 0       # Vehicles recorded at Elm Avenue/Rabbit Road
        scooters_count = 0            # Scooters at Elm Avenue/Rabbit Road
        vehicles_hanley_westway = 0   # Vehicles at Hanley Highway/Westway
        max_vehicles_hour = 0         # Peak traffic count in an hour
        max_vehicles_time = ""        # Store the time or times of the peak traffic hour
        rain_hours = 0                # Count of rain hours
        rain_hours_set = set()        # To count unique rain hours.
        hourly_counts = {}            # To count vehicles per hour.
        total_bicycles = 0            # Total bicycles recorded
        hourly_data = {}              # Store traffic data per hour for each junction | Data for histogram (Task D)

        # Open the CSV file for reading data
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)        # Reads the CSV file as a dictionary.
            
            # Loop through each row in the file.
            for row in reader:
                #The total number of vehicles passing through all junctions for the selected date.
                total_vehicles += 1           # Increment total vehicle count.

                #The total number of trucks passing through all junctions for the selected date.
                if row["VehicleType"] == "Truck":
                    total_trucks += 1

                #The total number of electric vehicles passing through all junctions for the selected date.
                if row["elctricHybrid"].lower() == "true":
                    total_electric_vehicles += 1

                #The number of “two wheeled” vehicles through all junctions for the date (bikes, motorbike, scooters).
                if row["VehicleType"] in ["Bicycle", "Motorcycle", "Scooter"]:
                    two_wheeled_vehicles += 1

                #The total number of busses leaving Elm Avenue/Rabbit Road junction heading north
                if (
                    row["JunctionName"] == "Elm Avenue/Rabbit Road"
                    and row["travel_Direction_out"] == "N"
                    and row["VehicleType"] == "Buss"
                ):
                    busses_leaving_north += 1

                #The total number of vehicles passing through both junctions without turning left or right.
                if row["travel_Direction_in"] == row["travel_Direction_out"]:
                    vehicles_no_turns += 1

                #The total number of vehicles recorded as over the speed limit for the selected date.
                if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                    vehicles_over_speed += 1

                #The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date.
                if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                    vehicles_elm_rabbit += 1
                    #Count only scooters at Elm Avenue/Rabbit Road
                    if row["VehicleType"] == "Scooter":
                        scooters_count += 1

                #The total number of vehicles recorded through only Hanley Highway/Westway junction for the selected date.
                if row["JunctionName"] == "Hanley Highway/Westway":
                    vehicles_hanley_westway += 1
                    hour = row["timeOfDay"][:2]        # Extract the hour.
                    hourly_counts[hour] = hourly_counts.get(hour, 0) + 1 # Count vehicles per hour

                #Count rain hours (Light Rain or Heavy Rain)
                if row["Weather_Conditions"] in ["Light Rain", "Heavy Rain"]:
                    hour = row["timeOfDay"][:2]  #Extract the hour part
                    rain_hours_set.add(hour)     #Add hour to the rain hours set
                    
                # Count bicycles and calculate average bicycles per hour
                if row["VehicleType"] == "Bicycle":
                    total_bicycles += 1
                    
                # Store data for creating histograms (Task D)
                hour = row["timeOfDay"][:2]  # Extract hour (HH)
                junction = row["JunctionName"]
                vehicle_count = 1  # Each row represents one vehicle passing
                
                # Initialize hourly data for this hour if not already done
                if hour not in hourly_data:
                    hourly_data[hour] = {"Elm Avenue/Rabbit Road": 0, "Hanley Highway/Westway": 0}
                
                # Increment counts for each junction based on the row's junction name
                if junction == "Elm Avenue/Rabbit Road":
                    hourly_data[hour]["Elm Avenue/Rabbit Road"] += vehicle_count
                elif junction == "Hanley Highway/Westway":
                    hourly_data[hour]["Hanley Highway/Westway"] += vehicle_count
                

            #The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway.
            if hourly_counts:
                max_vehicles_hour = max(hourly_counts.values())       #Find the peak number of vehicles in any hour
                
                #The time or times of the peak (busiest) traﬃc hour (or hours) on Hanley Highway/Westway 
                max_vehicles_time = ", ".join(
                    [f"Between {hour}:00 and {int(hour)+1}:00" for hour, count in hourly_counts.items() if count == max_vehicles_hour]
                )

        # Calculate the percentage
        # The percentage of all vehicles recorded that are Trucks for the selected date (rounded to an integer).
        trucks_percentage = round((total_trucks / total_vehicles) * 100) if total_vehicles else 0
        # The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters (rounded to integer)
        scooters_percentage = round((scooters_count / vehicles_elm_rabbit) * 100) if vehicles_elm_rabbit else 0
        
        # Calculate the average number of bicycles per hour
        average_bicycles_per_hour = round(total_bicycles/24)
        
        # Calculate the number of rain hours
        rain_hours = len(rain_hours_set)

        #Return all calculated metrics in a list
        return hourly_data, [
            f"\nData file selected is {file_path}",
            f"The total number of vehicles recorded for this date is {total_vehicles}",
            f"The total number of trucks recorded for this date is {total_trucks}",
            f"The total number of electric vehicles for this date is {total_electric_vehicles}",
            f"The total number of two-wheeled vehicles for this date is {two_wheeled_vehicles}",
            f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {busses_leaving_north}",
            f"The total number of vehicles through both junctions not turning left or right is {vehicles_no_turns}",
            f"The percentage of total vehicles recorded that are trucks for this date is {trucks_percentage}%",
            f"The average number of bicycles per hour for this date is {average_bicycles_per_hour}",
            f"The total number of vehicles recorded as over the speed limit for this date is {vehicles_over_speed}",
            f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {vehicles_elm_rabbit}",
            f"The total number of vehicles recorded through Hanley Highway/Westway junction is {vehicles_hanley_westway}",
            f"{scooters_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
            f"The highest number of vehicles in an hour on Hanley Highway/Westway is {max_vehicles_hour}",
            f"The most vehicles through Hanley Highway/Westway were recorded between {max_vehicles_time}",
            f"The number of hours of rain for this date is {rain_hours}\n"
            ]
        return hourly_data, outcomes  # Ensure outcomes are returned when successful
    
    except FileNotFoundError:
        raise FileNotFoundError  # Raise the error if the file isn't found


def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    
    #Loop through all the outcome strings and print them
    for line in outcomes:
        print(line)


# Task C: Save Results to Text File

def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    
    #Open the file in append mode
    with open(file_name, 'a') as file:
        for line in outcomes:                    #Loop through each line
            file.write(f"{line}\n")              #Write each outcome to the text file followed by a newline
        file.write("\n***************************\n")       #Add a separator after writing all outcomes

# Task D: Histogram Display (using tkinter Canvas)

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        
        # traffic_data, A list of how many vehicles passed each hour for two roads
        self.traffic_data = traffic_data
        # date, The date we’re making the graph for
        self.date = date
        # Create the main Tkinter application window
        self.root = tk.Tk()
        # Set the title of the application window
        self.root.title("Histogram")
        # Set the width of the canvas
        self.canvas_width = 1100
        # Set the height of the canvas
        self.canvas_height = 680
        # Create a canvas widget for drawing the histogram, with a white background
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white") 
        # Disable resizing of the application window
        self.root.resizable(False, False)
        # Add the canvas widget to the Tkinter window
        self.canvas.pack()

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        
        # Define the main Tkinter window size based on canvas dimensions
        # dimensions into a standard width x height format
        self.root.geometry(f"{self.canvas_width}x{self.canvas_height}")
        
        
        self.canvas.create_text(
            self.canvas_width / 2, 20,  # Position the text at the center near the top (20 pixels from the top)
            text=f"Histogram of Vehicle Frequency per Hour ({self.date})", # Displays the title of the histogram includes the date
            font=("Helvetica", 18, "bold"),  # Font style, size and bold styling
            fill="black" # Text color is black
        )

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        
        # Find the maximum vehicle count across all hours and junction locations
        # The bars are proportionally scaled to fit within the canvas height, which is ensured by this.
        max_value = max(max(values["Elm Avenue/Rabbit Road"], values["Hanley Highway/Westway"]) for values in self.traffic_data.values())
        bar_width = 15                       # Width of each bar
        bar_spacing = 10                     # Spacing between bars of different hours
        x_start = 50                         # Starting x-coordinate for the Y-axis
        y_base = self.canvas_height - 50     # Base y-coordinate for the X-axis (bottom of the canvas)
        y_scale = (y_base - 50) / max_value  # Scale to fit the bars within the canvas

        # Draw axes
        # Draw Y-axis
        # Vertical axis is drawn from the top (50 px) to the base of the canvas
        self.canvas.create_line(x_start, 50, x_start, y_base, width=2, fill="white")
        # Draw X-axis
        # Horizontal axis is drawn across the canvas just above the base margin, line color is black
        self.canvas.create_line(x_start, y_base, self.canvas_width - 50, y_base, width=2, fill="black") 

        # Add X-axis title
        # A centered title below the X-axis labels, describing the time range of the histogram
        self.canvas.create_text(
            (self.canvas_width - 50 + x_start) / 2,  # Center the text horizontally
            y_base + 40,  # Position below the hour labels
            text="Hours 00:00 to 24:00",     # Displays the title 
            font=("Helvetica", 12, "bold"),  # Font style, size and bold styling
            fill="black"   # Text color is black
        )

        # Draw bars for each hour
        # Iterate through the sorted hours in the traffic data
        hours = sorted(self.traffic_data.keys())
        for i, hour in enumerate(hours):
            elm_value = self.traffic_data[hour]["Elm Avenue/Rabbit Road"]     # Get Elm Avenue count for the hour
            hanley_value = self.traffic_data[hour]["Hanley Highway/Westway"]  # Get Hanley Highway count for the hour

            x1 = x_start + i * (bar_width * 2 + bar_spacing)  # Calculate x-coordinate for Elm bar
            # Each bar's height is determined by the scaled traffic count (y1_elm and y1_hanley)
            y1_elm = y_base - elm_value * y_scale             # Calculate y-coordinate based on vehicle count and scaling
            y1_hanley = y_base - hanley_value * y_scale       # Similar calculation for Hanley bar

            # Elm Avenue/Rabbit Road bars (green color)
            self.canvas.create_rectangle(x1, y1_elm, x1 + bar_width, y_base, fill="green", outline="black")
            self.canvas.create_text(x1 + bar_width / 2, y1_elm - 10,  # Display count above the bar
                                     text=str(elm_value), font=("Helvetica", 8), fill="green")

            # Hanley Highway/Westway bars (red color)
            x2 = x1 + bar_width  # Start of Hanley bar is next to Elm bar
            self.canvas.create_rectangle(x2, y1_hanley, x2 + bar_width, y_base, fill="red", outline="black")
            self.canvas.create_text(x2 + bar_width / 2, y1_hanley - 10,  # Display count above the bar
                                     text=str(hanley_value), font=("Helvetica", 8), fill="red")

            # Add hour labels
            # Labels under each pair of bars, centered between them
            self.canvas.create_text(x1 + bar_width,
                                    y_base + 20,
                                    text=hour,
                                    font=("Helvetica", 10),
                                    fill="black")

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        
        legend_x = 70  # X-coordinate of the legend's starting position
        legend_y = 30  # Y-coordinate of the legend's starting position
        
        # Elm Avenue/Rabbit Road (green color)
        # Draws a small green rectangle to represent the Elm Avenue/Rabbit Road data
        self.canvas.create_rectangle(legend_x,
                                     legend_y,
                                     legend_x + 20,
                                     legend_y + 20,
                                     fill="green",
                                     outline="black")
        
        # The label is offset horizontally (legend_x + 30) and vertically centered (legend_y + 10)
        # anchor="w" ensures the text aligns to the left of its starting position
        self.canvas.create_text(legend_x + 30,
                                legend_y + 10,
                                text="Elm Avenue/Rabbit Road",
                                anchor="w",
                                font=("Helvetica", 10),
                                fill="black")

        legend_y += 30 # Move to the next line for the Hanley legend
        
        # Hanley Highway/Westway bars (red color)
        # Draws a red rectangle and corresponding text label for Hanley Highway/Westway data
        self.canvas.create_rectangle(legend_x,
                                     legend_y,
                                     legend_x + 20,
                                     legend_y + 20,
                                     fill="red",
                                     outline="black")
        
        self.canvas.create_text(legend_x + 30,
                                legend_y + 10,
                                text="Hanley Highway/Westway",
                                anchor="w",
                                font=("Helvetica", 10),
                                fill="black")

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        
        self.setup_window()     # Configure the window and canvas
        self.draw_histogram()   # Draw the histogram with bars and labels
        self.add_legend()       # Add a legend to the canvas
        self.root.mainloop()    # Enter the Tkinter main event loop to display the UI

# Task E: Code Loops to Handle Multiple CSV Files

class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        # Getting ready to do a task
        # store the data from the current CSV file we're working on
        self.current_data = None
        # Name of a text file where we'll save results for later
        self.results_file = "results.txt"

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        # Here we call another function to read and process the CSV file
        # If the file works, we store its data in 'self.current_data' and return True
        data = process_csv_data(file_path)
        if data:
            self.current_data = data
            return True
        # If the file doesn't work, we return False
        return False

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        # We erase the old data by setting 'self.current_data' to None
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        # This is where the program asks the user questions and processes files
        while True:      # Repeat until the user says they want to stop
            while True:  # Repeat until a valid file is loaded
                # Ask the user to input a date
                date = validate_date_input()
                # Turn the date into the correct file path
                file_path = define_file_path(date)
                
                try:  # Process the CSV file
                    hourly_data, outcomes = process_csv_data(file_path)
                    # If the file is valid and processed successfully, exit this loop
                    if outcomes:
                        break
                    
                # If the file isn't found, tell the user and ask for a different date    
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found. Please enter another date.")

            # Show the results of the file on the screen
            display_outcomes(outcomes)
            # Save the results to a text file
            save_results_to_file(outcomes, self.results_file)
            
            # If the file has hourly data
            # Integrates a graphical component (HistogramApp) for data visualization
            if hourly_data:
                app = HistogramApp(hourly_data, date)
                app.run()
            
            # Ask the user if they want to process another file
            if not validate_continue_input():
                # If they say no, thank them and end the loop
                print("\nEnd of Run! Thank you for using the Traffic Data Processor!")
                break
            else:
                # If they say yes, clear the old data and get ready for the next file
                self.clear_previous_data()
                
    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.handle_user_interaction()
            

# Main system execution
def main_system():
    # Start the program by creating a MultiCSVProcessor object
    multi_csv_processor = MultiCSVProcessor()
    # Call the 'process_files()' method to begin processing files
    multi_csv_processor.process_files()

# This checks if the script is being run directly
if __name__ == "__main__":
    # If yes, it calls the main function to start the program
    main_system()
