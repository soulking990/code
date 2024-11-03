import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

# Set up the path for the ChromeDriver
service = Service('/opt/homebrew/bin/chromedriver')  # Update this path if needed

# Set up Chrome options for Brave browser
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'  # Path to Brave browser

# Initialize the WebDriver with the Brave browser
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the RateMyProfessor page for Rochester Institute of Technology
driver.get("https://www.ratemyprofessors.com/search/professors/807?q=*")

# Wait for 10 seconds to allow you to pick the department manually
print("Please select the department. You have 10 seconds.")
time.sleep(10)

# Function to scroll down and click "Show More" until all professors are loaded
def load_all_professors():
    while True:
        try:
            # Find and click the "Show More" button using its class name
            show_more_button = driver.find_element(By.CLASS_NAME, "Buttons__Button-sc-19xdot-1.PaginationButton__StyledPaginationButton-txi1dr-1.glImpo")
            ActionChains(driver).move_to_element(show_more_button).click(show_more_button).perform()
            time.sleep(0.5)  # Increase wait time slightly for better reliability
        except:
            # If "Show More" button is not found, break the loop
            break

# Call the function to load all professors
load_all_professors()

# Locate professor cards after loading all available professors
professor_cards = driver.find_elements(By.CLASS_NAME, "TeacherCard__InfoRatingWrapper-syjs0d-3.kcbPEB")

# List to hold extracted data
professors_data = []

if professor_cards:
    for card in professor_cards:
        # Extract the name
        try:
            name = card.find_element(By.CLASS_NAME, "CardName__StyledCardName-sc-1gyrgim-0.cJdVEK").text
        except:
            name = "N/A"
        
        # Extract the quality rating
        try:
            quality = card.find_element(By.CSS_SELECTOR, "div[class*='CardNumRating__CardNumRatingNumber']").text
        except:
            quality = "N/A"
        
        # Extract the number of ratings
        try:
            num_ratings = card.find_element(By.CLASS_NAME, "CardNumRating__CardNumRatingCount-sc-17t4b9u-3.jMRwbg").text
        except:
            num_ratings = "N/A"
        
        # Extract the percentage of "Would Take Again"
        try:
            would_take_again = card.find_elements(By.CLASS_NAME, "CardFeedback__CardFeedbackNumber-lq6nix-2.hroXqf")[0].text
        except:
            would_take_again = "N/A"
        
        # Extract the difficulty level
        try:
            difficulty = card.find_elements(By.CLASS_NAME, "CardFeedback__CardFeedbackNumber-lq6nix-2.hroXqf")[1].text
        except:
            difficulty = "N/A"

        # Create a dictionary for each professor and append to the list
        professor_info = {
            "Name": name,
            "Total Ratings": num_ratings,
            "Quality": quality,
            "Would Take Again": would_take_again,
            "Difficulty": difficulty
        }
        professors_data.append(professor_info)

    # Write the data to a JSON file
    with open("professors_data.json", "w", encoding="utf-8") as f:
        json.dump(professors_data, f, ensure_ascii=False, indent=4)

    print("Data written to professors_data.json")

else:
    print("No professors found.")

# Close the driver
driver.quit()
