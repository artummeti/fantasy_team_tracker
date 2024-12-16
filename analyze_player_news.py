from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# init the VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# analyze the sentiment of the article
def analyze_article(article_text):
    """
    Analyze the sentiment of the given article text.

    Args:
        article_text (str): The content of the news article.

    Returns:
        dict: Dictionary containing sentiment scores (positive, negative, neutral, compound).
    """
    sentiment_scores = analyzer.polarity_scores(article_text)
    return sentiment_scores

# decide whether to start or bench the player
def decide_start_or_bench(sentiment_scores, threshold=0.05):
    """
    Decide whether to start or bench the player based on sentiment scores.

    Args:
        sentiment_scores (dict): Sentiment scores from VADER analysis.
        threshold (float): Threshold for determining action based on compound sentiment.

    Returns:
        str: "Start", "Bench", or "Neutral" based on the sentiment.
    """
    if sentiment_scores['compound'] >= threshold:
        return "Start"
    elif sentiment_scores['compound'] <= -threshold:
        return "Bench"
    else:
        return "Neutral"
