"""
MeshBBS Meshtastic Interface

Provides the transport layer between the Meshtastic Python API
and the MeshBBS application.

Responsibilities
----------------
* Connect to a Meshtastic radio.
* Receive incoming packets.
* Ignore non-text packets.
* Ignore non-direct messages.
* Forward user messages into MeshBBS.
* Send replies back to the originating node.

No BBS business logic belongs in this module.
"""

from __future__ import annotations

from pubsub import pub
import meshtastic.serial_interface

from bbs.logger import get_logger
from bbs.application import MeshBBS
import time


class MeshtasticInterface:
    """
    Meshtastic transport layer.

    This class intentionally contains no business logic.

    It simply translates between Meshtastic packets and the
    MeshBBS application.
    """

    def __init__(
        self,
        application: MeshBBS,
    ) -> None:

        self.application = application

        self.logger = get_logger(__name__)

        self.interface: (
            meshtastic.serial_interface.SerialInterface | None
        ) = None

        self.logger.info(
            "Meshtastic interface created."
        )

    # ---------------------------------------------------------
    # Connection management
    # ---------------------------------------------------------

    def connect(self) -> None:
        """
        Connect to the attached Meshtastic radio.
        """

        self.logger.info(
            "Connecting to Meshtastic radio..."
        )

        self.interface = (
            meshtastic.serial_interface.SerialInterface()
        )

        pub.subscribe(
            self._on_receive,
            "meshtastic.receive",
        )

        self.logger.info(
            "Meshtastic connection established."
        )

    def close(self) -> None:
        """
        Close the Meshtastic interface.
        """

        self.logger.info(
            "Closing Meshtastic interface."
        )

        if self.interface is not None:
            self.interface.close()

            self.interface = None

        self.logger.info(
            "Meshtastic interface closed."
        )

    # ---------------------------------------------------------
    # Main loop
    # ---------------------------------------------------------

    def run(self) -> None:
        """
        Run the Meshtastic interface.

        After connecting, this method simply waits for incoming
        packets. Packet processing is performed by the PubSub
        callback.
        """

        if self.interface is None:
            raise RuntimeError(
                "Meshtastic interface is not connected."
            )

        self.logger.info(
            "MeshBBS is now listening for Meshtastic packets."
        )

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:

            self.logger.info(
                "Shutdown requested."
            )

        finally:
            self.close()

    # ---------------------------------------------------------
    # Packet callback
    # ---------------------------------------------------------

    def _on_receive(
        self,
        packet: dict,
        interface,
    ) -> None:
        """
        Invoked by the Meshtastic library whenever a packet
        is received.
        """

        try:

            self.logger.info(
                "Packet received."
            )

            self._log_packet(packet)

            if not self._is_text_packet(packet):

                self.logger.info(
                    "Ignoring non-text packet."
                )

                return

            if not self._is_direct_message(packet):

                self.logger.info(
                    "Ignoring channel message."
                )

                return

            node_id, short_name, long_name = (
                self._extract_sender(packet)
            )

            text = self._extract_text(packet)

            self.logger.info(
                "Direct message from %s (%s): %s",
                short_name,
                node_id,
                text,
            )

            self.logger.info(
                "Passing message to MeshBBS."
            )

            reply = self.application.handle_message(
                node_id=node_id,
                short_name=short_name,
                long_name=long_name,
                message=text,
            )

            if reply:

                self._send_reply(
                    destination=node_id,
                    message=reply,
                )

            self.logger.info(
                "Packet processing complete."
            )

        except Exception:

            self.logger.exception(
                "Unhandled exception while processing packet."
            )

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    def _log_packet(
        self,
        packet: dict,
    ) -> None:
        """
        Log the complete packet contents.

        During Sprint 12 this intentionally produces verbose
        logging to aid integration and debugging.
        """

        self.logger.info(
            "--------------------------------------------------"
        )

        self.logger.info(
            "Raw packet:"
        )

        self.logger.info(
            "%s",
            packet,
        )

        self.logger.info(
            "--------------------------------------------------"
        )
    # ---------------------------------------------------------
    # Packet inspection
    # ---------------------------------------------------------

    def _is_text_packet(
        self,
        packet: dict,
    ) -> bool:
        """
        Return True if this packet contains decoded text.

        Meshtastic places decoded application payloads inside
        the "decoded" section of the packet.

        If this assumption changes in future firmware versions,
        only this function should require modification.
        """

        decoded = packet.get("decoded")

        if decoded is None:
            return False

        return "text" in decoded


    def _is_direct_message(
        self,
        packet: dict,
    ) -> bool:
        """
        Return True if this packet is a Direct Message.

        IMPORTANT

        This function contains our only significant protocol
        assumption.

        During Heltec integration this should be the first
        function verified.

        If our assumption proves incorrect, only this function
        should require modification.
        """

        #
        # Initial assumption.
        #
        # Channel packets include "channel".
        # Direct messages do not.
        #

        return packet.get("channel") is None


    # ---------------------------------------------------------
    # Packet extraction
    # ---------------------------------------------------------

    def _extract_sender(
        self,
        packet: dict,
    ) -> tuple[str, str, str]:
        """
        Extract sender information.

        Returns

            node_id
            short_name
            long_name
        """

        from_id = packet.get("fromId", "UNKNOWN")

        user = packet.get("user", {})

        short_name = user.get(
            "shortName",
            from_id,
        )

        long_name = user.get(
            "longName",
            short_name,
        )

        return (
            from_id,
            short_name,
            long_name,
        )


    def _extract_text(
        self,
        packet: dict,
    ) -> str:
        """
        Extract decoded text payload.

        Returns an empty string if unavailable.
        """

        decoded = packet.get(
            "decoded",
            {},
        )

        return decoded.get(
            "text",
            "",
        )
    
    # ---------------------------------------------------------
    # Reply transmission
    # ---------------------------------------------------------

    def _send_reply(
        self,
        destination: str,
        message: str,
    ) -> None:
        """
        Send a reply back to a Meshtastic node.
        """

        if self.interface is None:
            raise RuntimeError(
                "Meshtastic interface is not connected."
            )

        self.logger.info(
            "Sending reply to %s",
            destination,
        )

        self.interface.sendText(
            text=message,
            destinationId=destination,
        )

        self.logger.info(
            "Reply sent."
        )