import pygame
import sys
from pygame.locals import *
import pygame_menu

pygame.init()           # intialize the pygame

# All variables of DISPLAY SET
P1name = "John Doe"     # human Default Name
P2name = "Bixby"        # Samsung intelligence Assistant Name

play_music = False
play_sound = True

T_MAX = 60
T_MIN = 0.1

white = (255, 255, 255)
black = (0, 0, 0)
red = (175, 0, 0)
green = (0, 120, 0)

PLAYER1 = 1
PLAYER2 = 2

fp = './sources/'

# All images are imports
img_board = pygame.image.load(fp+'pics/board.png')
img_cp1 = pygame.image.load(fp+'pics/cp_k_29.png')
img_cp2 = pygame.image.load(fp+'pics/cp_w_29.png')
img_panel = pygame.image.load(fp+'pics/panel.png')
img_icon = pygame.image.load(fp+'pics/catsmall.png')
img_cp3 = pygame.image.load(fp+'pics/cp_k_29 - Copy.png')
img_cp4 = pygame.image.load(fp+'pics/cp_W_29 - Copy.png')
img_cp5 = pygame.image.load(fp+'pics/cp_k_29_Green.png')
img_cp6 = pygame.image.load(fp+'pics/cp_W_29_Green.png')
pygame.display.set_icon(img_icon)

fps = 30

# Game Screen width and height
dispWidth = 900
dispHeight = 645

lineWidth = 1
lineWidth3 = 4
boxWidth = 40

marginWidth = 24

N = 15

# Set the Display
# 1*15 + 40 * (15-1) = 575
boardWidth = lineWidth*N+boxWidth*(N-1)

# (645-575)/2 = 35
starty = (dispHeight-boardWidth)/2
#35=0
startx = starty

# 2*24+575+48 = 671
infox = 2*marginWidth+boardWidth+48
# 35 + 24 + (1+41) * 1 =  101
infoy1 = startx+marginWidth+(lineWidth+boxWidth)*1
# 35 + (1+41) * 4 = 269
infoy2 = infoy1+(lineWidth+boxWidth)*4
# (1+40) * 4 = 164
infoWidth = (lineWidth+boxWidth)*4
# (1+40) * 3 = 123
infoHeight = (lineWidth+boxWidth)*3

cpSize = 29

plyrInfo1 = {'score': 0, 'time': 0}
plyrInfo2 = {'score': 0, 'time': 0}

tcnt=59

# check the horizontal vise players moves
#player=computer
def getHorizontals(board, player):
    # print('getHorizontals'+str(player))
    horizontals = ['' for i in range(15)]       # list [ 15[0,1,0,...] ]
    for i in range(15):
        for j in range(15):
            if board[i][j] == 3 - player:
                horizontals[i] += 'x'           # (x - human)
            elif board[i][j] == 0:
                horizontals[i] += 'o'           # (o - open)
            elif board[i][j] == player:
                horizontals[i] += '*'           # (* - computer)
    return horizontals
# check the Vertical vise players moves
def getVerticals(board, player):
   # print('getVerticals')
    verticals = ['' for i in range(15)]
    for i in range(15):
        for j in range(15):
            if board[i][j] == 3 - player:
                verticals[j] += 'x'
            elif board[i][j] == 0:
                verticals[j] += 'o'
            elif board[i][j] == player:
                verticals[j] += '*'
    return verticals

def getLeftDiags(board, player):
    # print('getLeftDiags')
    diags = ['' for i in range(29)]
    for i in range(15):
        if board[i][i] == 3 - player:
            diags[0] += 'x'
        elif board[i][i] == 0:
            diags[0] += 'o'
        elif board[i][i] == player:
            diags[0] += '*'
    for i in range(10):  # below the diagonal scan
        for j in range(15):
            if (i + 1 + j) > 14 or board[i + 1 + j][j] == 3 - player:
                diags[i + 1] += 'x'
            elif board[i + 1 + j][j] == 0:
                diags[i + 1] += 'o'
            elif board[i + 1 + j][j] == player:
                diags[i + 1] += '*'
    for i in range(10): #above the diagonal scan
        for j in range(15):
            if (i + 1 + j) > 14 or board[j][i + 1 + j] == 3 - player:
                diags[i + 11] += 'x'
            elif board[j][i + 1 + j] == 0:
                diags[i + 11] += 'o'
            elif board[j][i + 1 + j] == player:
                diags[i + 11] += '*'

    return diags

