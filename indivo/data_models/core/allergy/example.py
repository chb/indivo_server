from indivo.models import Allergy
from indivo.lib.iso8601 import parse_utc_date as date

allergy_fact = Allergy(
    date_diagnosed=date("2009-05-16"),
    diagnosed_by="Children's Hospital Boston",
    allergen_type="Drugs",
    allergen_type_type="http://codes.indivo.org/codes/allergentypes/",
    allergen_type_value="123",
    allergen_name="Penicillin",
    allergen_name_type="http://codes.indivo.org/codes/allergens/",
    allergen_name_value="234",
    allergen_name_abbrev="PCN",
    reaction="Blue Rash",
    specifics="This only happens on weekends."
    )
