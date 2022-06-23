import pygame

#Paddle class for creating and handling paddles
class Paddle:
  CONSTANT_VELOCITY=11
  #Initializing the properties of the objects
  def __init__(self,x,y,width,height,color):
    self.x=self.originalX=x
    self.y=self.originalY=y
    self.width=width
    self.height=height
    self.color=color

  #Method to draw rectangle on the basis of x,y positions
  def draw(self,win):
    pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))

  #Method to move the paddles
  def move(self,up=True):
    if up:
      self.y-=self.CONSTANT_VELOCITY
    else:
      self.y+=self.CONSTANT_VELOCITY
  
  #Method to reset paddles to their original positions
  def reset(self):
    self.x=self.originalX
    self.y=self.originalY