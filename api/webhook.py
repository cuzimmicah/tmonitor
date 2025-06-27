#!/usr/bin/env python3
"""
TwitterAPI.io Webhook Monitor - Vercel Serverless Function
A serverless awebhook receiver for real-time Twitter data from TwitterAPI.io
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify

# Initialize Flask app for Vercel
app = Flask(__name__)

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
API_KEY = os.environ.get('TWITTER_API_KEY')

def verify_webhook_request(request):
    """
    Verify the authenticity of the webhook request using API key
    """
    if not API_KEY:
        return False, "API key not configured"
        
    expected_api_key = API_KEY
    received_api_key = request.headers.get("X-API-Key")
    
    if not received_api_key:
        return False, "Missing X-API-Key header"
    
    if received_api_key != expected_api_key:
        return False, "Invalid API key"
    
    return True, "Verified"

def process_tweet_data(webhook_data):
    """
    Process the incoming tweet data and extract relevant information
    """
    processed_tweets = []
    
    try:
        event_type = webhook_data.get('event_type')
        rule_id = webhook_data.get('rule_id')
        rule_tag = webhook_data.get('rule_tag')
        tweets = webhook_data.get('tweets', [])
        
        logger.info(f"Processing {len(tweets)} tweets for rule: {rule_tag} ({rule_id})")
        
        for tweet in tweets:
            tweet_info = {
                'id': tweet.get('id'),
                'text': tweet.get('text', ''),
                'author': {
                    'id': tweet.get('author', {}).get('id'),
                    'username': tweet.get('author', {}).get('username'),
                    'name': tweet.get('author', {}).get('name')
                },
                'created_at': tweet.get('created_at'),
                'metrics': {
                    'retweet_count': tweet.get('retweet_count', 0),
                    'like_count': tweet.get('like_count', 0),
                    'reply_count': tweet.get('reply_count', 0)
                },
                'rule_info': {
                    'rule_id': rule_id,
                    'rule_tag': rule_tag
                },
                'processed_at': datetime.now().isoformat()
            }
            
            processed_tweets.append(tweet_info)
            
            # Log each tweet
            logger.info(f"Tweet from @{tweet_info['author']['username']}: {tweet_info['text'][:100]}...")
            
        return processed_tweets
        
    except Exception as e:
        logger.error(f"Error processing tweet data: {str(e)}")
        return []

@app.route('/api/webhook', methods=['POST'])
def webhook_handler():
    """
    Main webhook endpoint for receiving TwitterAPI.io data
    """
    try:
        # Verify the request
        is_valid, message = verify_webhook_request(request)
        if not is_valid:
            logger.warning(f"Unauthorized webhook request: {message}")
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get the JSON data
        webhook_data = request.get_json()
        if not webhook_data:
            logger.warning("Received webhook request with no JSON data")
            return jsonify({'error': 'No JSON data provided'}), 400
        
        logger.info("Received valid webhook request")
        
        # Process the tweet data
        processed_tweets = process_tweet_data(webhook_data)
        
        if processed_tweets:
            # In a serverless environment, you might want to:
            # - Send data to a database (MongoDB, PostgreSQL, etc.)
            # - Send to a message queue (Redis, RabbitMQ, etc.)
            # - Send notifications (email, Slack, Discord, etc.)
            # - Log to external service (Logflare, DataDog, etc.)
            
            # For now, we'll just log and return success
            logger.info(f"Successfully processed {len(processed_tweets)} tweets")
            
            # Example: You could send to external webhook or database here
            # await send_to_database(processed_tweets)
            # await send_notification(processed_tweets)
            
            return jsonify({
                'status': 'success',
                'message': f'Processed {len(processed_tweets)} tweets',
                'tweets_count': len(processed_tweets),
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            logger.info("No tweets to process")
            return jsonify({
                'status': 'success',
                'message': 'No tweets to process',
                'timestamp': datetime.now().isoformat()
            }), 200
            
    except Exception as e:
        logger.error(f"Error in webhook handler: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'TwitterAPI Monitor (Vercel)',
        'api_key_configured': bool(API_KEY)
    }), 200

# For Vercel, we need to export the app
def handler(request):
    return app(request.environ, lambda *args: None) 