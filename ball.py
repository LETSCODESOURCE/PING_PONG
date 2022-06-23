import pygame

#Ball class for creating and handling balls
class Ball:
  MAX_VELOCITY=10
  #Initialization of the properties of the object
  def __init__(self,x,y,radius,color):
    self.x=self.originalX=x
    self.y=self.originalY=y
    self.radius=radius
    self.xvel=self.MAX_VELOCITY
    self.yvel=1
    self.color=color
  
  #Method to draw circle
  def draw(self,win):
    pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

  #Method to move the circle by changing its x and y positions
  def move(self):
    self.x+=self.xvel
    self.y+=self.yvel
  
  #Method to reset the positions of the ball to its original position
  def reset(self):
    self.x=self.originalX
    self.y=self.originalY
    self.yvel=1
    self.xvel=-1*self.xvel#To move the ball towards the opposite paddle