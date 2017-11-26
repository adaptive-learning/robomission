"""Services for user-provided feedback.
"""
import logging
from django.core.mail import mail_managers

LOGGER = logging.getLogger(__name__)

MIN_N_WORDS = 4

FEEDBACK_TEMPLATE = """
comment:
{comment}

email:
{email}

user:
{user}

url:
{url}

time:
{time}
"""

def log_and_send(feedback):
    feedback_text = to_text(feedback)
    LOGGER.info('New feedback: ' + feedback_text)
    if is_likely_worthless(feedback):
        return
    mail_feedback(feedback_text)

def to_text(feedback):
    return FEEDBACK_TEMPLATE.format(
        comment=feedback.comment,
        email=feedback.email if feedback.email else '[missing]',
        user=feedback.user.pk if feedback.user else '[missing]',
        url=feedback.url,
        time=feedback.inserted)


def is_likely_worthless(feedback):
    return len(feedback.comment.split()) < MIN_N_WORDS


def mail_feedback(feedback_text):
    mail_managers(subject='Feedback Message', message=feedback_text)
