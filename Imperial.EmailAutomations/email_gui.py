import sys
import pygame
import pyperclip
from EmailTemp import get_email_template, calculate_instalments
from folder_suggester import suggest_folder

pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Email Template Selector")
FONT = pygame.font.Font(None, 24)
CLOCK = pygame.time.Clock()

# Simple UI primitives
class Button:
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
    def draw(self, surf):
        color = (70,130,180) if self.rect.collidepoint(pygame.mouse.get_pos()) else (100,150,200)
        pygame.draw.rect(surf, color, self.rect, border_radius=6)
        surf.blit(FONT.render(self.text, True, (255,255,255)), (self.rect.x+8, self.rect.y+6))
    def handle(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(ev.pos):
            self.action()

class TextInput:
    def __init__(self, rect, text=""):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.active = False

    def draw(self, surf):
        bg = (255,255,255) if self.active else (240,240,240)
        pygame.draw.rect(surf, bg, self.rect)
        pygame.draw.rect(surf, (120,120,120), self.rect, 2)
        txt_surf = FONT.render(self.text or "", True, (0,0,0))
        surf.blit(txt_surf, (self.rect.x+6, self.rect.y+6))
        # caret
        if self.active:
            caret_x = self.rect.x + 6 + txt_surf.get_width() + 1
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                pygame.draw.rect(surf, (0,0,0), (caret_x, self.rect.y+6, 2, FONT.get_height()))

    def handle(self, ev):
        # mouse: set focus
        if ev.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.active
            self.active = self.rect.collidepoint(ev.pos)
            if self.active and not was_active:
                try:
                    pygame.key.start_text_input()
                except Exception:
                    pass
            if not self.active and was_active:
                try:
                    pygame.key.stop_text_input()
                except Exception:
                    pass

        # text input (preferred) for characters
        if ev.type == pygame.TEXTINPUT and self.active:
            self.text += ev.text

        # fallback for special keys
        if ev.type == pygame.KEYDOWN and self.active:
            if ev.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif ev.key == pygame.K_RETURN:
                self.active = False
                try:
                    pygame.key.stop_text_input()
                except Exception:
                    pass
            # ignore other control keys here

# Cases mapping (keys used by get_email_template)
TEMPLATES = [
    ("Refunds Request", "refunds"),
    ("Deposit", "deposit"),
    ("Receipts", "receipts"),
    ("Instalments", "instalments"),
    ("Advance Billing", "advance_billing"),
    ("Confirmation of Payment", "confirmation_of_payment"),
    ("Payment Methods", "payment_methods"),
    ("Invoice Not Received", "invoice_not_received"),
    ("EPD", "epd"),
    ("Instalments Approved", "instalments_approved")
]

def draw_text_block(lines, x, y, surf):
    for i, line in enumerate(lines):
        surf.blit(FONT.render(line, True, (0,0,0)), (x, y + i*22))

def main():
    state = "menu"
    selected_case = None
    message = ""
    # inputs used in detail screen
    inp_name = TextInput((320, 120, 320, 30))
    inp_amount = TextInput((320, 170, 200, 30))
    inp_total = TextInput((320, 220, 200, 30))
    inp_sponsorship = TextInput((320, 320, 200, 30))
    include_calc = False
    deposit_paid = False
    sponsor_yes = False

    buttons = []
    for i, (label, key) in enumerate(TEMPLATES):
        btn = Button((50, 40 + i*48, 240, 40), label, lambda k=key: select_case(k))
        buttons.append(btn)

    back_btn = Button((50, 520, 120, 40), "Back", lambda: switch_to_menu())
    submit_btn = Button((620, 520, 120, 40), "Generate", lambda: submit())

    def select_case(key):
        nonlocal state, selected_case, message, include_calc, deposit_paid, sponsor_yes
        selected_case = key
        state = "details"
        message = ""
        include_calc = False
        deposit_paid = False
        sponsor_yes = False
        inp_name.text = ""
        inp_amount.text = ""
        inp_total.text = ""
        inp_sponsorship.text = ""

    def switch_to_menu():
        nonlocal state, message
        state = "menu"
        message = ""

    def submit():
        nonlocal message, state
        kwargs = {}
        name = inp_name.text.strip() or "Customer"
        kwargs['name'] = name
        # confirmation of payment needs amount
        if selected_case == "confirmation_of_payment":
            amt = inp_amount.text.strip()
            kwargs['amount'] = amt or "0.00"
        # instalments handling
        if selected_case in ("instalments", "instalments_approved"):
            if include_calc:
                try:
                    total = float(inp_total.text.replace(",", "") or "0")
                except ValueError:
                    message = "Invalid total amount"
                    return
                dep_flag = 'y' if deposit_paid else 'n'
                sponsor_flag = 'y' if sponsor_yes else 'n'
                sponsorship = 0.0
                if sponsor_yes:
                    try:
                        sponsorship = float(inp_sponsorship.text.replace(",", "") or "0")
                    except ValueError:
                        message = "Invalid sponsorship amount"
                        return
                kwargs['calc_text'] = calculate_instalments(total, dep_flag, sponsor_flag, sponsorship) if sponsor_yes else calculate_instalments(total, dep_flag, sponsor_flag)
                kwargs['sponsor'] = 'yes' if sponsor_yes else 'no'
        # generate email
        email_body = get_email_template(selected_case, **kwargs)
        # append calc_text if present
        if kwargs.get('calc_text'):
            email_body += kwargs['calc_text']
        # strip brackets like original
        for b in '()[]{}':
            email_body = email_body.replace(b, '')
        pyperclip.copy(email_body)
        # folder suggestion
        try:
            folder = suggest_folder(email_body)
        except Exception:
            folder = "n/a"
        message = "Email copied to clipboard. Suggested folder: " + folder
        state = "done"

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if state == "menu":
                for b in buttons:
                    b.handle(ev)
            elif state == "details":
                back_btn.handle(ev)
                submit_btn.handle(ev)
                inp_name.handle(ev)
                if selected_case == "confirmation_of_payment":
                    inp_amount.handle(ev)
                if selected_case in ("instalments", "instalments_approved"):
                    inp_total.handle(ev)
                    inp_sponsorship.handle(ev)
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_TAB:
                        # simple tab: toggle focus order
                        # not full implementation, keep minimal
                        pass
            elif state == "done":
                back_btn.handle(ev)
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                    switch_to_menu()

            # handle clicks for small toggles (deposit/sponsor/include calc)
            if state == "details" and ev.type == pygame.MOUSEBUTTONDOWN:
                mx,my = ev.pos
                # deposit toggle
                if 550 <= mx <= 740 and 220 <= my <= 252 and selected_case in ("instalments","instalments_approved"):
                    deposit_paid = not deposit_paid
                # sponsor toggle
                if 550 <= mx <= 740 and 270 <= my <= 302 and selected_case in ("instalments","instalments_approved"):
                    sponsor_yes = not sponsor_yes
                # include calc toggle
                if 550 <= mx <= 740 and 320 <= my <= 352 and selected_case in ("instalments","instalments_approved"):
                    include_calc = not include_calc

        SCREEN.fill((240,240,240))
        if state == "menu":
            SCREEN.blit(FONT.render("Select template:", True, (0,0,0)), (50,10))
            for b in buttons:
                b.draw(SCREEN)
        elif state == "details":
            SCREEN.blit(FONT.render(f"Selected: {selected_case}", True, (0,0,0)), (50,10))
            SCREEN.blit(FONT.render("Recipient name:", True, (0,0,0)), (160,125))
            inp_name.draw(SCREEN)
            y = 170
            if selected_case == "confirmation_of_payment":
                SCREEN.blit(FONT.render("Amount (e.g. 1200.00):", True, (0,0,0)), (140,175))
                inp_amount.draw(SCREEN)
            if selected_case in ("instalments","instalments_approved"):
                SCREEN.blit(FONT.render("Include calculation (click box):", True, (0,0,0)), (320,295))
                SCREEN.blit(FONT.render("Total amount:", True, (0,0,0)), (220,225))
                inp_total.draw(SCREEN)
                # deposit toggle
                SCREEN.blit(FONT.render(f"Deposit paid: [{'X' if deposit_paid else ' '}] (click to toggle)", True, (0,0,0)), (320,225))
                # sponsor toggle and sponsorship input
                SCREEN.blit(FONT.render(f"Sponsor present: [{'X' if sponsor_yes else ' '}] (click to toggle)", True, (0,0,0)), (320,275))
                SCREEN.blit(FONT.render("Sponsorship amount:", True, (0,0,0)), (170,325))
                inp_sponsorship.draw(SCREEN)
                SCREEN.blit(FONT.render(f"[{'X' if include_calc else ' '}] Click to include calc", True, (0,0,0)), (550,320))
            back_btn.draw(SCREEN)
            submit_btn.draw(SCREEN)
            if message:
                draw_text_block([message], 320, 420, SCREEN)
        elif state == "done":
            draw_text_block(["Done.", message, "Press Enter or Back to return."], 50, 100, SCREEN)
            back_btn.draw(SCREEN)

        pygame.display.flip()
        CLOCK.tick(30)

if __name__ == "__main__":
    main()