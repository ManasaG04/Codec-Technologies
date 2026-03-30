import webbrowser

def get_response(user_input: str) -> str:
    text = user_input.lower().strip()

    # ================== WEBSITES ==================
    if "open google" in text:
        webbrowser.open("https://www.google.com")
        return "Google has been opened in your browser."

    if "open youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "YouTube is now open. Enjoy watching videos."

    if "open gmail" in text:
        webbrowser.open("https://mail.google.com")
        return "Gmail is open. You can check your emails now."

    if "open amazon" in text:
        webbrowser.open("https://www.amazon.in")
        return "Amazon website is open for shopping."

    # ================== ACCOUNT & LOGIN ==================
    if "account" in text or "login" in text or "password" in text:

        if "create account" in text or "sign up" in text:
            return "To create an account, click on Sign Up and enter your details."

        if "forgot password" in text:
            return "Click on Forgot Password and follow the steps to reset it."

        if "reset password" in text:
            return "A password reset link will be sent to your registered email."

        if "login issues" in text:
            return "Login issues may occur due to incorrect credentials or network problems."

        if "update profile" in text:
            return "You can update your profile details from the Account Settings page."

        return "Account support includes sign up, login help, password reset, and profile updates."

    # ================== PAYMENTS & BILLING ==================
    if "payment" in text or "billing" in text or "refund" in text:

        if "refund policy" in text:
            return "Refunds are processed within 7–30 days depending on the service."

        if "payment failed" in text:
            return "Payment failure may occur due to bank issues or poor internet connection."

        if "invoice details" in text:
            return "Invoices can be downloaded from the Billing section of your account."

        if "payment methods" in text:
            return "We accept credit cards, debit cards, UPI, and net banking."

        return "Payment support covers refunds, invoices, and transaction issues."

    # ================== ORDERS & SERVICES ==================
    if "order" in text or "delivery" in text or "service" in text:

        if "order status" in text:
            return "You can track your order status from the My Orders page."

        if "cancel order" in text:
            return "Orders can be cancelled before they are shipped."

        if "delivery time" in text:
            return "Delivery time depends on your location and product availability."

        if "service availability" in text:
            return "Service availability varies by region. Please check your area."

        return "Order support includes tracking, cancellation, and delivery information."

    # ================== SUPPORT & CONTACT ==================
    if "support" in text or "contact" in text or "complaint" in text:

        if "support number" in text:
            return "📞 Customer Support Number: +91 98765 43210 (Available 24/7)"

        if "contact support" in text:
            return "You can contact support via email at support@example.com or phone."

        if "working hours" in text:
            return "Our support team is available 24/7, including weekends."

        if "raise complaint" in text:
            return "To raise a complaint, go to Support → Raise Complaint and submit details."

        return "Support services include contact help, working hours, and complaint handling."

    # ================== COMPANY & POLICIES ==================
    if "company" in text or "policy" in text or "privacy" in text:

        if "about company" in text:
            return "We are a customer-focused company providing quality services."

        if "privacy policy" in text:
            return "Your personal data is protected under our privacy policy."

        if "terms and conditions" in text:
            return "Terms and conditions explain the rules for using our services."

        return "Company information includes policies, values, and legal terms."

    # ================== FALLBACK ==================
    return (
        "I can help with:\n"
        "• Account & Login\n"
        "• Payments & Billing\n"
        "• Orders & Services\n"
        "• Support & Contact\n"
        "• Company Policies\n\n"
        "Please type your question related to these areas."
    )
