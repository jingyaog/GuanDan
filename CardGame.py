import random
import pygame
import time

# !!!!!!!!!!!!!!!!!!!!!!!!!!!
# Citations:
# Introduction and Rules of Guan Dan: https://www.pagat.com/climbing/guan_dan.html
# Background images: http://www.dreamtemplate.com/dreamcodes/documentation/background_images.html
#                    https://www.scroogetheboardgame.co.uk/contact-us
#                    https://www.photohdx.com/pic-472/vintage-red-damask-floral-pattern-canvas-background
# Images of cards: http://www.bkill.com/download/176402.html#soft-downUrl
# !!!!!!!!!!!!!!!!!!!!!!!!!!!

WIDTH = 1024
HEIGHT = 768
green = (0, 200, 0)
red = (200, 0, 0)
yellow = (240, 220, 0)
brightYellow = (255, 255, 0)
brightGreen = (0, 255, 0)
brightRed = (255, 0, 0)

def arrange(L):
    L.sort(key=lambda card: (card.realRank, card.suit))

class Game(object):
    def __init__(self, teamALevel=2, teamBLevel=2):
        self.teamALevel = teamALevel
        self.teamBLevel = teamBLevel
        self.players = []
        self.winners = []
        self.losers = []
        self.startPage = True
        self.settingsPage = False
        self.infoPage = False
        self.introPage = False
        self.rulesPage = False
        self.thePlayPage = False
        self.offlineMode = False
        self.endPage = False
        self.cardsOnTable = []
        self.handOnTable = Hand(self.cardsOnTable)
        self.lastPlayer = None
        self.isOver = (len([player for player in self.players if player.isOver]) > 2)
        self.nextRanking = 1
        self.wildRank = 2
        self.AISpeed = 500
        self.bg = "bg2.jpg"

    def setAISpeed(self):
        try:
            with open("settings.txt", "rt") as f:
                self.AISpeed = int(f.read().split()[0])
        except:
            pass

    def setBg(self):
        try:
            with open("settings.txt", "rt") as f:
                self.bg = f.read().split()[1]
        except:
            pass

    def drawBg(self, screen):
        bg = pygame.image.load(self.bg)
        screen.blit(bg, (0, 0))

    def drawBackButton(self, screen):
        font = pygame.font.Font(None, 30)
        self.backButton = pygame.Rect(842, 50, 100, 50)
        backText = font.render("Back", True, (0,) * 3)
        pygame.draw.rect(screen, yellow, self.backButton)
        screen.blit(backText, (865, 65))

    def drawStartPage(self):
        largeFont = pygame.font.Font(None, 100)
        font = pygame.font.Font(None, 30)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Start")
        self.offlineModeButton = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 - 40, 150, 50)
        self.settingsButton = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 + 70, 150, 50)
        self.infoButton = pygame.Rect(842, 667, 130, 50)
        guandanText = largeFont.render("Guan Dan", True, (255, 130, 0))
        offlineText = font.render("Offline Mode", True, (0,) * 3)
        settingsText = font.render("Settings", True, (0,) * 3)
        infoText = font.render("Information", True, (0,) * 3)
        self.drawBg(screen)
        screen.blit(guandanText, (350, 200))
        pygame.draw.rect(screen, green, self.offlineModeButton)
        screen.blit(offlineText, (WIDTH / 2 - 65, HEIGHT / 2 - 25))
        pygame.draw.rect(screen, red, self.settingsButton)
        screen.blit(settingsText, (WIDTH / 2 - 45, HEIGHT / 2 + 85))
        pygame.draw.rect(screen, yellow, self.infoButton)
        screen.blit(infoText, (850, 680))

    def drawSettingsPage(self, mousePos):
        font = pygame.font.Font(None, 30)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Settings")
        self.drawBg(screen)
        self.drawBackButton(screen)
        self.speed1Button = pygame.Rect(300, 200, 100, 50)
        self.speed2Button = pygame.Rect(450, 200, 100, 50)
        self.speed3Button = pygame.Rect(600, 200, 100, 50)
        self.bg1Button = pygame.Rect(300, 350, 100, 50)
        self.bg2Button = pygame.Rect(450, 350, 100, 50)
        self.bg3Button = pygame.Rect(600, 350, 100, 50)
        speedText = font.render("AI Speed: ", True, (255,) * 3)
        speed1Text = font.render("1s", True, (255,) * 3)
        speed2Text = font.render("2s", True, (255,) * 3)
        speed3Text = font.render("5s", True, (255,) * 3)
        bgText = font.render("Background: ", True, (255,) * 3)
        bg1Text = font.render("Blue", True, (255,) * 3)
        bg2Text = font.render("Green", True, (255,) * 3)
        bg3Text = font.render("Red", True, (255,) * 3)
        if self.speed1Button.collidepoint(mousePos):
            pygame.draw.rect(screen, brightGreen, self.speed1Button)
        else:
            pygame.draw.rect(screen, green, self.speed1Button)
        if self.speed2Button.collidepoint(mousePos):
            pygame.draw.rect(screen, brightGreen, self.speed2Button)
        else:
            pygame.draw.rect(screen, green, self.speed2Button)
        if self.speed3Button.collidepoint(mousePos):
            pygame.draw.rect(screen, brightGreen, self.speed3Button)
        else:
            pygame.draw.rect(screen, green, self.speed3Button)
        if self.bg1Button.collidepoint(mousePos):
            pygame.draw.rect(screen, brightGreen, self.bg1Button)
        else:
            pygame.draw.rect(screen, green, self.bg1Button)
        if self.bg2Button.collidepoint(mousePos):
            pygame.draw.rect(screen, brightGreen, self.bg2Button)
        else:
            pygame.draw.rect(screen, green, self.bg2Button)
        if self.bg3Button.collidepoint(mousePos):
            pygame.draw.rect(screen, brightGreen, self.bg3Button)
        else:
            pygame.draw.rect(screen, green, self.bg3Button)
        screen.blit(speedText, (100, 215))
        screen.blit(speed1Text, (340, 215))
        screen.blit(speed2Text, (490, 215))
        screen.blit(speed3Text, (640, 215))
        screen.blit(bgText, (100, 365))
        screen.blit(bg1Text, (327, 365))
        screen.blit(bg2Text, (470, 365))
        screen.blit(bg3Text, (631, 365))

    def drawInfoPage(self):
        font = pygame.font.Font(None, 30)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Information")
        self.drawBg(screen)
        self.drawBackButton(screen)
        self.introButton = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 - 100, 150, 50)
        self.rulesButton = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 + 15, 150, 50)
        self.thePlayButton = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 + 130, 150, 50)
        introText = font.render("Introduction", True, (0,) * 3)
        rulesText = font.render("Rules", True, (0,) * 3)
        thePlayText = font.render("The Play", True, (0,) * 3)
        pygame.draw.rect(screen, green, self.introButton)
        pygame.draw.rect(screen, green, self.rulesButton)
        pygame.draw.rect(screen, green, self.thePlayButton)
        screen.blit(introText, (WIDTH / 2 - 65, HEIGHT / 2 - 85))
        screen.blit(rulesText, (WIDTH / 2 - 30, HEIGHT / 2 + 32))
        screen.blit(thePlayText, (WIDTH / 2 - 42, HEIGHT / 2 + 145))

    def drawIntroPage(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Introduction")
        self.drawBg(screen)
        self.drawBackButton(screen)
        intro = pygame.image.load("intro.png")
        screen.blit(intro, (110, 150))

    def drawRulesPage(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rules")
        self.drawBg(screen)
        intro = pygame.image.load("rules.png")
        intro = pygame.transform.scale(intro, (1024, 700))
        screen.blit(intro, (0, 60))
        self.drawBackButton(screen)

    def drawThePlayPage(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Play")
        self.drawBg(screen)
        intro = pygame.image.load("thePlay.png")
        screen.blit(intro, (50, 110))
        self.drawBackButton(screen)

    def drawEndPage(self, game):
        largeFont = pygame.font.Font(None, 60)
        font = pygame.font.Font(None, 36)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("End")
        self.drawBg(screen)
        self.continueButton = pygame.Rect(WIDTH / 2 - 75, 600, 150, 60)
        continueText = font.render("Continue", True, (0,) * 3)
        winText = largeFont.render("WIN", True, (255,) * 3)
        loseText = largeFont.render("LOSE", True, (255,) * 3)
        winner1Text = font.render(f"{game.winners[0]}: No.{game.winners[0].ranking}", True, (255,) * 3)
        winner2Text = font.render(f"{game.winners[1]}: No.{game.winners[1].ranking}", True, (255,) * 3)
        loser1Text = font.render(f"{game.losers[0]}: No.{game.losers[0].ranking}", True, (255,) * 3)
        loser2Text = font.render(f"{game.losers[1]}: No.{game.losers[1].ranking}", True, (255,) * 3)
        pygame.draw.rect(screen, green, self.continueButton)
        screen.blit(continueText, (WIDTH / 2 - 58, 618))
        screen.blit(winText, (WIDTH / 2 - 300, 150))
        screen.blit(loseText, (WIDTH / 2 + 100, 150))
        screen.blit(winner1Text, (WIDTH / 2 - 300, 230))
        screen.blit(winner2Text, (WIDTH / 2 - 300, 280))
        screen.blit(loser1Text, (WIDTH / 2 + 100, 230))
        screen.blit(loser2Text, (WIDTH / 2 + 100, 280))

    def drawScoreboard(self, screen, game):
        font = pygame.font.Font(None, 30)
        teamAText = font.render(f"Team A Level: {game.teamALevel}", True, (255, 130, 0))
        teamBText = font.render(f"Team B Level: {game.teamBLevel}", True, (255, 130, 0))
        screen.blit(teamAText, (30, 20))
        screen.blit(teamBText, (30, 50))

    def drawBasics(self, screen, mousePos, game):
        font = pygame.font.Font(None, 24)
        self.passButton = pygame.Rect(WIDTH / 2 - 100, 500, 60, 30)
        self.playButton = pygame.Rect(WIDTH / 2 - 190, 500, 60, 30)
        self.hintButton = pygame.Rect(WIDTH / 2 - 10, 500, 60, 30)
        self.deseletButton = pygame.Rect(WIDTH / 2 + 80, 500, 100, 30)
        playText = font.render("Play", True, (0,) * 3)
        passText = font.render("Pass", True, (0,) * 3)
        hintText = font.render("Hint", True, (0,) * 3)
        deselectText = font.render("Deselect All", True, (0,) * 3)
        self.drawBg(screen)
        if game.turn == game.players[0]:
            if self.passButton.collidepoint(mousePos):
                pygame.draw.rect(screen, brightGreen, self.passButton)
            else:
                pygame.draw.rect(screen, green, self.passButton)
            if self.playButton.collidepoint(mousePos):
                pygame.draw.rect(screen, brightRed, self.playButton)
            else:
                pygame.draw.rect(screen, red, self.playButton)
            if self.hintButton.collidepoint(mousePos):
                pygame.draw.rect(screen, brightYellow, self.hintButton)
            else:
                pygame.draw.rect(screen, yellow, self.hintButton)
            if self.deseletButton.collidepoint(mousePos):
                pygame.draw.rect(screen, brightRed, self.deseletButton)
            else:
                pygame.draw.rect(screen, red, self.deseletButton)
            screen.blit(passText, (WIDTH / 2 - 89, 507))
            screen.blit(playText, (WIDTH / 2 - 178, 507))
            screen.blit(hintText, (WIDTH / 2 + 2, 507))
            screen.blit(deselectText, (WIDTH / 2 + 83, 507))
        self.drawBackButton(screen)
        self.drawScoreboard(screen, game)

    def start(self):
        # Distributing cards
        self.cards = Poker(2, self)
        self.cards.shuffle()
        for i in range(27):
            for player in self.players:
                player.get(self.cards.next())
        for player in self.players:
            arrange(player.cardsInHand)
        self.turn = random.choice(self.players)
        self.numTurns = 0
        self.nextRanking = 1

    def updateResult(self):
        for p in self.players:
            if p.ranking == 1:
                self.winners.append(p)
                self.winners.append(self.players[self.players.index(p) - 2])
                self.losers.append(self.players[self.players.index(p) - 3])
                self.losers.append(self.players[self.players.index(p) - 1])
        if set(self.winners) == {self.players[0], self.players[2]}:
            if {self.players[0].ranking, self.players[2].ranking} == {1, 2}:
                self.teamALevel += 3
            elif {self.players[0].ranking, self.players[2].ranking} == {1, 3}:
                self.teamALevel += 2
            else:
                self.teamALevel += 1
            if self.teamALevel > 14:
                self.teamALevel = 2
            self.wildRank = self.teamALevel
        if set(self.winners) == {self.players[1], self.players[3]}:
            if {self.players[1].ranking, self.players[3].ranking} == {1, 2}:
                self.teamBLevel += 3
            elif {self.players[1].ranking, self.players[3].ranking} == {1, 3}:
                self.teamBLevel += 2
            else:
                self.teamBLevel += 1
            if self.teamBLevel > 14:
                self.teamBLevel = 2
            self.wildRank = self.teamBLevel

    def newRound(self):
        for p in self.players:
            p.passed = False
            p.isOver = False
            p.cardsPlayed = []
            p.cardsInHand = []
        self.cardsOnTable = []
        self.handOnTable = Hand(self.cardsOnTable)
        self.lastPlayer = None
        self.start()

    def nextPlayer(self):
        if not self.players[self.players.index(self.turn) - 3].isOver:
            self.turn = self.players[self.players.index(self.turn) - 3]
        elif not self.players[self.players.index(self.turn) - 2].isOver:
            self.turn = self.players[self.players.index(self.turn) - 2]
        else:
            self.turn = self.players[self.players.index(self.turn) - 1]

class Card(object):
    def __init__(self, suit, rank, game):
        self.suit = suit
        self.rank = rank
        self.realRank = rank
        if rank == game.wildRank:
            self.realRank = 14.5
        self.image = pygame.image.load(f"pukeImage/{self}.png")
        self.isSelected = False
        self.isLocked = False

    def isInList(self, l):
        for ele in l:
            if self.__eq__(ele):
                return True
        return False

    def isWildCard(self):
        return self.realRank == 14.5 and self.suit == "H"

    def __str__(self):
        if self.rank == 10:
            rank_str = "T"
        elif self.rank == 11:
            rank_str = "J"
        elif self.rank == 12:
            rank_str = "Q"
        elif self.rank == 13:
            rank_str = "K"
        elif self.rank == 14:
            rank_str = "A"
        elif self.rank == 15:
            rank_str = "Small Joker"
        elif self.rank == 16:
            rank_str = "Big Joker"
        else:
            rank_str = str(self.rank)
        return f"{self.suit}{rank_str}"

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        return self.realRank > other.realRank

    def __ge__(self, other):
        return self.realRank >= other.realRank

    def __lt__(self, other):
        return self.realRank < other.realRank

    def __le__(self, other):
        return self.realRank <= other.rank

class Poker(object):
    def __init__(self, numDecks, game):
        self.cards = [Card(suit, rank, game) for suit in "CDHS" for rank in range(2, 15) for i in range(numDecks)]
        for i in range(numDecks):
            self.cards.append(Card("", 15, game))
            self.cards.append(Card("", 16, game))
        self.current = 0

    def __str__(self):
        return str([card for card in self.cards])

    def shuffle(self):
        self.current = 0
        random.shuffle(self.cards)

    def next(self):
        card = self.cards[self.current]
        self.current += 1
        return card


class Player(object):
    def __init__(self, name):
        self.name = name
        self.cardsInHand = []
        self.selectedCards = []
        self.lockedHands = []
        self.cardsPlayed = []
        self.handPlayed = Hand(self.cardsPlayed)
        self.passed = False
        self.isOver = False
        self.ranking = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def get(self, card):
        self.cardsInHand.append(card)

    def arrange(self, card_key):
        self.cardsInHand.sort(key=card_key)

    def playCards(self, game):
        h = Hand(self.selectedCards)
        self.cardsPlayed = []
        while self.selectedCards != []:
            card = self.selectedCards[0]
            self.cardsPlayed.append(card)
            self.selectedCards.remove(card)
            self.cardsInHand.remove(card)
        self.handPlayed = Hand(self.cardsPlayed)
        game.cardsOnTable = self.cardsPlayed
        game.handOnTable = Hand(game.cardsOnTable)
        game.lastPlayer = self
        self.passed = False
        game.numTurns += 1
        if len(self.cardsInHand) == 0:
            self.isOver = True
            self.overTurn = game.numTurns
            self.ranking = game.nextRanking
            game.nextRanking += 1

    def passTurn(self, game):
        for card in self.selectedCards:
            card.isSelected = False
        self.selectedCards = []
        self.cardsPlayed = []
        self.passed = True
        game.numTurns += 1
        game.nextPlayer()

    def drawNumCardsLeft(self, screen, game):
        font = pygame.font.Font(None, 30)
        playerText = font.render(f"{self}", True, (255,) * 3)
        text = font.render(f"{len(self.cardsInHand)} cards left", True, (255,) * 3)
        index = game.players.index(self)
        if index == 0:
            startX, startY = WIDTH / 2 - 55, 720
        elif index == 1:
            startX, startY = 895, HEIGHT / 2 - 100
        elif index == 2:
            startX, startY = WIDTH / 2 - 55, 20
        else:
            startX, startY = 15, HEIGHT / 2 - 100
        screen.blit(playerText, (startX, startY))
        screen.blit(text, (startX, startY + 20))

    def drawCardsPlayed(self, screen, game):
        index = game.players.index(self)
        if index == 0:
            startX, startY = WIDTH / 2 - ((len(self.cardsPlayed) - 1) * 20 + 105) / 2, 330
        elif index == 1:
            startX, startY = 690, HEIGHT/2 - 130
        elif index == 2:
            startX, startY = WIDTH/2 - ((len(self.cardsPlayed) - 1) * 20 + 105) / 2, 130
        else:
            startX, startY = 150, HEIGHT/2 - 130
        for i in range(len(self.cardsPlayed)):
            card = self.cardsPlayed[i]
            screen.blit(card.image, (startX + 20 * i, startY))

    def drawPass(self, screen, game):
        font = pygame.font.Font(None, 30)
        index = game.players.index(self)
        if index == 0:
            startX, startY = WIDTH / 2 - ((len(self.cardsPlayed) - 1) * 20 + 105) / 2, 450
        elif index == 1:
            startX, startY = 750, HEIGHT / 2 - 130
        elif index == 2:
            startX, startY = WIDTH / 2 - ((len(self.cardsPlayed) - 1) * 20 + 105) / 2, 130
        else:
            startX, startY = 150, HEIGHT / 2 - 130
        passText = font.render('PASS', True, (191,) * 3)
        screen.blit(passText, (startX, startY))

    def drawCards(self, screen):
        startX = WIDTH / 2 - ((len(self.cardsInHand) - 1) * 20 + 105) / 2
        startY = 560
        for i in range(len(self.cardsInHand)):
            card = self.cardsInHand[i]
            if card.isSelected:
                screen.blit(card.image, (startX + 20 * i, startY - 20))
            else:
                screen.blit(card.image, (startX + 20 * i, startY))

    # returns the indices of all the single hands with values greater than that of loHand
    def getWildCards(self):
        result = []
        for i in range(len(self.cardsInHand)):
            if self.cardsInHand[i].isWildCard():
                result.append(i)
        return result

    def getAllSingles(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        if len(self.cardsInHand) == 1:
            result.append([0])
        else:
            for i in range(len(self.cardsInHand)):
                if not self.cardsInHand[i].isLocked:
                    if self.cardsInHand[i - 1].rank != self.cardsInHand[i].rank and \
                            (self.cardsInHand[(i + 1) % len(self.cardsInHand)].rank != self.cardsInHand[i].rank or \
                                    self.cardsInHand[(i + 1) % len(self.cardsInHand)].isLocked):
                        if Hand([self.cardsInHand[i]]).getValue() > loValue:
                            result.append([i])
        return result

    def getAllPairs(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        if len(self.cardsInHand) == 2 and Hand(self.cardsInHand[:]).isPair():
            result.append([0, 1])
        else:
            for i in range(len(self.cardsInHand) - 1):
                if (not self.cardsInHand[i].isLocked) and (not self.cardsInHand[i+1].isLocked):
                    if self.cardsInHand[i - 1].rank != self.cardsInHand[i].rank and \
                            (self.cardsInHand[(i + 2) % len(self.cardsInHand)].rank != self.cardsInHand[i].rank or \
                                    self.cardsInHand[(i + 2) % len(self.cardsInHand)].isLocked) and \
                            Hand(self.cardsInHand[i:i + 2]).isPair():
                        if Hand(self.cardsInHand[i:i+2]).getValue() > loValue:
                            result.append([i, i+1])
        return result

    def getAllTriples(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        if len(self.cardsInHand) == 3 and Hand(self.cardsInHand[:]).isTriple():
            result.append([0, 1, 2])
        else:
            for i in range(len(self.cardsInHand) - 2):
                if self.cardsInHand[i].isLocked or self.cardsInHand[i+1].isLocked or self.cardsInHand[i+2].isLocked:
                    continue
                if self.cardsInHand[i - 1].rank != self.cardsInHand[i].rank and \
                        (self.cardsInHand[(i + 3) % len(self.cardsInHand)].rank != self.cardsInHand[i].rank or \
                                self.cardsInHand[(i + 3) % len(self.cardsInHand)].isLocked) and \
                        Hand(self.cardsInHand[i:i + 3]).isTriple():
                    if Hand(self.cardsInHand[i:i+3]).getValue() > loValue:
                        result.append([i, i + 1, i + 2])
        return result

    def getAllFullHouses(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        allTriples = self.getAllTriples()
        allPairs = self.getAllPairs()
        if allTriples == [] or allPairs == []:
            return []
        p1 = allPairs[0][0]
        result = []
        for triple in allTriples:
            t1 = triple[0]
            if Hand(self.cardsInHand[p1:p1+2] + self.cardsInHand[t1:t1+3]).getValue() > loValue:
                result.append([p1, p1+1, t1, t1+1, t1+2])
        return result

    def findStraight(self, loRank):
        result = []
        rank = loRank
        for i in range(len(self.cardsInHand)):
            if self.cardsInHand[i].isLocked:
                continue
            if rank > loRank + 4:
                break
            if self.cardsInHand[i].rank == rank:
                result.append(i)
                rank += 1
            if self.cardsInHand[i].rank > rank:
                return []
        return result

    def findAlmostStraightFlush(self, loRank):
        result = []
        for suit in "CDHS":
            rank = loRank
            hand = []
            for i in range(len(self.cardsInHand)):
                if self.cardsInHand[i].isLocked:
                    continue
                if rank > loRank + 4:
                    break
                if self.cardsInHand[i].suit == suit:
                    if self.cardsInHand[i].rank == rank:
                        hand.append(i)
                        rank += 1
                    elif self.cardsInHand[i].rank == rank + 1 and self.cardsInHand[i].rank < loRank + 5:
                        hand.append(i)
                        rank += 2
                    elif self.cardsInHand[i].rank > rank + 1:
                        break
            if len(hand) == 4 and self.cardsInHand[hand[0]].rank == loRank:
                result.append(hand)
        return result

    def getAllStraightNotFlushes(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        allSingles = []
        for single in self.getAllSingles():
            allSingles.append(single[0])
        for rank in range(2, 11):
            straight = self.findStraight(rank)
            if straight != []:
                hand = Hand([self.cardsInHand[i] for i in straight])
                if hand.getValue() > loValue and hand.isStraightNotFlush():
                    singleCount = 0
                    for i in straight:
                        if i in allSingles:
                            singleCount += 1
                    if singleCount > 1:
                        result.append(straight)
        return result

    def getAllStraightFlushes(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        for rank in range(2, 11):
            straight = self.findStraight(rank)
            if straight != []:
                hand = Hand([self.cardsInHand[i] for i in straight])
                if hand.getValue() > loValue and hand.isStraightFlush():
                    result.append(straight)
        return result

    def getAllAlmostStraightFlushes(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        for rank in range(2, 11):
            straights = self.findAlmostStraightFlush(rank)
            if straights != []:
                for straight in straights:
                    result.append(straight)
        return result

    def getAllTubes(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        allPairs = self.getAllPairs()
        if len(allPairs) >= 3:
            for i in range(len(allPairs) - 2):
                hand = Hand([self.cardsInHand[j] for j in allPairs[i] + allPairs[i + 1] + allPairs[i + 2]])
                if hand.isTube() and hand.getValue() > loValue:
                    result.append(allPairs[i] + allPairs[i + 1] + allPairs[i + 2])
        return result

    def getAllPlates(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        allTriples = self.getAllTriples()
        if len(allTriples) >= 2:
            for i in range(len(allTriples) - 1):
                hand = Hand([self.cardsInHand[j] for j in allTriples[i] + allTriples[i + 1]])
                if hand.isPlate() and hand.getValue() > loValue:
                    result.append(allTriples[i] + allTriples[i + 1])
        return result

    def getAllBombs(self, loHand=None):
        if loHand == None:
            loValue = 0
        else:
            loValue = loHand.getValue()
        result = []
        if len(self.cardsInHand) == 4 and Hand(self.cardsInHand[:]).isBomb():
            result.append([0, 1, 2, 3])
        if len(self.cardsInHand) == 5 and Hand(self.cardsInHand[:]).isBomb():
            result.append([0, 1, 2, 3, 4])
        if len(self.cardsInHand) == 6 and Hand(self.cardsInHand[:]).isBomb():
            result.append([0, 1, 2, 3, 4, 5])
        if len(self.cardsInHand) == 7 and Hand(self.cardsInHand[:]).isBomb():
            result.append([0, 1, 2, 3, 4, 5, 6])
        if len(self.cardsInHand) == 8 and Hand(self.cardsInHand[:]).isBomb():
            result.append([0, 1, 2, 3, 4, 5, 6, 7])
        for i in range(len(self.cardsInHand) - 4):
            if self.cardsInHand[i].isLocked or self.cardsInHand[i+1].isLocked or self.cardsInHand[i+2].isLocked or \
                    self.cardsInHand[i+3].isLocked:
                continue
            if self.cardsInHand[i - 1].rank != self.cardsInHand[i].rank and \
                    self.cardsInHand[(i + 4) % len(self.cardsInHand)].rank != self.cardsInHand[i].rank and \
                    Hand(self.cardsInHand[i:i + 4]).isBomb():
                if Hand(self.cardsInHand[i:i+4]).getValue() > loValue:
                    result.append([i, i + 1, i + 2, i + 3])
        for i in range(len(self.cardsInHand) - 5):
            if self.cardsInHand[i].isLocked or self.cardsInHand[i+1].isLocked or self.cardsInHand[i+2].isLocked or \
                    self.cardsInHand[i+3].isLocked or self.cardsInHand[i+4].isLocked:
                continue
            if self.cardsInHand[i - 1].rank != self.cardsInHand[i].rank and \
                    self.cardsInHand[(i + 5) % len(self.cardsInHand)].rank != self.cardsInHand[i].rank and \
                    Hand(self.cardsInHand[i:i + 5]).isBomb():
                if Hand(self.cardsInHand[i:i+5]).getValue() > loValue:
                    result.append([i, i + 1, i + 2, i + 3, i + 4])
        for straightFlush in self.getAllStraightFlushes():
            result.append(straightFlush)
        for i in range(len(self.cardsInHand) - 6):
            if self.cardsInHand[i].isLocked or self.cardsInHand[i+1].isLocked or self.cardsInHand[i+2].isLocked or \
                    self.cardsInHand[i+3].isLocked or self.cardsInHand[i+4].isLocked or self.cardsInHand[i+5].isLocked:
                continue
            if self.cardsInHand[i - 1].rank != self.cardsInHand[i].rank and \
                    self.cardsInHand[(i + 6) % len(self.cardsInHand)].rank != self.cardsInHand[i].rank and \
                    Hand(self.cardsInHand[i:i + 6]).isBomb():
                if Hand(self.cardsInHand[i:i+6]).getValue() > loValue:
                    result.append([i, i + 1, i + 2, i + 3, i + 4, i + 5])
        for i in range(len(self.cardsInHand) - 7):
            if self.cardsInHand[i].isLocked or self.cardsInHand[i+1].isLocked or self.cardsInHand[i+2].isLocked or \
                    self.cardsInHand[i+3].isLocked or self.cardsInHand[i+4].isLocked or self.cardsInHand[i+5].isLocked or \
                    self.cardsInHand[i+6].isLocked:
                continue
            if self.cardsInHand[i - 1].rank != self.cardsInHand[i].rank and \
                    self.cardsInHand[(i + 7) % len(self.cardsInHand)].rank != self.cardsInHand[i].rank and \
                    Hand(self.cardsInHand[i:i + 7]).isBomb():
                if Hand(self.cardsInHand[i:i+7]).getValue() > loValue:
                    result.append([i, i + 1, i + 2, i + 3, i + 4, i + 5, i + 6])
        if len(self.cardsInHand) >= 4:
            if self.cardsInHand[-4].rank == 15:
                result.append([-4, -3, -2, -1])
        return result

    def select(self, game, event):
        if game.players.index(self) == 0:
            startX = WIDTH / 2 - ((len(self.cardsInHand) - 1) * 20 + 105) / 2
            startY = 560
            x, y = event.pos
            if startX < x < startX + 20 * (len(self.cardsInHand) - 1) + 105:
                i = -1 if x > startX + 20 * (len(self.cardsInHand) - 1) else int((x - startX) // 20)
                if self.cardsInHand[i].isSelected:
                    if startY - 20 < y < startY + 130:
                        self.cardsInHand[i].isSelected = False
                else:
                    if startY < y < startY + 160:
                        self.cardsInHand[i].isSelected = True
        else:
            self.AISelect(game)
        self.selectedCards = [card for card in self.cardsInHand if card.isSelected]

    def lockHands(self):
        allAlmostStraightStraightFlushes = self.getAllAlmostStraightFlushes()
        allTriples = self.getAllTriples()
        hand = []
        if allAlmostStraightStraightFlushes != []:
            hand = allAlmostStraightStraightFlushes[-1] + [self.getWildCards()[0]]
        else:
            if allTriples != []:
                for i in allTriples[-1]:
                    if self.cardsInHand[i].isWildCard():
                        allTriples.pop(-1)
            if allTriples != []:
                hand = allTriples[-1] + [self.getWildCards()[0]]
        for i in hand:
            self.cardsInHand[i].isLocked = True
        self.lockedHands.append(hand)

    def AISelect(self, game):
        wildCards = self.getWildCards()
        for card in self.cardsInHand:
            card.isLocked = False
        self.lockedHands = []
        if len(wildCards) == 2:
            self.lockHands()
            self.lockHands()
        elif len(wildCards) == 1:
            self.lockHands()
        if game.lastPlayer == self:
            game.cardsOnTable = []
        if game.lastPlayer == game.players[game.players.index(self) - 1] or \
                game.lastPlayer == game.players[game.players.index(self) - 3]:
            if game.handOnTable.isSingle():
                allSingles = self.getAllSingles(game.handOnTable)
                for single in allSingles:
                    i1 = single[0]
                    if Hand([self.cardsInHand[i1]]).isValid(game):
                        self.cardsInHand[i1].isSelected = True
                        break
            if game.handOnTable.isPair():
                allPairs = self.getAllPairs(game.handOnTable)
                for pair in allPairs:
                    i1, i2 = pair[0], pair[1]
                    if Hand([self.cardsInHand[i1], self.cardsInHand[i2]]).isValid(game):
                        self.cardsInHand[i1].isSelected = True
                        self.cardsInHand[i2].isSelected = True
                        break
            if game.handOnTable.isTriple():
                allTriples = self.getAllTriples(game.handOnTable)
                for triple in allTriples:
                    i1, i2, i3 = triple[0], triple[1], triple[2]
                    if Hand([self.cardsInHand[i1], self.cardsInHand[i2], self.cardsInHand[i3]]).isValid(game):
                        for i in [i1, i2, i3]:
                            self.cardsInHand[i].isSelected = True
                        break
            if game.handOnTable.isFullHouse():
                allFullHouses = self.getAllFullHouses(game.handOnTable)
                for fullHouse in allFullHouses:
                    i1, i2, i3, i4, i5 = fullHouse[0], fullHouse[1], fullHouse[2], fullHouse[3], fullHouse[4]
                    if Hand([self.cardsInHand[i1], self.cardsInHand[i2], self.cardsInHand[i3], self.cardsInHand[i4],
                             self.cardsInHand[i5]]).isValid(game):
                        for i in [i1, i2, i3, i4, i5]:
                            self.cardsInHand[i].isSelected = True
                        break
            if game.handOnTable.isStraightNotFlush():
                allStraightNotFlushes = self.getAllStraightNotFlushes(game.handOnTable)
                for straightNotFlush in allStraightNotFlushes:
                    i1, i2, i3, i4, i5 = straightNotFlush[0], straightNotFlush[1], straightNotFlush[2], \
                                         straightNotFlush[3], straightNotFlush[4]
                    if Hand([self.cardsInHand[i1], self.cardsInHand[i2], self.cardsInHand[i3], self.cardsInHand[i4],
                             self.cardsInHand[i5]]).isValid(game):
                        for i in [i1, i2, i3, i4, i5]:
                            self.cardsInHand[i].isSelected = True
                        break
            if game.handOnTable.isTube():
                allTubes = self.getAllTubes(game.handOnTable)
                for tube in allTubes:
                    i1, i2, i3, i4, i5, i6 = tube[0], tube[1], tube[2], tube[3], tube[4], tube[5]
                    if Hand([self.cardsInHand[i1], self.cardsInHand[i2], self.cardsInHand[i3], self.cardsInHand[i4],
                             self.cardsInHand[i5], self.cardsInHand[i6]]).isValid(game):
                        for i in [i1, i2, i3, i4, i5, i6]:
                            self.cardsInHand[i].isSelected = True
                        break
            if game.handOnTable.isPlate():
                allPlates = self.getAllPlates(game.handOnTable)
                for plate in allPlates:
                    i1, i2, i3, i4, i5, i6 = plate[0], plate[1], plate[2], plate[3], plate[4], plate[5]
                    if Hand([self.cardsInHand[i1], self.cardsInHand[i2], self.cardsInHand[i3], self.cardsInHand[i4],
                             self.cardsInHand[i5], self.cardsInHand[i6]]).isValid(game):
                        for i in [i1, i2, i3, i4, i5, i6]:
                            self.cardsInHand[i].isSelected = True
                        break
            if game.handOnTable.isBomb() or game.handOnTable.isStraightFlush():
                allBombs = self.getAllBombs(game.handOnTable)
                for bomb in allBombs:
                    bombHand = Hand([self.cardsInHand[i] for i in bomb])
                    if bombHand.isValid(game):
                        for i in bomb:
                            self.cardsInHand[i].isSelected = True
                        break
            self.selectedCards = [card for card in self.cardsInHand if card.isSelected]
            if self.selectedCards == []:
                if game.lastPlayer == game.players[game.players.index(self) - 3] or \
                        (game.lastPlayer == game.players[game.players.index(self) - 1] and len(game.lastPlayer.cardsInHand) < 10):
                    allBombs = self.getAllBombs(game.handOnTable)
                    if allBombs != []:
                        for bomb in allBombs:
                            bombHand = Hand([self.cardsInHand[i] for i in bomb])
                            if bombHand.isValid(game):
                                for i in bomb:
                                    self.cardsInHand[i].isSelected = True
                                break
                    else:
                        if len(self.lockedHands) == 1:
                            if len(self.lockedHands[0]) == 5:
                                if (game.handOnTable.getValue() > 140 or len(game.lastPlayer.cardsInHand) < 10) and \
                                        Hand([self.cardsInHand[i] for i in self.lockedHands[0]]).isValid(game):
                                    for i in self.lockedHands[0]:
                                        self.cardsInHand[i].isSelected = True
                            else:
                                if Hand([self.cardsInHand[i] for i in self.lockedHands[0]]).isValid(game):
                                    for i in self.lockedHands[0]:
                                        self.cardsInHand[i].isSelected = True
                        if len(self.lockedHands) == 2:
                            if len(self.lockedHands[1]) == 5:
                                if game.handOnTable.getValue() > 140 and Hand([self.cardsInHand[i] for i in self.lockedHands[0]]).isValid(game):
                                    for i in self.lockedHands[0]:
                                        self.cardsInHand[i].isSelected = True
                            else:
                                if Hand([self.cardsInHand[i] for i in self.lockedHands[0]]).isValid(game):
                                    for i in self.lockedHands[0]:
                                        self.cardsInHand[i].isSelected = True
            else:
                self.selectedCards = []
        if game.lastPlayer == game.players[game.players.index(self) - 2]:
            if len(self.cardsInHand) == 1:
                if Hand(self.cardsInHand).isValid(game):
                    self.cardsInHand[0].isSelected = True
            self.selectedCards = []
        if game.cardsOnTable == []:
            weights = dict()
            allSingles = self.getAllSingles()
            if allSingles != []:
                weights[0] = Hand([self.cardsInHand[i] for i in allSingles[0]]).getValue() - 0
            allPairs = self.getAllPairs()
            if allPairs != []:
                weights[1] = Hand([self.cardsInHand[i] for i in allPairs[0]]).getValue() - 20
            allTriples = self.getAllTriples()
            if allTriples != []:
                weights[2] = Hand([self.cardsInHand[i] for i in allTriples[0]]).getValue() - 40
            allFullHouses = self.getAllFullHouses()
            if allFullHouses != []:
                weights[3] = Hand([self.cardsInHand[i] for i in allFullHouses[0]]).getValue() - 60 - 2
            allStraightNotFlushes = self.getAllStraightNotFlushes()
            if allStraightNotFlushes != []:
                weights[4] = Hand([self.cardsInHand[i] for i in allStraightNotFlushes[0]]).getValue() - 80 - 3
            allTubes = self.getAllTubes()
            if allTubes != []:
                weights[5] = Hand([self.cardsInHand[i] for i in allTubes[0]]).getValue() - 100 - 3
            allPlates = self.getAllPlates()
            if allPlates != []:
                weights[6] = Hand([self.cardsInHand[i] for i in allPlates[0]]).getValue() - 120 - 3
            handsLeft = [allSingles, allPairs, allTriples, allFullHouses, allStraightNotFlushes, allTubes, allPlates]
            if weights == {}:
                allBombs = self.getAllBombs()
                for bomb in allBombs:
                    for i in bomb:
                        self.cardsInHand[i].isSelected = True
                    break
            else:
                weightList = [weights[i] for i in weights]
                weightKeys = [key for key in weights]
                minWeight = min(weightList)
                hand = handsLeft[weightKeys[weightList.index(minWeight)]]
                for i in hand[0]:
                    self.cardsInHand[i].isSelected = True



class Hand(object):
    def __init__(self, cards):
        arrange(cards)
        self.cards = cards

    def __repr__(self):
        return str(self.cards)

    def isSingle(self):
        return len(self.cards) == 1

    def isPair(self):
        return len(self.cards) == 2 and (self.cards[0].rank == self.cards[1].rank or self.cards[1].isWildCard())

    def isTriple(self):
        return len(self.cards) == 3 and (self.cards[0].rank == self.cards[1].rank == self.cards[2].rank or
                                         (self.cards[0] == self.cards[1] and self.cards[2].isWildCard()) or
                                         (self.cards[1].isWildCard() and self.cards[2].isWildCard()))

    def isStraight(self):
        if len(self.cards) == 5:
            c1, c2, c3, c4, c5 = self.cards
            d1, d2, d3, d4, d5 = sorted([c1, c2, c3, c4, c5], key=lambda x: x.rank)
            return (c2.rank == c1.rank+1 and c3.rank == c2.rank+1 and c4.rank == c3.rank+1 and c5.rank == c4.rank+1
                   and c5.rank < 15) or \
                   (d2.rank == d1.rank+1 and d3.rank == d2.rank+1 and d4.rank == d3.rank+1 and d5.rank == d4.rank+1
                   and d5.rank < 15) or \
                   (c5.isWildCard() and ((c2.rank == c1.rank+1 and c3.rank == c2.rank+1 and c4.rank == c3.rank+1 and c4.rank < 14)
                       or (c2.rank == c1.rank+1 and c3.rank == c2.rank+1 and c4.rank == c3.rank+2)
                       or (c2.rank == c1.rank+1 and c3.rank == c2.rank+2 and c4.rank == c3.rank+1)
                       or (c2.rank == c1.rank+2 and c3.rank == c2.rank+1 and c4.rank == c3.rank+1)
                       or (c2.rank == c1.rank+1 and c3.rank == c2.rank+1 and c4.rank == c3.rank+1 and c1.rank >= 2)))
        return False

    def isFullHouse(self):
        if len(self.cards) == 5:
            c1, c2, c3, c4, c5 = self.cards
            return (Hand([c1, c2]).isPair() and Hand([c3, c4, c5]).isTriple() and c2.rank != c3.rank) or \
                   (Hand([c1, c2, c3]).isTriple() and Hand([c4, c5]).isPair() and c3.rank != c4.rank) or \
                   (Hand([c1, c2]).isPair() and Hand([c3, c4]).isPair() and c2.rank != c3.rank and c5.isWildCard()) or \
                   (Hand([c1, c2, c3]).isTriple() and c3.rank != c4.rank and c5.isWildCard()) or \
                   (Hand([c2, c3, c4]).isTriple() and c1.rank != c2.rank and c5.isWildCard())
        return False

    def isFlush(self):
        if len(self.cards) == 5:
            c1, c2, c3, c4, c5 = self.cards
            return len({c1.suit, c2.suit, c3.suit, c4.suit, c5.suit}) == 1 or \
                   (len({c1.suit, c2.suit, c3.suit, c4.suit}) == 1 and c5.isWildCard()) or \
                   (len({c1.suit, c2.suit, c3.suit}) == 1 and c4.isWildCard() and c5.isWildCard())
        return False

    def isStraightNotFlush(self):
        return self.isStraight() and not self.isFlush()

    def isTube(self):
        if len(self.cards) == 6:
            c1, c2, c3, c4, c5, c6 = self.cards
            if c6.isWildCard():
                return (c1.rank == c2.rank and c3.rank == c4.rank and c3.rank == c2.rank+1 and c5.rank == c4.rank+1 and c5.rank < 15) or \
                       (c1.rank == c2.rank and c4.rank == c5.rank and c3.rank == c2.rank+1 and c4.rank == c3.rank+1 and c5.rank < 15) or \
                       (c2.rank == c3.rank and c4.rank == c5.rank and c2.rank == c1.rank+1 and c4.rank == c3.rank+1 and c6.rank < 15)
            else:
                return c1.rank == c2.rank and c3.rank == c4.rank and c5.rank == c6.rank and c3.rank == c2.rank+1 and \
                       c5.rank == c4.rank+1 and c6.rank < 15
        return False

    def isPlate(self):
        if len(self.cards) == 6:
            c1, c2, c3, c4, c5, c6 = self.cards
            return (c1.rank == c2.rank == c3.rank and c4.rank == c5.rank == c6.rank and c4.rank == c3.rank+1 and \
                   c6.rank < 15) or \
                   (c6.isWildCard() and Hand([c1, c2, c3, c4, c5]).isFullHouse())
        return False

    def isBomb(self):
        if len(self.cards) == 4:
            c1, c2, c3, c4 = self.cards
            return len(set(card.rank for card in self.cards)) == 1 or (c4.isWildCard() and Hand([c1, c2, c3]).isTriple())
        if len(self.cards) == 5:
            c1, c2, c3, c4, c5 = self.cards
            return len(set(card.rank for card in self.cards)) == 1 or (c5.isWildCard() and Hand([c1, c2, c3, c4]).isBomb())
        if len(self.cards) == 6:
            c1, c2, c3, c4, c5, c6 = self.cards
            return len(set(card.rank for card in self.cards)) == 1 or (c6.isWildCard() and Hand([c1, c2, c3, c4, c5]).isBomb())
        if len(self.cards) == 7:
            c1, c2, c3, c4, c5, c6, c7 = self.cards
            return len(set(card.rank for card in self.cards)) == 1 or (c7.isWildCard() and Hand([c1, c2, c3, c4, c5, c6]).isBomb())
        if len(self.cards) == 8:
            c1, c2, c3, c4, c5, c6, c7, c8 = self.cards
            return len(set(card.rank for card in self.cards)) == 1 or (c8.isWildCard() and Hand([c1, c2, c3, c4, c5, c6, c7]).isBomb())
        return False

    def isStraightFlush(self):
        return self.isStraight() and self.isFlush()

    def isJokerBomb(self):
        return len(self.cards) == 4 and self.cards[0].rank == 15

    def isValid(self, game):
        if game.cardsOnTable != []:
            handOnTable = Hand(game.cardsOnTable)
            if self.cards == []:
                return False
            if handOnTable.isSingle():
                return (self.isSingle() and self.getValue() > handOnTable.getValue()) or self.getValue() >= 140
            elif handOnTable.isPair():
                return (self.isPair() and self.getValue() > handOnTable.getValue()) or self.getValue() >= 140
            elif handOnTable.isTriple():
                return (self.isTriple() and self.getValue() > handOnTable.getValue()) or self.getValue() >= 140
            elif handOnTable.isFullHouse():
                return (self.isFullHouse() and self.getValue() > handOnTable.getValue()) or self.getValue() >= 140
            elif handOnTable.isStraightNotFlush():
                return (self.isStraightNotFlush() and self.getValue() > handOnTable.getValue()) or self.getValue() >= 140
            elif handOnTable.isTube():
                return (self.isTube() and self.getValue() > handOnTable.getValue()) or self.getValue() >= 140
            elif handOnTable.isPlate():
                return (self.isPlate() and self.getValue() > handOnTable.getValue()) or self.getValue() >= 140
            else:
                return self.getValue() > handOnTable.getValue()
        else:
            return self.isSingle() or self.isPair() or self.isTriple() or self.isFullHouse() or self.isStraight() or \
                   self.isTube() or self.isPlate() or self.isBomb() or self.isJokerBomb()

    def getValue(self):
        if self.isSingle():
            return self.cards[0].realRank
        elif self.isPair():
            return 20 + self.cards[0].realRank
        elif self.isTriple():
            return 40 + self.cards[0].realRank
        elif self.isFullHouse():
            c1, c2, c3, c4, c5 = self.cards[0], self.cards[1], self.cards[2], self.cards[3], self.cards[4]
            if c5.isWildCard():
                if Hand([c1, c2, c3]).isTriple():
                    return 60 + c1.realRank
                else:
                    return 60 + max([c1.rank, c2.rank, c3.rank, c4.rank])
            else:
                return 60 + self.cards[0].realRank if self.cards[1].realRank == self.cards[2].realRank else 60 + self.cards[3].realRank
        elif self.isStraightNotFlush():
            return 80 + self.cards[0].realRank
        elif self.isTube():
            return 100 + self.cards[0].realRank
        elif self.isPlate():
            return 120 + self.cards[0].realRank
        elif self.isBomb():
            if len(self.cards) <= 5:
                return 140 + (len(self.cards) - 4) * 20 + self.cards[0].realRank
            else:
                return 200 + (len(self.cards) - 6) * 20 + self.cards[0].realRank
        elif self.isStraightFlush():
            return 180 + self.cards[0].realRank
        elif self.isJokerBomb():
            return 300
        else:
            return -1