def getRightDiags(board, player):
    # print('getRightDiags')
    diags = ['' for i in range(29)]
    for i in range(15):
        if board[i][14 - i] == 3 - player:
            diags[0] += 'x'
        elif board[i][14 - i] == 0:
            diags[0] += 'o'
        elif board[i][14 - i] == player:
            diags[0] += '*'
    for i in range(10):
        for j in range(15):
            if (10 - i + j) > 14 or board[10 - i + j][14 - j] == 3 - player:
                diags[i + 1] += 'x'
            elif board[10 - i + j][14 - j] == 0:
                diags[i + 1] += 'o'
            elif board[10 - i + j][14 - j] == player:
                diags[i + 1] += '*'
    for i in range(10):
        for j in range(15):
            if (13 - j) - i < 0 or board[j][(13 - j) - i] == 3 - player:
                diags[i + 11] += 'x'
            elif board[j][(13 - j) - i] == 0:
                diags[i + 11] += 'o'
            elif board[j][(13 - j) - i] == player:
                diags[i + 11] += '*'

    return diags

def eval(board, player):
    # print('eval')
    newBoard = board.copy()
    hori = getHorizontals(newBoard, player)
    vert = getVerticals(newBoard, player)
    leftD = getLeftDiags(newBoard, player)
    rightD = getRightDiags(newBoard, player)
    allLines = hori + vert + leftD + rightD
    
    allLines = [line for line in allLines if line.count('*') > 1]

    score = 0
    # print('evalLine')
    for line in allLines:
        score += evalLine(line)
    return score

def evalLine(line):
    # * for piece placed, x for blocked square, o for open square
    # print('evalline')
    five = '*****'
    # print(five)

    open_four = 'o****o'
    # print(open_four)

    closed_four1 = 'x****o'
    # print(closed_four1)
    closed_four2 = 'o****x'
    # print(closed_four2)
    closed_four3 = '*o***'
    # print(closed_four3)
    closed_four4 = '***o*'
    # print(closed_four4)
    closed_four5 = '**o**'
    # print(closed_four5)

    open_three1 = 'o***oo'
    # print(open_three1)
    open_three2 = 'oo***o'
    # print(open_three2)
    open_three3 = 'o*o**o'
    # print(open_three3)
    open_three4 = 'o**o*o'
    # print(open_three4)

    closed_three1 = 'x***oo'
    # print(closed_three1)
    closed_three2 = 'oo***x'
    # print(closed_three2)
    closed_three3 = 'xo***ox'
    # print(closed_three3)
    closed_three4 = 'o*o**x'
    # print(closed_three4)
    closed_three5 = 'x*o**o'
    # print(closed_three5)
    closed_three6 = 'x**o*o'
    # print(closed_three6)
    closed_three6 = 'o**o*x'
    # print(closed_three6+'2')

    open_two1 = 'o**o'
    # print(open_two1)
    open_two2 = 'o*o*o'
    # print(open_two2)
    open_two3 = 'o*oo*o'
    # print(open_two3)

    closed_two1 = 'x**o'
    # print(closed_two1)
    closed_two2 = 'x*o*o'
    # print(closed_two2)
    closed_two3 = 'o*o*x'
    # print(closed_two3)
    closed_two4 = 'o**x'
    # print(closed_two4)

    five_count = line.count(five)
    # print(five_count)
    four_count = line.count(open_four)
    # print(four_count)
    cfour_count = line.count(closed_four1) + line.count(closed_four2) + line.count(
        closed_four3) + line.count(closed_four4) + line.count(closed_four5)
    # print(cfour_count)
    three_count = line.count(open_three1) + line.count(open_three2) + \
        line.count(open_three3) + line.count(open_three4)
    # print(three_count)
    cthree_count = line.count(closed_three1) + line.count(closed_three2) + line.count(
        closed_three3) + line.count(closed_three4) + line.count(closed_three5) + line.count(closed_three6)
    # print(cthree_count)
    two_count = line.count(open_two1) + \
        line.count(open_two2) + line.count(open_two3)
    # print(two_count)
    ctwo_count = line.count(closed_two1) + line.count(closed_two2) + \
        line.count(closed_two3) + line.count(closed_two4)
    # print(ctwo_count)

    # return the value of posibility of winning the game...
    if five_count:
        return 1000000
    if four_count:
        return 99999
    if cfour_count + three_count > 1:
        return 9000
    score = 200 * (cfour_count + three_count) + 10 * \
        (cthree_count + two_count) + 5 * (ctwo_count)

    # print(score)
    return score

