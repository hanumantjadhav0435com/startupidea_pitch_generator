import os
import logging
from flask_mail import Message
from flask import url_for, render_template_string
from app import mail

def send_password_reset_email(email, token):
    """
    Send password reset email to user
    """
    try:
        subject = "Password Reset Request - AI Pitch Generator"
        
        # Create reset URL
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        
        # Email template
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 AI Pitch Generator</h1>
                    <p>Password Reset Request</p>
                </div>
                <div class="content">
                    <h2>Hello!</h2>
                    <p>You requested a password reset for your AI Pitch Generator account.</p>
                    <p>Click the button below to reset your password:</p>
                    <a href="{reset_url}" class="button">Reset Password</a>
                    <p>If you didn't request this, please ignore this email.</p>
                    <p><strong>Note:</strong> This link will expire in 1 hour.</p>
                </div>
                <div class="footer">
                    <p>© 2025 AI Pitch Generator. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        AI Pitch Generator - Password Reset Request
        
        Hello!
        
        You requested a password reset for your AI Pitch Generator account.
        
        Click the link below to reset your password:
        {reset_url}
        
        If you didn't request this, please ignore this email.
        
        Note: This link will expire in 1 hour.
        
        © 2025 AI Pitch Generator. All rights reserved.
        """
        
        msg = Message(
            subject=subject,
            recipients=[email],
            html=html_body,
            body=text_body
        )
        
        mail.send(msg)
        logging.info(f"Password reset email sent to {email}")
        
    except Exception as e:
        logging.error(f"Failed to send password reset email: {str(e)}")
        raise Exception(f"Failed to send email: {str(e)}")

def send_welcome_email(email, username):
    """
    Send welcome email to new user
    """
    try:
        subject = "Welcome to AI Pitch Generator!"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Welcome to AI Pitch Generator!</h1>
                </div>
                <div class="content">
                    <h2>Hello {username}!</h2>
                    <p>Welcome to AI Pitch Generator! We're excited to have you on board.</p>
                    <p>With our platform, you can:</p>
                    <ul>
                        <li>Generate professional investor pitches using AI</li>
                        <li>Create compelling pitch decks instantly</li>
                        <li>Download presentations as PowerPoint files</li>
                        <li>Refine and iterate on your startup ideas</li>
                    </ul>
                    <p>Ready to get started?</p>
                    <a href="{url_for('dashboard', _external=True)}" class="button">Create Your First Pitch</a>
                </div>
                <div class="footer">
                    <p>© 2025 AI Pitch Generator. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Welcome to AI Pitch Generator!
        
        Hello {username}!
        
        Welcome to AI Pitch Generator! We're excited to have you on board.
        
        With our platform, you can:
        - Generate professional investor pitches using AI
        - Create compelling pitch decks instantly
        - Download presentations as PowerPoint files
        - Refine and iterate on your startup ideas
        
        Ready to get started? Visit your dashboard to create your first pitch.
        
        © 2025 AI Pitch Generator. All rights reserved.
        """
        
        msg = Message(
            subject=subject,
            recipients=[email],
            html=html_body,
            body=text_body
        )
        
        mail.send(msg)
        logging.info(f"Welcome email sent to {email}")
        
    except Exception as e:
        logging.error(f"Failed to send welcome email: {str(e)}")
        # Don't raise exception for welcome email failures
        pass
