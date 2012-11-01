from indivo.models import Fact
from indivo.fields import CodedValueField

class SocialHistory(Fact):
    smoking_status = CodedValueField()
