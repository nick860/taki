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
			c. "P" = plus 
			d. "T" = taki sequence start
			e. "+2" = take 2 cards
		e.g - "S_B"

3. "cc" - change color to the one chosen"

4. "ct" - colorful taki card.

It should be mentioned that the signs for the cards in the bot's hands differ from the one's that are provided for the game table. If a card of change color or colorful taki is in the bot's hand, it will not have a specif color assigned to it till it's played. If it is placed on the game table then the back-end will send a message of the current card and accompany it with it's color, e.g - "cc_R" or "ct_G".