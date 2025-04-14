import threading
import streamlit as st
from helpers import init_app
from outlook_reader import OutlookApp, OutlookListner, OutlookReader
from email import policy
from email.parser import BytesParser


# Setup App style and display title
init_app()


@st.dialog("**Gen-AI Summary**")
def summarize(email):
    st.text(email[100:])


@st.dialog("**Gen-AI Auto Reply**")
def auto_reply(email):
    st.text(email[100:])


# Function to display email details
def display_emails(emails):
    for index, email in enumerate(emails):
        with st.expander(f"Email {index + 1}: {email.Subject}"):
            st.write("**Sender:**\n\n")
            st.text(getattr(email, "SenderEmailAddress", "N/A"))
            st.write("**Received Time:**\n\n")
            st.text(getattr(email, "ReceivedTime", "N/A"))
            cols = st.columns(3)
            with cols[0].popover("**👁️‍🗨️ Preview Mail Body**"):
                st.write(email.Body)
            with cols[1]:
                if st.button("📋 Summarize with Gen-AI", key=f"S{index}"):
                    summarize(email.Body)
            with cols[2]:
                if st.button("↩️ Auto Reply with Gen-AI", key=f"R{index}"):
                    auto_reply(email.Body)


# Streamlit app
def main():
    if "new_emails" not in st.session_state:
        st.session_state.new_emails = []

    mails_container = st.empty().container()
    with st.sidebar:
        st.header("Mailbox Options")
        outlook_app = OutlookApp()
        all_mail_boxes = outlook_app.get_all_mail_boxes()
        mailbox = st.selectbox("📫 Select Mailbox", all_mail_boxes)

        if mailbox:
            reader = OutlookReader(outlook_app, mail_box=mailbox)
            all_folders = reader.get_all_folders()
            folder = st.selectbox("📁 Select Folder", all_folders, index=1)

            if folder:
                num_emails = st.number_input(
                    "Number of Emails to Display",
                    min_value=1,
                    max_value=100,
                    value=5,
                    step=1,
                )
                show_emails = st.button("Show Emails")
                if show_emails:
                    last_mails = reader.get_last_mails(num_emails, folder=folder)
                    with mails_container:
                        st.write(f"- Last {num_emails} mails received in {folder}:")
                        display_emails(last_mails)

        st.write("---")
        start_email_listener = st.sidebar.button("Start Email Listener")
        logs_container = st.container(height=400)

    # Callback function for new emails
    def on_new_email(email):
        logs_container.text(f"Recived: {getattr(email, 'SenderEmailAddress', 'N/A')}")

    # Email listener
    if start_email_listener:
        logs_container.text("Listening for new emails...")
        threading.Thread(
            target=OutlookListner, args=(on_new_email,), daemon=True
        ).start()

    # Display new emails received
    if st.session_state.new_emails:
        st.write("New Emails Received:")
        display_emails(st.session_state.new_emails)
    
    # Added by Achraf -----------------------------------------
    def parse_eml_to_dict(file_path):
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        return {
            "Sender": msg.get("From"),
            "To": msg.get("To"),
            "Cc": msg.get("Cc"),
            "Body": msg.get_body(preferencelist=('plain', 'html')).get_content()
        }
    uploaded_file = st.sidebar.file_uploader("📤 Upload .eml Email File", type=["eml"])
    if uploaded_file is not None:
        with open("temp_email.eml", "wb") as f:
            f.write(uploaded_file.getbuffer())

        parsed_email = parse_eml_to_dict("temp_email.eml")
        st.subheader("Parsed Email Content")
        st.write(f"**Sender**: {parsed_email['Sender']}")
        st.write(f"**To**: {parsed_email['To']}")
        st.write(f"**Cc**: {parsed_email['Cc']}")
        st.write("**Body:**")
        st.text(parsed_email["Body"])
    # End Achraf -----------------------------------------



if __name__ == "__main__":
    main()
