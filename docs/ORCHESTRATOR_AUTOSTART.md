# Automatisk DataOrchestrator Start/Stopp

## Översikt

DataOrchestrator startar nu automatiskt i bakgrunden när du byter till "Live API" i dashboarden. Detta eliminerar behovet av manuell async-kod för att starta systemet.

## Hur Det Fungerar

### 1. Orchestrator Manager

En ny `OrchestratorManager` klass har skapats som:
- Kör DataOrchestrator i en separat bakgrundstråd med asyncio event loop
- Möjliggör synkron kod (Dash callbacks) att starta/stoppa asynkrona processer
- Hanterar orchestrator som en global singleton
- Är trådsäker med proper locking

### 2. Automatisk Start

När du byter till "Live API" i dashboarden:
1. `get_data_stream(use_mock=False)` anropas
2. En DataOrchestrator skapas automatiskt
3. OrchestratorManager startar den i bakgrunden
4. REST batch-loop, WebSocket handler och rotation-loop startar
5. Status rapporteras till dashboarden

### 3. Automatisk Stopp

När du byter tillbaka till "Mock Data":
1. Dashboard callback detekterar ändringen
2. `stop_global_orchestrator()` anropas
3. Alla tasks avbryts korrekt
4. WebSocket-anslutning stängs
5. Bakgrundstråden avslutas

## API

### Funktioner

```python
from modules.data_stream import (
    get_data_stream,
    get_orchestrator_manager,
    start_global_orchestrator,
    stop_global_orchestrator,
    get_global_orchestrator_status
)

# Skapa data stream (startar automatiskt om live)
data_stream = get_data_stream(use_mock=False)

# Hämta status
status = get_global_orchestrator_status()
print(status)
# {
#     'running': True,
#     'mode': 'live',
#     'uptime': '0:05:23',
#     'error': None,
#     'thread_alive': True,
#     'loop_running': True
# }

# Manuell stopp (vanligtvis inte nödvändigt)
stop_global_orchestrator()
```

### OrchestratorManager Metoder

```python
manager = get_orchestrator_manager()

# Starta orchestrator
success = manager.start_orchestrator(orchestrator)

# Stoppa orchestrator
success = manager.stop_orchestrator()

# Hämta status
status = manager.get_status()
```

## Felhantering

Systemet hanterar fel robustly:

1. **Nätverksfel**: Om API inte kan nås, försöker orchestrator starta men stoppar vid fel
2. **Task-fel**: Enskilda tasks som kraschar påverkar inte andra tasks
3. **Cleanup**: Alla resurser städas upp korrekt vid stopp
4. **Status-rapportering**: Fel rapporteras via `get_status()` och visas i dashboarden

## Dashboard Integration

### Status i "Recent Errors & Warnings"

I Data Source-panelen visas nu:

**Live API Mode:**
```
🟢 [14:23:45] Orchestrator Manager: RUNNING (uptime: 0:05:23)
🟢 [14:23:45] REST Task: running
🟢 [14:23:45] WS Listen Task: running
🟢 [14:23:45] WS Rotation Task: running
📊 Active symbols in cache: 95
📈 Top trending: AAPL, TSLA, NVDA, GOOGL, MSFT
```

**Mock Data Mode:**
```
🟡 [14:23:45] Running in mock data mode
🟢 [14:23:45] Orchestrator properly stopped (mock mode)
🟢 [14:21:45] Mock data generator active
```

**Fel-scenario:**
```
🔴 [14:23:45] Orchestrator Manager: STOPPED - [Errno -5] No address associated with hostname
🟡 [14:23:45] REST Task: stopped
🟡 [14:23:45] WS Listen Task: stopped
🔴 WebSocket connection errors: 3
```

## Testning

Kör testerna för att verifiera funktionaliteten:

```bash
# Fullständigt test (kräver nätverksåtkomst)
python tests/test_data_stream_autostart.py

# Förenklat test (fungerar utan nätverk)
python tests/test_orchestrator_autostart_simple.py
```

## Tekniska Detaljer

### Tråd-säkerhet

OrchestratorManager använder:
- `threading.Lock` för att skydda kritiska sektioner
- Global singleton med lazy initialization
- Thread-safe status queries

### Asyncio Event Loop

- En ny event loop skapas för bakgrundstråden
- Loopen körs i `run_forever()` mode
- Tasks skapas med `asyncio.create_task()`
- Proper cleanup med `loop.stop()` och `loop.close()`

### Återanvändning

Om orchestrator redan körs, återanvänds den:
```python
# Första anropet - skapar och startar
stream1 = get_data_stream(use_mock=False)

# Andra anropet - återanvänder samma orchestrator
stream2 = get_data_stream(use_mock=False)

# stream1 och stream2 pekar på samma orchestrator-instans
```

## Begränsningar

1. **En orchestrator åt gången**: Endast en global orchestrator kan köra samtidigt
2. **Synkron interface**: Även om orchestrator är async, är externa interface synkront
3. **Ingen progressbar**: Start sker i bakgrunden utan visuell indikator (status visas i panelen)

## Framtida Förbättringar

- [ ] Progress indicator under orchestrator-start
- [ ] Restart-funktion för att återansluta vid nätverksfel
- [ ] Health checks med automatisk recovery
- [ ] Metrics och monitoring för orchestrator-prestanda
- [ ] Support för multipla orchestrators med olika konfigurationer

## Felsökning

### Orchestrator startar inte

1. Kontrollera API-nyckel i `config.py`
2. Verifiera nätverksåtkomst
3. Kolla loggar för felmeddelanden
4. Testa med mock mode först

### Tasks visar "stopped"

1. Vänta lite - tasks kan ta några sekunder att starta
2. Kontrollera för nätverksfel i "Recent Errors"
3. Försök stoppa och starta om orchestrator

### Memory leaks

1. Se till att stoppa orchestrator korrekt
2. Använd `stop_global_orchestrator()` vid shutdown
3. Kontrollera att tråden avslutas

## Support

För frågor eller problem, öppna ett issue i GitHub-repositoryt.
