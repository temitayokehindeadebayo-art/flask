from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for sessions

# ------------------- AI RESPONSES -------------------
ai_responses = {
    "hello": "Hello 👋! How can I assist you today?",
    "hi": "Hi there! 🚀 Ready to help.",
    "hey": "Hey! What brings you here today?",
    "help": "Sure! I can help with orders, payments, or general inquiries.",
    "order": "To place an order, please provide the product name and quantity.",
    "track order": "Please provide your order ID 📦 so I can track it.",
    "shipping": "We offer standard (5–7 days) and express (2–3 days) shipping 🚚.",
    "delivery time": "Delivery usually takes 3–5 business days depending on location.",
    "payment": "We accept credit card, PayPal, and crypto 💳.",
    "refund": "Refunds are processed within 5–7 business days.",
    "return": "To return an item, please visit the returns page or provide your order ID.",
    "cancel order": "To cancel, provide your order ID and I’ll process the request.",
    "discount": "We currently have a 10% discount for first-time customers 🎉.",
    "coupon": "Apply coupons at checkout under 'Promo Code' section.",
    "support": "Our support team is available 24/7 🕐.",
    "contact": "You can reach us at support@example.com 📧.",
    "business hours": "We’re open Monday–Friday, 9 AM – 6 PM.",
    "location": "Our main office is located in New York, USA 🗽.",
    "products": "We sell electronics, fashion, and home essentials 🛒.",
    "warranty": "Most products come with a 1-year warranty.",
    "technical issue": "Try restarting your device or reinstalling the app 🔄.",
    "account": "You can manage your account settings in your profile.",
    "password": "To reset your password, click 'Forgot Password' on the login page.",
    "login": "Please enter your email and password on the login page 🔑.",
    "signup": "Sign up with your email and enjoy special discounts ✨.",
    "unsubscribe": "You can unsubscribe from emails at the bottom of any newsletter.",
    "bye": "Goodbye! Have an amazing day ✨",
    "thanks": "You’re welcome! 😊 Happy to help.",
    "who are you": "I’m your AI assistant 🤖, here to help with your questions.",
    "what can you do": "I can assist with orders, payments, refunds, and support inquiries.",
    "update": "You can check product updates in your account dashboard 📲.",
    "faq": "Visit our FAQ page for more common questions.",
    "chat agent": "Switching you to a human agent 👩‍💼...",
}

# ------------------- AGENT RESPONSES -------------------
agent_responses = {
    "hello": "👩‍💼 Hi there! You’re now connected to a live agent. How can I help?",
    "hi": "👩‍💼 Hello! An agent is here to assist you.",
    "help": "Of course! Can you please tell me a bit more about your issue so I can assist better?",
    "order": "📦 Could you please provide your order ID so I can check the details?",
    "track order": "🔎 I’ll track that for you. May I have your order ID?",
    "refund": "💳 I understand you’d like a refund. Once I have your order details, I’ll start the process right away.",
    "return": "📦 You can return your item — let me help you with the instructions. May I confirm your order ID first?",
    "cancel order": "❌ I can assist with cancelling your order. Please provide the order ID to proceed.",
    "delay": "🙏 I’m sorry about the delay. Let me look into the shipping status for you.",
    "email": "📧 Could you confirm the email address linked to your account?",
    "problem": "🤔 Thanks for letting me know. Could you clarify your issue so I can better assist?",
    "waiting": "⏳ Thank you for your patience! I’m checking this for you right now.",
    "escalate": "📨 I’ve escalated your case to our specialist team for faster resolution.",
    "priority": "🚀 This seems important. I’ll make sure your request is prioritized.",
    "bye": "👋 Thank you for chatting with us. Have a wonderful day!",
    "thanks": "😊 You’re very welcome! Happy to assist anytime.",
    "contact": "☎️ You can always reach us here or by phone during business hours.",
    "support": "💼 Our support team is always here to help with refunds, orders, and account issues.",
    "order id": "🆔 Please provide your order ID. It should be a 10-digit number (e.g., 1234567890).",
}


default_response = "I’m not sure about that 🤔, but I’ll forward it to a human agent."

# ------------------- ROUTES -------------------
@app.route("/")
def index():
    # reset mode to AI by default
    session["mode"] = "ai"
    return render_template("index2.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message", "").lower()
    mode = session.get("mode", "ai")  # default is AI

    # If user asks for agent, switch permanently to agent mode
    if "chat agent" in user_message or "talk to agent" in user_message:
        session["mode"] = "agent"
        return jsonify({"response": "👩‍💼 You are now connected to a human agent."})

    # Handle AI mode
    if mode == "ai":
        response = ai_responses.get(user_message, default_response)

        # If AI explicitly said "Switching you to agent"
        if "Switching you to a human agent" in response:
            session["mode"] = "agent"
        return jsonify({"response": response})

    # Handle Agent mode
    elif mode == "agent":
        response = random.choice(agent_responses)
        return jsonify({"response": response})

    # Fallback
    return jsonify({"response": default_response})


if __name__ == "__main__":
    app.run(debug=True)
