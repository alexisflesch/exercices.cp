import random
from word_search_generator import WordSearch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = 1404, 1872  # Portrait mode dimensions
MAX_WORDS = 40
WORLD_LIST_FILE = "liste_mots.txt"
GRID_MARGIN = 0.10  # Increased space before the grid (15% of page height)
TEXT_MARGIN = 0.05  # Margin around the word list

def load_words(filename):
    with open(filename, "r", encoding="utf-8") as file:
        words = [line.strip().upper() for line in file.readlines() if line.strip()]
    return " ".join(random.sample(words, min(len(words), MAX_WORDS)))

def create_word_search(grid_size=15):
    words = load_words(WORLD_LIST_FILE)
    puzzle = WordSearch(words, size=grid_size)
    return puzzle  # Return the puzzle object

def get_word_list(puzzle):
    return [word.text for word in puzzle.placed_words]

def draw_grid(c, puzzle, grid_size, cell_size, offset_x, offset_y, font_size):
    grid = puzzle.puzzle
    
    c.setFont("Helvetica", font_size)

    for row in range(grid_size):
        for col in range(grid_size):
            x = offset_x + col * cell_size
            y = offset_y - row * cell_size
            c.setLineWidth(3)
            c.setStrokeGray(0.8)
            c.rect(x, y, cell_size, cell_size, stroke=1, fill=0)
            c.setLineWidth(1)
            c.setStrokeColor(colors.black)
            letter = grid[row][col]
            c.drawCentredString(x + cell_size / 2, y + cell_size / 2 - font_size * 0.3, letter)

def draw_word_list(c, words, max_width, start_x, start_y, font_size, line_height):
    c.setFont("Helvetica", font_size)
    current_x, current_y = start_x, start_y
    space_width = c.stringWidth(" ")

    for word in words:
        word_width = c.stringWidth(word, "Helvetica", font_size)
        
        # Move to next line if the word doesn't fit
        if current_x + word_width > max_width:
            current_x = start_x
            current_y -= line_height  # Move to the next line
        
        c.drawString(current_x, current_y, word)
        current_x += word_width + space_width  # Add space after the word

def generate_pdf(output_file, num_puzzles=50):
    c = canvas.Canvas(output_file, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    c.setTitle("Mots mêlés")

    for _ in range(num_puzzles):

        sizes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        grid_size = random.choice(sizes)
        puzzle = create_word_search(grid_size)

        # Calculate grid dimensions dynamically
        grid_area_size = PAGE_WIDTH * 0.9  # 90% of page width
        cell_size = grid_area_size / grid_size
        font_size = max(14, int(cell_size * 0.6))  # Adjust font size relative to cell size

        offset_x = (PAGE_WIDTH - grid_size * cell_size) / 2
        offset_y = PAGE_HEIGHT - (PAGE_HEIGHT * GRID_MARGIN)  # More space at the top
        
        c.setFont("Helvetica", 24)
        draw_grid(c, puzzle, grid_size, cell_size, offset_x, offset_y, font_size)

        # Prepare word list
        words = get_word_list(puzzle)
        word_list_width = PAGE_WIDTH * 0.9
        start_x = (PAGE_WIDTH - word_list_width) / 2
        start_y = PAGE_HEIGHT * 0.2  # Word list starts lower
        word_font_size = 36
        line_height = word_font_size * 1.5  # More space between lines for readability

        draw_word_list(c, words, start_x + word_list_width, start_x, start_y, word_font_size, line_height)
        
        c.showPage()
    
    c.save()

generate_pdf("out/mots_meles.pdf")
