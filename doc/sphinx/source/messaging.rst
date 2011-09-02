Messaging and Notifications
===========================

In Indivo X, apps and users can message or notify each other. This page describes the various means 
of communication.

Messaging
---------

Messaging in Indivo is very much like email: every message has a subject and a body. 

Records vs. Accounts and Routing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Are messages sent to a record, or to an account? In Indivo X, messages can be sent to either one, 
but they always end up in an account's inbox (records don't have inboxes). In other words, if an 
app sends a message to a record, it is routed to a set of accounts with a note indicating which 
record it pertains to. The rules for routing record messages are, for now simple: the owner of the 
record and any account that has full access to that record receive a copy of a message sent to 
that record.

Message Content
^^^^^^^^^^^^^^^

Messages have a subject, a body, and a body type, which indicates the formatting of the body. (The 
subject can only be plain text.) The two body types supported at this time are plaintext and markdown. 
Plaintext is what it sounds like: text that is shown as is, without any HTML interpretation. 
`Markdown <http://daringfireball.net/projects/markdown/>`_ is a format that allows for simple markup 
features like bold, italics, and links, without all the complexity (and security complications) of HTML.

Specifics of Markdown
"""""""""""""""""""""

Markdown support in Indivo is in so-called "safe mode," where any HTML markup is silently stripped from 
the markdown content, and only markdown syntax is transformed into HTML bold, italics, and simple links. 
All links open up in new browser windows, except for links that are meant to send the user to the app 
that sent the message.

Specifically, with the following markdown syntax::

  Go [back to the FDA app]({APP_BASE}/message?id={MESSAGE_ID}) for more information.

Notice the URL contains standard URL template variable notation, using curly brackets. The variables 
``{APP_BASE}`` and ``{MESSAGE_ID}`` are substituted appropriately, and because this is a link to an app, 
clicking it will *not* open a new window, but rather send the user to that app, with the given URL.

Messaging a Record
^^^^^^^^^^^^^^^^^^

Messaging an Account
^^^^^^^^^^^^^^^^^^^^


Notifications
-------------

Notifications only pertain to records.
