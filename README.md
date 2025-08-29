# Python Black Jack
A Simple Black Jack Game.<br>
Based on Code from the Book 'Object Oriented Python' by Irv Kalb

## Required libraries
- pygame
- pygwidgets

## Credits
Main Code and Game Logic: Jared Witt<br>
Original files 'Card.py' 'Deck.py' and 'Game.py' provided in Chapter_12 of th GitHub Repository: https://github.com/IrvKalb/Object-Oriented-Python-Code

### Known Bugs
- split player can still hit their first hand if it was a blackjack

### Future Implementation
- Implement shoe logic and visualization
  - visualization of shoe near top right
  - shoe reshuffle logic
  - make shoe reshuffle determined by a cut card
  - when new shoe is made, have the player choose the cut card location
- Add dynamic player count
  - Add a leave or join button
  - Game starts with no players. Once a player is seated, a round can begin
- Add more betting options (other than +/-10)
- Create blackjack table background
- Show a discard pile
- Card dealing animations (moves from shoe to hand or hand to discard in the amount of time it takes to play cardFlip.wav)
- Track game stats in a save file
- Insurance option even though nobody takes it (low priority)
  - add player buttons for insurance stage
  - display text that says "nobody is home" if dealer didn't have a black jack
  - remove is anyone home button. Automatically reveal after all players respond yes or no
