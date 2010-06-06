Conq - the simplified space conquering game
===========================================
In the game of conq, you play as the blue nation trying to dominate the system of planets you find yourself in.  Of course, this would be too easy if there were not other nations trying to do the same.  The game is played by letting the planets produce fleets for you over time and then sending these fleets to other planets.

Planets
-------
The game automatically generates the planets in the system and gives each nation a starting planet.  There are two attributes of each planet: size and capacity.

The size of a planet is shown by its radius.  This size determines the speed at which the planet generates fleets.  Larger planets generate fleets more quickly than smaller planets.

The capacity of the planet is shown by the radius of its atmosphere.  A larger atmosphere can support more fleets.

If a planet is occupied by a nation, the planet will take the national color.  It will then start generating fleets for the nation.  The size of the garrison is shown by the radius of the ring around the planet.  When an attacking fleet reaches a planet, the fleet size is compared to the garrison size.  If the fleet is larger, the planet becomes occupied by the attacker, the attacking fleet is reduced by the size of the garrison, and the resulting fleet is placed in the garrison.  If the fleet is not large enough to break through the garrison, the garrison is reduced by the size of the fleet and the planet remains occupied by the defender.

Sending Fleets
--------------
A fleet is sent by clicking down on a player owned planet and dragging to the planet to attack.  The percentage of the garrison to send is determined by how far from the planet center the initial click is made.  To send all of the garrison, click on the outside of the garrison (but still inside the atmosphere).  To send half of the garrison, click halfway between the outside of the atmosphere and the planet center.  To send a very small fleet, click near the planet center.

Once the click is released on a valid target, the garrison will be reduced by the fleet size and the fleet will be shown with a line connecting the fleet to the target planet.  Once a fleet reaches the atmosphere, the battle takes place.

Game Over
---------
The game ends in victory when the player owns all planets and all opponent fleets have reached their targets.  If the player no longer occupies any planets and no fleets are in transit to a planet, the game ends and the player loses.
