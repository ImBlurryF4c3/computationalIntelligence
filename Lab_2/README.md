# NIM Game using Adaptive (μ+λ)-ES
## In collaboration with Marco Colangelo s309798
The aim of this lab was coding an agent able of competing against the OPTIMAL agent in the Nim game.

We used a set of fixed rules that we bound to the respective weights firstly set as random values, calibrated though the ES strategy then. 
- The weights have been used as priority values during the choice of the rule to apply for the agent in each single turn.
- The fitness counts the number of wins over a number of games set by a parameter.
- The mutation is applied through a normal distribution.


The idea of the code is the same for both the versions (mine and Marco's one) but since I had the opportunity to train the model more time changing also some of the rules proposed, we have been successfully achieved a win rate against the optimal player of 55% (λ = 20, μ = 5)---> You can find the solution in the control_room.py file