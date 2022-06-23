from pygame import Color

#Button class for cerating and handling buttons
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	#Method to update the button on hovering
	def update(self, screen):
		screen.blit(self.text, self.text_rect)

	#Method to check if mouse is over the button or not
	def checkForInput(self, position):
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
			return True
		return False

	#Method to change color of the text_rect
	def changeColor(self, position):
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)

		else:
			self.text = self.font.render(self.text_input, True, self.base_color)