# count the all moves, which is the player could be moved.

def getMoves(board):
    moves = []
    for i in range(15):
        for j in range(15):
            if board[i][j] == 0:
                score = 7 - max(abs(i - 7), abs(j - 7))
                moves.append((score, i, j))
    moves.sort()
    moves.reverse()
    return moves

class minimaxAgentHard():
    #global justcnt
    #justcnt=0
    def __init__(self):
        self.board = [[0 for j in range(15)] for i in range(15)]
        self.maxdepth = 4

    def minimax(self, currPlayer, depth=4):
        self.maxdepth = depth
        self.bestmove = None
        score = self.alphabetaHard(
            currPlayer, depth, float('-inf'), float('inf'))
        row, col = self.bestmove
        #print(score)
        return score, row, col

    def alphabetaHard(self, currPlayer, depth, alpha, beta):
        #global justcnt
        #justcnt+=1
        #print(justcnt)
        if depth <= 0:
            return eval(self.board, currPlayer) - eval(self.board, 3 - currPlayer)

        #score = eval(self.board, currPlayer) - eval(self.board, 3 - currPlayer)
        moves = getMoves(self.board)
        bestmove = None

        for score, row, col in moves:

            self.board[row][col] = currPlayer
            nextPlayer = 3 - currPlayer
            score = -self.alphabetaHard(nextPlayer, depth - 1, -beta, -alpha)
            self.board[row][col] = 0

            if score > alpha:
                alpha = score
                bestmove = (row, col)
                if alpha >= beta:
                    break

        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove

        return alpha

class minimaxAgentEasy():
    #global justcnt
    #justcnt=0
    def __init__(self):
        self.board = [[0 for j in range(15)] for i in range(15)]
        self.maxdepth = 4

    def minimax(self, currPlayer, depth=4):
        self.maxdepth = depth
        self.bestmove = None
        score = self.alphabetaEasy(
            currPlayer, depth, float('-inf'), float('inf'))
        row, col = self.bestmove
        #print(score)
        return score, row, col

    def alphabetaEasy(self, currPlayer, depth, alpha, beta):
        #global justcnt
        #justcnt+=1
        #print(justcnt)

        if depth <= 0:
            return eval(self.board, currPlayer) - eval(self.board, 3 - currPlayer)

        #score = eval(self.board, currPlayer) - eval(self.board, 3 - currPlayer)
        moves = getMoves(self.board)
        bestmove = None

        for score, row, col in moves:
            self.board[row][col] = currPlayer
            nextPlayer = 3 - currPlayer
            score = -self.alphabetaEasy(nextPlayer, depth - 2, -beta, -alpha)
            self.board[row][col] = 0
            if score > alpha:
                alpha = score
                bestmove = (row, col)
            if alpha >= beta:
                break

        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove

        return alpha

def darkenBackground():
    pixels = pygame.PixelArray(setDisplay)
    for x in range(dispWidth):
        if x >= (dispWidth-infoWidth-90):
            for y in range(dispHeight):
                pixels[x][y] = pygame.Color('dark red')


