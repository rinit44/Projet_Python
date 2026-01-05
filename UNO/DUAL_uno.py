# Author: Rinit Krasniqi, Rodrigo Fernandes Valente, claude.ai
# Date: 05.12.2024
# Name: uno.py
# Description: A simple local two-player UNO game using Pygame

import pygame
import random

# -------------------- Game Constants --------------------
COLORS = ['rouge', 'jaune', 'vert', 'bleu']
VALUES = [str(i) for i in range(0, 10)] + ['Skip', '+2']
WILD_VALUES = ['Wild', 'Wild+4']

# -------------------- Card Class --------------------
class Card:
    """Represents a single UNO card with a color and value."""
    
    def __init__(self, color, value):
        self.color = color  # None for wild cards
        self.value = value

    def is_wild(self):
        """Check if the card is a wild card (no specific color)."""
        return self.color is None

    def matches(self, other_card, current_color):
        """
        Determine if this card can be played on top of another card.
        
        Args:
            other_card: The card on top of the discard pile
            current_color: The current active color (important for wild cards)
            
        Returns:
            True if the card can be played, False otherwise
        """
        # Wild cards can always be played
        if self.is_wild():
            return True
        # First card of the game (no top card yet)
        if other_card is None:
            return True
        # Match by color
        if self.color == current_color:
            return True
        # Match by value (e.g., red 5 on blue 5)
        if self.value == other_card.value:
            return True
        return False

    def __repr__(self):
        return f"Card({self.color}, {self.value})"

# -------------------- Deck Class --------------------
class Deck:
    """Represents the deck of UNO cards."""
    
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        """Build a complete UNO deck with all cards."""
        self.cards = []
        # Add colored number and action cards
        for color in COLORS:
            # One '0' card per color
            self.cards.append(Card(color, '0'))
            # Two of each other value per color
            for value in VALUES[1:]:
                self.cards.append(Card(color, value))
                self.cards.append(Card(color, value))
        # Add 4 Wild and 4 Wild+4 cards
        for _ in range(4):
            self.cards.append(Card(None, 'Wild'))
            self.cards.append(Card(None, 'Wild+4'))

    def shuffle(self):
        """Shuffle the deck randomly."""
        random.shuffle(self.cards)

    def draw(self, n=1):
        """
        Draw n cards from the deck.
        
        Args:
            n: Number of cards to draw
            
        Returns:
            List of drawn cards (may be fewer than n if deck runs out)
        """
        drawn = []
        for _ in range(n):
            if not self.cards:
                break
            drawn.append(self.cards.pop())
        return drawn

    def add_cards(self, cards):
        """
        Add cards back to the deck and reshuffle.
        Used when the deck runs out and we need to recycle the discard pile.
        
        Args:
            cards: List of cards to add back to the deck
        """
        self.cards.extend(cards)
        self.shuffle()

