import pygame
import random

# -------------------- UNO Model --------------------
COLORS = ['rouge', 'jaune', 'vert', 'bleu']
VALUES = [str(i) for i in range(0,10)] + ['Skip', '+2']
WILD_VALUES = ['Wild', 'Wild+4']

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def is_wild(self):
        return self.color is None

    def matches(self, other_card, current_color):
        # Wild cards always match
        if self.is_wild():
            return True
        # Any card matches if there is no top card yet
        if other_card is None:
            return True
        # Match by color
        if self.color == current_color:
            return True
        # Match by value
        if self.value == other_card.value:
            return True
        return False

    def __repr__(self):
        return f"Cartes({self.color},{self.value})"

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        # Build full UNO deck
        self.cards = []
        for color in COLORS:
            self.cards.append(Card(color, '0'))
            for value in VALUES[1:]:
                self.cards.append(Card(color, value))
                self.cards.append(Card(color, value))
        for _ in range(4):
            self.cards.append(Card(None, 'Wild'))
            self.cards.append(Card(None, 'Wild+4'))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n=1):
        # Draw n cards from the deck
        drawn = []
        for _ in range(n):
            if not self.cards:
                break
            drawn.append(self.cards.pop())
        return drawn

    def add_cards(self, cards):
        # Add a batch of cards to the deck and reshuffle
        self.cards.extend(cards)
        self.shuffle()

# -------------------- Game State --------------------
class GameState:
    def __init__(self):
        self.deck = Deck()
        self.discard = []
        self.hands = {0: [], 1: []}
        self.current_player = 0
        self.top_card = None
        self.current_color = None
        self.game_over = False
        self.winner = None
        self.pending_draw = 0
        self.message = ''

    def start(self):
        # Deal initial hands
        for i in range(2):
            self.hands[i] = self.deck.draw(7)

        # Draw first top card, avoiding starting with Wild+4
        while True:
            c = self.deck.draw(1)[0]
            if c.value == 'Wild+4':
                self.deck.cards.insert(0, c)
                self.deck.shuffle()
                continue
            self.top_card = c
            self.discard.append(c)
            self.current_color = random.choice(COLORS) if c.is_wild() else c.color
            # Apply opening special effects
            if c.value == 'Skip':
                self.message = "Premier tour: Skip appliqué"
                self.current_player = (self.current_player + 1) % 2
            elif c.value == '+2':
                self.pending_draw += 2
                self.current_player = (self.current_player + 1) % 2
            break

    def play_card(self, player, card_index, chosen_color=None):
        if player != self.current_player or self.game_over:
            return False, 'Pas ton tour'
        card = self.hands[player][card_index]

        # Must resolve pending draw before other actions
        if self.pending_draw > 0 and card.value not in ['+2','Wild+4']:
            return False, f"Il faut tirer des cartes {self.pending_draw} avant de jouer quoi que ce soit d'autre"

        # Check if card is playable
        if not card.matches(self.top_card, self.current_color):
            return False, 'Card not playable'

        # Play card
        self.hands[player].pop(card_index)
        self.discard.append(card)
        self.top_card = card
        self.current_color = chosen_color if card.is_wild() else card.color

        # Special effects
        if card.value == 'Skip':
            self.message = f"Player {player + 1} à joué skip"
        elif card.value == '+2':
            self.pending_draw += 2
            self.current_player = (self.current_player + 1) % 2
            self.message = f"Player {self.current_player + 1} doit piocher 2 cartes"
        elif card.value == 'Wild+4':
            self.pending_draw += 4
            self.current_player = (self.current_player + 1) % 2
            self.message = f"Player {self.current_player + 1} doit piocher 4 cartes"
        else:
            # Normal turn switch
            self.current_player = (self.current_player + 1) % 2

        # Check win condition
        for p in [0,1]:
            if len(self.hands[p]) == 0:
                self.game_over = True
                self.winner = p

        return True, 'Joué avec succès'

    def draw_cards(self, player, n=1):
        if player != self.current_player or self.game_over:
            return False, 'Pas ton tour'

        # If draw penalty is pending, you must draw all at once
        if self.pending_draw > 0:
            n = self.pending_draw
            self.pending_draw = 0

        drawn = self.deck.draw(n)
        self.hands[player].extend(drawn)
        self.current_player = (self.current_player + 1) % 2
        self.message = f"{len(drawn)} cartes tirées"
        return True, f'{len(drawn)} cartes tirée'

# -------------------- Pygame UI --------------------
SCREEN_W, SCREEN_H = 900, 600
CARD_W, CARD_H = 80, 120

def draw_card_surface(card):
    # Render a card surface for display
    surf = pygame.Surface((CARD_W, CARD_H))
    surf.fill((200,200,200))
    if card.is_wild():
        pygame.draw.rect(surf, (50,50,50), (0,0,CARD_W,CARD_H), border_radius=6)
        text = card.value
    else:
        color_map = {'rouge':(200,50,50),'vert':(50,150,50),'bleu':(50,50,200),'jaune':(220,200,50)}
        pygame.draw.rect(surf, color_map.get(card.color,(200,200,200)), (0,0,CARD_W,CARD_H), border_radius=6)
        text = card.value
    font = pygame.font.SysFont(None, 24)
    txt = font.render(text, True, (0,0,0))
    surf.blit(txt, (6,6))
    return surf

