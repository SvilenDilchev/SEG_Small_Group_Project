from django import forms
from django.test import SimpleTestCase
from django.forms.widgets import TextInput
from django.template import Template, Context

from tasks.widgets import BootstrapDateTimePickerInput


class BootstrapDateTimePickerInputTestCase(SimpleTestCase):
    # The calendar date picker test class (uses a bootstrap widget)

    def test_widget_rendering(self):
        widget = BootstrapDateTimePickerInput()
        rendered = widget.render(
            "datetime_field", "2023-01-15 12:30", attrs={"id": "datetime_field"}
        )
        expected_html = """
        <div class="input-group date" id="datetimepicker_datetime_field" data-target-input="nearest">
        <input type="text" name="datetime_field" value="2023-01-15 12:30" id="datetime_field" data-target="#datetimepicker_datetime_field" class="form-control datetimepicker-input" format="%Y-%m-%d %H:%M">

        <div class="input-group-append" data-target="#datetimepicker_datetime_field" data-toggle="datetimepicker">
            <div class="input-group-text"><i class="fa fa-calendar"></i></div>
            </div>
        </div>

        <script>
        $(function () {
            $("#datetimepicker_datetime_field").datetimepicker({
                format: 'YYYY-MM-DD HH:mm',
            });
        });
        </script>
        """
        self.assertHTMLEqual(rendered, expected_html)

    def test_widget_context(self):
        widget = BootstrapDateTimePickerInput()
        context = widget.get_context(
            "datetime_field", "2023-01-15 12:30", attrs={"id": "datetime_field"}
        )

        self.assertIn("widget", context)
        self.assertIn("datetimepicker_id", context["widget"])

        expected_id = "datetimepicker_datetime_field"
        self.assertEqual(context["widget"]["datetimepicker_id"], expected_id)

    def test_template_used(self):
        widget = BootstrapDateTimePickerInput()
        template = widget.get_template_name()

        self.assertEqual(template, "widgets/bootstrap_datetimepicker.html")

    def test_widget_with_custom_attrs(self):
        widget = BootstrapDateTimePickerInput()
        rendered = widget.render(
            "datetime_field",
            "2023-01-15 12:30",
            attrs={"id": "custom_id", "class": "custom-class"},
        )

        expected_html = """
        <div class="input-group date" id="datetimepicker_datetime_field" data-target-input="nearest">
        <input type="text" name="datetime_field" value="2023-01-15 12:30" id="custom_id" class="form-control datetimepicker-input" data-target="#datetimepicker_datetime_field" format="%Y-%m-%d %H:%M">

        <div class="input-group-append" data-target="#datetimepicker_datetime_field" data-toggle="datetimepicker">
            <div class="input-group-text"><i class="fa fa-calendar"></i></div>
            </div>
        </div>

        <script>
        $(function () {
            $("#datetimepicker_datetime_field").datetimepicker({
                format: 'YYYY-MM-DD HH:mm',
            });
        });
        </script>
        """
        self.assertHTMLEqual(rendered, expected_html)
