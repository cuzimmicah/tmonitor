#!/usr/bin/env python3
"""
TwitterAPI.io Webhook Monitor
A Flask-based webhook receiver for real-time Twitter data from TwitterAPI.io
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
API_KEY = os.getenv('TWITTER_API_KEY')
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

if not API_KEY:
    logger.error("TWITTER_API_KEY not found in environment variables!")
    exit(1)

def verify_webhook_request(request):
    """
    Verify the authenticity of the webhook request using API key
    """
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
                }
            }
            
            processed_tweets.append(tweet_info)
            
            # Log each tweet
            logger.info(f"Tweet from @{tweet_info['author']['username']}: {tweet_info['text'][:100]}...")
            
        return processed_tweets
        
    except Exception as e:
        logger.error(f"Error processing tweet data: {str(e)}")
        return []

def save_tweets_to_file(tweets):
    """
    Save processed tweets to a JSON file for persistence
    """
    try:
        filename = f"tweets_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Load existing data if file exists
        existing_tweets = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_tweets = json.load(f)
        
        # Append new tweets
        existing_tweets.extend(tweets)
        
        # Save back to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_tweets, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved {len(tweets)} tweets to {filename}")
        
    except Exception as e:
        logger.error(f"Error saving tweets to file: {str(e)}")

@app.route('/webhook', methods=['POST'])
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
            # Save tweets to file
            save_tweets_to_file(processed_tweets)
            
            # You can add custom processing here:
            # - Send notifications
            # - Update database
            # - Trigger other systems
            # - Perform sentiment analysis
            # - etc.
            
            return jsonify({
                'status': 'success',
                'message': f'Processed {len(processed_tweets)} tweets',
                'tweets_count': len(processed_tweets)
            }), 200
        else:
            logger.info("No tweets to process")
            return jsonify({
                'status': 'success',
                'message': 'No tweets to process'
            }), 200
            
    except Exception as e:
        logger.error(f"Error in webhook handler: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'TwitterAPI Monitor'
    }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    """
    Get basic statistics about processed tweets
    """
    try:
        today_filename = f"tweets_{datetime.now().strftime('%Y%m%d')}.json"
        
        if os.path.exists(today_filename):
            with open(today_filename, 'r', encoding='utf-8') as f:
                tweets = json.load(f)
                
            return jsonify({
                'tweets_today': len(tweets),
                'last_updated': datetime.now().isoformat(),
                'file': today_filename
            }), 200
        else:
            return jsonify({
                'tweets_today': 0,
                'last_updated': datetime.now().isoformat(),
                'message': 'No tweets received today'
            }), 200
            
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Error retrieving stats'}), 500

if __name__ == '__main__':
    logger.info("Starting TwitterAPI.io Webhook Monitor...")
    logger.info(f"Server will run on {HOST}:{PORT}")
    logger.info("Available endpoints:")
    logger.info("  POST /webhook - Main webhook endpoint")
    logger.info("  GET  /health  - Health check")
    logger.info("  GET  /stats   - Tweet statistics")
    
    # Start the Flask development server
    app.run(host=HOST, port=PORT, debug=False)
