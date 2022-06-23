#IMPORTING MODULES
import os
import pickle
from button import Button #BUTTON HANDLING
import pygame #for designing ping pong game
import sys
import moviepy.editor#TO PlAY VIDEO IN PYGAME
from paddle import Paddle
from ball import Ball


#Constant Values Used
WIDTH,HEIGHT=1280,720
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
END_LIVES=0
FPS=80
WHITE=(255,255,255)
BLACK=(0,0,0)
PADDLE_WIDTH,PADDLE_HEIGHT=20,100
BALL_RADIUS=7

#Database file used to store scores
DATABASE_FILE='./assets/ScoreBoard.dat'

#Variables storing color hash values
PINK='#83f52C'
GLOWBLUE="#08f7fe"
GLOWGREEN="#09fbd3"
LIGHT_ORANGE="#dfff11"
GLOWPINK="#f353bb"
LIGHTPURPLE="#CE96FB"
ELECTRIC_GREEN="#ccff00"
ELECTRIC_ORANGE="#ff3503"
LIME_GREEN="#fe4164"
LIGHTTEAL="#00C2BA"

#Variables storing font file path
AQUIRE='./assets/Aquire.otf'
AQUIRE_LIGHT="./assets/AquireLight.otf"
MAIN_MUSIC='assets/main_music.mp3'
AQUIRE_BOLD="./assets/AquireBold.otf"

#Variables storing BG image path
BG_IMAGE = pygame.image.load("assets/bg.jpg")

#Sound file path
GAME_WON_SOUND=pygame.mixer.Sound('./assets/gamewon.wav')
CLICK_SOUND=pygame.mixer.Sound('./assets/click_sound.wav')
LIVE_GONE_SOUND=pygame.mixer.Sound('./assets/scored.wav')

#Music file path
GAME_START_MUSIC='assets/game_start_music.mp3'
BALL_HIT_SOUND=pygame.mixer.Sound('./assets/hits.mp3')

#BG video file path
PONG_LOADING="./assets/pong_loading.mp4"

#setting caption for the game
pygame.display.set_caption("PING PONG")

#to initialize the pygame
pygame.init()


#function to set the fonts which will be ready to get render
def get_font(size,font=AQUIRE): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(font, size)


