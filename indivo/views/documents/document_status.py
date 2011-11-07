from indivo.views.base import *
from indivo.views.documents.document import _get_document


@transaction.commit_on_success
def document_set_status(request, record, document_id):
  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  status_str, reason_str = 'status', 'reason'
  try:
    document.set_status(request.principal, 
                        request.POST[status_str],
                        request.POST[reason_str])
  except:
    return HttpResponseBadRequest()

  return DONE

def document_status_history(request, record, document_id):
  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  return render_template('document_status_history', 
          { 'document_id'      : document.id,
            'document_history' : DocumentStatusHistory.objects.filter(
                                  record    = record.id, 
                                  document  = document.id)})
