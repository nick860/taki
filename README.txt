This is an explanation about the communication between the back-end and the front-end of our taki bot.

We are transmitting the game data via sockets and process it through string manipultaion to extract all the needed data.

There are multiple types of signs which represent different characters and situations that the front-end should display:

1. "<number>_<color>;"
	<number> = the number on the card
	<color> = the first letter of the color of the card
	e.g. - "6_R"

2."<sign>_<color>;"
	<sign> = same as number but has all the non-number values
		includes: 
			a. ">" = change direction
			b. "S" = stop 
			d. "T" = taki sequence start
		e.g - "S_B"

3. "cc" - change color to the one chosen"

4. "ct" - colorful taki card.