# -------------------- Game State --------------------
class GameState:
    """Manages the complete state of an UNO game."""
    
    def __init__(self):
        self.deck = Deck()
        self.discard = []  # Pile of played cards
        self.hands = {0: [], 1: []}  # Cards held by each player
        self.current_player = 0  # 0 or 1
        self.top_card = None  # Card on top of discard pile
        self.current_color = None  # Active color (important after wild cards)
        self.game_over = False
        self.winner = None
        self.pending_draw = 0  # Number of cards to draw from +2 or Wild+4
        self.message = ''  # Status message displayed to players
        self.just_drew = False  # Flag to indicate if player just drew a card
        
    def has_playable_card(self, player):
        """
        Check if a player has any card they can play.
        
        Args:
            player: Player index (0 or 1)
            
        Returns:
            True if player has at least one playable card
        """
        for card in self.hands[player]:
            if card.matches(self.top_card, self.current_color):
                return True
        return False
        
    def start(self):
        """Initialize the game by dealing cards and drawing the first card."""
        # Deal 7 cards to each player
        for i in range(2):
            self.hands[i] = self.deck.draw(7)

        # Draw first card - only numbered cards allowed to avoid unfair starts
        while True:
            c = self.deck.draw(1)[0]
            # Only accept numbered cards (0-9) for the starting card
            if c.value in [str(i) for i in range(10)]:
                self.top_card = c
                self.discard.append(c)
                self.current_color = c.color
                break
            else:
                # Put special/wild cards back in deck
                self.deck.cards.insert(0, c)
                self.deck.shuffle()

    def play_card(self, player, card_index, chosen_color=None):
        """
        Attempt to play a card from a player's hand.
        
        Args:
            player: Player index (0 or 1)
            card_index: Index of the card in the player's hand
            chosen_color: Color chosen when playing a wild card
            
        Returns:
            Tuple (success: bool, message: str)
        """
        # Validate turn and game state
        if player != self.current_player or self.game_over:
            return False, 'Pas ton tour'
        
        card = self.hands[player][card_index]

        # Must resolve pending draw before playing other cards
        if self.pending_draw > 0 and card.value not in ['+2', 'Wild+4']:
            return False, f"Il faut tirer {self.pending_draw} cartes avant de jouer autre chose"

        # Check if card can be played
        if not card.matches(self.top_card, self.current_color):
            return False, 'Carte non jouable'

        # Play the card
        self.hands[player].pop(card_index)
        self.discard.append(card)
        self.top_card = card
        self.current_color = chosen_color if card.is_wild() else card.color
        self.just_drew = False  # Reset draw flag after playing

        # Apply special card effects
        if card.value == 'Skip':
            # Skip: opponent loses their turn, current player plays again
            self.current_player = (self.current_player + 1) % 2
            self.current_player = (self.current_player + 1) % 2
            opponent = (player + 1) % 2 + 1
            self.message = f"Joueur {player + 1} joue Skip - Joueur {opponent} passe son tour!"
        elif card.value == '+2':
            # +2: next player must draw 2 cards
            self.pending_draw += 2
            opponent = (player + 1) % 2 + 1
            self.message = f"Joueur {opponent} doit piocher 2 cartes"
            self.current_player = (self.current_player + 1) % 2
        elif card.value == 'Wild+4':
            # Wild+4: next player must draw 4 cards
            self.pending_draw += 4
            opponent = (player + 1) % 2 + 1
            self.message = f"Joueur {opponent} doit piocher 4 cartes"
            self.current_player = (self.current_player + 1) % 2
        else:
            # Normal card: switch to next player
            self.current_player = (self.current_player + 1) % 2

        # Check for win condition (player has no cards left)
        for p in [0, 1]:
            if len(self.hands[p]) == 0:
                self.game_over = True
                self.winner = p

        return True, 'Carte jouée avec succès'

    def draw_cards(self, player, n=1):
        """
        Draw cards for a player.
        
        Args:
            player: Player index (0 or 1)
            n: Number of cards to draw (overridden if there's a penalty)
            
        Returns:
            Tuple (success: bool, message: str, can_play: bool)
        """
        # Validate turn and game state
        if player != self.current_player or self.game_over:
            return False, 'Pas ton tour', False

        # If there's a draw penalty, must draw all penalty cards
        if self.pending_draw > 0:
            n = self.pending_draw
            self.pending_draw = 0
            # When drawing penalty cards, cannot play immediately
            drawn = self.deck.draw(n)
            self.hands[player].extend(drawn)
            self.current_player = (self.current_player + 1) % 2
            self.message = f"Joueur {player + 1}: {len(drawn)} carte(s) piochée(s)"
            self.just_drew = False
            return True, f'{len(drawn)} carte(s) piochée(s)', False

        # Draw cards and add to player's hand
        drawn = self.deck.draw(n)
        self.hands[player].extend(drawn)
        self.just_drew = True  # Mark that player just drew
        
        # Check if any drawn card can be played
        can_play = False
        for card in drawn:
            if card.matches(self.top_card, self.current_color):
                can_play = True
                break
        
        if can_play:
            self.message = f"Joueur {player + 1}: {len(drawn)} carte(s) piochée(s) - Vous pouvez jouer!"
        else:
            # If drawn card cannot be played, turn ends
            self.current_player = (self.current_player + 1) % 2
            self.message = f"Joueur {player + 1}: {len(drawn)} carte(s) piochée(s) - Aucune carte jouable"
            self.just_drew = False
        
        return True, f'{len(drawn)} carte(s) piochée(s)', can_play

# -------------------- Pygame UI --------------------
SCREEN_W, SCREEN_H = 900, 600
CARD_W, CARD_H = 80, 120

def draw_card_surface(card):
    """
    Render a card as a pygame Surface.
    
    Args:
        card: Card object to render
        
    Returns:
        pygame Surface with the card drawn on it
    """
    surf = pygame.Surface((CARD_W, CARD_H))
    surf.fill((200, 200, 200))
    
    # Draw card background based on type
    if card.is_wild():
        # Wild cards are dark gray
        pygame.draw.rect(surf, (50, 50, 50), (0, 0, CARD_W, CARD_H), border_radius=6)
    else:
        # Colored cards
        color_map = {
            'rouge': (200, 50, 50),
            'vert': (50, 150, 50),
            'bleu': (50, 50, 200),
            'jaune': (220, 200, 50)
        }
        pygame.draw.rect(surf, color_map.get(card.color, (200, 200, 200)), 
                        (0, 0, CARD_W, CARD_H), border_radius=6)
    
    # Draw card value text
    font = pygame.font.SysFont(None, 24)
    txt = font.render(card.value, True, (255, 255, 255))
    surf.blit(txt, (6, 6))
    
    return surf

