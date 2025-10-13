# 🚀 Obscuraflow Adaptive Data Flow Implementation

## Översikt

Obscuraflow använder nu en hybrid-strategi för att maximera datakvalitet och responsivitet inom begränsade API-gränser (Finnhub Free Tier: 60 calls/minut).

## Installation

### Beroenden

Installera nödvändiga paket:

```bash
pip install -r requirements.txt
```

Viktiga beroenden för dataflödet:
- `websockets>=12.0` - För WebSocket-anslutningar
- `requests>=2.31.0` - För REST API-anrop
- `asyncio` - För asynkron hantering (ingår i Python 3.7+)

## Arkitektur

### Komponenter

```
┌─────────────────┐
│  DataOrchestrator│
│   (Koordinator)  │
└────────┬─────────┘
         │
         ├─────────────────┬──────────────────┐
         │                 │                  │
    ┌────▼────┐      ┌────▼────┐      ┌─────▼─────┐
    │  REST   │      │WebSocket│      │ Trending  │
    │ Batcher │      │ Handler │      │   Pool    │
    └────┬────┘      └────┬────┘      └─────┬─────┘
         │                 │                  │
         └─────────────────┴──────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Dashboard  │
                    │   Panels    │
                    └─────────────┘
```

### 1. REST Batcher (`rest_batcher.py`)

**Ansvar:**
- Hämtar snapshot-data (OHLC, volym, RSI, etc.)
- Delar upp symboler i batcher (6 × 10 symboler)
- Kör varje batch var 10:e sekund → ≈60 calls/min
- Respekterar rate limits med intelligent queueing

**Specifikationer:**
- Batch size: 10 symboler
- Batch interval: 10 sekunder
- Max calls/min: 60
- Rate limit tracking med sliding window

**Användning:**
```python
from modules.data_stream import RestBatcher

batcher = RestBatcher(
    api_key="your_api_key",
    symbols=symbols_list,
    batch_size=10,
    batch_interval=10.0
)

# Starta batch-loop
await batcher.start_batch_loop(trending_pool)
```

### 2. WebSocket Handler (`ws_handler.py`)

**Ansvar:**
- Initierar WebSocket endast för top-symboler
- Begränsar till max 50 aktiva subscriptions samtidigt
- Roterar sub-listan var 12 sekunder baserat på trend_score
- Avsubscriberar inaktiva symboler, subscribar nya top-symboler

**Specifikationer:**
- Max subscriptions: 50
- Rotation interval: 12 sekunder
- Tick cache: 30 sekunder per symbol
- Auto-reconnect vid connection loss

**Användning:**
```python
from modules.data_stream import WebSocketHandler

ws_handler = WebSocketHandler(
    api_key="your_api_key",
    max_subscriptions=50,
    rotation_interval=12.0
)

# Anslut och starta
await ws_handler.connect()
await ws_handler.listen_for_ticks(trending_pool)
```

### 3. Trending Pool (enhanced)

**Ansvar:**
- Beräknar trend_score per symbol
- Kombinerar batch-data och tick-data
- Rankar symboler baserat på volym, momentum, volatilitet
- Returnerar top-symboler för WebSocket-rotation

**Nya funktioner:**
- `update_symbol()` - För batch-data (högre vikt)
- `update_symbol_tick()` - För tick-data (lägre vikt, högre frekvens)
- Differentierad viktning mellan källor

**Användning:**
```python
from modules.trending_pool import TrendingPool

pool = TrendingPool(max_history=100, dampening_factor=0.3)

# Batch update
pool.update_symbol(symbol, batch_trend_data)

# Tick update
pool.update_symbol_tick(symbol, tick_trend_data)

# Hämta top-symboler
top_symbols = pool.get_top_symbols(count=50)
```

### 4. Data Orchestrator (`orchestrator.py`)

**Ansvar:**
- Koordinerar REST batcher och WebSocket handler
- Startar och stoppar alla komponenter
- Tillhandahåller unified interface för marknadsdata
- Hanterar rotation-loop för WebSocket subscriptions

**Användning:**
```python
from modules.data_stream import DataOrchestrator

# Skapa orchestrator
orchestrator = DataOrchestrator(
    api_key="your_api_key",
    symbols=symbols_list,
    use_mock_data=False,
    batch_size=10,
    batch_interval=10.0,
    max_ws_subscriptions=50
)

# Starta alla processer
await orchestrator.start()

# Hämta marknadsdata
market_summary = orchestrator.get_market_summary()
symbol_data = orchestrator.get_symbol_data('AAPL')

# Stoppa när klar
await orchestrator.stop()
```

## Dataflöde

### Steg-för-steg