#Function to handle data inside the leaderboard
def leaderBoard():
  clock=pygame.time.Clock()

  #Adding the background imgae to the whole screen
  WIN.blit(BG_IMAGE, (0, 0))
  
  #list to store the dictionary in the .dat file 
  leaders=[]
  #list to store the names
  name_lists=[]
  #list to store the scores
  score_lists=[]

  #Checking if file is present
  if os.path.isfile(DATABASE_FILE):
    pickle_on=open(DATABASE_FILE,"rb")
    try:
      while True:
        leaders.append(pickle.load(pickle_on))
    except EOFError:
      pass
    for count,i in enumerate(leaders[::-1]):#iterating reverse to get the top leaders
      if count<=9:#takes ten
        name_lists.append(get_font(30).render(f"{max(i.keys())}",1,WHITE))
        score_lists.append(get_font(30).render(f"{max(i.values())}",1,WHITE))
      else:
        break

    #blitting to the screen by the distance of 40 and taking down margin(from the center) 20 times of the no. of leaders
    for i,(j,k) in enumerate(zip(name_lists,score_lists)):#zip returns value in form of tuple
      WIN.blit(j,(WIDTH//4-j.get_width()//2,HEIGHT//2-j.get_height()//2+40*i-20*len(name_lists)))
      WIN.blit(k,(WIDTH*(3/4)-k.get_width()//2,HEIGHT//2-k.get_height()//2+40*i-20*len(name_lists)))
    name_label=get_font(30).render("LEADERS",1,LIGHTPURPLE)
    score_label=get_font(30).render("SCORE",1,LIGHTPURPLE)
    WIN.blit(name_label,(WIDTH//4-name_label.get_width()//2,300-20*len(name_lists)))
    WIN.blit(score_label,(WIDTH*(3/4)-score_label.get_width()//2,300-20*len(name_lists)))
  
  #if data is not available then displaying message accordingly
  else:
    None_text=get_font(40,AQUIRE_LIGHT).render("OOPS",1,WHITE)
    WIN.blit(None_text,(WIDTH//2-None_text.get_width()//2,HEIGHT//2-None_text.get_height()//2-50))
    None_text=get_font(40,AQUIRE_LIGHT).render("NO DATA IS AVAILABLE",1,WHITE)
    WIN.blit(None_text,(WIDTH//2-None_text.get_width()//2,HEIGHT//2-None_text.get_height()//2))
    None_text=get_font(40,AQUIRE_LIGHT).render("WILL UPDATE SHORTLY",1,WHITE)
    WIN.blit(None_text,(WIDTH//2-None_text.get_width()//2,HEIGHT//2-None_text.get_height()//2+50))

  # OPTIONS_TEXT = get_font(60).render("LEADERBOARD", True, GLOWBLUE)
  # OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, 200-len(name_lists)*15))
  # WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)
  leader_text = get_font(60).render("LEADERBOARD", True, GLOWBLUE)
  WIN.blit(leader_text,(WIDTH//2-leader_text.get_width()//2, 200-len(name_lists)*15-leader_text.get_height()//2))


  #In the while loop to check if player have pressed the back button
  while True:
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

    #Creating the back button
    OPTIONS_BACK = Button(image=None, pos=(640, 515+len(name_lists)*10),text_input="BACK", font=get_font(60), base_color=GLOWGREEN, hovering_color=LIGHT_ORANGE)

    #checking for the change in color and updating
    OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    OPTIONS_BACK.update(WIN)

    #listening to player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            CLICK_SOUND.play()
            WIN.blit(BG_IMAGE,(0,0))
            return

    clock.tick(FPS)
    #Keep resfreshing the screen to make sure every changes are visible(like hovering)
    pygame.display.update()


#function to show label to players when high score is achieved
def high_score():
  high_Score_text=get_font(40,AQUIRE_BOLD).render("HIGH SCORE",1,WHITE)
  GAME_WON_SOUND.play()
  response=True
  while response:
    WIN.blit(high_Score_text,(WIDTH//2-high_Score_text.get_width()//2,HEIGHT//2-high_Score_text.get_height()//2))
    pygame.display.update()
    for event in pygame.event.get():
      #if player click cross to close the dialog box then end the game and close the file
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        response=False
        break


#Function to display the controls so that player could return or replay when game ends
def menu_or_restart():
  control_list=["X to return back to MENU","Any key to REPLAY"]
  control_text=[]
  for i in control_list:
    control_text.append(get_font(30,AQUIRE_LIGHT).render(i,1,WHITE))
  for l in range(len(control_text)):
    WIN.blit(control_text[l],(WIDTH//2-control_text[l].get_width()//2,HEIGHT//2-control_text[l].get_height()//2+120+l*60))
  pygame.display.update()
  response=True
  while response:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key==pygame.K_x:#if x is pressed then return back to main_menu
          CLICK_SOUND.play()
          pygame.mixer.music.fadeout(2000)
          pygame.mixer.music.unload()
          response=False
          main_menu()
        else:
          CLICK_SOUND.play()#else any key press will lead to replay
          response=False


#Function to store the new max score in the .dat file
def save_MAX(highScorer,max_score):  
    filename=DATABASE_FILE
    with open(filename, 'ab+') as fp:
        pickle.dump({f"{highScorer}":max_score},fp)


#function to handle collision of ball with walls and paddles
def handle_collision(ball,left_paddle,right_paddle,left_score,right_score,max_score,is_max_achieved,players,highScoreShown):
  #just to make sure our highScore function runs only once when highscore achieved
  if not is_max_achieved:
    global highScorer
    highScorer=None

  #To handle ball collision with wall
  #if ball goes below the panel
  if ball.y+ball.radius>=HEIGHT:
    if ball.yvel>0:#additional condition to make sure it does not stuck. So that it doesn't stuck.
      ball.yvel=-1*ball.yvel
      BALL_HIT_SOUND.play()
  #if ball goes above the panel
  elif ball.y-ball.radius<=0:
    if ball.yvel<0:#so that it doesn't stuck
      ball.yvel=-1*ball.yvel
      BALL_HIT_SOUND.play()
  
  #To handle ball collision with left paddle
  if ball.xvel<0:#If it is meeting let paddle then its vel must be less than 0
    
    #To check if it is colliding left paddle
    if ball.y>=left_paddle.y and ball.y <=left_paddle.y + left_paddle.height:
      if ball.x-ball.radius<=left_paddle.x+PADDLE_WIDTH:
        ball.xvel=-1*ball.xvel

        middle_y=left_paddle.y+PADDLE_HEIGHT//2;
        ball_diff_paddle=middle_y-ball.y
        intensity_factor=(left_paddle.height/2)/ball.MAX_VELOCITY;#intensity factor which handles the speed at which ball get reflects after hitting the paddles

        yvel=ball_diff_paddle/intensity_factor
        ball.yvel=-1*yvel#ballvel always get negative if hits upper part and postive if hits lower part 
    #to check if it is meeting right paddle
        
        left_score+=1;
        BALL_HIT_SOUND.play()#if it hits then play the sound

        #checking if max score is achieved
        if left_score>max_score:
          if not highScoreShown:
            high_score()#display highscore label

          highScoreShown=True
          max_score=left_score
          is_max_achieved=True
          highScorer=players[0]#left player achieved the highscore

  #To handle ball collision with right paddle
  else:
    if ball.y>=right_paddle.y and ball.y <=right_paddle.y + right_paddle.height:
      if ball.x+ball.radius>=right_paddle.x:
        ball.xvel=-1*ball.xvel

        middle_y=right_paddle.y+PADDLE_HEIGHT//2;
        ball_diff_paddle=middle_y-ball.y
        intensity_factor=(right_paddle.height/2)/ball.MAX_VELOCITY;
        yvel=ball_diff_paddle/intensity_factor
        ball.yvel=-1*yvel#ballvel always get negative if hits upper part and postive if hits lower part
        
        right_score+=1
        BALL_HIT_SOUND.play()#playing sound

        if right_score>max_score:
          if not highScoreShown:
            high_score()#display highscore label

          highScoreShown=True
          max_score=right_score
          is_max_achieved=True
          highScorer=players[1]

  return (left_score,right_score,max_score,is_max_achieved,highScorer,highScoreShown)


#function to handle the key events made by players
def handle_paddle_movement(keys,left_paddle,right_paddle):
  #Here True and False boolean values are used to tell whether to make paddle move up or down. True---> UP
  if keys[pygame.K_w] and left_paddle.y-left_paddle.CONSTANT_VELOCITY>=0:
    left_paddle.move(True)
  if keys[pygame.K_s] and left_paddle.y+left_paddle.CONSTANT_VELOCITY+PADDLE_HEIGHT<=HEIGHT:
    left_paddle.move(False)
  if keys[pygame.K_UP] and right_paddle.y-right_paddle.CONSTANT_VELOCITY>=0: 
    right_paddle.move(True)
  if keys[pygame.K_DOWN] and right_paddle.y+right_paddle.CONSTANT_VELOCITY+PADDLE_HEIGHT<=HEIGHT:
    right_paddle.move(False)


#function to generate colorful border in game playing
def generate_border():
  for counter,i in enumerate(range(10,HEIGHT,HEIGHT//10)):
    if(counter%2):
      COLOR=LIME_GREEN
    else:
      COLOR=PINK
    pygame.draw.rect(WIN,COLOR,(WIDTH//2-5,i,10,HEIGHT//20))


#function resposible for drawing the whole game environment
def draw(paddles,ball,left_lives,right_lives,left_score,right_score,players):
  WIN.fill(BLACK)
  for paddle in paddles:
    paddle.draw(WIN)

  generate_border()

#rendering the score and lives label and their values. But they are yet to be blit
  left_lives_text=get_font(40,AQUIRE_LIGHT).render(f"{left_lives}",1,WHITE)
  right_lives_text=get_font(40,AQUIRE_LIGHT).render(f"{right_lives}",1,WHITE)
  left_score_text=get_font(40,AQUIRE_LIGHT).render(f"{left_score}",1,WHITE)
  right_score_text=get_font(40,AQUIRE_LIGHT).render(f"{right_score}",1,WHITE)

  left_lives_label=get_font(15,AQUIRE_LIGHT).render(f"{players[0]} LIVES",1,WHITE)
  right_lives_label=get_font(15,AQUIRE_LIGHT).render(f"{players[1]} LIVES",1,WHITE)
  left_score_label=get_font(15,AQUIRE_LIGHT).render("SCORE",1,WHITE)
  right_score_label=get_font(15,AQUIRE_LIGHT).render("SCORE",1,WHITE)

#blitting the text values to update my screen data. Yet to update my display screen to make them visible to gamers
  WIN.blit(left_score_label,(WIDTH*(1/8)-left_score_label.get_width()//2,10))
  WIN.blit(left_lives_label,(WIDTH*(3/8)-left_lives_label.get_width()//2,10))
  WIN.blit(left_score_text,(WIDTH*(1/8)-left_score_text.get_width()//2,20))
  WIN.blit(left_lives_text,(WIDTH*(3/8)-left_lives_text.get_width()//2,20))

  WIN.blit(right_score_label,(WIDTH*(5/8)-right_score_label.get_width()//2,10))
  WIN.blit(right_lives_label,(WIDTH*(7/8)-right_lives_label.get_width()//2,10))
  WIN.blit(right_score_text,(WIDTH*(5/8)-right_score_text.get_width()//2,20))
  WIN.blit(right_lives_text,(WIDTH*(7/8)-right_lives_text.get_width()//2,20))


#drawing my circle every time this block iterates to make sure movement is visible
  ball.draw(WIN)
#automatically updating the x and y position of ball, so that draw will make a circle at new position
  ball.move()
  pygame.display.update()


#function to retriever max value(highest score) stored in our .dat file
def retrieve_MAX():
  #checking if file is present or not. If true then fetch the date otherwise let the max_score be 0
  if os.path.isfile(DATABASE_FILE):
    objs = []
    pickle_on=open(DATABASE_FILE,"rb")
    try:
      while True:
        objs.append(pickle.load(pickle_on))
    except EOFError:
      pass
    lists=[]
    for i in objs:
      lists.append(max(i.values()))
    max_score=max(lists)
  else:
    max_score=0
  return max_score


#Function to start the game and handle stuffs from its repetitive drawing to winning the game
def game_starts(players):
  run=True
  highScoreShown=False

  clock=pygame.time.Clock()#assigning the clock to control the iterations of while loop

  #Initializing the left and right paddle
  left_paddle=Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT,ELECTRIC_GREEN)
  right_paddle=Paddle(WIDTH-10-PADDLE_WIDTH,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT,ELECTRIC_ORANGE)
  left_lives,right_lives=5,5
  left_score,right_score=0,0

  ball=Ball(WIDTH//2,HEIGHT//2,BALL_RADIUS,WHITE)

  #Calling function to retrieved highest score from the .dat file
  max_score=retrieve_MAX()
  is_max_achieved=False

  #to give time and environment to players before starting of game.
  draw([left_paddle,right_paddle],ball,left_lives,right_lives,left_score,right_score,players)
  pygame.display.update()

  #Providing the delay of one second before and after starting of the BG music
  pygame.time.delay(1000)
  pygame.mixer.music.set_volume(0.2)
  pygame.mixer.music.load(MAIN_MUSIC)
  pygame.mixer.music.play(-1)
  pygame.time.delay(1000)

  while run:
    clock.tick(FPS)#lowers while execution to 60 times per second

    #calling draw inside the while loops will keep refreshing the screen and make movement of ball and paddles appear on the screen
    draw([left_paddle,right_paddle],ball,left_lives,right_lives,left_score,right_score,players)

    for event in pygame.event.get():#it will get all type of events from keyboard,mouse
      if event.type==pygame.QUIT:#if closing the window
        pygame.quit()
        sys.exit()
    keys=pygame.key.get_pressed()
    handle_paddle_movement(keys,left_paddle,right_paddle)

    #calling the function to check whether any collision had occur and updating the different values accordingly
    (left_score,right_score,max_score,is_max_achieved,highScorer,highScoreShown)=handle_collision(ball,left_paddle,right_paddle,left_score,right_score,max_score,is_max_achieved,players,highScoreShown)
    #If left paddle misses the ball
    if ball.x<0:
      LIVE_GONE_SOUND.play()
      left_lives-=1
      pygame.time.delay(1000)
      ball.reset()#reset the ball where it was initially when game started

    #If right paddle misses the ball
    elif ball.x>WIDTH:
      LIVE_GONE_SOUND.play()
      right_lives-=1
      pygame.time.delay(1000)
      ball.reset()#reset the ball where it was initially when game started


    won =False
    #if lives get 0
    if left_lives<=END_LIVES:
      GAME_WON_SOUND.play()
      win_text="Right player Won"
      won=True

    elif right_lives<=END_LIVES:
      GAME_WON_SOUND.play()
      win_text="Left player Won"
      won=True

    #End of the game and checking whether highscore has been achieved or not. Resetting ball,paddles and other values.
    if won:
      winner_text=get_font(40,AQUIRE_LIGHT).render(win_text,1,WHITE)
      WIN.blit(winner_text,(WIDTH//2-winner_text.get_width()//2,HEIGHT//2-winner_text.get_height()//2))
      pygame.display.update()
      pygame.time.delay(3000)

      #If max is achieved then show the text
      if is_max_achieved:
        save_MAX(highScorer,max_score)
        GAME_WON_SOUND.play()
        max_achiever_name=f"{highScorer.upper()} achieved highest score {max_score}"
        max_achiever_text=get_font(40,AQUIRE_LIGHT).render(max_achiever_name,1,WHITE)
        WIN.blit(max_achiever_text,(WIDTH//2-max_achiever_text.get_width()//2,HEIGHT//2-max_achiever_text.get_height()//2+60))
        pygame.display.update()
        pygame.time.delay(2000)
      
      #Reset all the values to restart the game or return back to main_menu
      right_paddle.reset()
      left_paddle.reset()
      ball.reset()
      is_max_achieved=False
      left_score=0
      right_score=0
      right_lives=5
      left_lives=5
      highScoreShown=False
      
      #Checking whether player wan't to restart or return
      menu_or_restart()


#To listen the keys entered by the players any key to start the play. This is done to give time to players to read the game contorls
def controls():
  clock=pygame.time.Clock()
  while True:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type==pygame.KEYDOWN:
        pygame.mixer.music.fadeout(2000)
        pygame.mixer.music.unload()
        return


#Function to read player name
def read_input(player_no):
    Clock=pygame.time.Clock()
    user_text=''
    while True:
      input_text=get_font(40,AQUIRE).render(f"Enter Player {player_no} Name",1,GLOWPINK)
      WIN.blit(BG_IMAGE,(0,0))
      WIN.blit(input_text,(WIDTH//2-input_text.get_width()//2,HEIGHT//2-input_text.get_height()//2-100))
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key==pygame.K_BACKSPACE:
            user_text=user_text[:-1]#removing the last character from string if backspace is pressed
          elif event.key==pygame.K_RETURN:
            return user_text
          else:
            user_text+=event.unicode
      
      #Displaying the text pressed by the players
      text_surface=get_font(40,AQUIRE_LIGHT).render(user_text,1,LIGHTTEAL)
      WIN.blit(text_surface,(WIDTH//2-text_surface.get_width()//2-len(user_text)*2,HEIGHT//2-text_surface.get_height()//2))
      pygame.display.update()
      Clock.tick(FPS)


#Function to take the name of the players
def name():
  players=[]
  clock=pygame.time.Clock()
  while True:
    clock.tick(FPS)#lowers while execution to 60(FPS) times per second
    for event in pygame.event.get():#it will get all type of events from keyboard,mouse
      if event.type==pygame.QUIT:#if closing the window
        pygame.quit()#come outside the while
        sys.exit()#close the file

    #calling the read_input() to take the name of the first(1) and second(2) player
    players.append(read_input(1))
    players.append(read_input(2))

    WIN.blit(BG_IMAGE, (0, 0))
    pygame.display.update()
    
    #After taking the name showing the controls to players to play the game
    control_list=["Use w s keys for left paddle","Use up down keys for right paddle","Press any key to Continue"]
    control_text=[]
    for i in control_list:
      control_text.append(get_font(30,AQUIRE_BOLD).render(i,1,GLOWPINK))
    for l in range(len(control_text)):
      WIN.blit(control_text[l],(WIDTH//2-control_text[l].get_width()//2,HEIGHT//2-control_text[l].get_height()//2+l*60-60))
    pygame.display.update()

    controls()#calling controls to give time to players to read the controls
    
    game_starts(players)


#Function which handles the main_menu and action on the buttons like play,leaderboard,exit
def main_menu():
  #Starting the BG music at the full volume(1)
  pygame.mixer.music.set_volume(1)
  pygame.mixer.music.load(GAME_START_MUSIC)
  pygame.mixer.music.play(-1)#-1 to make sure music runs at loop

  clock=pygame.time.Clock()
  while True:
    clock.tick(FPS)
    WIN.blit(BG_IMAGE, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    PLAY_BUTTON = Button(image=None, pos=(640, 200), 
                        text_input="PLAY", font=get_font(75), base_color=GLOWGREEN, hovering_color=LIGHT_ORANGE)
    OPTIONS_BUTTON = Button(image=None, pos=(640, 350), 
                        text_input="LEADERBOARD", font=get_font(75), base_color=GLOWGREEN, hovering_color=LIGHT_ORANGE)
    QUIT_BUTTON = Button(image=None, pos=(640, 500), 
                        text_input="QUIT", font=get_font(75), base_color=GLOWGREEN, hovering_color=LIGHT_ORANGE)

    #Handling the hover over the button
    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(WIN)
    
    #Handling the click events over the buttons or the dialog box
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
            CLICK_SOUND.play()
            name()
          if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
            CLICK_SOUND.play()
            leaderBoard()
          if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            CLICK_SOUND.play()
            pygame.quit()
            sys.exit()

    pygame.display.update()


#Function which handles the loading screen which comes at the very beginning
def loading():
  loading=get_font(50,AQUIRE_LIGHT).render("LOADING",1,WHITE)
  WIN.blit(loading,(WIDTH//2-loading.get_width()//2,HEIGHT//2-loading.get_height()//2))
  pygame.display.update()
  pygame.time.delay(2000)#waits for the 2 seconds

  #After than running the pong video
  video = moviepy.editor.VideoFileClip(PONG_LOADING)
  clip_resized = video.resize((WIDTH, HEIGHT))
  clip_resized = clip_resized.loop(duration = 4)
  clip_resized.preview()

  #After end of the video we start the main_menu
  main_menu()


if __name__=='__main__':#just to make sure that we are running the current file, then only run the game(i.e. main())(for other files __name__ will not be equal to '__main__'). It is just to make sure that if someone import this file(module) to another then it shouldn't be running directly cause that wound not what any programmer would wan't.
  loading()#Whole game starts from here