<picture>
  <img src="./img/rotombot_logo.png" alt="Project description image" height="150px" width="150px"/>
</picture>

# Rotom Bot
The official server management bot for the Discord server <a href="https://discord.gg/7FBupspBZB"> The Pokehub</a> written in Python using the discord.py wrapper.
</br></br>


# Bot features
## Tournament registration
Rotom Bot offers an in-house tournament registration system for <a href="https://pokemonshowdown.com/"> Pokemon Showdown</a>-based tournaments 
which is connected to the <a href="https://github.com/smogon/pokemon-showdown-client/blob/master/WEB-API.md">Showdown API</a> for verification of users and battle replays. 

Registering for a tournament in the registration channel ```<@member> <Showdown ID>``` </br>
<picture>
  <img src="./img/rotombot_tour_reg.jpg" alt="Tournament registration" height="50%" width="50%"/>
</picture>
  
Displaying a list of tournament participants ```.participants``` </br>
<picture>
  <img src="./img/rotombot_tour_list.jpg" alt="Tournament list" height="50%" width="50%" />
</picture>
  
Announcement of battle replay results dynamically </br>
<picture>
  <img src="./img/rotombot_tour_verify_replay.jpg" alt="Tournament verify replay" height="50%" width="50%"/>
</picture>
  <picture>
  <img src="./img/rotombot_tour_annouce_outcome.jpg" alt="Tournament announce outcome" height="50%" width="50%"/>
</picture>


## League management
The server hosts Pokemon league-style tournaments/events annually in which most, if not all components of the tournament are handled by Rotom Bot itself.

Display registered pool of challenger ```.pl <gen>``` or elite ```.epl <gen>``` </br>
<picture>
  <img src="./img/rotombot_league_pool.jpg" alt="League pool" height="50%" width="50%" />
</picture>
  <picture>
  <img src="./img/rotombot_league_epool.jpg" alt="League elite pool" height="50%" width="50%" />
</picture>

Display profile of normal participant (challenger, gym leader, elite) ```.p <gen>``` </br>
<picture>
  <img src="./img/rotombot_league_profile.jpg" alt="League profile" height="50%" width="50%"/>
</picture>

Display profile of current champion  ```.champion``` </br>
  <picture>
  <img src="./img/rotombot_league_profile_champ.jpg" alt="League champion profile" height="50%" width="50%"/>
</picture>


## Role management for teams
Rotom Bot offers a role management system for "Villain Teams" based on the main Pokemon games. 
Members can freely join teams via Rotom Bot commands to access secret team chats with a 24-hour limit.

Select a desired team from the given choices  ```.jt``` </br>
<picture>
  <img src="./img/rotombot_team_reg_selection.jpg" alt="Join team selection" height="50%" width="50%"/>
</picture>

Directly join a team ```.jt <Team>``` </br>
<picture>
  <img src="./img/rotombot_team_reg_direct.png" alt="Join team direct" height="50%" width="50%"/>
</picture>

Leave your current team ```.jt None``` </br>
<picture>
  <img src="./img/rotombot_team_leave.png" alt="Leave team" height="50%" width="50%"/>
</picture>

Bot restricts member from switching teams if they have just switched teams recently within 24 hours
<picture>
  <img src="./img/rotombot_team_duration_limit.jpg" alt="Team switch duration limit" height="50%" width="50%"/>
</picture>


## Profanity filter
Messages sent in server is filtered through a profanity filter based on <a href="https://github.com/snguyenthanh/better_profanity">better_profanity</a>
to introduce a Discord Pokemon community suitable for all ages. 

Disallowed messages are deleted by the bot immediately </br>
<picture>
  <img src="./img/rotombot_profanity_delete_msg.jpg" alt="Profanity delete message" height="50%" width="50%"/>
</picture>

Deleted messages are logged in a moderator channel </br>
<picture>
  <img src="./img/rotombot_profanity_deleted_msg.jpg" alt="Profanity deleted" height="50%" width="50%"/>
</picture>