def updateInfo(info1, info2, plyr):

    setDisplay.blit(img_panel, (infox, 0))
    turn_name1 = "Now Turn Is : "
    turn = pygame.font.SysFont('Time New Roman', 24, bold=True)
    textSurf, textRect = makeTextObjs(turn_name1, turn, white)
    textRect.center = (int(infox+90), int(infoy1-65))
    setDisplay.blit(textSurf, textRect)

    if plyr == PLAYER1:
        pygame.draw.rect(setDisplay, black, (infox+2, infoy1+2,
                         infoWidth-1, infoHeight-1), lineWidth3)
        turn_name = P1name+" ( "+P1move+" ) "
    else:
        pygame.draw.rect(setDisplay, black, (infox+2, infoy2+2,
                         infoWidth-1, infoHeight-1), lineWidth3)
        turn_name = P2name+" ( "+P2move+" ) "

    textSurf, textRect = makeTextObjs(turn_name, turn, white)
    textRect.center = (int(infox+90), int(infoy1-30))
    setDisplay.blit(textSurf, textRect)

    #ttlText = pygame.font.SysFont('Calibri', 24)
    scoreText = pygame.font.SysFont('Calibri', 20, bold=True)
    #timeText = pygame.font.SysFont('Calibri', 20)

    textttl = P1name
    textsc = 'Score: %d' % info1['score']
    texttm = 'Time: %.2f s' % info1['time']
    textSurf, textRect = makeTextObjs(textttl, scoreText, red)
    textRect.center = (int(infox+infoWidth/2), int(infoy1+infoHeight/2)-30)
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(textsc, scoreText, green)
    textRect.center = (int(infox+infoWidth/2), int(infoy1+infoHeight/2))
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(texttm, scoreText, black)
    textRect.center = (int(infox+infoWidth/2), int(infoy1+infoHeight/2)+26)
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(P1move, scoreText, red)
    textRect.center = (int(infox+infoWidth/2), int(infoy1+infoHeight/2)+50)
    setDisplay.blit(textSurf, textRect)

    textttl = P2name
    textsc = 'Score: %d' % info2['score']
    texttm = 'Time: %.2f s' % info2['time']
    textSurf, textRect = makeTextObjs(textttl, scoreText, red)
    textRect.center = (int(infox+infoWidth/2), int(infoy2+infoHeight/2)-30)
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(textsc, scoreText, green)
    textRect.center = (int(infox+infoWidth/2), int(infoy2+infoHeight/2))
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(texttm, scoreText, black)
    textRect.center = (int(infox+infoWidth/2), int(infoy2+infoHeight/2)+26)
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(P2move, scoreText, red)
    textRect.center = (int(infox+infoWidth/2), int(infoy2+infoHeight/2)+50)
    setDisplay.blit(textSurf, textRect)

    moves_Bstr = "Black Move : "+str(Bcount)
    textSurf, textRect = makeTextObjs(moves_Bstr, turn, white)
    textRect.center = (int(infox+80), int(infoy2+175))
    setDisplay.blit(textSurf, textRect)
    moves_Wstr = "White Move : "+str(Wcount)
    textSurf, textRect = makeTextObjs(moves_Wstr, turn, white)
    textRect.center = (int(infox+80), int(infoy2+200))
    setDisplay.blit(textSurf, textRect)

    mode_str = "Mode : "+mode
    textSurf, textRect = makeTextObjs(mode_str, turn, white)
    textRect.center = (int(infox+80), int(infoy2+250))
    setDisplay.blit(textSurf, textRect)

    turn = pygame.font.SysFont('Time New Roman', 24, bold=True)
    timer = "Timer : "+str(tcnt)
    textSurf, textRect = makeTextObjs(timer, turn, black)
    textRect.center = (int(infox+80), int(590))
    setDisplay.blit(textSurf, textRect)
    #print(timer)

    pygame.display.update()


def whatNext():
    for event in pygame.event.get([KEYDOWN, KEYUP, QUIT]):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            continue
        return event.key
    return None


def makeTextObjs(text, font, tcolor):
    textSurface = font.render(text, True, tcolor)
    return textSurface, textSurface.get_rect()


