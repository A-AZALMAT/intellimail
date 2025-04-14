from typing import Any, Callable
import pythoncom
import win32com.client


class OutlookApp:
    def __init__(self) -> None:
        pythoncom.CoInitialize()
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace(
            "MAPI"
        )

    def get_all_mail_boxes(self):
        return [m.Name for m in self.outlook.Folders]


class OutlookReader:
    def __init__(
        self, outlook_app: OutlookApp, mail_box: str = "WORLD-TPF-SUPPORT"
    ) -> None:
        self.root_folder = outlook_app.outlook.Folders[mail_box]

    def get_last_mails(self, n: int, folder: str = "Inbox"):
        return [
            item for _, item in zip(range(n), self.root_folder.Folders[folder].Items)
        ]

    def get_all_folders(self):
        return [f.Name for f in self.root_folder.Folders]


class OutlookListner:
    def __init__(self, callback: Callable[[Any], None]) -> None:
        # Event handler class for Outlook events
        class OutlookEventHandler:
            @staticmethod
            def OnNewMailEx(EntryIDCollection):
                for ID in EntryIDCollection.split(","):
                    item = Outlook.Session.GetItemFromID(ID)
                    if item.Class == win32com.client.constants.olMail:
                        callback(item)

        Outlook = win32com.client.DispatchWithEvents(
            "Outlook.Application", OutlookEventHandler
        )
        olNs = Outlook.GetNamespace("MAPI")
        Inbox = olNs.GetDefaultFolder(6)  # noqa: F841
        pythoncom.PumpMessages()


if __name__ == "__main__":
    outlook_app = OutlookApp()
    all_mail_boxes = outlook_app.get_all_mail_boxes()
    print("- Mail boxes available:", all_mail_boxes)

    reader = OutlookReader(outlook_app)
    all_folders = reader.get_all_folders()
    print("\n- List of all folders:", all_folders)

    last_5_mails = reader.get_last_mails(5)
    print("\n- Last 5 mails received in Inbox:", last_5_mails)

    def on_new_email(email):
        """function to execute after each mail recieved"""
        print("\n*** New mail recieved ***")
        print("- Subj: " + email.Subject)
        print("- Body: " + email.Body)

    listner = OutlookListner(callback=on_new_email)
