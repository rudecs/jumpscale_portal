{% extends ".space/default.md" %}

{% block body %}

###Edit $$page page

{{edit_markdown: app:$$app actor:$$actor space:$$space bucket:$$bucket path:$$path page:$$page}}

{% endblock %}