def msgSurface(plyr, textColor,msg):

    darkenBackground()
    text1=''
    text=''
    smallText = pygame.font.SysFont('Calibri', 20, bold=True)
    largeText = pygame.font.SysFont('Calibri', 21, bold=True)

    if plyr == PLAYER1 and PLTYP1 == 'human':
        if msg:
            text1 = 'Maximum time exceeded!'
            text=P1name+' Wins!'
        else:
            text = P1name+' Wins!'
    elif plyr == PLAYER1 and PLTYP1 == 'computer':
        if msg:
            text1 = 'Maximum time exceeded!'
            text=P2name+' Wins!'
        else:
            text = P2name+' Wins!'
    elif plyr == PLAYER2 and PLTYP2 == 'human':
        if msg:
            text1 = 'Maximum time exceeded!'
            text=P1name+' Wins!'
        else:
            text = P1name+' Wins!'
    elif plyr == PLAYER2 and PLTYP2 == 'computer':
        if msg:
            text1 = 'Maximum time exceeded!'
            text=P2name+' Wins!'
        else:
            text = P2name+' Wins!'

    if msg:
        print(text1)
        titleTextSurf, titleTextRect = makeTextObjs(text1, largeText, white)
        titleTextRect.center = (int(dispWidth-infoWidth+35),
                            int((dispHeight-100+70)/2))
        setDisplay.blit(titleTextSurf, titleTextRect)

    titleTextSurf, titleTextRect = makeTextObjs(text, largeText, white)
    titleTextRect.center = (int(dispWidth-infoWidth+35),
                            int((dispHeight-100)/2))
    setDisplay.blit(titleTextSurf, titleTextRect)

    typTextSurf, typTextRect = makeTextObjs(
        'Press any key to continue...', smallText, white)
    typTextRect.center = (int(dispWidth-infoWidth+35),
                          int((dispHeight-100)/2)+120)
    setDisplay.blit(typTextSurf, typTextRect)
    pygame.display.update()
    fpsTime.tick()

    while whatNext() == None:
        for event in pygame.event.get([QUIT]):
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsTime.tick()

    main(False)


