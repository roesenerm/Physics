import pygame
import math
import random
from nupic.frameworks.opf.modelfactory import ModelFactory
import model_params

background_colour = (255,255,255)
width, height = 600, 400
screen = pygame.display.set_mode((width, height))

class Particle:
    def __init__(self, (x,y), size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0,0,255)
        self.thickness = 1
        self.speed = 5
        self.angle = 0
        self.angle = random.uniform(0, math.pi*2)

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.runNupic(self.x)
            self.runNupic(self.y)
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.runNupic(self.x)
            self.runNupic(self.y)
        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.runNupic(self.x)
            self.runNupic(self.y)
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.runNupic(self.x)
            self.runNupic(self.y)

    def runNupic(self, gameEvent):
        # Create the model for predicting Game Event.
        model = ModelFactory.create(model_params.MODEL_PARAMS)
        model.enableInference({'predictedField': 'event'})
        
        # Get the Game Event.
        event = gameEvent
        
        # Run the input through the model.
        modelInput = {'event': event}
        result = model.run(modelInput)
        
        # Update inference.
        inference = result.inferences['multiStepBestPredictions'][1]
        print 'Inference:', inference


pygame.display.set_caption('tutorial 1')

my_first_particle = Particle((150,50), 15)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_colour)

    my_first_particle.move()
    my_first_particle.bounce()
    my_first_particle.display()
    pygame.display.flip()

