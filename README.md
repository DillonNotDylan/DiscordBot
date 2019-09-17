The following modules are require to experience the full capability of the Bot:
- json
- libnacl
- discord
- youtube_dl
- discord.py rewrite[voice]


# First and foremost, a Discord account is a requirement for this Bot.
  - navigate to: https://discordapp.com/register to make an account

# Next we'll set up the server that this Bot will be a part of.
  - navigate to: https://discordapp.com/developers/applications/
  - log in with your account.
  - click "new application" in the top right of the page.
  - create a name for the server that the Bot will be residing in.

# Now we can get the Bots unique token (don't share this with anyone)
  - In the middle of the page to the right, under "client secret", press "click to reveal".
  - Take that string of numbers and letters and paste it into the designated area in the your_token.txt file.

# Once the server is made, the Bot will have to have permissions granted to it.
  - Discord uses a special link to authorize the Bot, so you'll have to change 
    the following hyperlink depending on what kind of permissions you would like to give the Bot
  - navigate to the left hand side of the Discord developer page and select the OAuth2 tab.
  - here you can select what type of client it is (bot) and what kind of permissions you'd like to give it (administrator)
  - You can either generate your own link, or use the one below if you'd like to make your Bot an administrator
  - Your client ID can be found in the OAuth2 tab in the middle-right of the page
  - https://discordapp.com/api/oauth2/authorize?client_id=<YOUR_CLIENT_ID>&permissions=8&scope=bot
  
# Run the bot.py script and bring life to your server!
