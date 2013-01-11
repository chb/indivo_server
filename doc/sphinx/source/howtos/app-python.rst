===================================
Building an Indivo App using Python
===================================

This is a walkthrough on writing an Indivo X application that is embedded within Indivo X. In this example, the application will help to manage the user's medical problems (i.e. arthritis, hypertension, ...)

Getting Started
===============

An Indivo App is just a web site that:

* presents a web interface to the user, framed within the Indivo user interface
* connects to Indivo X on the backend to fetch and store data

The :doc:`Indivo API <../api-reference>` defines how to call the Indivo X server on the backend.

This document explains the details of how to build an Indivo app, using Python. Of course, any other programming language / web platform can be used following the same principles.

.. note::

	As of Indivo X Beta 1, this problems app is fully integrated into the Indivo UI Server, for ease of deployment. This does not change the fact that you can and should build additional apps as separate servers.

Scope
-----

Our sample application will help track a user's medical problem list, using coded-value lookups to fill in the problem name.

General Architecture and User Flow
----------------------------------

A user will add the Indivo Problems application to their record on demand, or it may be added for them by an administrative application. User Authentication is entirely performed via Indivo.

Indivo Problems will store all of its data in Indivo X, using the :doc:`Problem data model <../data-models/problem>`. Notes added to the problem will be stored as standard annotations. Thus, Indivo Problems does not require anything other than application logic: no database, no authentication mechanism, just HTML serving and access to the Indivo X API.

Authentication
==============

The steps involved in adding an application to an Indivo record are:

* the user navigates to the *App Settings* pane in Indivo 
* Indivo lists the available applications, including Indivo Problems, which the user selects and enables.
* Indivo opens up an IFRAME onto the app's ``index`` URL, with either ``record_id`` or ``carenet_id`` as a URL query parameter.
* The app begins an oAuth authorization protocol with the Indivo backend server.
* The IFRAME is redirected to the Indivo authorization screen
* when the user approves the app, the IFRAME is redirected to the app's ``oauth_callback`` URL, which can now complete the oAuth process and access Indivo.

Thus, our application needs:

* an ``index`` URL::
	
		/start_auth?record_id={record_id}&carenet_id={carenet_id}

  .. note:: 
	
  	Only one of those two params will be filled in.

* an ``oauth_callback`` URL that complies with the oAuth protocol (v1.0a)::

	/after_auth?oauth_token={oauth_token}&oauth_verifier={oauth_verifier}

**IMPORTANT**: the Indivo system is split into a UI server, which presents the HTML user interface, and a BACKEND server, which communicates only in XML. The oAuth process involves both servers: oAuth calls are made against the BACKEND server, while the browser is redirected to the UI server.

Understanding Record-Based vs. Carenet-Based
--------------------------------------------

When an app is invoked in Indivo, it is either invoked at the record level, or at the carenet level. A record-level app launch means that the app is launched by the record-owner, and can access all of that user's data. A carenet-level app launch means that the app is launched by a guest of the record-owner, and can see only limited data within that specific carenet. In general record-level apps display additional logic that carenet-level apps do not, e.g. the sharing controls.

Authentication Logic
--------------------

Let's build the logic for these two entry points.

Start
^^^^^

We start with a python function declaration::

	def start_auth(request):
	   """
	   begin the oAuth protocol with the server
	   """

and now we need access to Indivo to get our oAuth request token from the backend server::

    server_params = {"api_base": settings.INDIVO_SERVER_LOCATION,
                                "authorization_base": settings.INDIVO_UI_SERVER_BASE}
    consumer_params = settings.INDIVO_SERVER_OAUTH
    client = IndivoClient(server_params, consumer_params)

Note how we're pulling the credentials from the Django settings, which are stored in ``settings.py``
Also, in the actual codebase, we've modularized this to a ``get_indivo_client`` function.

Next, we check to see if we were passed a ``record_id`` or ``carenet_id`` parameter, which is what happens when Indivo opens up an IFRAME onto our start URL, since it knows exactly what record (or carenet) is currently being accessed. We use this ``record_id`` or ``carenet_id`` to set up our oAuth parameters, and then get ourselves a request token::

    # do we have a record_id or carenet_id?
    record_id = request.GET.get('record_id', None)
    carenet_id = request.GET.get('carenet_id', None)
 
    # prepare request token parameters
    params = {'oauth_callback':'oob'}
    if record_id:
        params['indivo_record_id'] = record_id
    if carenet_id:
        params['indivo_carenet_id'] = carenet_id
 
    # request a request token
    request_token = client.fetch_request_token(params)

Now that we have this request token, it's time to store it in the web session for later and send the user to Indivo for authorization::

    # store the request token in the session for when we return from auth
    request.session['request_token'] = request_token
       
    # redirect to the UI server
    return HttpResponseRedirect(client.auth_redirect_url)

The redirect is now to the UI server, which is different from the backend server (the client takes care of this detail for you, since you simply ask for the ``auth_redirect_url``)

