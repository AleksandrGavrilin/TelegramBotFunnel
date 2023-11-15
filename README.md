![](img_for_readme/main_img.jpg)
_____
Program with a chatbot (that interacting like a “funnel”), with the addition of new users to the database.
_____
### <span style='color:rgb(47, 79, 79)'> Main functionality of the program: </span>
- interaction with the user using a chatbot;
- adding new users to the database;
- the ability to view the number of registered people in the database for today by sending the command "/users_today" to the account's favorites.
### <span style='color:rgb(47, 79, 79)'> Chat operation: </span>
1. The funnel begins after the first message from the client;
2. The bot also checks whether the person is in the database, and if not, then registers him in the database and the funnel begins;
3. in 10 minutes - Good afternoon!
4. in 90 minutes - I have prepared material for you;
5. Immediately after - Sending any photo;
6. After 2 hours, if the “Have a nice day” trigger is not found in the message history (on behalf of our account) - I’ll be back soon with new material!

### <span style='color:rgb(47, 79, 79)'> Usage. </span>
1. download project;
2. create telegram bot with BotFather, and copy token;
3. replace the token in the main.py file;
4. run program on computer or server.