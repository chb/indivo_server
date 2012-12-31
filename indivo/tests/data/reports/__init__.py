from allergy import TEST_ALLERGIES, TEST_ALLERGY_EXCLUSIONS, TEST_ALLERGIES_INVALID
from immunization import TEST_IMMUNIZATIONS
from lab_result import TEST_LAB_RESULTS
from lab_panel import TEST_LAB_PANELS
from medication import TEST_MEDICATIONS
from problem import TEST_PROBLEMS
from procedure import TEST_PROCEDURES
from clinical_note import TEST_CLINICAL_NOTES
from vital import TEST_VITALS
from social_history import TEST_SOCIAL_HISTORIES

TEST_REPORTS = (TEST_LAB_RESULTS
                + TEST_LAB_PANELS
                + TEST_ALLERGIES
                + TEST_ALLERGY_EXCLUSIONS
                + TEST_IMMUNIZATIONS
                + TEST_MEDICATIONS
                + TEST_PROBLEMS
                + TEST_PROCEDURES
                + TEST_CLINICAL_NOTES
                + TEST_VITALS
                + TEST_SOCIAL_HISTORIES)

TEST_REPORTS_INVALID = TEST_ALLERGIES_INVALID