## Text translation
Rotom Bot offers a text translation feature, which comes in handy in case someone sent a non-English message in chat. 
Based on <a href="https://github.com/ssut/py-googletrans">Googletrans</a> with some slight modifications.

Text translation with auto-detect language ```.t <text to be translated>``` </br>
<picture>
  <img src="./img/rotombot_translator_auto.jpg" alt="Text translation auto-detect" height="50%" width="50%"/>
</picture>

Text translation with input-output languages defined ```.t <text to be translated> --<input lang> --<output lang>``` </br>
<picture>
  <img src="./img/rotombot_translator_src_dst.jpg" alt="Text translation input-output" height="50%" width="50%"/>
</picture>


## Urban Dictionary and English Dictionary feature
Rotom Bot offers lookup of text on the Urban Dictionary via <a href="https://rapidapi.com/community/api/urban-dictionary">Urban Dictionary API on RapidAPI</a> and English dictionaries via <a href="https://github.com/geekpradd/PyDictionary">PyDictionary</a>

Text lookup on Urban Dictionary ```.urban <text to be searched>``` </br>
<picture>
  <img src="./img/rotombot_urban.jpg" alt="Urban" height="50%" width="50%"/>
</picture>

Text lookup on an English Dictionary ```.dict <text to be searched>``` </br>
<picture>
  <img src="./img/rotombot_dict.jpg" alt="Dict" height="50%" width="50%"/>
</picture>


## Snipe and edit snipe feature
Rotom Bot offers snipe (recover the previous message deleted) and esnipe (recover the previous message edited) features which works for messages modified within the last 60 seconds. These features are mainly for some conversational fun in the server.

Snipe message ```.snipe``` </br>
<picture>
  <img src="./img/rotombot_snipe.jpg" alt="Urban" height="50%" width="50%"/>
</picture>

Edit snipe message ```.es``` </br>
<picture>
  <img src="./img/rotombot_esnipe.jpg" alt="Dict" height="50%" width="50%"/>
</picture>


## Games section
Rotom Bot offers a game section which includes a few message-based games. Nobody really plays them nowadays though :( , 
but they were an interesting learning experience for the dev.

Guess The Number ```.gg``` </br>
<picture>
  <img src="./img/rotombot_guess_numbers.jpg" alt="Guess The Number" height="50%" width="50%"/>
</picture>

Tic-Tac-Toe (implemented this one with a minimax algorithm) ```.ttt``` </br>
<picture>
  <img src="./img/rotombot_ttt.jpg" alt="Tic-Tac-Toe" height="50%" width="50%"/>
</picture>

Rock-Paper-Scissors ```.rps``` </br>
<picture>
  <img src="./img/rotombot_rps.jpg" alt="Rock-Paper-Scissors" height="50%" width="50%"/>
</picture>


## Miscellaneous features
Rotom Bot offers a multitude of other smaller features which are generally quite useful. 

Discord avatar/profile picture of a server member or self ```.av <Member name>(optional)``` </br>
<picture>
  <img src="./img/rotombot_av.jpg" alt="Avatar" height="50%" width="50%"/>
</picture>

Pokedex entry of a pokemon  ```.dex <Pokemon name>``` </br>
<picture>
  <img src="./img/rotombot_dex.jpg" alt="Dex" height="50%" width="50%"/>
</picture>

Competitive pokemon sets fetched from Smogon ```sets <Pokemon name>``` </br>
<picture>
  <img src="./img/rotombot_sets.jpg" alt="Sets" height="50%" width="50%"/>
</picture>

Pokemon weakness based on typing ```.weak <Pokemon name>``` </br>
<picture>
  <img src="./img/rotombot_weakness.jpg" alt="Weakness" height="50%" width="50%"/>
</picture>

Learnset of Pokemon (all moves that can be learned) ```.learnset <Pokemon name>``` </br>
<picture>
  <img src="./img/rotombot_learnset.jpg" alt="Weakness" height="50%" width="50%"/>
</picture>
