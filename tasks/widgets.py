from django import forms
from django.forms import TextInput


# A widget used to add a date picker in the form of a calendar allows you to choose a date in form:
# YYYY-MM-DD H:M
class BootstrapDateTimePickerInput(forms.DateTimeInput, TextInput):
    template_name = "widgets/bootstrap_datetimepicker.html"

    def get_context(self, name, value, attrs):
        datetimepicker_id = "datetimepicker_{name}".format(name=name)
        if attrs is None:
            attrs = dict()
        attrs["data-target"] = "#{id}".format(id=datetimepicker_id)
        attrs["class"] = "form-control datetimepicker-input"
        attrs["format"] = "%Y-%m-%d %H:%M"
        context = super().get_context(name, value, attrs)
        context["widget"]["datetimepicker_id"] = datetimepicker_id
        return context

    def get_template_name(self):
        return self.template_name


widgets = {
    "DateTimePicker": BootstrapDateTimePickerInput(),
}
