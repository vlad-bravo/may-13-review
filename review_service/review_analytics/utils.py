import pandas as pd
import plotly.express as px

def get_review_stats(user):
    # Здесь должна быть логика получения отзывов из вашей БД
    # Пример:
    reviews = user.reviews.all()
    positive = reviews.filter(sentiment='positive').count()
    negative = reviews.filter(sentiment='negative').count()
    neutral = reviews.filter(sentiment='neutral').count()
    
    return {
        'total': reviews.count(),
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'positive_percent': (positive / reviews.count() * 100) if reviews.count() else 0,
        'negative_percent': (negative / reviews.count() * 100) if reviews.count() else 0,
    }

def generate_review_chart(stats):
    data = {
        'Sentiment': ['Positive', 'Negative', 'Neutral'],
        'Count': [stats['positive'], stats['negative'], stats['neutral']]
    }
    df = pd.DataFrame(data)
    fig = px.pie(df, values='Count', names='Sentiment', title='Отзывы по тональности')
    return fig.to_html(full_html=False)