def run_game():
    """Main game loop."""
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('UNO - Local 2 Joueurs')
    clock = pygame.time.Clock()

    # Initialize game state
    state = GameState()
    state.start()

    # UI state variables
    running = True
    selected_idx = None  # Index of selected wild card (waiting for color choice)
    chosen_color = None
    show_hand = False  # Whether current player's hand is visible

    # Create UI elements
    font = pygame.font.SysFont(None, 36)
    btn_player0 = pygame.Rect(50, SCREEN_H//2 - 25, 150, 50)
    btn_player1 = pygame.Rect(SCREEN_W - 200, SCREEN_H//2 - 25, 150, 50)
    btn_quit = pygame.Rect(SCREEN_W - 110, 10, 100, 40)
    btn_draw = pygame.Rect(SCREEN_W//2 - 75, SCREEN_H - 180, 150, 40)
    btn_pass = pygame.Rect(SCREEN_W//2 + 85, SCREEN_H - 180, 150, 40)

    # Main game loop
    while running:
        clock.tick(30)
        screen.fill((30, 30, 30))  # Dark background

        mx, my = pygame.mouse.get_pos()
        
        # -------------------- Cursor Management --------------------
        # Change cursor to hand pointer when hovering over clickable elements
        cursor_hand = False
        
        if btn_quit.collidepoint(mx, my):
            cursor_hand = True
        elif btn_player0.collidepoint(mx, my) and state.current_player == 0:
            cursor_hand = True
        elif btn_player1.collidepoint(mx, my) and state.current_player == 1:
            cursor_hand = True
        elif show_hand and btn_draw.collidepoint(mx, my):
            cursor_hand = True
        elif show_hand and state.just_drew and btn_pass.collidepoint(mx, my):
            cursor_hand = True
        elif show_hand:
            # Check if hovering over any card
            hand = state.hands[state.current_player]
            max_width = SCREEN_W - 40
            total_card_width = len(hand) * CARD_W
            
            # Calculate spacing (overlap if too many cards)
            if total_card_width > max_width:
                spacing = (max_width - CARD_W) // max(1, len(hand) - 1)
            else:
                spacing = CARD_W + 10
            
            start_x = (SCREEN_W - (len(hand) - 1) * spacing - CARD_W) // 2
            for i, card in enumerate(hand):
                rect = pygame.Rect(start_x + i * spacing, SCREEN_H - CARD_H - 20, CARD_W, CARD_H)
                if rect.collidepoint(mx, my):
                    cursor_hand = True
                    break
        
        # Apply cursor
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if cursor_hand else pygame.SYSTEM_CURSOR_ARROW)
        
        # -------------------- Event Handling --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Quit button
                if btn_quit.collidepoint(mx, my):
                    running = False

                # Show hand buttons - reveal cards for current player
                if btn_player0.collidepoint(mx, my) and state.current_player == 0:
                    show_hand = True
                elif btn_player1.collidepoint(mx, my) and state.current_player == 1:
                    show_hand = True

                # Pass button (only visible after drawing)
                if show_hand and state.just_drew and btn_pass.collidepoint(mx, my):
                    state.current_player = (state.current_player + 1) % 2
                    state.just_drew = False
                    show_hand = False
                    state.message = "Tour passé"

                # Draw button
                if show_hand and btn_draw.collidepoint(mx, my):
                    if state.just_drew:
                        state.message = "Vous avez déjà pioché! Jouez ou passez."
                    elif state.pending_draw > 0:
                        # Must draw penalty cards
                        state.draw_cards(state.current_player)
                        show_hand = False
                    elif not state.has_playable_card(state.current_player):
                        # No playable cards, draw one
                        success, msg, can_play = state.draw_cards(state.current_player)
                        if not can_play:
                            show_hand = False
                    else:
                        # Player has playable cards, cannot draw
                        state.message = "Vous avez des cartes jouables!"

                # Card clicking
                if show_hand:
                    hand = state.hands[state.current_player]
                    max_width = SCREEN_W - 40
                    total_card_width = len(hand) * CARD_W
                    
                    # Calculate spacing
                    if total_card_width > max_width:
                        spacing = (max_width - CARD_W) // max(1, len(hand) - 1)
                    else:
                        spacing = CARD_W + 10
                    
                    start_x = (SCREEN_W - (len(hand) - 1) * spacing - CARD_W) // 2

                    # Detect which card was clicked
                    for i, card in enumerate(hand):
                        rect = pygame.Rect(start_x + i * spacing, SCREEN_H - CARD_H - 20, CARD_W, CARD_H)
                        if rect.collidepoint(mx, my):
                            if card.is_wild():
                                # Wild card: need to choose color
                                selected_idx = i
                                state.message = 'Choisissez une couleur: R(ouge) V(ert) B(leu) J(aune)'
                            elif card.matches(state.top_card, state.current_color):
                                # Play the card
                                success, msg = state.play_card(state.current_player, i)
                                if success:
                                    show_hand = False
                                    selected_idx = None
                            else:
                                # Card cannot be played
                                state.message = 'Carte non jouable'

            elif event.type == pygame.KEYDOWN and show_hand:
                # Color selection for wild cards (R, G, B, Y keys)
                if event.key in (pygame.K_r, pygame.K_v, pygame.K_b, pygame.K_j) and selected_idx is not None:
                    keymap = {
                        pygame.K_r: 'rouge',
                        pygame.K_v: 'vert',
                        pygame.K_b: 'bleu',
                        pygame.K_j: 'jaune'
                    }
                    chosen_color = keymap[event.key]
                    success, msg = state.play_card(state.current_player, selected_idx, chosen_color)
                    if success:
                        selected_idx = None
                        chosen_color = None
                        show_hand = False

        # -------------------- Rendering --------------------
        
        # Player action buttons
        pygame.draw.rect(screen, (70, 70, 200), btn_player0)
        pygame.draw.rect(screen, (200, 70, 70), btn_player1)
        screen.blit(font.render('Joueur 1', True, (255, 255, 255)), 
                   (btn_player0.x + 10, btn_player0.y + 10))
        screen.blit(font.render('Joueur 2', True, (255, 255, 255)), 
                   (btn_player1.x + 10, btn_player1.y + 10))

        # Quit button
        pygame.draw.rect(screen, (200, 0, 0), btn_quit)
        screen.blit(font.render('Quitter', True, (255, 255, 255)), 
                   (btn_quit.x + 5, btn_quit.y + 5))

        # Draw button (only visible when hand is shown)
        if show_hand:
            # Green if must/can draw, gray otherwise
            can_draw = not state.just_drew and (state.pending_draw > 0 or not state.has_playable_card(state.current_player))
            color = (50, 150, 50) if can_draw else (100, 100, 100)
            pygame.draw.rect(screen, color, btn_draw)
            draw_text = f"Piocher ({state.pending_draw})" if state.pending_draw > 0 else "Piocher"
            screen.blit(font.render(draw_text, True, (255, 255, 255)), 
                       (btn_draw.x + 10, btn_draw.y + 5))
            
            # Pass button (only visible after drawing)
            if state.just_drew:
                pygame.draw.rect(screen, (150, 100, 50), btn_pass)
                screen.blit(font.render('Passer', True, (255, 255, 255)), 
                           (btn_pass.x + 30, btn_pass.y + 5))

        # Top card display (center of screen)
        if state.top_card:
            top_surf = draw_card_surface(state.top_card)
            screen.blit(top_surf, (SCREEN_W//2 - CARD_W//2, SCREEN_H//2 - CARD_H//2))
            screen.blit(font.render(f'Couleur: {state.current_color}', True, (255, 255, 255)), 
                       (SCREEN_W//2 - 80, SCREEN_H//2 + CARD_H//2 + 6))

        # Current player's hand (bottom of screen)
        if show_hand:
            hand = state.hands[state.current_player]
            max_width = SCREEN_W - 40
            total_card_width = len(hand) * CARD_W
            
            # Calculate spacing (cards overlap if too many)
            if total_card_width > max_width:
                spacing = (max_width - CARD_W) // max(1, len(hand) - 1)
            else:
                spacing = CARD_W + 10
            
            start_x = (SCREEN_W - (len(hand) - 1) * spacing - CARD_W) // 2
            
            # Draw all cards
            for i, card in enumerate(hand):
                surf = draw_card_surface(card)
                rect = surf.get_rect(topleft=(start_x + i * spacing, SCREEN_H - CARD_H - 20))
                screen.blit(surf, rect.topleft)

        # Game information (top left)
        screen.blit(font.render(f"Joueur 1: {len(state.hands[0])} cartes", True, (255, 255, 255)), 
                   (20, 20))
        screen.blit(font.render(f"Joueur 2: {len(state.hands[1])} cartes", True, (255, 255, 255)), 
                   (20, 50))
        screen.blit(font.render(f"Tour: Joueur {state.current_player + 1}", True, (255, 255, 0)), 
                   (20, 80))
        screen.blit(font.render(f"Message: {state.message}", True, (255, 255, 0)), 
                   (20, 110))

        pygame.display.flip()

        # -------------------- Game Over --------------------
        if state.game_over:
            screen.fill((30, 30, 30))
            msg = f"Joueur {state.winner + 1} a gagné!"
            screen.blit(font.render(msg, True, (255, 255, 0)), 
                       (SCREEN_W//2 - 100, SCREEN_H//2))
            pygame.display.flip()
            pygame.time.wait(5000)  # Show victory screen for 5 seconds
            running = False

    pygame.quit()

if __name__ == '__main__':
    run_game()