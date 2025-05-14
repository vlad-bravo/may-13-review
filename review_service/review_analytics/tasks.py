from celery import shared_task
from django.template.loader import render_to_string
# import telegram
from django.conf import settings

@shared_task
def send_telegram_report(user_id):
    ...
    # from accounts.models import CustomUser
    # from review_analytics.utils import get_review_stats
    
    # try:
    #     user = CustomUser.objects.get(id=user_id)
    #     if not user.telegram_chat_id:
    #         return False
        
    #     stats = get_review_stats(user)
    #     message = render_to_string('dashboard/telegram_report.txt', {
    #         'user': user,
    #         'stats': stats,
    #     })
        
    #     bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    #     bot.send_message(
    #         chat_id=user.telegram_chat_id,
    #         text=message
    #     )
    #     return True
    # except Exception as e:
    #     print(f"Error sending Telegram report: {e}")
    #     return False
