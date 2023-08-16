# Assignment 1 - Student's Report

Please make sure that the report is no longer than 500 words.

## Author: BENJAMIN MICHEAL NOLAN - 220220586

## Class of the Agent Program

I started out with a simple reflex design in order to implement all required actuators, sensors and actions to provide 
all the instructions to the agent as required, alongside with the wall, obstacle and food coordinate logic so that the 
AI agent can at the least attempt to succeed in its goal to find and eat food.
With more time, I would have begun building other classes, such as building out logic for food hunting to be more 
efficient with shortest path algorithms to achieve a higher score in the shortest amount of time.

## AI Techniques Considered

I did not use a particular technique perse, however I did build the logic around the intercept of the agent and the 
components (walls, obstacles and food) to determine if the agent is near or on a component to decide whether the 
direction needs to be changed (hitting a wall or obstacle) and deciding which direction to take 
(checking neighbouring coordinates for obstacles) and the step process to open the mouth of the agent snake prior
to the food coordinate, eating the food on the coordinate and closing the mouth afterward.
With the objective to find food, eat it and score points, this objective was met as required, although more work was 
needed to find the shortest path to reach a higher score.

## Reflections

Initial challenge was learning how to implement the data types for each sensor as it was different to the
vacuum data structure, although the building out of the logic for the walls and obstacles simultaneously working with 
directional x and y coordinates (collision detection) was the biggest and most time-consuming challenge.
A lot of the time each test concluded with the agent hitting corners and side walls without changing direction, which
then required more work on building out bound-logic, once this was rectified the next challenge was obstacles and
whether an obstacle had an adjacent wall or another obstacle so that the agent does not turn into a direction that
would be a wall or another obstacle and cause Game over.
Sometimes this still occurs and needs more work.
The final challenge was getting the agent to find where the food is in sight and head over to the direction where it is,
whether the food was before the coordinate in the direction the agent is heading, on the x or y intercept and when it 
passed through.
So far I could only factor the up and down directions looking at constant y, however when there is another food 
coordinate in its path, it changes direction again, even if the food coordinate is on the other side of an obstacle.
This needs more work to check if an obstacle is before the food coordinate so that it doesn't go for it as it will
not be in line of sight.


