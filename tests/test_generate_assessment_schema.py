from contextlib import contextmanager

import jsonschema
import pytest

from schema_generator.assessment import generate_schema


# we define a basic, assessment-passing, g9 declaration here (though interestingly it doesn't include informational
# fields so it wouldn't actually pass the *validation* schema). this could be fleshed out to enable it to be used as a
# common "example" valid declaration from other apps: having it live here in this repository and regularly checked
# in these tests ensures that it is always up to date with what is defined in the framework's yaml files... future work
# to look at.


def _definite_pass_g9_declaration():
    return {
        # discretionary
        "GAAR": False,
        "bankrupt": False,
        "confidentialInformation": False,
        "conflictOfInterest": False,
        "distortedCompetition": False,
        "distortingCompetition": False,
        "environmentalSocialLabourLaw": False,
        "graveProfessionalMisconduct": False,
        "influencedContractingAuthority": False,
        "misleadingInformation": False,
        "seriousMisrepresentation": False,
        "significantOrPersistentDeficiencies": False,
        "taxEvasion": False,
        "unspentTaxConvictions": False,
        "witheldSupportingDocuments": False,

        # mandatory
        "10WorkingDays": True,
        "MI": True,
        "accurateInformation": True,
        "accuratelyDescribed": True,
        "canProvideFromDayOne": True,
        "conspiracy": False,
        "corruptionBribery": False,
        "employersInsurance": (
            u"Not applicable - your organisation does not need employer\u2019s liability insurance because your "
            u"organisation employs only the owner or close family members."
        ),
        "environmentallyFriendly": True,
        "equalityAndDiversity": True,
        "fraudAndTheft": False,
        "fullAccountability": True,
        "helpBuyersComplyTechnologyCodesOfPractice": True,
        "informationChanges": True,
        "offerServicesYourselves": True,
        "organisedCrime": False,
        "proofOfClaims": True,
        "publishContracts": True,
        "readUnderstoodGuidance": True,
        "servicesDoNotInclude": True,
        "servicesHaveOrSupport": True,
        "termsAndConditions": True,
        "termsOfParticipation": True,
        "terrorism": False,
        "understandHowToAskQuestions": True,
        "understandTool": True,
        "unfairCompetition": True,
    }


@contextmanager
def _empty_context_manager():
    yield


@pytest.mark.parametrize("declaration_update,use_baseline,should_pass", (
    # a definite pass
    ({}, False, True,),
    ({}, True, True,),
    # pass with arbitrary other, hopefully ignored, fields
    ({"bullockbefriendingBard": "Bous Stephanoumenos"}, False, True,),
    ({"bullockbefriendingBard": "Bous Stephanoumenos"}, True, True,),
    # definite fails
    ({"readUnderstoodGuidance": False}, False, False,),
    ({"readUnderstoodGuidance": False}, True, False,),
    ({"employersInsurance": "Through metempsychosis"}, False, False,),
    ({"employersInsurance": "Through metempsychosis"}, True, False,),
    # discretionary
    ({"graveProfessionalMisconduct": True}, False, False,),
    ({"graveProfessionalMisconduct": True}, True, True,),
))
def test_g9_declaration_assessment(declaration_update, use_baseline, should_pass):
    # these test(s) are a bit funny in that they all make the same call to the function-under-test and then
    # assert a different thing about the return value, so we could improve on run time if necessary by only performing
    # the call once if necessary...
    schema = generate_schema("g-cloud-9", "declaration", "declaration")
    if use_baseline:
        schema = schema["definitions"]["baseline"]

    candidate = _definite_pass_g9_declaration()
    candidate.update(declaration_update)

    with (_empty_context_manager() if should_pass else pytest.raises(jsonschema.ValidationError)):
        jsonschema.validate(candidate, schema)
