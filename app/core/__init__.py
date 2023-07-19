"""
Core backend function like email sending.
"""

from . import security
from .config import settings
from .email_sender import send_email
