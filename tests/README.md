# Obscuraflow Tests

Denna mapp innehåller tester för Obscuraflow moduler.

## test_module_flow.py

Ett integrationstest som verifierar flödet mellan de fyra första modulerna:

- **data_stream**: Hämtar marknadsdata och analyserar trender
- **trending_pool**: Rankar symboler baserat på trenddata
- **decision_core**: Samlar agentbeslut och analyserar konsensus
- **vote_engine**: Löser konflikter genom viktad röstning

### Köra testet

```bash
cd /home/runner/work/Obscuraflow/Obscuraflow
PYTHONPATH=/home/runner/work/Obscuraflow/Obscuraflow python tests/test_module_flow.py
```

Eller från projektets rotkatalog:

```bash
PYTHONPATH=. python tests/test_module_flow.py
```

### Vad testet gör

1. Initierar alla fyra moduler
2. Hämtar mockdata för marknadsdata (8 symboler)
3. Analyserar trender och uppdaterar trending pool
4. Rankar symboler baserat på score
5. Simulerar agentbeslut från 6 olika agenter
6. Analyserar konsensus för varje symbol
7. Routar beslut till lämpliga moduler
8. Använder vote_engine vid konflikter
9. Visar statistik och sammanfattning

### Förväntad output

Testet skriver ut detaljerad information om:
- Modulinitialisering
- Marknadsdata och trendanalys
- Rankade symboler
- Agentbeslut och konsensus
- Routing och konflikthantering
- Statistik från alla moduler

Testet slutar med:
```
================================================================================
TEST SLUTFÖRT MED FRAMGÅNG! ✓
================================================================================
```

## test_conflict_resolution.py

Ett specifikt test för konflikthantering och viktad röstning.

### Köra testet

```bash
PYTHONPATH=. python tests/test_conflict_resolution.py
```

### Vad testet gör

1. Skapar en konfliktsituation med 50/50 buy/sell beslut
2. Eskalerar till VoteEngine för viktad röstning
3. Beräknar vinnare baserat på confidence och vikter
4. Simulerar utfall och uppdaterar agentsvikter
5. Kör en andra röstning med uppdaterade vikter
6. Visar hur agenternas inflytande förändras över tid

Detta test demonstrerar hur systemet:
- Identifierar konflikter automatiskt
- Löser konflikter genom viktad röstning
- Lär sig från utfall och justerar agentsvikter
- Ger mer inflytande till agenter som presterar bättre

## Mockdata

Testet använder mockdata för att simulera realtidsdata utan att behöva en riktig API-anslutning. Detta gör det möjligt att testa modulerna isolerat och verifiera att de fungerar tillsammans korrekt.

Mockdata inkluderar:
- Aktiepris, volym, förändring och procentuell förändring
- Trendanalys med volym, momentum och volatilitet scores
- Slumpmässiga men realistiska värden för testning

## Köra alla tester

För att köra alla tester i sekvens:

```bash
PYTHONPATH=. python tests/test_module_flow.py && \
PYTHONPATH=. python tests/test_conflict_resolution.py
```
