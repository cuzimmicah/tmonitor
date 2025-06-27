# TwitterAPI.io Webhook Monitor

A serverless webhook receiver for real-time Twitter data from TwitterAPI.io, deployable on Vercel.

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/tmonitor)

## 📋 Features

- ✅ **Serverless webhook receiver** for TwitterAPI.io
- ✅ **Real-time tweet processing** with structured data extraction
- ✅ **Security verification** using API key authentication
- ✅ **Health check endpoint** for monitoring
- ✅ **Zero-maintenance deployment** on Vercel
- ✅ **Scalable and cost-effective** serverless architecture

## 🔧 Local Development

### Prerequisites
- Python 3.9+
- TwitterAPI.io account and API key

### Setup

1. **Clone and install dependencies:**
   ```bash
   git clone <your-repo>
   cd tmonitor
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   ```bash
   cp env_template.txt .env
   ```

3. **Add your API key to `.env`:**
   ```
   TWITTER_API_KEY=your_actual_api_key_here
   ```

4. **Run locally:**
   ```bash
   python monitor.py
   ```

5. **Test endpoints:**
   ```bash
   # Health check
   curl http://localhost:5000/health
   
   # Test webhook
   curl -X POST http://localhost:5000/webhook \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key" \
     -d '{"test": true}'
   ```

## 🌐 Vercel Deployment

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Add environment variable:**
   ```bash
   vercel env add TWITTER_API_KEY
   # Enter your TwitterAPI.io API key when prompted
   ```

4. **Redeploy:**
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via Vercel Dashboard

1. **Connect GitHub repository** to Vercel
2. **Add environment variable** in Vercel dashboard:
   - Key: `TWITTER_API_KEY`
   - Value: Your TwitterAPI.io API key
3. **Deploy automatically** on every push

### Your Webhook URLs

After deployment, your webhook URLs will be:
- **Webhook:** `https://your-app.vercel.app/api/webhook`
- **Health Check:** `https://your-app.vercel.app/api/health`

## 📊 TwitterAPI.io Configuration

1. **Log in to TwitterAPI.io**
2. **Go to Filter Rules**
3. **Create a new rule** with your filter conditions
4. **Set webhook URL** to: `https://your-app.vercel.app/api/webhook`
5. **Save and activate** the rule

Example filter rules:
- `from:elonmusk` - Tweets from Elon Musk
- `#AI OR #ML` - Tweets about AI or Machine Learning
- `crypto bitcoin` - Tweets mentioning crypto and bitcoin

## 🔒 Security

- **API Key Verification**: All webhook requests are verified using the `X-API-Key` header
- **Environment Variables**: Sensitive data stored securely in Vercel environment variables
- **HTTPS Only**: All production traffic encrypted via Vercel's HTTPS

## 📝 API Endpoints

### POST `/api/webhook`
Main webhook endpoint for receiving TwitterAPI.io data.

**Headers:**
- `Content-Type: application/json`
- `X-API-Key: your_api_key`

**Response:**
```json
{
  "status": "success",
  "message": "Processed 3 tweets",
  "tweets_count": 3,
  "timestamp": "2023-06-01T12:34:56Z"
}
```

### GET `/api/health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-06-01T12:34:56Z",
  "service": "TwitterAPI Monitor (Vercel)",
  "api_key_configured": true
}
```

## 🛠 Customization

The webhook processor is designed to be easily extensible. In the `process_tweet_data()` function, you can add:

- **Database storage** (MongoDB, PostgreSQL, etc.)
- **Real-time notifications** (Slack, Discord, email)
- **Data analytics** (sentiment analysis, trending topics)
- **External integrations** (Zapier, IFTTT, etc.)

Example integrations:
```python
# Send to database
await database.tweets.insert_many(processed_tweets)

# Send Slack notification
await slack.send_message(f"New tweets: {len(processed_tweets)}")

# Trigger analytics
await analytics.process_sentiment(processed_tweets)
```

## 💰 Cost Considerations

### Vercel Pricing
- **Hobby Plan**: Free for personal projects (100GB bandwidth/month)
- **Pro Plan**: $20/month for production use (1TB bandwidth/month)

### TwitterAPI.io Pricing
- **API calls**: $0.00012 - $0.00015 per request
- **Check frequency**: Affects total monthly cost
- See the [complete guide](TwitterAPI_Webhook_Guide.md) for detailed pricing analysis

## 🐛 Troubleshooting

### Common Issues

1. **"URL must return HTTP 200"**
   - Check that your Vercel deployment is successful
   - Test the health endpoint: `https://your-app.vercel.app/api/health`
   - Ensure environment variables are set correctly

2. **"Unauthorized" errors**
   - Verify your `TWITTER_API_KEY` environment variable
   - Check that TwitterAPI.io is sending the correct API key

3. **Function timeout**
   - Vercel functions have a 10-second timeout on hobby plan
   - Consider optimizing data processing for large tweet batches

### Debug Commands

```bash
# Check deployment status
vercel ls

# View function logs
vercel logs

# Test webhook locally
vercel dev
```

## 📚 Additional Resources

- [TwitterAPI.io Documentation](https://twitterapi.io/docs)
- [Vercel Python Functions Guide](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Complete Implementation Guide](TwitterAPI_Webhook_Guide.md)

## 📄 License

MIT License - feel free to use this for your projects!

---

**Need help?** Check the troubleshooting section or open an issue on GitHub. 