import cv2
import numpy as np
import pyautogui
from PIL import Image
import matplotlib.pyplot as plt


pyautogui.click(150, 300)
# Take a screenshot of the entire screen
screenshot = pyautogui.screenshot()

# Define the coordinates for cropping
left = 78
top = 164
right = 335
bottom = 421

# Crop the screenshot to the specified area
cropped_image = screenshot.crop((left, top, right, bottom))

# Save the cropped image (optional)
cropped_image.save("cropped_screenshot.png")


# Define the size of the grid
grid_size = 16

# Calculate the size of each cell in the grid
cell_width = cropped_image.width // grid_size
cell_height = cropped_image.height // grid_size

# Define the specific colors
specific_colors = {
    1: (0, 0, 255),    
    2: (0, 128, 0),  
    3: (255, 0, 0),  
    4: (0, 0, 128),  
    5: (128, 0, 0),   
    6: (0, 128, 128),  
    7: (0, 0, 0),    
    8: (128, 128, 128), 
    0: (192, 192, 192),  
    -1: (255, 255, 255) 
}

def is_color_match(color, specific_color):
    return color == specific_color

# Check the color at the center of each grid cell
grid_colors = []
for row in range(grid_size):
    grid_row = []
    for col in range(grid_size):
        # Calculate the center of the current grid cell
        center_x = col * cell_width + cell_width // 2
        center_y = row * cell_height + cell_height // 2
        
        # Get the color of the center pixel
        center_color = cropped_image.getpixel((center_x, center_y))
        
        # Determine which specific color the center color matches
        grid_value = None
        for value, specific_color in specific_colors.items():
            if is_color_match(center_color, specific_color):
                grid_value = value
                break
        
        # If the detected color is 0, check the color 7 pixels higher
        if grid_value == 0:
            try:
                higher_color = cropped_image.getpixel((center_x, center_y - 7))
                if is_color_match(higher_color, specific_colors[-1]):
                    grid_value = -1
            except IndexError:
                pass  # Ignore if the coordinates are out of the image bounds
                
        grid_row.append(grid_value if grid_value is not None else 'Unknown')
    grid_colors.append(grid_row)

# Display the grid colors
for row in grid_colors:
    print(row)

original_matrix = grid_colors
# Initialize the new matrix with zeros
# Convert lists to numpy arrays
original_matrix = np.array(original_matrix)
new_matrix = np.zeros((16, 16))
new_matrix = new_matrix - 1

# Define directions for neighbors: (up, down, left, right, and all 4 diagonals)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def click_cell(i, j, cell_width, cell_height, top_left_x, top_left_y):
    # Calculate the center of the cell
    center_x = top_left_x + j * cell_width + cell_width // 2
    center_y = top_left_y + i * cell_height + cell_height // 2
    # Perform the mouse click
    pyautogui.click(center_x, center_y)

def count_negative_ones(matrix, x, y):
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 16 and 0 <= ny < 16 and matrix[nx, ny] == -1:
            count += 1
    return count

def update_new_matrix(original_matrix, new_matrix):
    for i in range(16):
        for j in range(16):
            if original_matrix[i, j] > 0:
                num_neg_ones = count_negative_ones(original_matrix, i, j)
                if num_neg_ones > 0:
                    new_value = original_matrix[i, j] / num_neg_ones
                    for dx, dy in directions:
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < 16 and 0 <= ny < 16:
                            if new_matrix[nx, ny] == -1:
                                new_matrix[nx, ny] = new_value
                            else:
                                new_matrix[nx, ny] = 1 - ((1 - new_matrix[nx, ny]) * (1 - new_value))
                else:
                    new_matrix[i, j] = original_matrix[i, j]

for i in range(10):
    screenshot = pyautogui.screenshot()

    # Crop the screenshot to the specified area
    cropped_image = screenshot.crop((left, top, right, bottom))

    # Save the cropped image (optional)
    cropped_image.save("cropped_screenshot.png")

    grid_colors = []
    for row in range(grid_size):
        grid_row = []
        for col in range(grid_size):
            # Calculate the center of the current grid cell
            center_x = col * cell_width + cell_width // 2
            center_y = row * cell_height + cell_height // 2
            
            # Get the color of the center pixel
            center_color = cropped_image.getpixel((center_x, center_y))
            
            # Determine which specific color the center color matches
            grid_value = None
            for value, specific_color in specific_colors.items():
                if is_color_match(center_color, specific_color):
                    grid_value = value
                    break
            
            # If the detected color is 0, check the color 7 pixels higher
            if grid_value == 0:
                try:
                    higher_color = cropped_image.getpixel((center_x, center_y - 7))
                    if is_color_match(higher_color, specific_colors[-1]):
                        grid_value = -1
                except IndexError:
                    pass  # Ignore if the coordinates are out of the image bounds
                    
            grid_row.append(grid_value if grid_value is not None else 'Unknown')
        grid_colors.append(grid_row)

    original_matrix = grid_colors
   
    original_matrix = np.array(original_matrix)
    new_matrix = np.zeros((16, 16))
    new_matrix = new_matrix - 1

    update_new_matrix(original_matrix, new_matrix)

    for k in range(16):
        for l in range(16):
            if original_matrix[k,l] >= 0:
                new_matrix[k,l] = 1

    closest_value_position = None
    min_distance = float('inf')

    # Iterate through the matrix
    for i in range(new_matrix.shape[0]):
        for j in range(new_matrix.shape[1]):
            # Calculate the distance from 0
            distance = abs(new_matrix[i, j])
            
            # Update the position if the current distance is smaller than the minimum distance
            if distance < min_distance:
                min_distance = distance
                closest_value_position = (i, j)

    top_left_x = 78
    top_left_y = 164

    # Example: Click the cell at position (3, 2)
    click_cell(closest_value_position[0], closest_value_position[1], cell_width, cell_height, top_left_x, top_left_y)

new_matrix = np.round(new_matrix, 2)

print("New Matrix:")
for row in new_matrix:
    print(row)

# Plotting the heatmap
#plt.imshow(new_matrix, cmap='hot', interpolation='nearest')
#plt.colorbar()
#plt.title("Heatmap of New Matrix")
#plt.show()


closest_value_position = None
min_distance = float('inf')

# Iterate through the matrix
for i in range(new_matrix.shape[0]):
    for j in range(new_matrix.shape[1]):
        # Calculate the distance from 0
        distance = abs(new_matrix[i, j])
        
        # Update the position if the current distance is smaller than the minimum distance
        if distance < min_distance:
            min_distance = distance
            closest_value_position = (i, j)


# Assuming each cell is 40x40 pixels and the grid starts at the top-left corner (100, 100)

# Example: Click the cell at position (3, 2)
click_cell(closest_value_position[0], closest_value_position[1], cell_width, cell_height, top_left_x, top_left_y)