def runGame():

    theWinner = 0
    currPlayer = PLAYER1

    setDisplay.blit(img_board, (0, 0))                  # set the board image
    updateInfo(plyrInfo1, plyrInfo2, currPlayer)

    pygame.display.update()                         # update the screen

    chessMat = []
    for dummy_iy in range(N):
        chessMat.append([0 for dummy_idx in range(N)])

    # AI
    srchr1.board = chessMat
    srchr2.board = chessMat
    #####
    cnt = 0
    while True:  # main game loop
        global Bcount, Wcount
        Bcount = 0
        Wcount = 0
        row, col = 0, 0
        plyrInfo1['time']=0
        plyrInfo2['time']=0
        while theWinner == 0:
            cnt += 1
            for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # players play in turn
            t_start = pygame.time.get_ticks()
            #print(t_start)
            if currPlayer == PLAYER1 and PLTYP1 == 'human':
                prow=row
                pcol=col
                row, col = getPiecePos(currPlayer)
                while not isValid((row, col), chessMat):
                    row, col = getPiecePos(currPlayer)
                if cnt != 1:
                    drawPiece((prow, pcol), pervplayer)
                Bcount = Bcount+1

            elif currPlayer == PLAYER1 and PLTYP1 == 'computer':
                prow=row
                pcol=col
                score, row, col = srchr1.minimax(1, 2)
                if not isValid((row, col), chessMat):
                    row, col = sysIndexGen(chessMat, currPlayer)
                if cnt != 1:
                    drawPiece((prow, pcol), pervplayer)
                Bcount = Bcount+1
                

            elif currPlayer == PLAYER2 and PLTYP2 == 'human':
                prow=row
                pcol=col
                row, col = getPiecePos(currPlayer)
                while not isValid((row, col), chessMat):
                    row, col = getPiecePos(currPlayer)
                if cnt != 1:
                    drawPiece((prow, pcol), pervplayer)
                Wcount = Wcount+1
                

            elif currPlayer == PLAYER2 and PLTYP2 == 'computer':
                prow=row
                pcol=col
                score, row, col = srchr1.minimax(1, 2)
                if not isValid((row, col), chessMat):
                    row, col = sysIndexGen(chessMat, currPlayer)
                if cnt != 1:
                    drawPiece((prow, pcol), pervplayer)
                Wcount = Wcount+1
                
            t_end = pygame.time.get_ticks()
            #print(t_end)
            # add new piece
            chessMat[row][col] = currPlayer
            theWinner = checkIfWins(chessMat, currPlayer)
            if theWinner == 0:
                drawPieceGreen((row, col), currPlayer)
                pervplayer = currPlayer
            elif theWinner != 0:
                drawPieceback((row, col), currPlayer)

            # if play_sound:
            #    pygame.mixer.pre_init(44100)
            #    cpSound = pygame.mixer.Sound(fp+'music/Snd_click.ogg')
            #    cpSound.set_volume(12)
            #    cpSound.play()

            t_call = t_end - t_start
            t_rem = T_MIN*1000 - t_call

            if t_rem > 0:
                pygame.time.wait(int(t_rem))
            elif t_call > T_MAX*1000:
                print('Maximum time exceeded!')
                if currPlayer == PLAYER1:
                    theWinner = PLAYER2
                else:
                    theWinner = PLAYER1

            if currPlayer == PLAYER1 and PLTYP1 == 'human':
                plyrInfo1['time'] += t_call/1000.0
                currPlayer = PLAYER2
            elif currPlayer == PLAYER1 and PLTYP1 == 'computer':
                plyrInfo2['time'] += t_call/1000.0
                currPlayer = PLAYER2
            elif currPlayer == PLAYER2 and PLTYP2 == 'computer':
                plyrInfo2['time'] += t_call/1000.0
                currPlayer = PLAYER1
            elif currPlayer == PLAYER2 and PLTYP2 == 'human':
                plyrInfo1['time'] += t_call/1000.0
                currPlayer = PLAYER1

            updateInfo(plyrInfo1, plyrInfo2, currPlayer)

            ##            print 'data1', data1 ##
            ##            print 'data2', data2 ##
            ##            print '' ##

            fpsTime.tick(fps)
            #pygame.display.update()

        print('Winner: Player', theWinner)
        printMat(chessMat)
        if theWinner == PLAYER1 and PLTYP1 == 'human':
            plyrInfo1['score'] += 1
        elif theWinner == PLAYER1 and PLTYP1 == 'computer':
            plyrInfo2['score'] += 1
        elif theWinner == PLAYER2 and PLTYP2 == 'human':
            plyrInfo1['score'] += 1
        elif theWinner == PLAYER2 and PLTYP2 == 'computer':
            plyrInfo2['score'] += 1

        msgSurface(theWinner, green,False)


def printMat(mat):
    for bdraw in mat:
        print(bdraw)
    print('=' * 45)


def drawPieceback(indice, player):
    x = startx+lineWidth/2+indice[1]*(lineWidth+boxWidth)-(cpSize-1)/2
    y = starty+lineWidth/2+indice[0]*(lineWidth+boxWidth)-(cpSize-1)/2

    if player == PLAYER1:
        setDisplay.blit(img_cp3, (x, y))
    else:
        setDisplay.blit(img_cp4, (x, y))


def drawPiece(indice, player):
    x = startx+lineWidth/2+indice[1]*(lineWidth+boxWidth)-(cpSize-1)/2
    y = starty+lineWidth/2+indice[0]*(lineWidth+boxWidth)-(cpSize-1)/2

    if player == PLAYER1:
        setDisplay.blit(img_cp1, (x, y))
    else:
        setDisplay.blit(img_cp2, (x, y))


def drawPieceGreen(indice, player):
    x = startx+lineWidth/2+indice[1]*(lineWidth+boxWidth)-(cpSize-1)/2
    y = starty+lineWidth/2+indice[0]*(lineWidth+boxWidth)-(cpSize-1)/2
    #print(x,y)
    if player == PLAYER1:
        setDisplay.blit(img_cp5, (x, y))
    else:
        setDisplay.blit(img_cp6, (x, y))


