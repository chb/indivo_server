from indivo.views.base import *
from indivo.views.documents.document import _get_document


@transaction.commit_on_success
def document_set_status(request, record, document_id):
  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  status_str, reason_str = 'status', 'reason'
  if not (request.POST.has_key(status_str) and \
          request.POST.has_key(reason_str) and \
          document.set_status(request, 
                              request.POST[status_str], 
                              request.POST[reason_str])):
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
