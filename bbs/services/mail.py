"""
Mail service.

Implements the business logic for private mail.
"""

from __future__ import annotations

from datetime import UTC, datetime

from bbs.context import ExecutionContext
from bbs.models import Mail
from bbs.repositories.mail import MailRepository
from bbs.repositories.users import UserRepository


class MailService:
    """Business logic for private mail."""

    def __init__(
        self,
        mail: MailRepository,
        users: UserRepository,
    ) -> None:
        self._mail = mail
        self._users = users

    def send(
        self,
        context: ExecutionContext,
        recipient_short_name: str,
        subject: str,
        body: str,
    ) -> int:
        """
        Send a private message.

        Returns the new mail ID.
        """

        recipient = self._users.find_by_short_name(
            recipient_short_name.strip(),
        )

        if recipient is None:
            raise ValueError("Unknown recipient.")

        subject = subject.strip()
        body = body.strip()

        if not subject:
            raise ValueError("Subject cannot be empty.")

        if not body:
            raise ValueError("Message body cannot be empty.")

        mail = Mail(
            id=None,
            sender_node_id=context.node_id,
            recipient_node_id=recipient.node_id,
            subject=subject,
            body=body,
            created=datetime.now(UTC).isoformat(timespec="seconds"),
            read_at=None,
        )

        return self._mail.add(mail)

    def read(
        self,
        mail_id: int,
    ) -> Mail | None:
        """
        Read a message.

        Marks the message as read the first time it is opened.
        """

        mail = self._mail.get(mail_id)

        if mail is None:
            return None

        display_name = self._users.get_display_name(
            mail.sender_node_id
        )

        if display_name is not None:
            mail.sender_node_id = display_name

        if mail is None:
            return None

        if mail.read_at is None:
            timestamp = datetime.now(
                UTC
            ).isoformat(timespec="seconds")

            self._mail.mark_read(
                mail_id,
                timestamp,
            )

            mail.read_at = timestamp

        return mail

    def list(
        self,
        context: ExecutionContext,
    ) -> list[Mail]:
        """Return the authenticated user's inbox."""

        inbox = self._mail.get_for_recipient(
            context.node_id,
        )

        for mail in inbox:
            display_name = self._users.get_display_name(
                mail.sender_node_id
            )

            if display_name is not None:
                mail.sender_node_id = display_name

        return inbox

    def delete(
        self,
        mail_id: int,
        context: ExecutionContext,
    ) -> None:
        """
        Delete a message.

        The recipient may delete their own mail.
        SYSOP may delete any message.
        """

        mail = self._mail.get(mail_id)

        if mail is None:
            return None

        display_name = self._users.get_display_name(
            mail.sender_node_id
        )

        if display_name is not None:
            mail.sender_node_id = display_name

        if (
            mail.recipient_node_id != context.node_id
            and not context.is_admin
        ):
            raise PermissionError(
                "Permission denied."
            )

        self._mail.delete(mail_id)