# ... (all previous code stays identical up to run_game)

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('UNO - Local')
    clock = pygame.time.Clock()

    state = GameState()
    state.start()

    running = True
    selected_idx = None
    chosen_color = None
    show_hand = False

    font = pygame.font.SysFont(None, 36)
    btn_player0 = pygame.Rect(50, SCREEN_H//2 - 25, 150, 50)
    btn_player1 = pygame.Rect(SCREEN_W - 200, SCREEN_H//2 - 25, 150, 50)
    btn_quit = pygame.Rect(SCREEN_W - 110, 10, 100, 40)  # Quit button

    while running:
        clock.tick(30)
        screen.fill((30,30,30))

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Quit button
                if btn_quit.collidepoint(mx,my):
                    running = False

                # Show hand button
                if btn_player0.collidepoint(mx,my) and state.current_player == 0:
                    show_hand = True
                elif btn_player1.collidepoint(mx,my) and state.current_player == 1:
                    show_hand = True

                # Hand interaction
                if show_hand:
                    hand = state.hands[state.current_player]
                    # Must draw penalty cards first
                    if state.pending_draw > 0:
                        state.draw_cards(state.current_player, state.pending_draw)
                        show_hand = False
                    else:
                        # Detect clicked card
                        start_x = (SCREEN_W - len(hand)*(CARD_W+10))//2
                        for i, card in enumerate(hand):
                            rect = pygame.Rect(start_x + i*(CARD_W+10), SCREEN_H - CARD_H - 20, CARD_W, CARD_H)
                            if rect.collidepoint(mx, my):
                                if card.is_wild():
                                    selected_idx = i
                                    state.message = 'Choisissez une couleur: R G B Y'
                                elif card.matches(state.top_card, state.current_color):
                                    state.play_card(state.current_player, i)
                                    show_hand = False
                                else:
                                    state.message = 'Carte non jouable'

            elif event.type == pygame.KEYDOWN and show_hand:
                # Draw card
                if event.key == pygame.K_d:
                    state.draw_cards(state.current_player)
                    show_hand = False
                # Wild color choice
                elif event.key in (pygame.K_r, pygame.K_g, pygame.K_b, pygame.K_y) and selected_idx is not None:
                    keymap = {pygame.K_r:'rouge', pygame.K_g:'vert', pygame.K_b:'bleu', pygame.K_y:'jaune'}
                    chosen_color = keymap[event.key]
                    state.play_card(state.current_player, selected_idx, chosen_color)
                    selected_idx = None
                    chosen_color = None
                    show_hand = False

        # Player buttons
        pygame.draw.rect(screen, (70,70,200), btn_player0)
        pygame.draw.rect(screen, (200,70,70), btn_player1)
        screen.blit(font.render('Joueur 1', True, (255,255,255)), (btn_player0.x+10, btn_player0.y+10))
        screen.blit(font.render('Joueur 2', True, (255,255,255)), (btn_player1.x+10, btn_player1.y+10))

        # Quit button
        pygame.draw.rect(screen, (200,0,0), btn_quit)
        screen.blit(font.render('Quitter', True, (255,255,255)), (btn_quit.x+5, btn_quit.y+5))

        # Top card display
        if state.top_card:
            top_surf = draw_card_surface(state.top_card)
            screen.blit(top_surf, (SCREEN_W//2 - CARD_W//2, SCREEN_H//2 - CARD_H//2))
            screen.blit(font.render(f'Couleur actuelle: {state.current_color}', True, (255,255,255)), (SCREEN_W//2 - 80, SCREEN_H//2 + CARD_H//2 + 6))

        # Active player's hand
        if show_hand:
            hand = state.hands[state.current_player]
            start_x = (SCREEN_W - len(hand)*(CARD_W+10))//2
            for i, card in enumerate(hand):
                surf = draw_card_surface(card)
                rect = surf.get_rect(topleft=(start_x + i*(CARD_W+10), SCREEN_H - CARD_H - 20))
                screen.blit(surf, rect.topleft)
                idx_txt = font.render(str(i), True, (0,0,0))
                screen.blit(idx_txt, (rect.x+4, rect.y+CARD_H-22))

        # UI info
        screen.blit(font.render(f"Joueur 1 cartes: {len(state.hands[0])}", True, (255,255,255)), (20,20))
        screen.blit(font.render(f"Joueur 2 cartes: {len(state.hands[1])}", True, (255,255,255)), (20,50))
        screen.blit(font.render(f"Tour en cours: Player {state.current_player + 1}", True, (255,255,0)), (20,80))
        screen.blit(font.render(f"Message: {state.message}", True, (255,255,0)), (20,110))

        pygame.display.flip()

        # End of game screen
        if state.game_over:
            screen.fill((30,30,30))
            msg = f"Joueur {state.winner + 1} victoire !"
            screen.blit(font.render(msg, True, (255,255,0)), (SCREEN_W//2 - 100, SCREEN_H//2))
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False

    pygame.quit()

if __name__ == '__main__':
    run_game()
