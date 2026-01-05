from django import forms
from .models import *

# ---------------------------
# LookupOption (with category assignment + validation)
# ---------------------------
class LookupOptionAdminForm(forms.ModelForm):
    class Meta:
        model = LookupOption
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        option_type = cleaned.get("option_type")
        category = cleaned.get("category")

        # EVENT_CATEGORY must not be assigned a sensory category
        if option_type == LookupOption.TYPE_EVENT_CATEGORY and category is not None:
            self.add_error("category", "Event category options must not have a sensory category (leave blank).")

        # All other option types must have a sensory category assigned
        if option_type and option_type != LookupOption.TYPE_EVENT_CATEGORY and category is None:
            self.add_error("category", "This option type must be assigned to a SensoryCategory.")

        return cleaned