def getPiecePos(currPlayer):
    global tcnt
    tcnt=59
    pygame.time.set_timer(pygame.USEREVENT, 1000)#Set timer 
    while True:
        #print('a')
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                row = int(round((y-starty-lineWidth/2.0)/(lineWidth+boxWidth)))
                col = int(round((x-startx-lineWidth/2.0)/(lineWidth+boxWidth)))

                return row, col
            elif event.type == pygame.USEREVENT:
                if tcnt > 0:
                    tcnt -= 1
                    updateInfo(plyrInfo1, plyrInfo2, currPlayer)
                else:
                    msgSurface(3-currPlayer,'green',True)


def isValid(indice, mat):

    newRow = indice[0]
    newCol = indice[1]

    if newRow < 0 or newRow > N-1:
        return False
    elif newCol < 0 or newCol > N-1:
        return False

    return mat[newRow][newCol] == 0


def sysIndexGen(mat, player):
    for row in range(N):
        for col in range(N):
            if mat[row][col] == 0:
                return row, col


def checkIfWins(board, player):
    directions = ((1, 0), (0, 1), (1, 1), (1, -1))
    for i in range(15):
        for j in range(15):
            if board[i][j] != player:
                continue
            for dir in directions:
                c, r = i, j
                count = 0
                for k in range(5):
                    if c > 14 or c < 0 or r > 14 or r < 0 or board[c][r] != player:
                        break
                    c += dir[0]
                    r += dir[1]
                    count += 1
                c, r = i, j
                c -= dir[0]
                r -= dir[1]
                if count == 5:
                    for k in range(5):
                        c += dir[0]
                        r += dir[1]
                        drawPieceback((c, r), player)
                    return player
    return 0


global fpsTime
global cpSound
global setDisplay

setDisplay = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption('Go Moku')

if play_music:
    pygame.mixer.pre_init(44100)
    bgSound = pygame.mixer.Sound(fp+'music/BackgroundMusic1.mp3')
    bgSound.set_volume(3)
    bgSound.play(-1)

fpsTime = pygame.time.Clock()


def main(run):
    global srchr1, srchr2, P1move, P2move, mode, Wcount, Bcount, PLTYP1, PLTYP2
    srchr1 = minimaxAgentEasy()
    srchr2 = minimaxAgentEasy()

    PLTYP1 = 'human'
    PLTYP2 = 'computer'

    P1move = "BLACK"
    P2move = "WHITE"

    mode = "EASY"
    Wcount = 0
    Bcount = 0

    def start_the_game():
        #msgSurface(1,green,True)
        runGame()

    def set_difficulty(value, diff):
        global srchr1, srchr2, mode
        if value[0][0] == 'HARD':
            srchr1 = minimaxAgentHard()
            srchr2 = minimaxAgentHard()
            mode = 'HARD'
        else:
            srchr1 = minimaxAgentEasy()
            srchr2 = minimaxAgentEasy()
            mode = 'EASY'
        #print(value)

    def set_name(value):
        # print(value)
        global P1name
        if value == '':
            P1name = "Jhon Doe"
        else:
            P1name = value

    def set_move(value, diff):
        global PLTYP1, PLTYP2, P1move, P2move
        if value[0][0] == 'WHITE':
            PLTYP1 = 'computer'
            PLTYP2 = 'human'
            P1move = "WHITE"
            P2move = "BLACK"
        else:
            PLTYP1 = 'human'
            PLTYP2 = 'computer'
            P1move = "BLACK"
            P2move = "WHITE"
        #print(value)

    menu = pygame_menu.Menu('Welcome', dispWidth, dispHeight,
                            theme=pygame_menu.themes.THEME_SOLARIZED)

    if run:
        menu.add.text_input('Name :', default='John Doe', onchange=set_name)
        run = False
    menu.add.selector(
        'Move :', [('BLACK', 1), ('WHITE', 2)], onchange=set_move)
    menu.add.selector(
        'Difficulty :', [('EASY', 1), ('HARD', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit',  pygame_menu.events.EXIT)
    menu.mainloop(setDisplay)

main(True)