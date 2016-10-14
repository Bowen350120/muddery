
"""
This file checks user's edit actions and put changes into db.
"""

from django.db.models.fields.related import ManyToOneRel
from muddery.utils.exception import MudderyError
from muddery.worlddata.editor.form_view import FormView
from worlddata import forms


class DialogueView(FormView):
    """
    This object deal with dialogue's edit forms and views.
    """

    def parse_request(self):
        """
        Parse request data.

        Returns:
            boolean: Parse success.
        """
        if not super(DialogueView, self).parse_request():
            return False

        self.template_file = getattr(self.form_class.Meta, "form_template", "dialogue_form.html")
        return True

    def get_context(self):
        """
        Get render context.

        Returns:
            context
        """
        context = super(DialogueView, self).get_context()

        # Dialogue sentences
        # Get models and recoreds.
        try:
            sentence_form_class = forms.Manager.get_form("dialogue_sentences")
            model = sentence_form_class.Meta.model
        except Exception, e:
            raise MudderyError("Invalid form: %s." % "dialogue_sentences")

        context["sentence_title"] = model._meta.verbose_name_plural

        # Get dialogue's sentences.
        sentences = []
        sentence_fields = []
        if self.key:
            fields = model._meta.get_fields()
            sentence_fields = [field for field in fields if not isinstance(field, ManyToOneRel)]

            sentence_records = model.objects.filter(dialogue=self.key)
            sentences = [{"pk": record.pk, "items": [getattr(record, field.name, "") for field in fields]} for record in sentence_records]

        context["dialogue_key"] = self.key
        context["fields"] = sentence_fields
        context["sentences"] = sentences

        return context

    def delete_form(self):
        """
        Delete a record.

        Returns:
            HttpResponse
        """
        super(DialogueView, self).delete_form()

        # Delete dialogue sentences.
        if self.key:
            try:
                sentence_form_class = forms.Manager.get_form("dialogue_sentences")
                model = sentence_form_class.Meta.model
            except Exception, e:
                raise MudderyError("Invalid form: %s." % "dialogue_sentences")

            sentence_records = model.objects.filter(dialogue=self.key)
            sentence_records.delete()

        return self.quit_form()