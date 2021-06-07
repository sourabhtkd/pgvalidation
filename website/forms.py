from django import forms

from website.models import Membership, DurationType


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['id', 'title', 'actual_price', 'duration_type', 'duration', 'created_on', 'is_active']

    def clean_duration(self):
        duration_type = self.cleaned_data.get('duration_type', '')

        if not duration_type:
            raise forms.ValidationError('select duration type first')

        duration = self.cleaned_data['duration']
        if duration_type == DurationType.DAY:
            if duration >= 30:
                raise forms.ValidationError('Use duration type month for 30 or more days')
        elif duration_type == DurationType.MONTH:
            if duration > 11:
                raise forms.ValidationError('Use Duration Type Year for 12 or more months')
        elif duration_type == DurationType.YEAR:
            pass
        return duration
