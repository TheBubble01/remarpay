import os
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

def generate_receipt_image(payment_request, output_path):
    # Create a blank white image
    img = Image.new('RGB', (600, 350), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load a font (fallback to default if needed)
    try:
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'arial.ttf')
        font = ImageFont.truetype(font_path, 16)
    except:
        font = ImageFont.load_default()

    # Optional: load logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'remarpay_logo.png')
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).resize((80, 80))
        img.paste(logo, (10, 10))

    # Receipt content
    lines = [
        "Remar Pay - Payment Receipt",
        f"Country: {payment_request.country.upper()}",
        f"Client: {payment_request.depositor_name} ({payment_request.depositor_phone})",
        f"Receiver: {payment_request.receiver_name} ({payment_request.receiver_phone})",
        f"Amount Sent: {payment_request.deposit_amount_dinar} LYD",
        f"Converted: {payment_request.converted_amount} {payment_request.country.upper()}",
        f"Conversion Rate: {payment_request.conversion_rate}",
        f"Fee Applied: {'Yes' if payment_request.fee_applied else 'No'}",
        f"Handled By: {payment_request.cashier.name}",
    ]

    # Append country-specific payment details
    if payment_request.country == 'nigeria':
        lines.extend([
            "Payment Details:",
            f"- Bank Name: {payment_request.receiver_bank_name}",
            f"- Account Number: {payment_request.receiver_account_number}",
            f"- Account Name: {payment_request.receiver_account_name}"
        ])
    elif payment_request.country in ['niger', 'cameroon']:
        lines.extend([
            "Payment Details (NITA):",
            f"- Receiver Name: {payment_request.receiver_name}",
            f"- Receiver Phone: {payment_request.receiver_phone}",
            f"- NITA Office: {payment_request.nita_office}"
        ])


    y = 100
    for line in lines:
        draw.text((20, y), line, fill=(0, 0, 0), font=font)
        y += 30

    # Save to path
    img.save(output_path)
