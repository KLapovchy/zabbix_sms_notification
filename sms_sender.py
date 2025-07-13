#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
from twilio.rest import Client

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_config(path):
    if not os.path.exists(path):
        print(f"[ERROR] Config file not found: {path}")
        sys.exit(1)
    with open(path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("[ERROR] Failed to parse config file.")
            sys.exit(1)

def send_sms(to_number, subject, message, config):
    full_message = f"{subject}\n\n{message}"
    client = Client(config["account_sid"], config["auth_token"])

    try:
        sms = client.messages.create(
            body=full_message,
            from_=config["from_number"],
            to=to_number
        )
        print(f"[INFO] SMS sent to {to_number}. Message SID: {sms.sid}")
    except Exception as e:
        print(f"[ERROR] Failed to send SMS: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) < 4:
        print("Usage: sms_sender.py <to_number> <subject> <message>")
        sys.exit(1)

    to_number = sys.argv[1]
    subject = sys.argv[2]
    message = sys.argv[3]

    config = load_config(CONFIG_FILE)
    send_sms(to_number, subject, message, config)

if __name__ == "__main__":
    main()
