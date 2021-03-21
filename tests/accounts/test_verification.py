from unittest.mock import patch

from django.test import TestCase
from twilio.base.exceptions import TwilioRestException

from accounts.verification import sendEmailVerification, sendSMSVerification


class sendEmailVerificationTestCase(TestCase):
    @patch("accounts.verification.send_email")
    def test_(self, mock_send_email):
        sendEmailVerification("+15555555555", "000000")
        mock_send_email.assert_called()
        self.assertEqual(1, len(mock_send_email.mock_calls))
        expected = {"verification_code": "000000"}
        self.assertEqual("emails/email_verification.html", mock_send_email.call_args[0][0])
        self.assertEqual(expected, mock_send_email.call_args[0][1])
        self.assertEqual("Penn Labs email verification", mock_send_email.call_args[0][2])
        self.assertEqual("+15555555555", mock_send_email.call_args[0][3])


class sendSMSVerificationTestCase(TestCase):
    @patch("accounts.verification.capture_message")
    def test_invalid_client(self, mock_sentry):
        sendSMSVerification("+15555555555", "000000")
        mock_sentry.assert_called()
        self.assertEqual(1, len(mock_sentry.mock_calls))
        expected = {"level": "error"}
        self.assertEqual(expected, mock_sentry.call_args[1])

    @patch("accounts.verification.capture_message")
    @patch("accounts.verification.Client")
    def test_rest_exception(self, mock_client, mock_sentry):
        mock_client.return_value.messages.create.side_effect = TwilioRestException("", "")
        sendSMSVerification("+15555555555", "000000")
        mock_sentry.assert_called()
        self.assertEqual(1, len(mock_sentry.mock_calls))
        expected = {"level": "error"}
        self.assertEqual(expected, mock_sentry.call_args[1])

    @patch("accounts.verification.Client")
    def test_send_sms(self, mock_client):
        sendSMSVerification("+15555555555", "000000")
        mock_client.assert_called()
        mock_calls = mock_client.mock_calls
        self.assertEqual(2, len(mock_calls))
        expected = {
            "to": "+15555555555",
            "body": "Your Penn Labs Account Verification Code is: 000000",
            "from_": "",
        }
        self.assertEqual(expected, mock_client.mock_calls[1][2])