```
1. REST Batcher (varje 10 sekunder)
   └─> Hämtar batch (10 symboler)
   └─> Pushar till TrendingPool
   └─> TrendingPool beräknar trend_score

2. TrendingPool
   └─> Rankar alla symboler
   └─> Returnerar top 50 symboler

3. WebSocket Handler (varje 12 sekunder)
   └─> Hämtar top 50 från TrendingPool
   └─> Jämför med aktiva subs
   └─> Avsubscriberar gamla, subscribar nya
   └─> Max 50 aktiva samtidigt

4. WebSocket Ticks (kontinuerligt)
   └─> Tar emot tick-data för aktiva subs
   └─> Pushar till TrendingPool (lägre vikt)
   └─> Uppdaterar trend_score inkrementellt

5. Dashboard/Panels
   └─> Hämtar från DataOrchestrator
   └─> Får kombinerad data (batch + ticks)
   └─> Real-time uppdatering
```

## Fördelar

| Fördel | Beskrivning |
|--------|-------------|
| **Rate Limit Safe** | Respekterar 60 calls/min strikt med intelligent batching |
| **Low Latency** | WebSocket ger real-time ticks för aktiva symboler |
| **Resource Efficient** | Begränsar WebSocket till 50 subs, rotera baserat på aktivitet |
| **Robust** | Fallback till mock data vid API-problem |
| **Scalable** | Kan enkelt justeras för fler/färre symboler |

## Konfiguration

### Config-parametrar

```python
# config.py
USE_MOCK_DATA = False  # Sätt till False för live data

# API Configuration
FINNHUB_API_KEY = "your_api_key_here"

# Batch Configuration
REST_BATCH_SIZE = 10           # Symboler per batch
REST_BATCH_INTERVAL = 10.0     # Sekunder mellan batcher

# WebSocket Configuration  
WS_MAX_SUBSCRIPTIONS = 50      # Max samtidiga subscriptions
WS_ROTATION_INTERVAL = 12.0    # Sekunder mellan rotationer

# TrendingPool Configuration
TRENDING_POOL_HISTORY = 100    # Historik per symbol
TRENDING_DAMPENING = 0.3       # Dämpningsfaktor för flukt
```

## Användning i Dashboard

Dashboarden får automatiskt tillgång till den nya arkitekturen:

```python
# dash_app/panels/any_panel.py
from modules.data_stream.data_stream import get_data_stream
from dash_app.config import USE_MOCK_DATA

# Får automatiskt rätt implementation (mock eller live)
data_stream = get_data_stream(use_mock=USE_MOCK_DATA)
market_summary = data_stream.get_market_summary()
```

## Migration från Gammal Implementation

### Tidigare (orsakade 429 errors):
```python
# Hämtade alla symboler samtidigt
for symbol in symbols:
    quote = client.get_quote(symbol)  # 12 calls direkt = rate limit!
```

### Nu (respekterar rate limits):
```python
# Batch 1: 10 symboler (10s)
# Batch 2: 10 symboler (20s)
# Batch 3: 10 symboler (30s)
# ... etc
# Total: ≈60 calls/min, ingen rate limit
```

## Tester

```bash
# Test REST Batcher
PYTHONPATH=. python3 -m pytest tests/test_rest_batcher.py

# Test WebSocket Handler
PYTHONPATH=. python3 -m pytest tests/test_ws_handler.py

# Test Orchestrator
PYTHONPATH=. python3 -m pytest tests/test_orchestrator.py
```

## Troubleshooting

### Problem: "No module named 'websockets'"

**Lösning:**
```bash
# Installera websockets-modulen
pip install websockets>=12.0

# Eller installera alla beroenden
pip install -r requirements.txt
```

### Problem: Får fortfarande 429 errors

**Lösning:**
- Kontrollera att `batch_interval` är minst 10 sekunder
- Verifiera att `batch_size * (60 / batch_interval) <= 60`
- Kolla logs för rate limit tracking

### Problem: WebSocket disconnect

**Lösning:**
- Auto-reconnect är implementerat
- Kontrollera API-nyckel validity
- Verifiera att max_subscriptions <= 50

### Problem: Tom data

**Lösning:**
- Vänta minst 10 sekunder för första batch
- Kontrollera att symboler är giltiga
- Fallback till mock data aktiveras automatiskt vid API-problem

## Nästa Steg

1. ✅ Implementera REST batching
2. ✅ Implementera WebSocket handler
3. ✅ Integrera med TrendingPool
4. ✅ Skapa DataOrchestrator
5. ⏳ Testa med riktig Finnhub API
6. ⏳ Finjustera parametrar baserat på faktisk användning
7. ⏳ Lägg till metrics och monitoring

## Kontakt

För frågor eller problem, kontakta utvecklingsteamet.
