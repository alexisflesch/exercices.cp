from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
import random
import scipy.spatial
import math

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = 1404, 1872
GRID_SIZE = 8  # 8x8 grid
CELL_SIZE = 100  # Size of each square in pixels
MARGIN_X = (PAGE_WIDTH - GRID_SIZE * CELL_SIZE) // 2  # Centering horizontally
MARGIN_Y_TOP = PAGE_HEIGHT - (GRID_SIZE * CELL_SIZE) - 100  # Adjusted margin for top grid
MARGIN_Y_BOTTOM = 100  # Adjusted margin for bottom grid

def generate_convex_polygon(min_coord, max_coord):
    """Generates a convex polygon with integer coordinates."""
    num_points = random.randint(7, 15)  # Random number of points between 7 and 15
    points = []
    for _ in range(num_points):
        x = random.randint(min_coord, max_coord)
        y = random.randint(min_coord, max_coord)
        points.append([x, y])

    hull = scipy.spatial.ConvexHull(points)
    polygon_points = [points[i] for i in hull.vertices]
    polygon_points.append(polygon_points[0])  # Close the polygon
    return polygon_points

def generate_polygon_random_walk(num_points, step_size, max_turn=math.pi/4, grid_size=GRID_SIZE):
    """Generates a polygon using a random walk, constrained to the grid, avoiding straight lines and overlaps."""
    points = [[random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)]]
    angle = 0
    for _ in range(num_points - 1):
        valid_move = False
        while not valid_move:  # Keep trying until a valid move is found
            angle += random.uniform(-max_turn, max_turn)
            x = points[-1][0] + int(step_size * math.cos(angle))
            y = points[-1][1] + int(step_size * math.sin(angle))

            # Keep points within the grid (wrap around)
            x = x % grid_size
            y = y % grid_size

            new_point = [x, y]

            # Check for straight lines and overlaps:
            if new_point != points[-1] and new_point not in points:  # No duplicates or staying in place
                if len(points) > 1:
                    # Check if the new segment would create a straight line with the previous one
                    if (points[-1][0] - points[-2][0]) * (y - points[-1][1]) != (x - points[-1][0]) * (points[-1][1] - points[-2][1]):
                        valid_move = True
                else: # First segment, no need to check for straight lines
                    valid_move = True

        points.append(new_point)
    points.append(points[0])  # Close the polygon
    return points


def draw_grid(c, x_offset, y_offset, grid_size):
    """Draw a light gray grid centered on the page."""
    c.setStrokeGray(0.8)
    c.setLineWidth(3)
    for i in range(grid_size + 1):
        c.line(x_offset + i * CELL_SIZE, y_offset, x_offset + i * CELL_SIZE, y_offset + grid_size * CELL_SIZE)
        c.line(x_offset, y_offset + i * CELL_SIZE, x_offset + grid_size * CELL_SIZE, y_offset + i * CELL_SIZE)

def draw_path(c, path, x_offset, y_offset):
    """Draw the black path without intersections and add bullet points at line ends."""
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(3)
    c.setFillColorRGB(0, 0, 0)  # Set fill color for bullet points
    
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        c.line(x_offset + x1 * CELL_SIZE, y_offset + y1 * CELL_SIZE,
               x_offset + x2 * CELL_SIZE, y_offset + y2 * CELL_SIZE)
        c.circle(x_offset + x2 * CELL_SIZE, y_offset + y2 * CELL_SIZE, 5, fill=1)  # Bullet point
    
    # Close the polygon by connecting the last point to the first
    x1, y1 = path[-1]
    x2, y2 = path[0]
    c.line(x_offset + x1 * CELL_SIZE, y_offset + y1 * CELL_SIZE,
           x_offset + x2 * CELL_SIZE, y_offset + y2 * CELL_SIZE)
    c.circle(x_offset + x2 * CELL_SIZE, y_offset + y2 * CELL_SIZE, 5, fill=1)  # Bullet point



def generate_pdf(filename, num_pages=50):
    """Generate the PDF with multiple exercises."""
    c = canvas.Canvas(filename, pagesize=portrait((PAGE_WIDTH, PAGE_HEIGHT)))
    c.setTitle("Grilles")  # Set the PDF title
    for _ in range(num_pages):
        if random.random() < 0.5:  # Randomly switch between two grid sizes
            path = generate_convex_polygon(0, GRID_SIZE - 1)  # Adjusted range
        else:
            path = generate_polygon_random_walk(random.randint(5, 7), 3.5, grid_size=GRID_SIZE) # Example parameters
        
        # Draw top grid with path
        draw_grid(c, MARGIN_X, MARGIN_Y_TOP, GRID_SIZE)
        draw_path(c, path, MARGIN_X, MARGIN_Y_TOP)
        
        # Draw empty grid below with first guiding line including bullet points
        draw_grid(c, MARGIN_X, MARGIN_Y_BOTTOM, GRID_SIZE)
        if len(path) > 1:
            x1, y1 = path[0]
            x2, y2 = path[1]
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(3)
            c.line(MARGIN_X + x1 * CELL_SIZE, MARGIN_Y_BOTTOM + y1 * CELL_SIZE,
                   MARGIN_X + x2 * CELL_SIZE, MARGIN_Y_BOTTOM + y2 * CELL_SIZE)
            c.circle(MARGIN_X + x1 * CELL_SIZE, MARGIN_Y_BOTTOM + y1 * CELL_SIZE, 5, fill=1)
            c.circle(MARGIN_X + x2 * CELL_SIZE, MARGIN_Y_BOTTOM + y2 * CELL_SIZE, 5, fill=1)
        
        c.showPage()
    
    c.save()


# Generate the PDF
generate_pdf("out/grilles.pdf")
