import smtplib, os
from JumpScale import j
import JumpScale.baselib.mailclient
from JumpScale.portal.portal import exceptions


ujson = j.db.serializers.getSerializerType('j')


class system_emailsender(j.code.classGetBase()):

    """
    Email sender
    """
    # Maybe we can add this later
    output_format_mapping = {
        'json': ujson.dumps
    }

    def __init__(self):
        self._te = {}
        self.actorname = "emailsender"
        self.appname = "system"

   def format(self, obj, format=None):		
        if not format or format not in self.output_format_mapping:		
            format = 'json'		
        output_formatter = self.output_format_mapping[format]		
        return output_formatter(obj)

    def send(self, sender_name, sender_email, receiver_email, subject, body, *args, **kwargs):
        """
        param:sender_name The name of the sender
        param:sender_email The email of the sender
        param:receiver_email The email of the receiver
        param:subject Email subject
        param:body Email body
        result 'Success' in case of success, or 'Failure: ERROR_MSG' in case of the error message.
        """

        # The idea behind honeypots is simple. Most spamming bots are stupid & fill all the form fields, so if I put
        # an invisible field in the form it will be filled by the bot, but not by humans.
        #
        # For better protection, I can encode the names & IDs of the fields here, but this should be done at a later
        # time
        honeypot = kwargs.pop('honeypot', None)
        if honeypot:
            return 'Error: SPAMMER'

        kwargs.pop('ctx', None)

        # smtp_server, smtp_login, smtp_password = j.apps.system.contentmanager.dbmem.cacheGet(smtp_key)

        if sender_name:
            sender = '{0} <{1}>'.format(sender_name, sender_email)
        else:
            sender = sender_email

        # This is the same email pattern used in `contact_form` macro
        email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"
        if not j.codetools.regex.match(email_pattern, receiver_email):
            raise exceptions.BadReques('receiver email is not formatted well.')
        if not j.codetools.regex.match(email_pattern, sender_email):
            raise exceptions.BadReques('your email is not formatted well.')

        receivers = [receiver_email]
        j.clients.email.send(receivers, sender, subject, body)

        return 'Success'