And that's it, we're finished with half of the code needed to connect an app with Indivo X for authentication and medical-record connectivity!

Post Auth
^^^^^^^^^

Once the user has approved the application for addition, Indivo X will redirect the user to the ``oauth_callback`` URL at our Problems App web server, and now it's time for us to complete the authentication process by converting our request token into an access token. We start with a new Python function::

	def after_auth(request):
	   """
	   after Indivo authorization, exchange the request token for an access token and store it in the web session.
	   """

Then, we retrieve the request token we stored in the session, as well as the token string and oauth verifier we receive as URL parameters::

    # get the token and verifier from the URL parameters
    oauth_token, oauth_verifier = request.GET['oauth_token'], request.GET['oauth_verifier']
 
    # retrieve request token stored in the session
    token_in_session = request.session['request_token']

We quickly check that the token in the URL parameter matches the web session, just to be extra safe::

    # is this the right token?
    if token_in_session['oauth_token'] != oauth_token:
        return HttpResponse("uh oh bad token")

Then we connect to Indivo using the consumer secret but also the request-token details to exchange the request token for an access token::

    # get the indivo client and use the request token as the token for the exchange
    server_params = {"api_base": settings.INDIVO_SERVER_LOCATION,
                                "authorization_base": settings.INDIVO_UI_SERVER_BASE}
    consumer_params = settings.INDIVO_SERVER_OAUTH
    client = IndivoClient(server_params, consumer_params)
    client.update_token(token_in_session)
    access_token = client.exchange_token(oauth_verifier)

Once again, in the actual code, we've modularized the client creation to the ``get_indivo_client`` function.

And that's it, we're fully connected! We now store the access token details in the web session for later use, and redirect to the app's homepage::

    # store stuff in the session
    request.session['access_token'] = access_token
 
    # depending on whether we get a record or carenet id back.
    if access_token.has_key('xoauth_indivo_record_id'):
        request.session['record_id'] = access_token['xoauth_indivo_record_id']
    else:
        request.session['carenet_id'] = access_token['xoauth_indivo_carenet_id']
 
    # go to list of problems
    return HttpResponseRedirect("/")

Notice how the access token came back with an extra parameter that indicates the identifier of the Indivo record we just managed to bind, or of the carenet.

URL handlers
------------

