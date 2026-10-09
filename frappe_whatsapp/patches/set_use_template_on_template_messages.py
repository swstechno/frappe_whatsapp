"""Back-fill use_template on template messages saved before before_insert set it."""

import frappe


def execute():
    """Check use_template on messages before_insert sent as templates while
    leaving it unchecked; the form hid their Template field.

    Filters on message_type too: before #205 derived it from `template`, a
    row with `template` set but message_type left Manual went out as plain
    text, so it must stay unchecked."""
    message = frappe.qb.DocType("WhatsApp Message")
    (
        frappe.qb.update(message)
        .set(message.use_template, 1)
        .where(message.message_type == "Template")
        .where(message.template.isnotnull())
        .where(message.template != "")
        .where(message.use_template == 0)
    ).run()
