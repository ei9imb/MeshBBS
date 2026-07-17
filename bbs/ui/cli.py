"""
Interactive command-line interface for MeshBBS.
"""

from __future__ import annotations

from pathlib import Path

from bbs.commands.router import CommandRouter


class CommandLineInterface:
    """Interactive console interface."""

    def __init__(self, router: CommandRouter) -> None:
        self._router = router
        self._menu = "main"

        self._bulletin_subject = ""
        self._bulletin_body = ""
        self._selected_bulletin = ""
        self._mail_recipient = ""
        self._mail_subject = ""
        self._mail_body = ""
        self._selected_mail = ""

    def run(self) -> None:
        """Run the interactive command loop."""

        self._display_banner()

        while True:
            command = input(f"{self._menu}> ").strip()

            if self._menu == "main" and command.upper() == "E":
                self._display_main_menu()
                continue

            #
            # BULLETINS MENU
            #

            if self._menu == "bulletins":
                match command.upper():

                    case "P":
                        self._menu = "post_subject"

                        print()
                        print("Post Bulletin")
                        print("--------------")
                        print()
                        print("Enter subject:")
                        print()

                        continue

                    case "R":
                        self._menu = "bulletin_select"

                        response = self._router.execute("LB")

                        print()
                        print(response)
                        print()
                        print("Enter bulletin number.")
                        print("[B]ack")
                        print()

                        continue

                    case "D":
                        self._menu = "bulletin_delete_select"

                        response = self._router.execute("LDB")

                        print()
                        print(response)
                        print()
                        print("Enter bulletin number.")
                        print("[B]ack")
                        print()

                        continue

                    case "B":
                        self._display_main_menu()
                        continue

            #
            # POST BULLETIN
            #

            if self._menu == "post_subject":

                self._bulletin_subject = command
                self._menu = "post_body"

                print()
                print("Enter bulletin body:")
                print()

                continue

            if self._menu == "post_body":

                self._bulletin_body = command
                self._menu = "post_confirm"

                print()
                print("Subject :", self._bulletin_subject)
                print("Body    :", self._bulletin_body)
                print()
                print("[P]ost")
                print("[B]ack")
                print()

                continue

            if self._menu == "post_confirm":

                match command.upper():

                    case "P":

                        response = self._router.execute(
                            f"PB.{self._bulletin_subject}.{self._bulletin_body}"
                        )

                        print()
                        print(response)
                        print()

                        self._bulletin_subject = ""
                        self._bulletin_body = ""

                        self._display_bulletins_menu()

                        continue

                    case "B":

                        self._bulletin_subject = ""
                        self._bulletin_body = ""

                        self._display_bulletins_menu()

                        continue

            #
            # READ BULLETINS
            #

            if self._menu == "bulletin_select":

                match command.upper():

                    case "B":
                        self._display_bulletins_menu()
                        continue

                response = self._router.execute(f"RB.{command}")

                print()
                print(response)
                print()
                print("[B]ack")
                print()

                self._menu = "bulletin"

                continue

            if self._menu == "bulletin":

                match command.upper():

                    case "B":

                        self._menu = "bulletin_select"

                        response = self._router.execute("LB")

                        print()
                        print(response)
                        print()
                        print("Enter bulletin number.")
                        print("[B]ack")
                        print()

                        continue

            #
            # DELETE BULLETINS
            #

            if self._menu == "bulletin_delete_select":

                match command.upper():

                    case "B":
                        self._display_bulletins_menu()
                        continue

                self._selected_bulletin = command
                self._menu = "bulletin_delete_confirm"

                print()
                print(f"Delete bulletin {command}?")
                print()
                print("[Y]es")
                print("[N]o")
                print()

                continue

            if self._menu == "bulletin_delete_confirm":

                match command.upper():

                    case "Y":

                        response = self._router.execute(
                            f"DB.{self._selected_bulletin}"
                        )

                        print()
                        print(response)
                        print()

                        self._selected_bulletin = ""

                        self._display_bulletins_menu()

                        continue

                    case "N":

                        self._selected_bulletin = ""

                        self._display_bulletins_menu()

                        continue

            #
            # MAIL MENU
            #

            if self._menu == "mail":

                match command.upper():

                    case "S":

                        self._menu = "mail_recipient"

                        print()
                        print("Send Mail")
                        print("---------")
                        print()
                        print("Recipient short name:")
                        print()

                        continue

                    case "R":

                        self._menu = "mail_select"

                        response = self._router.execute("LM")

                        print()
                        print(response)
                        print()
                        print("Enter mail number.")
                        print("[B]ack")
                        print()

                        continue

                    case "D":

                        self._menu = "mail_delete_select"

                        response = self._router.execute("LM")

                        print()
                        print(response)
                        print()
                        print("Enter mail number.")
                        print("[B]ack")
                        print()

                        continue

                    case "B":

                        self._display_main_menu()

                        continue


            #
            # SEND MAIL
            #

            if self._menu == "mail_recipient":

                self._mail_recipient = command

                self._menu = "mail_subject"

                print()
                print("Subject:")
                print()

                continue


            if self._menu == "mail_subject":

                self._mail_subject = command

                self._menu = "mail_body"

                print()
                print("Message:")
                print()

                continue


            if self._menu == "mail_body":

                self._mail_body = command

                self._menu = "mail_confirm"

                print()
                print("Send this mail?")
                print()
                print(f"To      : {self._mail_recipient}")
                print(f"Subject : {self._mail_subject}")
                print()
                print(self._mail_body)
                print()
                print("[S]end")
                print("[B]ack")
                print()

                continue


            if self._menu == "mail_confirm":

                match command.upper():

                    case "S":

                        response = self._router.execute(
                            f"SM.{self._mail_recipient}.{self._mail_subject}.{self._mail_body}"
                        )

                        print()
                        print(response)
                        print()

                        self._mail_recipient = ""
                        self._mail_subject = ""
                        self._mail_body = ""

                        self._display_mail_menu()

                        continue

                    case "B":

                        self._mail_recipient = ""
                        self._mail_subject = ""
                        self._mail_body = ""

                        self._display_mail_menu()

                        continue


            #
            # READ MAIL
            #

            if self._menu == "mail_select":

                if command.upper() == "B":

                    self._display_mail_menu()

                    continue

                response = self._router.execute(f"RM.{command}")

                print()
                print(response)
                print()
                print("[B]ack")
                print()

                self._menu = "mail_read"

                continue


            if self._menu == "mail_read":

                if command.upper() == "B":

                    self._menu = "mail_select"

                    response = self._router.execute("LM")

                    print()
                    print(response)
                    print()
                    print("Enter mail number.")
                    print("[B]ack")
                    print()

                    continue


            #
            # DELETE MAIL
            #

            if self._menu == "mail_delete_select":

                if command.upper() == "B":

                    self._display_mail_menu()

                    continue

                self._selected_mail = command

                self._menu = "mail_delete_confirm"

                print()
                print(f"Delete mail {command}?")
                print()
                print("[Y]es")
                print("[N]o")
                print()

                continue


            if self._menu == "mail_delete_confirm":

                match command.upper():

                    case "Y":

                        response = self._router.execute(
                            f"DM.{self._selected_mail}"
                        )

                        print()
                        print(response)
                        print()

                        self._selected_mail = ""

                        self._display_mail_menu()

                        continue

                    case "N":

                        self._selected_mail = ""

                        self._display_mail_menu()

                        continue

            #
            # STATISTICS
            #

            if self._menu == "statistics":

                print(f"DEBUG: statistics menu received '{command}'")

                match command.upper():

                    case "B":
                        print("DEBUG: Back pressed")
                        self._display_main_menu()
                        continue

            #
            # HELP
            #

            if self._menu == "help":

                match command.upper():

                    case "N":

                        self._menu = "help2"

                        response = self._router.execute("HELP.2")

                        print()
                        print(response)
                        print()
                        print("[B]ack")
                        print()

                        continue

                    case "B":
                        self._display_main_menu()
                        continue

            if self._menu == "help2":

                match command.upper():

                    case "B":

                        self._display_main_menu()
                        continue

            if not command:
                continue

            if command.upper() in ("Q", "QUIT", "EXIT"):
                print("73!")
                break

            if self._menu == "main":
                match command.upper():
                    case "B":
                        self._display_bulletins_menu()
                        continue

                    case "M":
                        self._display_mail_menu()
                        continue

                    case "S":
                        self._menu = "statistics"

                        response = self._router.execute("ST")

                        print()
                        print(response)
                        print()
                        print("[B]ack")
                        print()

                        continue

                    case "H":
                        self._menu = "help"

                        response = self._router.execute("HELP")

                        print()
                        print(response)
                        print()
                        print("[B]ack")
                        print()

                        continue

            response = self._router.execute(command)

            print()
            print(response)
            print()

    def _display_banner(self) -> None:
        """Display the startup banner."""

        splash = Path(
            "bbs/assets/splash.txt"
        ).read_text(
            encoding="utf-8"
        )

        print(splash)

        print("Node    : MBBS")
        print("Version : 1.0.0")
        print("Mesh    : Connected")
        print()
        print("[E]nter")
        print()

    def _display_main_menu(self) -> None:
        """Display the main menu."""

        self._menu = "main"

        print("Main Menu")
        print("---------")
        print()

        print("[B]ulletins")
        print()
        print("[M]ail")
        print()
        print("[S]tatistics")
        print()
        print("[H]elp")
        print()
        print("[Q]uit")
        print()

    def _display_bulletins_menu(self) -> None:
        """Display the Bulletins menu."""

        self._menu = "bulletins"

        print("Bulletins")
        print("----------")
        print()

        print("[P]ost Bulletin")
        print()

        print("[R]ead Bulletin")
        print()

        print("[D]elete Bulletin")
        print()

        print("[B]ack")
        print()


    def _display_mail_menu(self) -> None:
        """Display the Mail menu."""

        self._menu = "mail"

        print("Mail")
        print("----")
        print()

        print("[S]end Mail")
        print()

        print("[R]ead Mail")
        print()

        print("[D]elete Mail")
        print()

        print("[B]ack")
        print()