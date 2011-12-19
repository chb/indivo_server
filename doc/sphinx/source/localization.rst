Indivo Localization
===================

Indivo is developed entirely in America, and all of its text is written in English. However, the value 
of a PCHR should not be limited to those who can read a specific language, and all of Indivo's core 
functionality is not language-specific. Indivo therefore provides functionality for **Localization** 
(abbreviated L10n), or adapting the software for use in a specific region by translating its text. 
Indivo builds upon Django's native support for L10n in order to accomplish this.

Overview
--------

There are four main steps involved in localizing Indivo: marking strings for translation, creating 
language files for a specific locale, translating the strings, and compiling the translated strings. 
This document will cover each of these steps. Note that all Indivo Localization is implemented in our 
reference `UI Server <http://www.github.com/chb/indivo_ui_server>`_, as Indivo Server itself produces 
pure XML, not human-readable text. Any Indivo UI app written in Django could use the same steps to achieve 
localization, however.

Supported Locales
-----------------

You may not have to go to the trouble to do any translation. Below is a list of currently supported 
languages that Indivo has already been translated into:

* en_US: American English

If you found your language on the above list, simply edit your settings.py file as described 
:ref:`below <localization-wrapping-up>` and Indivo will be automatically translated for you.

Marking Strings for Translation
-------------------------------

In order to translate Indivo, all human-readable text produced by the UI must be identified for 
translation. We've taken a first stab and identified most of the strings that we think need to be 
translated, but we may well have missed some. If you find an untranslated string in the source code 
that needs translation, you can mark it as follows:

* Surround the text with ``{% trans %}`` tags. For example, ::
  
    <h>ENGLISH HEADER</h>
 
  becomes ::

    <h>{% trans "ENGLISH HEADER" %}</h>

* If the text is a block paragraph, or contains other Django template tags, use the ``{% blocktrans %}`` tag::

    <nowiki><p>Now I'm talking about something important! And refering to the variable {{var}}!</p></nowiki>

  becomes ::

    <nowiki><p>{% blocktrans %}Now I'm talking about something important! And refering to the variable {{var}}!
    {% endblocktrans %}</p></nowiki>

* Note: Indivo UI Server produces text in ``.html`` files, ``.ejs`` files, and ``.js`` files. We've added 
  some code to allow you to treat all of these files the same way: simply wrap the string you want translated 
  in the appropriate Django tags.

* For more detailed information, see Django's documentation on this 
  `here <https://docs.djangoproject.com/en/1.0/topics/i18n/#in-template-code>`_.

* Tell us about your changes! Submit a github pull request, and we will incorporate your tagged strings so that 
  others can translate them into all of the Indivo supported locales.

Creating Message Files
----------------------

Generate the File
^^^^^^^^^^^^^^^^^

Once you've indicated which strings should be translated, Django will create a single file containing all of the 
strings you need to translate in order to localize Indivo. This file, called a 'message file', has the extension 
``.po`` and can be created by running (from the top-level ``indivo_ui_server directory``)::

  python manage.py makemessages -l LOCALE -e .html,.ejs,.py

Where ``LOCALE`` refers to the language code you wish to translate to, indicated in what Django calls 
`'locale name format' <https://docs.djangoproject.com/en/1.2/topics/i18n/#term-locale-name>`_. Basically, this 
means that the language code takes the form ``ll[_CC]``, where the first two characters, lowercase, represent 
the desired language, and the optional last two characters, uppercase, represent the country variant of the 
language. For example, ``it`` for italian, and ``pt_BR`` for Brazilian portuguese. For a complete listing of the 
locales that Django current supports, see 
`the listing in their source code <https://code.djangoproject.com/browser/django/trunk/django/conf/locale>`_.

A Look at the File
^^^^^^^^^^^^^^^^^^

If you open your ``*.po`` file, which was placed in ``indivo_ui_server/locale/LOCALE/LC_MESSAGES/``, you will see, 
for each marked string, the following structure::

  #: path/to/python/module.py:23
  msgid "Welcome to my site."
  msgstr ""

The line beginning with ``#`` indicates the source file where the message came from, the ``msgid`` line is the 
original English text to be translated, and the ``msgstr`` line is where you will write your translations.

Translating Strings
-------------------

Unfortunately, Django isn't smart enough to actually do all of the translation for you (and if it did, Indivo 
would come out looking like it had been run through Google translate). To get an accurate translation of Indivo 
into your local language, you will need to go through the .po file generated in the previous section and 
translate each string indicated by a line beginning with ``msgid``. For each such string, translate the 
string into your local language, and place the result in the line just below it (starting with ``msgstr``). 
This is the tedious part of localization, but it is a necessary one to insure a complete translation.

Compiling Message Files
-----------------------

Now that you've translated Indivo, you need to get those translations into a pre-compiled format so that Django 
can be efficient in translating Indivo in realtime. This is done with a simple command::

  python manage.py compilemessages

This compiles your ``*.po`` file into a ``*.mo`` file, which Django uses when Indivo is running.

**Note:** If you ever go back and change any of your translated strings in the ``*.po`` file, you'll need to recompile 
the file into a ``*.mo`` file. Likewise, if you mark additional strings for translation, you'll need to 
regenerate the message file for the new strings to be available for translation.

.. _localization-wrapping-up:

Wrapping Up
-----------

And that's it! You've successfully translated Indivo. A few final things to consider:

* If you ever go back and change any of your translated strings in the ``*.po`` file, you'll need to recompile 
  the file into a ``*.mo`` file. Likewise, if you mark additional strings for translation, you'll need to 
  regenerate the message file for the new strings to be available for translation.

* You still need tell Indivo to translate into your particular language: you can do this by editing 
  ``indivo_ui_server/settings.py`` and changing the ``LANGUAGE_CODE`` setting to match your current locale. 
  Note that in ``settings.py``, the ``LANGUAGE_CODE`` should be of the form ``ll[-cc]``, not ``ll[_CC]`` 
  (note the dash separator and lowercase country code).

* If you've translated Indivo into a new lanuage, we want to hear about it! Submit your translation to us as a pull 
  request on github, and we'll make sure that others have access to it.

* For a more detailed description of how Django handles L10n, see 
  https://docs.djangoproject.com/en/1.2/topics/i18n/localization/.
