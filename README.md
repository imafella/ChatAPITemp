# ChatAPI
API designed around IM functionality. 

Project Guidelines:
- APIs should be designed with following requirements in mind:
    - one-on-one chat between users
    - group chats
    - multimedia messages
    - reaction to messages
    - editing/deleting a message
    - view past messages of a chat 
    - Add/remove participants in a group chat

- You are not required to develop UI/client for this API server.
- Ensure to adhere to coding standards and best practices for maintainability, security and scalability.
- Feel free to incorporate any creative elements that you deem essential but are not mentioned as a requirement in this assessment
- Please document your code and explain your approach
- Include notes about any limitations of your approach and how you could improve it further if you had more time to work on it.

This is a Python Flask application meant to simulate interactions of an IM messenger client.


Assumptions:
    Some Database exists for Users
    Some Database exists for Chats
    Some Database exists for Messages
    Some Database exists for Reactions
    No Auth piece was req at the time of this project, in place some calls expect a 'user' field in the header that houses the DB id of the user.
    No Admin piece was added. A field was made to promote a user to admin, it remains without function.

A Yaml is included to detail how the REST Api is meant to work. Open it with a nice viewer such as https://editor.swagger.io/
Some things in the YAML are outdated as things changed during the development. The YAML was created first before any code was written. Some things were updated in it on the fly. Other changes may have been missed.

Given the Time constraint of Friday days end, The requested Media piece is implemented in an incomplete state. It has not been tested. However the database has a field to house the binary of the file and the file type.
At this time, the feature is incomplete however.

As per the guidelines, the following is my response:

APIs should be designed with following requirements in mind:

    - one-on-one chat between users
    - group chats
	Both of the above points don't matter to an API. I have created a chat that allows users to add or remove other users on the fly. It is possible to move from a one on one chat to a group to having no other users in the chat. 

    - multimedia messages
	As stated above, incomplete due to EOD of Friday.

    - reaction to messages
	Implimented /message/{messageId}/reaction, 
	also capability to edit and delete /reaction/{reactionId}.

    - editing/deleting a message
	Implimented using /message/{messageId} endpoints

    - view past messages of a chat 
	At present all messages load in bulk. Given more time pagination would have been applied.

    - Add/remove participants in a group chat
	PATCH /chat/{chatId} detailed in the YAML and the Postman collection.

I opted for flask as it was a framework I had heard of and given the timeframe mild familiarity was favored over spending more time researching other comperable frameworks.

The order this project was completed is detailed in the git history. It was a fun time.


    