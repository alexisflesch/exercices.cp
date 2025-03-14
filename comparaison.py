from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
import random

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = 1404, 1872
MARGIN_X = 200
MARGIN_Y = 300
COLUMN_SPACING = 500
VERTICAL_RULE_X = PAGE_WIDTH // 2
COLUMN_MARGIN = MARGIN_X  # Ensure left margin for second column
TEXT_WIDTH = 150  # Estimated max width for number representation

# Number of exercises per page
EXERCISES_PER_PAGE = 1  # One exercise per page

# Function to represent a number as a sum of tens and units
def number_as_sum(n):
    tens = n // 10
    units = n % 10
    parts = ["10" for _ in range(tens)]
    if units:
        parts.append(str(units))
    return "+".join(parts)

# Exercise: Compare two numbers with dots in between
def exercise_type_1(c, x, y):
    """Generate an exercise with two random numbers and dots in between."""
    c.setFont("Helvetica", 40)
    c.drawString(MARGIN_X, PAGE_HEIGHT - MARGIN_Y, "Ajoute le signe <, > ou =")
    y_offset = 100  
    y -= y_offset  # Add vertical space
    for i in range(5):  # 5 exercises per column
        for col in range(2):  # Two columns
            num1 = random.randint(1, 59)
            num2 = random.randint(1, 80)
            
            # 50% probability to write num1 as a sum of tens and units
            if random.random() < 0.5:
                num1 = random.randint(1, 59)  # Ensure sum representation does not exceed 59
                if random.random() < 0.3:
                    num2 = num1  # 30% probability to match num2
                num1_str = number_as_sum(num1)
            else:
                num1_str = str(num1)
            
            col_x = x + col * (COLUMN_SPACING + COLUMN_MARGIN)
            c.setFont("Helvetica", 36)
            
            # Right-align first number
            num1_x = col_x + TEXT_WIDTH
            c.drawRightString(num1_x, y - i * 120, num1_str)
            
            # Draw centered dots (5 dots instead of 3)
            dot_x = num1_x + 60  # Center dots better
            c.setFont("Helvetica", 36)
            c.setFillGray(0.5)  # Grey color
            c.drawString(dot_x, y - i * 120 - 10, ".....")
            c.setFillGray(0)  # Reset color to black
            
            # Right-align second number
            num2_x = dot_x + 120
            c.drawString(num2_x, y - i * 120, str(num2))
    
    # Draw vertical rule between columns
    c.setLineWidth(3)
    c.setStrokeColorRGB(0.1, 0.1, 0.1)
    c.line(VERTICAL_RULE_X, y - 500, VERTICAL_RULE_X, y + 40)


def exercise_type_2(c, x, y):
    """Generate an exercise where students must sort numbers."""
    y_offset = 350  # Increased vertical spacing for multiple exercises
    spacing = 150  # Increased horizontal spacing between numbers
    box_size = 100  # Size of the boxes for answers
    
    for i in range(4):  # 4 exercises per page
        y_exercise = y - (i * y_offset)
        
        c.setFont("Helvetica", 40)
        if random.random() < 0.5:
            c.drawString(x, y_exercise, "Range les nombres du plus petit au plus grand")
        else:
            c.drawString(x, y_exercise, "Range les nombres du plus grand au plus petit")
        
        y_exercise -= 80  # Increased spacing between title and numbers
        
        # Generate 6 unique random numbers in [2,80]
        numbers = random.sample(range(2, 81), 6)
        
        c.setFont("Helvetica", 36)
        
        # Draw numbers on the top line
        for j, num in enumerate(numbers):
            num_x = x + j * spacing/2
            c.drawString(num_x, y_exercise, str(num))
        

        y_exercise -= 10  # Increased spacing between numbers and boxes

        # Draw empty boxes below
        c.setLineWidth(3)
        y_boxes = y_exercise - 120  # Increased spacing between numbers and boxes
        c.setStrokeGray(0.8)  # Light gray color
        
        for j in range(6):
            box_x = x + j * spacing
            c.rect(box_x - 10, y_boxes, box_size, box_size, stroke=1, fill=0)
        
        c.setStrokeGray(0)  # Reset color
        c.setLineWidth(1)   # Reset line width


def exercise_type_3(c, x, y):
    """Generate an exercise where students must find the previous and next number."""
    row_height = 100  # Row height for the table
    col_width = 250  # Column width for the first and third columns
    middle_col_width = col_width * 2  # Middle column twice as large
    table_width = col_width * 2 + middle_col_width
    x_centered = (1404 - table_width) / 2  # Center table horizontally
    y_exercise = y
    
    c.setFont("Helvetica", 40)
    c.drawString(x_centered, y_exercise, "Complète le tableau")
    
    y_exercise -= 165  # Increased spacing between title and table

    c.setFillGray(0.9)  # Light gray fill color    
    c.rect(x_centered, y_exercise-.9*row_height, col_width, 1.4*row_height, stroke=1, fill=1)
    c.rect(x_centered + col_width + middle_col_width, y_exercise-.9*row_height, col_width, 1.4*row_height, stroke=1, fill=1)

    c.setFillGray(0)  # Reset fill color

    # Draw table header
    c.setFont("Helvetica", 36)
    c.drawString(x_centered + 20, y_exercise, "Nombre juste")
    c.drawString(x_centered + col_width + middle_col_width + 20, y_exercise, "Nombre juste")

    y_exercise -= .5*row_height  # Move down for table rows
    c.drawString(x_centered + 80, y_exercise, "avant")
    c.drawString(x_centered +col_width + middle_col_width + 80, y_exercise, "après")


    
    y_exercise -= 1.4*row_height  # Move down for table rows
    
    # Draw table rows
    for _ in range(5):  # 5 rows per table
        num = random.randint(1, 100)
        
        # Draw full table with horizontal and vertical lines
        c.rect(x_centered, y_exercise, col_width, row_height, stroke=1, fill=0)  # Empty left column
        c.rect(x_centered + col_width, y_exercise, middle_col_width, row_height, stroke=1, fill=0)  # Middle column with number
        c.rect(x_centered + col_width + middle_col_width, y_exercise, col_width, row_height, stroke=1, fill=0)  # Empty right column
        
        # Write number in middle column
        c.drawString(x_centered + col_width + middle_col_width / 2 - 20, y_exercise + 30, str(num))
        
        y_exercise -= row_height  # Move to the next row


# List of exercise functions
EXERCISE_FUNCTIONS = [exercise_type_1, exercise_type_2, exercise_type_3]


def generate_pdf(filename, num_pages=50):
    """Generate a PDF with different number comparison exercises."""
    c = canvas.Canvas(filename, pagesize=portrait((PAGE_WIDTH, PAGE_HEIGHT)))
    c.setTitle("Comparaison de nombres")
    
    for _ in range(num_pages):

        
        exercise_func = random.choice(EXERCISE_FUNCTIONS)
        exercise_func(c, MARGIN_X, PAGE_HEIGHT - MARGIN_Y - 100)
        
        c.showPage()
    
    c.save()

# Generate the PDF
generate_pdf("out/comparaison.pdf")
