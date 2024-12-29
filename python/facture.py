import uno, msgbox, sys, os
import screen_io as ui
from com.sun.star.awt import XActionListener
# def add_to_sys_path(path):
#     original_sys_path = sys.path.copy()
#     sys.path.append(path)
#     try:
#         yield
#     finally:
#         sys.path = original_sys_path

# # Usage
# with add_to_sys_path('./'):
#     import screen_io
   

# Global variables
service_count = 1
piece_count = 1
service_fields = []
piece_fields = []
o_dialog = None

# Function to show the invoice dialog
def show_invoice_dialog():
    global o_dialog, service_count, piece_count

    service_count = 1
    piece_count = 1
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    dialog_lib = smgr.createInstanceWithContext("com.sun.star.awt.DialogLibraries", ctx)
    dialog_lib.loadLibrary("Standard")

    o_dialog = dialog_lib.Standard.facture.createDialog()
    
    # Configure listeners for buttons
    configure_button_listeners()

    # Execute the dialog
    o_dialog.execute()
ui.MsgBox("test", title="Confirmation of phrase")

def configure_button_listeners():
    global o_dialog

    # Add listeners for various buttons
    add_listener("btnAddService", "add_service", DialogListener)
    add_listener("btnAddPiece", "add_piece", DialogListener)
    add_listener("btnClientAdd", "add_client", DialogListener)
    add_listener("btnClientUpdate", "update_client", DialogListener)
    add_listener("btnClientVerify", "verify_client", DialogListener)
    add_listener("btnClientDelete", "delete_client", DialogListener)

def add_listener(button_name, command, listener_class):
    button = o_dialog.getControl(button_name)
    button.setActionCommand(command)
    listener = listener_class()
    button.addActionListener(listener)

# Listener for dialog actions
class DialogListener(XActionListener):
    def actionPerformed(self, event):
        command = event.ActionCommand
        if command == "add_service":
            add_service()
        elif command == "add_piece":
            add_piece()
        elif command == "add_client":
            add_client()
        elif command == "update_client":
            update_client()
        elif command == "verify_client":
            verify_client()
        elif command == "delete_client":
            delete_client()
        else:
            print(f"Unknown command: {command}")

    def disposing(self, event):
        pass

# Function to add a service field
def add_service():
    global service_count, service_fields, o_dialog
    service_count += 1
    print(f"Service count is now: {service_count}")
    # Implement adding a new service control to the dialog
    # and adjusting the dialog layout accordingly.

# Function to add a piece field
def add_piece():
    global piece_count, piece_fields, o_dialog
    piece_count += 1
    print(f"Piece count is now: {piece_count}")
    # Implement adding a new piece control to the dialog
    # and adjusting the dialog layout accordingly.

# Function to handle adding a client
def add_client():
    global o_dialog
    last_name = o_dialog.getControl("cmbLastName").Text
    first_name = o_dialog.getControl("cmbFirstName").Text
    address = o_dialog.getControl("txtAddress").Text
    email = o_dialog.getControl("txtEmail").Text
    phone = o_dialog.getControl("txtPhone").Text

    if not last_name or not first_name or not address or not email or not phone:
        print("All fields are required.")
        return
    
    print(f"Adding client: {first_name} {last_name}")

# Define additional functions like `update_client`, `verify_client`, and `delete_client`

#  entry point
if __name__ == "__main__":
    show_invoice_dialog()