We build URL handlers in Django's ``urls.py``::

	from views import start_auth, after_auth
	
	urlpatterns = patterns(' ',
	    # authentication
	    (r'^start_auth', start_auth),
	    (r'^after_auth', after_auth),

Recording and Displaying Problems
=================================

The rest of the application is a standard web app that displays a list of problems and lets the user add a new one. The generic web components are best explained by the existing Django documentation. Here, we cover briefly the Indivo-specific touchpoints.

Getting information from Indivo
-------------------------------

Every call to the Indivo Problem List app requires information from Indivo. Thus, in every call, it is useful to set up the client front-end to Indivo as::

    server_params = {"api_base": settings.INDIVO_SERVER_LOCATION,
                                "authorization_base": settings.INDIVO_UI_SERVER_BASE}
    consumer_params = settings.INDIVO_SERVER_OAUTH
    client = IndivoClient(server_params, consumer_params)
    client.update_token(request.session['access_token'])

In the Indivo Problem List code, this is packaged as ``get_indivo_client`` in the ``utils.py`` file.

Reading a list of Problems
--------------------------

Though each problem is its own Indivo document, problems might come from a CCR, from a list of problems in another schema, etc... Thus, it is always best to access Problems through our :ref:`reporting APIs <reporting-APIs>` when listing problems, which will list all of the reports processed from all input documents.

The call is slightly different depending on whether this is a record or carenet (eventually, Indivo may provide a single API call to make this easier, but for now we must differentiate)::

    client = get_indivo_client(request)
 
    if request.session.has_key('record_id'):
        record_id = request.session['record_id']
        
        # Note that we're asking for our response data in JSON form: we could also get it as XML or RDF
        resp, content = client.generic_list(record_id=record_id, data_model="Problem", body={'response_type':'application/json'})
        if resp['status'] != '200':
            # TODO: handle errors
            raise Exception("Error reading problems: %s"%content)
        probs = simplejson.loads(content)

    else:
        carenet_id = request.session['carenet_id']
        # Read problems from the carenet: This also returns JSON, which is the default return type for data
        resp, content = client.carenet_generic_list(carenet_id=carenet_id, data_model="Problem")
        if resp['status'] != '200':
            # TODO: handle errors
            raise Exception("Error reading problems from carenet: %s"%content)
        probs = simplejson.loads(content)

Notice that we've used the simplejson library to parse our JSON return data. It is now available to us in the ``probs`` variable, as a python array that will look like::

	[
	    {
	    "__modelname__": "Problem",
	    "__documentid__":"12345",
	    "startDate": "2009-05-16T12:00:00Z",
	    "endDate": "2009-05-16T16:00:00Z",
	    "name_title": "Backache (finding)",
	    "name_system": "http://purl.bioontology.org/ontology/SNOMEDCT/",
	    "name_identifier": "161891005"
	    }, 
	    ... More Problems ...
	]

Creating a Document
-------------------

To create a document, one must first put together the necessary XML. The way we do this in our sample application is to use Django's templating system to interpolate values into the XML template for ``Problem``::

    # get the variables and create a problem XML
    params = {'coding_system': 'http://purl.bioontology.org/ontology/SNOMEDCT/', 
                     'date_onset': request.POST['date_onset'], 
                     'date_resolution': request.POST['date_resolution'], 
                     'code_fullname': request.POST['code_fullname'], 
                     'code': request.POST['code'], 
                     'comments' : request.POST['comments']}
    problem_xml = render_raw('problem', params, type='xml')
  
Then, we submit this as a new document::

    resp, content = client.document_create(record_id=request.session['record_id'], body=problem_xml, 
                                                                  content_type='application/xml')
    if resp['status'] != '200':
        # TODO: handle errors
        raise Exception("Error creating new problem: %s"%content)

Coded Values
^^^^^^^^^^^^ 

In the course of creating a document, one needs to access coded values, for example SNOMED codes. Indivo makes coded values available via its API, e.g::

    resp, content = client.coding_system_query(system_short_name='snomed', body={'q':query})
   
which will return a JSON list of codes, each with properties ``abbrev``, ``code``, ``physician_value``, ``umls_code``, and ``consumer_value``.

In our sample application, we take this return value and format it for the `jQuery Autocomplete Plugin <ttp://www.devbridge.com/projects/autocomplete/jquery/>`_::

    query = request.GET['query']
 
    resp, content = client.coding_system_query(system_short_name='snomed', body={'q':query})
    if resp['status'] != '200':
        # TODO: handle errors
        raise Exception("Error getting coding systems data: %s"%content)
    codes = simplejson.loads(content)
    formatted_codes = {'query': query, 'suggestions': [c['consumer_value'] for c in codes], 'data': codes} 
    return HttpResponse(simplejson.dumps(formatted_codes), mimetype="text/plain")

Reading a single Document
-------------------------

From the report, we can get the ``document_id`` from which each problem is extracted. Using this ``document_id``, it's easy to get the original document itself. In this case, the document won't contain any extra information form what was found inside the report, but oftentimes the document will contain more detail or other contextual data.

Again, we must be conscious of whether this is within a record or carenet::

    record_id = request.session.get('record_id', None)
 
    if record_id:
        resp, content = client.record_specific_document(record_id=record_id, document_id=problem_id)
        if resp['status'] != '200':
            # TODO: handle errors
            raise Exception("Error fetching document: %s"%content)
        doc_xml = content

    else:
        carenet_id = request.session['carenet_id']
        # read the document
        resp, content = client.carenet_document(carenet_id=carenet_id, document_id=problem_id)
        if resp['status'] != '200':
            # TODO: handle errors
            raise Exception("Error fetching document from carenet: %s"%content)
        doc_xml = content

Notifying the Record
--------------------

Sometimes, a PHA needs to notify a record of some action::

     client.record_notify(record_id=request.session['record_id'], 
                                    body={'content':'a new problem has been added to your problem list'})

Adding UI Widgets
=================

Indivo X, as of alpha 2, supports UI widgets that an app can easily integrate into its interface. The first such widget is "Sharing and Audit", which lets a user modify the sharing preferences and quickly view the audit log for a particular document. This sharing widget should really only be displayed when the app is *record-level*.

Getting SURL Credentials
------------------------

To invoke a widget, an app must first generate SURL credentials, i.e. credentials that will allow it to generate Signed URL. Signed URLs ensure that only authorized apps can embed a specific widget. Fortunately, the Indivo client provides a simple built-in method for generating these SURL credentials::

    surl_credentials = client.get_surl_credentials()

Setting up the JavaScript
-------------------------

Once SURL credentials have been generated, it's time to load the widget JavaScript and initialize it. This is done in the HTML template::

    <script src="{INDIVO_UI_SERVER_BASE}/lib/widgets.js"></script>

then::

    <script>
      Indivo.setup('{INDIVO_UI_SERVER_BASE}');
    </script>

and::

    <script>
      Indivo.Auth.setToken("{surl_credentials.token}","{surl_credentials.secret}");
    </script>

Adding the Widget
-----------------

Finally, it's time to add the widget::

	{% if record_id %}
		<script>
			Indivo.Widget.DocumentAccess.add('{record_id}', '{problem_id}');
		</script>
	{% endif %}

Note how this widget is only added if there is a ``record_id``, since a carenet-level app should not display the sharing widget. And, in fact, if it tried, it wouldn't know the ``record_id`` needed, and if it guessed it correctly it would not have the right permissions to do so.
