from base import report_content_to_test_docs

_TEST_SOCIAL_HISTORIES = [
    """
    <Models xmlns="http://indivo.org/vocab/xml/documents#">
      <Model name="SocialHistory">
        <Field name="smoking_status_title">Former Smoker</Field>
        <Field name="smoking_status_code_title">Former Smoker</Field>
        <Field name="smoking_status_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
        <Field name="smoking_status_code_identifier">8517006</Field>
      </Model>
    </Models>
    """,
]

TEST_SOCIAL_HISTORIES = report_content_to_test_docs(_TEST_SOCIAL_HISTORIES)





