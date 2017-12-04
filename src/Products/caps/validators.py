"""Form validation"""

from plone.supermodel import model
from plone.directives import form
from plone.supermodel import model
from z3c.form import validator
from zope import schema
import zope.component

class PhoneNumberValidator(validator.SimpleFieldValidator):
    """z3c.form validator class for international phone numbers
    """

    def validate(self, value):
        """Validate international phone number on input
        """
        super(PhoneNumberValidator, self).validate(value)

        allowed_characters = '+- () / 0123456789'

        if value != None:
            value = value.strip()

            if value == '':
                # Assume empty string = no input
                return

            # The value is not required
            for c in value:
                if c not in allowed_characters:
                    raise zope.interface.Invalid(
                        _(u'Phone number contains bad characters')
                    )

            if len(value) < 7:
                raise zope.interface.Invalid(_(u'Phone number is too short'))


# Set conditions for which fields the validator class applies
validator.WidgetValidatorDiscriminators(
    PhoneNumberValidator,
    field=IPizzaOrder['phone_number']
)

# Register the validator so it will be looked up by z3c.form machinery
# this should be done via ZCML
zope.component.provideAdapter(PhoneNumberValidator)