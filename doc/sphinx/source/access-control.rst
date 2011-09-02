Access Control
==============
After the credentials of a request have been verified using oAuth, incoming requests must 
only be allowed to access and manipulate data in ways consistent with their credentials. 
The Indivo access control module handles this authorization.

Key Goals
---------
The aim is to accomplish the following:

* Access Control abstracted from business logic.
* Deny-by-default Access Control: if an Indivo view is not explicitly given permissions, 
  it cannot be executed by anyone. 
* View-function-level access control: Indivo buys fully into the REST model: namely, if 2 
  users can access the same view function, they will get the same response from it. This 
  makes the view function a natural level of granularity for access control.
* Groupings of view functions based on their access requirements: view functions with similar 
  restriction levels should be groupable to make the system easier to use.

Example Usage
-------------
In order to illustrate the desired behavior of the system, we give an example of what a 
developer must do upon implementing a new view function. For this example, the view function  
will be 'get_carenet_document', which takes a carenet and a document id and returns the document. 
The developer must:

* Identify the set of role predicates that define access to the view function. In this case, anyone 
  in the same carenet as the document should be able to access the document, so the role predicate 
  ``IsInCarenet`` defines access to the view function.
* Build an access function, which takes the view function arguments and the principal and returns a 
  boolean indicating whether the principal may access the view function. For example::

    def carenet_document_access(principal, carenet):
      return principal.isInCarenet(carenet)

* Bind the view function to the access function by creating a new AccessRule object::
  
    AccessRule('Carenet Document Access', carenet_document_access, [get_carenet_document])

* Note that the third argument to the AccessRule constructor is a list of view functions. This means 
  that if there are other view functions which allow the same access as 'get_carenet_document', we 
  could group them in the AccessRule. For example::
  
    AccessRule('Carenet Document Access', carenet_document_access, 
               [get_carenet_document, get_carenet_immunization_list, get_carenet_medication_list])

And that's it! Now any principle in a carenet may attempt to get documents in the carenet. Note that the 
call may still return a 404 if the desired document isn't actually in the referenced carenet--but this not 
an access control issue. Also note that if the developer forgets to define a mapping from a view function 
to an access rule, all attempts to access the view will result in a 403 Access Denied error.

Components of the system
------------------------
As illustrated above, there are several components to the new access control system:

* An interface of role predicates that must be implemented by each subclass of Principal (right now 
  MachineApp, AccessToken, PHA, Account, ReqToken, NoUser). These roles encapsulate the relationships 
  between a principle and data, and include (but are not limited to at this point in time):

  * isProxiedByApp
  * createdAccount
  * createdRecord
  * ownsRecord
  * scopedToRecord
  * fullySharesRecord
  * isInCarenet

  A role predicate is defined as a function that returns true if the principal possesses that role with 
  respect to the passed data, and false if it doesn't. Each principal must implement all role predicates 
  that apply to it. The abstract Principle class will provide a default implementation that always returns 
  False, so unimplemented roles will deny by default.
* A set of access functions, which evaluate one or more role predicates above to determine whether a 
  principal may access data.
* A set of AccessRule objects, which preserve mappings from groups of view functions to access functions.

Authorization Pipeline
----------------------
When an incoming request is processed by the access control system, the following steps occur:

* The principal of the request is determined.
* The view function about to be accessed is looked up in the AccessRules mapping from view functions to 
  access functions, returning the corresponding access function
* That access function calls one or more data role predicates belonging to the request's principal, which 
  are evaluated based on the current principal's implementation.
* The access rule function returns true or false. If true, the request executes as normal. If false, a 403 
  Access Denied error is returned.
