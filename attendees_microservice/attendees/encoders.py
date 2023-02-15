from common.json import ModelEncoder
from .models import Attendee, ConferenceVO, AccountVO


class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceVODetailEncoder(),
    }

    def get_extra_data(self, o):
        account_count = AccountVO.objects.filter(email=o.email).count()
        print(o.email)
        return {"has_account": account_count > 0}
