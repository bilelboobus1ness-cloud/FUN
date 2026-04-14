import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
from twilio.rest import Client

class NotificationService:
    """Service to send notifications via email, WhatsApp, and Telegram"""
    
    def __init__(self):
        self.email_sender = os.getenv('EMAIL_SENDER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.whatsapp_account_sid = os.getenv('WHATSAPP_ACCOUNT_SID', '')
        self.whatsapp_auth_token = os.getenv('WHATSAPP_AUTH_TOKEN', '')
        self.whatsapp_from = os.getenv('WHATSAPP_FROM_NUMBER', '')
        
        if self.whatsapp_account_sid and self.whatsapp_auth_token:
            self.twilio_client = Client(self.whatsapp_account_sid, self.whatsapp_auth_token)
    
    def send_email(self, recipient, subject, body, html_body=None):
        """Send email notification"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_sender
            msg['To'] = recipient
            
            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)
            
            print(f"Email sent to {recipient}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_whatsapp(self, phone_number, message):
        """Send WhatsApp notification via Twilio"""
        try:
            message = self.twilio_client.messages.create(
                from_=self.whatsapp_from,
                body=message,
                to=f'whatsapp:{phone_number}'
            )
            print(f"WhatsApp sent to {phone_number}: {message.sid}")
            return True
        except Exception as e:
            print(f"Error sending WhatsApp: {e}")
            return False
    
    def send_telegram(self, chat_id, message):
        """Send Telegram notification"""
        try:
            url = f'https://api.telegram.org/bot{self.telegram_token}/sendMessage'
            params = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            print(f"Telegram sent to {chat_id}")
            return True
        except Exception as e:
            print(f"Error sending Telegram: {e}")
            return False
    
    def send_trade_alert(self, user, trade_signal, notification_prefs):
        """Send trade alert to user based on their preferences"""
        subject = f"🎯 NEW TRADE SIGNAL: {trade_signal['currency_pair']}"
        
        body = f"""
NEW TRADE SIGNAL

Currency Pair: {trade_signal['currency_pair']}
Signal Type: {trade_signal['signal_type']}
Entry Price: {trade_signal['entry_price']}
Stop Loss: {trade_signal['stop_loss']}
Take Profit: {trade_signal['take_profit']}
Lot Size: {trade_signal['lot_size']}
Risk Amount: ${trade_signal['risk_amount']}
Execution Time: {trade_signal['execution_time']}
News Source: {trade_signal['news_source']}

Open BLAAN dashboard for more details:
https://yourapp.com/trades

Risk Percentage: {user.get('trading_account', {}).get('risk_percentage', 2)}%
"""
        
        html_body = f"""
        <html>
            <body>
                <h2>🎯 NEW TRADE SIGNAL</h2>
                <p><strong>Currency Pair:</strong> {trade_signal['currency_pair']}</p>
                <p><strong>Signal Type:</strong> {trade_signal['signal_type']}</p>
                <p><strong>Entry Price:</strong> {trade_signal['entry_price']}</p>
                <p><strong>Stop Loss:</strong> {trade_signal['stop_loss']}</p>
                <p><strong>Take Profit:</strong> {trade_signal['take_profit']}</p>
                <p><strong>Lot Size:</strong> {trade_signal['lot_size']}</p>
                <p><strong>Risk Amount:</strong> ${trade_signal['risk_amount']}</p>
                <p><strong>Execution Time:</strong> {trade_signal['execution_time']}</p>
                <a href="https://yourapp.com/trades">Open BLAAN Dashboard</a>
            </body>
        </html>
        """
        
        if notification_prefs.get('email') and user.get('email'):
            self.send_email(user['email'], subject, body, html_body)
        
        if notification_prefs.get('whatsapp') and user.get('whatsapp'):
            self.send_whatsapp(user['whatsapp'], f"{subject}\n\n{body}")
        
        if notification_prefs.get('telegram') and user.get('telegram_id'):
            self.send_telegram(user['telegram_id'], f"<b>{subject}</b>\n\n{body}")
