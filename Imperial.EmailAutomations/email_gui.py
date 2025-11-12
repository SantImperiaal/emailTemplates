import pygame
import sys
from EmailTemp import get_email_template
import pyperclip

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)
BACKGROUND_COLOR = (240, 240, 240)
TEXT_COLOR = (0, 0, 0)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Email Template Selector")

    # Define common email templates
    templates = [
        ("Refunds Request", "refunds"),
        ("Deposit", "deposit"),
        ("Instalments", "instalments"),
        ("Confirmations of Payment", "confirmation_of_payment"),
        ("Payment Methods", "payment_methods"),
        ("EPD", "epd")
    ]

    # Create buttons
    buttons = []
    for i, (text, template_key) in enumerate(templates):
        y_pos = 50 + (BUTTON_HEIGHT + BUTTON_MARGIN) * i
        btn = Button(
            WINDOW_WIDTH // 4,
            y_pos,
            WINDOW_WIDTH // 2,
            BUTTON_HEIGHT,
            text,
            lambda k=template_key: handle_template_selection(k)
        )
        buttons.append(btn)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            mouse_pos = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEMOTION:
                for btn in buttons:
                    btn.is_hovered = btn.rect.collidepoint(mouse_pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        btn.action()

        # Draw buttons
        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()

    pygame.quit()

def handle_template_selection(template_key):
    email_body = get_email_template(template_key, name="Customer")
    pyperclip.copy(email_body)
    print(f"Template '{template_key}' copied to clipboard!")

if __name__ == "__main__":
    main()