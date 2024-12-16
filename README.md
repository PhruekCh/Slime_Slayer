# Slime Slayer

### Project description
This is a game simulation, The game rules are you need to eliminate all slimes collide each other and the arena, in order to go to the next level.
It is simple yet not easy to clear as the feature of the game can create infinite level of the game and it gets harder as you progress.

### Features
- Moving by press "W" and "S" to move forward and backward, "A" and "D" to rotating the angle of your avatar so you can move in every direction.
- The red arrow on your avatar will indicate the direction you are facing.
- Attack move, if the slime was in the range, you will eliminate the slime.
- Life system, you can hit by slimes 3 times before you ran out of lives, which display on the top of the screen.
- Slime can collide with each other so attack can comes from many ways.
- Animation, when you defeat the slime it will dissapear by frame by frame animation.
- Level, when eliminating all slimes, the path opens to you. Progressing to next level and there's no level cap, meaning you can go how far you want if you can win.
- Reset level, It's ok if you lost. Coming back to level 1 instantly when you lost to any level you're out of lives.

### How to install and run the project

git fork then git pull.

run on file named "run_ball.py"

### Usage
Youtube Link: https://youtu.be/9hR97ayGuJ4

When starting the game by running the "run_ball.py"
- 3 lives will be given. If those ran out, you will need to restart the game from pause menu that will pop up.
- When losing life you will have 4 seconds to be invincible to recover from their attacks.
- You will have invincible shield for 3 seconds so that you will not lose lives when all slimes jump it before you knew it.
- Moving by press "W" and "S" to move forward and backward, "A" and "D" to rotating the angle of your avatar as the red arrow point the direction.
- "E" to attack, if the slime was in the range, you will eliminate the slime.
- Slime will collide with everything so be careful with their moves.
- When clearing out all of them, you can restart to level 1 by pressing "R" or "N" to go to next level.
- Next level will increase speed and number of slime in that arena.

### Project design and implementation

![UML Class Diagram](https://cdn.discordapp.com/attachments/1311006911818109010/1318245611216048189/UML_class.jpeg?ex=67619f65&is=67604de5&hm=da74c6bc9b6832cd196207699965e4e7ac0a3adf90651f65a2ca3b64024813e9&)

I had import ball to bouncing simulator to represent as a bouncing monster. AvatarController used to control player avatar
both appearance and functions to match in Bouncing simulator. Event is what professor gave me, I did change a little bit of parameter
and use to queue event in Bouncing sim also. Animated use to run animation when monster get hits of the smoke folder containing 16 frames.

I use original ball class change it appearance and collision a bit, remove the paddle and make an avatar to act as player representative.
by making it more interesting I made the avatar collision with ball detection, so it could have lives. and moving player avatar by turtle also.
When creating object in bouncingsimulator I need to make it function. When reset the level it just create new object with same attributes
same goes with next level but adding value to attributes to object directly.

There's still some bugs I found that doesn't affect gameplay. When goes to new level (more than 1) and close it by X the tab
it will generate turtle screen and drawing border. I can't find the cause yet, it could be fix with quit function but
I don't think it's a good way to solve it that way.

### Rate my project sophistication level
I would give it **90**. The reason is it may not involve with much physic other than what professor gave me,
but I extent the possibility of it, the potential of being a game. Anything can be made to be interesting with great idea.

