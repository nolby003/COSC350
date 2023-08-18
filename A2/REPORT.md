# Assignment 2 - Student's Report

Please make sure that the report is no longer than 500 words.

## Author: BENJAMIN MICHEAL NOLAN - 220220586

## Complexity of the Problem 

As with all skeleton code problems, learning how it all goes together and works is always complex in itself. 
The complexity of solving this problem is always initially understanding the makeup of the program prior to implementing 
all the missing functions.
Looking back at the environment files helps to understand how values are used and how the programs talks back to each 
function.

## AI Techniques Considered

After I had implemented most of the requirements, the most difficult was implementing the intelligent behaviours by 
finding the most suitable algorithm to use. 
I had an issue trying to pass the minimax algo to the function after several iterations, so I decided to go with the 
Monte Carlo Tree Search (MCTS) algo which seemed to work quite well without error, quite an easy implementation.
I cannot observe and test how minimax works for the AI part in comparison to MCTS, but MCTS seemed to work quite well.

## Reflections

I spent many days trying to solve the legal moves implementation given how workshops gave nothing away in how to really 
solve this, spent most of the time looking back at environment files and classes to understand how to best implement
it, alongside the actuators, sensors and actions.
Advance rules: Powerup was the most time spent in the legal moves component before I even started to implement the AI
and human behaviours, but happen to get it all going just in time before the assignment was due.
It was the greatest programming challenge to date.