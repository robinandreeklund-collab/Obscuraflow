# Enhanced Dashboard Features Guide

## 🎯 Overview

The Obscuraflow dashboard now includes enhanced features with real Finnhub API integration and much more detailed data visualization.

## 🔄 Data Source Toggle

### Location
Found at the bottom of the sidebar navigation menu.

### Options
1. **Mock Data** (Default)
   - Simulated realistic market data
   - No API calls required
   - Perfect for development and testing
   - Instant response times

2. **Live API**
   - Real-time data from Finnhub
   - Actual market quotes and prices
   - Historical data and company profiles
   - Requires internet connection

### How to Toggle
1. Open the dashboard
2. Scroll to bottom of sidebar
3. Select "Mock Data" or "Live API"
4. The setting is controlled in `dash_app/config.py`

## 📊 Enhanced Panels

### Decision Core - Enhanced
The enhanced Decision Core panel now includes:

**Market Overview:**
- Live quotes for 12 major symbols (AAPL, GOOGL, MSFT, TSLA, AMZN, META, NVDA, AMD, NFLX, BA, JPM, V)
- Real-time price changes with color coding (green = up, red = down)
- Open, High, Low, Current prices
- Percentage changes

**Visualizations:**
- Price change bar chart
- Trading volume analysis
- Agent decision distribution
- Consensus analysis by symbol

**Agent Performance:**
- Individual agent accuracy metrics
- Decision counts and status
- Performance progress bars
- Active/inactive status indicators

**Consensus Analysis:**
- Symbol-by-symbol breakdown
- Number of agents voting
- Consensus decision (BUY/SELL/HOLD)
- Confidence levels
- Strong/Moderate/Weak indicators

## 🔧 API Configuration

### Finnhub API Key
Located in `dash_app/config.py`:
```python
FINNHUB_API_KEY = "d3in10hr01qmn7fkr2a0d3in10hr01qmn7fkr2ag"
```

### Settings
```python
USE_MOCK_DATA = True  # Set to False for live API data

DEFAULT_SYMBOLS = [
    'AAPL', 'GOOGL', 'MSFT', 'TSLA',
    'AMZN', 'META', 'NVDA', 'AMD',
    'NFLX', 'BA', 'JPM', 'V'
]

AUTO_REFRESH_INTERVAL = 5000  # milliseconds
```

### API Features
- **Smart Caching**: 60 seconds for quotes, 1 hour for profiles
- **Rate Limiting**: 100ms delay between batch requests
- **Error Handling**: Automatic fallback to mock data
- **Timeout Protection**: 5-10 second request timeouts

## 📈 API Endpoints Used

### Quote Data
```
GET https://finnhub.io/api/v1/quote?symbol=AAPL
```
Returns: Current price, high, low, open, previous close, change

### Company Profile
```
GET https://finnhub.io/api/v1/stock/profile2?symbol=AAPL
```
Returns: Name, industry, market cap, IPO date, website

### Historical Candles
```
GET https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=D&from=X&to=Y
```
Returns: OHLCV data for specified time range

## 🚀 Usage Examples

### Basic Usage
```bash
# Start with default settings (mock data)
python run_dashboard.py
```

### Enable Live API
Edit `dash_app/config.py`:
```python
USE_MOCK_DATA = False  # Change to False
```

Then restart:
```bash
python run_dashboard.py
```

### Change API Key
Edit `dash_app/config.py`:
```python
FINNHUB_API_KEY = "your_api_key_here"
```

### Add More Symbols
Edit `dash_app/config.py`:
```python
DEFAULT_SYMBOLS = [
    'AAPL', 'GOOGL', 'MSFT', 'TSLA',
    'AMZN', 'META', 'NVDA', 'AMD',
    'YOUR_SYMBOL_HERE'  # Add your symbols
]
```

## 🎨 Enhanced Visualizations

### Price Change Chart
- Color-coded bars (green/red)
- Percentage labels
- Sorted by symbol
- Responsive design

### Volume Analysis
- Purple bars showing relative volume
- Millions (M) notation
- Hover for exact values
- Interactive tooltips

### Agent Performance
- Progress bars for accuracy
- Color-coded status
- Decision counts
- Real-time updates

### Consensus Tables
- Symbol-by-symbol breakdown
- Voting agent counts
- Confidence percentages
- Status indicators (✅ Strong, ⚠️ Moderate, ❌ Weak)

## 📊 Data Structure

### Quote Response
```python
{
    'c': 180.50,    # Current price
    'h': 182.00,    # High
    'l': 179.00,    # Low
    'o': 180.00,    # Open
    'pc': 179.50,   # Previous close
    'd': 1.00,      # Change ($)
    'dp': 0.56,     # Change (%)
    't': 1234567890 # Timestamp
}
```

### Market Summary
```python
{
    'total_symbols': 12,
    'gainers': 7,
    'losers': 5,
    'unchanged': 0,
    'avg_change_percent': 1.23,
    'quotes': {...},
    'timestamp': '2025-10-12T21:30:00'
}
```

## 🔮 Future Enhancements

### Planned Features
- [ ] WebSocket integration for true real-time updates
- [ ] Additional API endpoints (news, recommendations, earnings)
- [ ] More detailed historical charts
- [ ] Custom symbol watchlists
- [ ] Alert thresholds
- [ ] Export functionality

### API Limits
Finnhub free tier:
- 60 API calls per minute
- 30 API calls per second
- Consider upgrading for production use

## 📝 Troubleshooting

### API Not Working
1. Check internet connection
2. Verify API key in `config.py`
3. Check Finnhub status: https://finnhub.io/
4. Review browser console for errors
5. Enable mock data as fallback

### Slow Performance
1. Reduce `DEFAULT_SYMBOLS` list
2. Increase `AUTO_REFRESH_INTERVAL`
3. Check API rate limits
4. Verify caching is working

### Data Not Updating
1. Check auto-refresh interval
2. Verify data source toggle setting
3. Clear browser cache
4. Restart dashboard application

## 💡 Tips

1. **Development**: Use mock data for fast iteration
2. **Testing**: Use live API to verify real data flow
3. **Production**: Consider API rate limits and caching
4. **Performance**: Adjust refresh intervals based on usage
5. **Monitoring**: Watch browser console for API errors

---

**For support, check the main README.md or create an issue on GitHub.**
