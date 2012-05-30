from indivo.tests.internal_tests import InternalTests
from indivo.validators import ValueInSetValidator, ExactValueValidator
from django.core.exceptions import ValidationError

VAL = 'abc'
VALS = ['bcd', 'cde', 4]
BAD_VALS = ['rst', 'piw', 3]

class ValidatorUnitTests(InternalTests):

    def setUp(self):
        super(ValidatorUnitTests, self).setUp()
        self.v_inset_null = ValueInSetValidator(VALS, nullable=True)
        self.v_inset = ValueInSetValidator(VALS)
        self.v_null = ExactValueValidator(VAL, nullable=True)
        self.v = ExactValueValidator(VAL)

    def tearDown(self):
        super(ValidatorUnitTests,self).tearDown()

    def test_valid_vals(self):
        
        # the correct single value should validate
        self.assertNotRaises(ValidationError, self.v, VAL)
        self.assertNotRaises(ValidationError, self.v_null, VAL)

        # correct values from the set should validate
        for v in VALS:
            self.assertNotRaises(ValidationError, self.v_inset, v)
            self.assertNotRaises(ValidationError, self.v_inset_null, v)


        # empty values should validate against nullable validators
        self.assertNotRaises(ValidationError, self.v_null, None)
        self.assertNotRaises(ValidationError, self.v_null, '')
        self.assertNotRaises(ValidationError, self.v_inset_null, None)
        self.assertNotRaises(ValidationError, self.v_inset_null, '')

    def test_invalid_vals(self):
        
        # incorrect values shouldn't validate
        for v in BAD_VALS:
            self.assertRaises(ValidationError, self.v, v)
            self.assertRaises(ValidationError, self.v_null, v)
            self.assertRaises(ValidationError, self.v_inset, v)
            self.assertRaises(ValidationError, self.v_inset_null, v)

        # empty values shouldn't validate against non-nullable validators
        self.assertRaises(ValidationError, self.v, None)
        self.assertRaises(ValidationError, self.v, '')
        self.assertRaises(ValidationError, self.v_inset, None)
        self.assertRaises(ValidationError, self.v_inset, '')
