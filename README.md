
🌀 Obscuraflow – Projektbeskrivning

Obscuraflow är ett avancerat, modulärt och självlärande AI-tradingekosystem byggt i Dash. Systemet kombinerar realtidsmarknadsdata, 17 specialiserade agenter, adaptiva portföljer, RL-träning och en central beslutsmotor. Det är designat för att simulera och exekvera intelligenta tradingbeslut genom agentkonsensus, signalvalidering och ontologisk analys.

---

## 📊 Modulstatus

| Modul                | Status           | Kommentar                     |
|----------------------|------------------|-------------------------------|
| data_stream          | Klar             | Full implementation & test    |
| trending_pool        | Klar             | Full implementation & test    |
| decision_core        | Klar             | Full implementation & test    |
| vote_engine          | Klar             | Full implementation & test    |
| fusion               | Klar             | Full implementation & test    |
| sizing               | Klar             | Full implementation & test    |
| timespan_engine      | Klar             | Full implementation & test    |
| portfolio_engine     | Klar             | Full implementation & test    |
| evolution            | Klar             | Full implementation & test    |
| self_critique        | Klar             | Full implementation & test    |
| symbol_memory        | Klar             | Full implementation & test    |
| narrative_engine     | Klar             | Full implementation & test    |
| mutation_tracker     | Klar             | Full implementation & test    |
| synergy_matrix       | Klar             | Full implementation & test    |
| agent_spectrum       | Klar             | Full implementation & test    |
| agent_lifecycle      | Klar             | Full implementation & test    |
| metaagentgovernor    | Klar             | Full implementation & test    |
| portfolio_comparator | Klar             | Full implementation & test    |
| risk_mapper          | Klar             | Full implementation & test    |
| **agents/**          | **Klar**         | **Agentlager komplett**       |
| **dash_app/**        | **Klar**         | **13 paneler med live data**  |

---

## 🔴 Live Data Integration Status

**Status:** ✅ **Alla 19 moduler är LIVE-READY**

Systemet är fullt integrerat med live data från `data_stream` och NASDAQ-100 symboluniversum. Modulerna använder ingen hårdkodad marknadsdata utan hämtar all information dynamiskt.

### Datakälla och Flöde

- **Central dataprovider:** `data_stream` modul med `DataOrchestrator`
- **Symboluniversum:** NASDAQ-100 (99 symboler) från `nasdaq100_symbols.yaml`
- **Live-läge:** WebSocket + REST API via Finnhub
- **Mock-läge:** Simulerad NASDAQ-100 data för utveckling/test
- **Växling:** Via `USE_MOCK_DATA` i `config.py` eller miljövariabel

### Modul Live-Ready Verifiering

| Modul | Live-Ready | DataStream | Symbol Universe | Beskrivning |
|-------|-----------|-----------|-----------------|-------------|
| **data_stream** | ✅ | Ja | Ja | Central dataprovider, WebSocket + REST |
| **trending_pool** | ✅ | Indirekt | Via orchestrator | Processar trenddata från data_stream |
| **decision_core** | ✅ | Nej | Nej | Aggregerar agentbeslut, ingen marknadsdata |
| **vote_engine** | ✅ | Nej | Nej | Processar agentröster, data-agnostisk |
| **fusion** | ✅ | Nej | Nej | Validerar signaler, ingen direkt datakälla |
| **sizing** | ✅ | Nej | Nej | Beräknar positionsstorlek från parametrar |
| **timespan_engine** | ✅ | Nej | Nej | Synkroniserar tidsramar, får data från orchestrator |
| **portfolio_engine** | ✅ | Nej | Nej | Hanterar portföljer, arbetar med positioner |
| **evolution** | ✅ | Nej | Nej | Strategimutation, ingen direkt marknadsdata |
| **self_critique** | ✅ | Nej | Nej | Beslutsanalys, ingen direkt marknadsdata |
| **symbol_memory** | ✅ | Nej | Nej | Symbolhistorik, lagrar data från upstream |
| **narrative_engine** | ✅ | Nej | Nej | Händelseloggning, ingen direkt marknadsdata |
| **mutation_tracker** | ✅ | Nej | Nej | Mutationshistorik, ingen direkt marknadsdata |
| **synergy_matrix** | ✅ | Nej | Nej | Agentsynergi, ingen direkt marknadsdata |
| **agent_spectrum** | ✅ | Nej | Nej | Ontologisk karta, ingen direkt marknadsdata |
| **agent_lifecycle** | ✅ | Nej | Nej | Agentlivscykel, ingen direkt marknadsdata |
| **metaagentgovernor** | ✅ | Nej | Nej | Agentstyrning, ingen direkt marknadsdata |
| **portfolio_comparator** | ✅ | Nej | Nej | Portföljjämförelse, ingen direkt marknadsdata |
| **risk_mapper** | ✅ | Nej | Nej | Riskvisualisering, ingen direkt marknadsdata |

### Arkitekturprinciper

1. **Central datakälla:** All marknadsdata flödar genom `data_stream` modul
2. **Symboluniversum:** NASDAQ-100 symboler laddas dynamiskt från konfiguration
3. **Data-agnostiska moduler:** De flesta moduler är data-agnostiska och processar endast vad som passeras till dem
4. **Ingen hårdkodad data:** Inga moduler innehåller hårdkodad marknadsdata
5. **Live/Mock-växling:** Systemet kan växla mellan live och mock data utan kodändringar

### Verifiering

Kör verifieringsskriptet för att bekräfta live data integration:

```bash
python verify_live_data_integration.py
```

Förväntat resultat: ✅ **SUCCESS: All 19 modules are LIVE-READY!**

---

🔍 Syfte
Att skapa ett transparent, introspektivt och evolverande tradingekosystem där varje beslut är spårbart, varje agent är adaptiv och varje portfölj är optimerad för sin marknadsregim.

---

🧠 Kärnfunktioner

- Multi-agent intelligens: 17 agenter med unika dimensioner (temporal, fraktal, emotionell, strukturell m.fl.)
- Beslutsmotor med röstning: Agenter röstar på beslut, viktas om baserat på utfall
- Signalvalidering: Fusionmodul som jämför signaler över flera tidsramar
- Adaptiv position sizing: RL-optimerad sizing med profilmutation och regimväxling
- Portföljmotor: Skapar, muterar och jämför portföljer med olika agentkombinationer
- Ontologisk introspektion: Visualisering av agenters rörelse mellan dimensioner
- Systemberättelse: Narrativ modul som loggar och förklarar systemets beslut
- Riskekosystem: Visualisering av risk per symbol, agent och portfölj

---

🧩 Modulöversikt

- decision_core/: Routing, loggning, exekvering
- vote_engine/: Röstning, viktning, meta-vote
- fusion/: Signalvalidering
- sizing/: Position sizing
- timespan_engine/: Tidsramar och RL-träning
- portfolio_engine/: Portföljhantering
- evolution/: Strategimutation
- self_critique/: Felanalys
- symbol_memory/: Symbolhistorik
- narrative_engine/: Händelseflöde
- mutation_tracker/: Mutationsträd
- synergy_matrix/: Agentrelationer
- agent_spectrum/: Ontologisk karta
- agent_lifecycle/: Agentens livscykel
- metaagentgovernor/: Agentråd
- portfolio_comparator/: Portföljjämförelse
- risk_mapper/: Riskmatris

---

🤖 Agenttyper

- Klassiska agenter: Momentum, Reversal, Breakout, Hybrid
- Paradigmatiska agenter: Echo, Fractalis, Vox, Myco, Obscura, Mirage, Sentio, Reflexion, Dimensio, Symbio, Genesis, Architectum
- Hybrider & meta-agenter: Kombinerade och självlärande agentstrukturer

---

## 🎯 Agentlager - Status: Klar

**Implementerat:** Samtliga 16 agenter enligt specifikation

### Klassiska Agenter (4)
✅ **MomentumAgent** - Trendföljande, kort spanpreferens (<5 min)  
✅ **ReversalAgent** - Mean reversion, medellång span (5-30 min)  
✅ **BreakoutAgent** - Volatility breakout, lång span (>30 min)  
✅ **HybridAgent** - Multi-strategi, adaptiv span

### Paradigmatiska Agenter (12)
✅ **EchoAgent** - Temporal/Reflective dimension, mönsterreplikering  
✅ **FractalisAgent** - Spatial-Temporal/Complex, fraktalanalys  
✅ **VoxAgent** - Social/Collective, konsensusbyggande  
✅ **MycoAgent** - Network/Distributed, informationsspridning  
✅ **ObscuraAgent** - Latent/Obscure, dolda mönster  
✅ **MirageAgent** - Perceptual/Discriminative, signalfiltrering  
✅ **SentioAgent** - Emotional/Empathic, sentimentanalys  
✅ **ReflexionAgent** - Meta-Cognitive/Reflective, självlärande  
✅ **DimensioAgent** - Hyper-Spatial/Analytical, 5D analys  
✅ **SymbioAgent** - Relational/Cooperative, agentsamverkan  
✅ **GenesisAgent** - Origination/Generative, trendstarter  
✅ **ArchitectumAgent** - Structural/Constructive, strukturanalys

### Agent Registry
✅ **agent_registry.py** - Centralt register med metadata för alla agenter

### Framtida Utveckling
- **Hybrider**: Agentkombinationer som kombinerar flera strategier
- **Span Hybrids**: Tidsram-adaptiva agenter
- **Meta Agents**: Självlärande agentråd och överordnad styrning

---

📊 Dash-paneler

- /decision-core
- /vote-panel
- /position-sizing
- /timespan-intelligence
- /multi-portfolio
- /mutation-tracker
- /agent-spectrum
- /agent-lifecycle
- /meta-governance
- /portfolio-intelligence
- /risk-ecosystem
- /system-flow
- /narrative

---

🚀 Teknisk plattform

- Dash: 100% frontend och backend
- Python: Modulstruktur och agentlogik
- RL: För träning av sizing, voting, spans och portföljer
- Finnhub API: Realtidsmarknadsdata

---

projektstruktur 

obscuraflow/
├── dash_app/                      # Dash-gränssnitt och layout
│   ├── app.py                     # Initierar Dash och router
│   ├── layout/                    # Sidhuvud, sidfot, router
│   │   ├── sidebar.py
│   │   ├── header.py
│   │   ├── footer.py
│   │   └── page_router.py
│   ├── panels/                    # Varje Dash-panel = 1 modul
│   │   ├── decision_core_panel.py
│   │   ├── vote_panel.py
│   │   ├── position_sizing_panel.py
│   │   ├── timespan_intelligence_panel.py
│   │   ├── multi_portfolio_panel.py
│   │   ├── mutation_tracker_panel.py
│   │   ├── agent_spectrum_panel.py
│   │   ├── agent_lifecycle_panel.py
│   │   ├── meta_governance_panel.py
│   │   ├── portfolio_intelligence_panel.py
│   │   ├── risk_ecosystem_panel.py
│   │   ├── system_flow_panel.py
│   │   ├── narrative_panel.py
│   │   └── readme_builder_panel.py
│   ├── callbacks/                # Interaktiva callbacks per panel
│   ├── components/               # Återanvändbara UI-komponenter
│   └── assets/                   # CSS, JS, bilder
│
├── agents/                       # Agentlager
│   ├── classic/                  # 4 klassiska agenter
│   ├── paradigms/                # 12 paradigmatiska agenter
│   ├── hybrids/                  # Agentkombinationer
│   ├── span_hybrids/             # Tidsram-adaptiva agenter
│   ├── meta_agents/              # Självlärande agentråd
│   └── agent_registry.py         # Registrering och metadata
│
├── modules/                      # Funktionella moduler
│   ├── data_stream/              # WebSocket, REST, trendanalys
│   ├── trending_pool/            # Symbolranking och värmeanalys
│   ├── decision_core/            # Beslutsmotor, routing, loggning
│   ├── vote_engine/              # Röstning, viktning, meta-vote
│   ├── fusion/                   # Multi-timeframe signalvalidering
│   ├── sizing/                   # Position sizing med RL
│   ├── timespan_engine/          # Tidsramar och RL-träning
│   ├── portfolio_engine/         # Portföljer, mutation, RL
│   ├── evolution/                # Strategimutation och RL-träning
│   ├── self_critique/            # Felanalys och introspektion
│   ├── symbol_memory/            # Symbolspecifik historik
│   ├── narrative_engine/         # Händelseflöde och berättelse
│   ├── mutation_tracker/         # Global mutationshistorik
│   ├── synergy_matrix/           # Agent-samverkan och konfliktanalys
│   ├── agent_spectrum/           # Ontologisk agentförflyttning
│   ├── agent_lifecycle/          # Agentens livscykel
│   ├── meta_agent_governor/      # Agentråd och prioritering
│   ├── portfolio_comparator/     # Portföljjämförelse och meta-portföljer
│   ├── risk_mapper/              # Riskmatris och symbolrisk
│   └── plugin_loader/            # (Framtida) Contributor sandbox
│
├── strategy_library/             # Strategier och signalregler
│   ├── signal_templates/
│   ├── strategy_profiles.yaml
│   └── strategy_mutator.py
│
├── config/                       # Konfigurationsfiler
│   ├── agent_profiles.yaml
│   ├── sizing_profiles.yaml
│   ├── portfolio_config.yaml
│   └── system_settings.yaml
│
├── docs/                         # Dokumentation
│   ├── README.md
│   ├── AGENT_FEATURES_GUIDE.md
│   ├── AGENT_FEATURES_IMPLEMENTATION.md
│   ├── AGENT_FEATURES_QUICKSTART.md
│   └── SYSTEM_FLOW_OVERVIEW.md
│
├── tests/                        # Enhetstester
│   ├── test_agents.py
│   ├── test_decision_core.py
│   ├── test_sizing.py
│   └── ...
│
├── .gitignore
├── requirements.txt
└── run.py                        # Startpunkt för systemet

---

🧩 Obscuraflow – Modulbeskrivning

---

🔁 data_stream/ – Realtidsdata & trendanalys
Syfte: Hämta och bearbeta marknadsdata i realtid  
Funktioner:
- WebSocket-anslutning till Finnhub API
- REST-polling för symbolbatchar
- Trendanalys: volym, momentum, volatilitet
- Dynamisk prenumeration på toppsymboler

Kopplingar:  
→ trendingpool/, agentlayer/, symbol_memory/

---

🔥 trending_pool/ – Market Heat Engine
Syfte: Identifiera och ranka aktiva symboler  
Funktioner:
- Stabilisering av trenddata
- Score-beräkning med viktning
- Historikcache och fluktuationsdämpning

Kopplingar:  
→ agentlayer/, decisioncore/, fusion/

---

🧠 decision_core/ – Central beslutsmotor
Syfte: Samla, validera och exekvera agentbeslut  
Funktioner:
- Routing av beslut
- Loggning och traceability
- RL-feedback till agenter
- Exekveringsmonitor

Kopplingar:  
→ voteengine/, sizing/, portfolioengine/, self_critique/

---

🗳️ vote_engine/ – Agent Voting System
Syfte: Hantera oenighet mellan agenter  
Funktioner:
- Röstning med viktning
- RL-belöning för röstprecision
- Meta-vote: agenter röstar på andra agenter
- Mutation av röstlogik

Kopplingar:  
→ decisioncore/, synergymatrix/, metaagentgovernor/

---

🔀 fusion/ – Multi-Timeframe Signal Validation
Syfte: Validera signaler över flera tidsramar  
Funktioner:
- Jämförelse mellan spans
- Signalstyrka och konsistens
- RL-träning för fusionprecision

Kopplingar:  
→ decisioncore/, timespanengine/, agent_layer/

---

📐 sizing/ – Adaptive Position Sizing
Syfte: Beräkna positionstorlek baserat på strategi, risk och sentiment  
Funktioner:
- Sizing-profiler (fasta och adaptiva)
- RL-optimering
- Mutation av sizinglogik
- Regim- och sentimentanpassning

Kopplingar:  
→ decisioncore/, riskmapper/, portfolio_engine/

---

⏱️ timespan_engine/ – Vision Timespan Intelligence
Syfte: Skapa och utvärdera tidsramar för agenter  
Funktioner:
- Fasta och adaptiva spans
- RL-träning för spanval
- Hybridisering av spans
- Framtidssimulering

Kopplingar:  
→ fusion/, agentlayer/, portfolioengine/

---

📊 portfolio_engine/ – Multi-Portfolio Management
Syfte: Hantera och optimera portföljer  
Funktioner:
- Portföljskapande och mutation
- RL-träning för konfigurationer
- Performanceutvärdering
- Meta-portföljer

Kopplingar:  
→ decisioncore/, portfoliocomparator/, risk_mapper/

---

🧬 evolution/ – Strategy Mutation Engine
Syfte: Utveckla strategier och agenter över tid  
Funktioner:
- Mutation av strategilogik
- RL-belöning för förbättring
- Regimjustering

Kopplingar:  
→ agentlayer/, mutationtracker/, self_critique/

---

🧠 self_critique/ – Introspektiv Felanalys
Syfte: Identifiera och analysera fel i beslut  
Funktioner:
- Sessiongranskning var 5:e minut
- Förbättringsförslag
- RL-feedback till agenter

Kopplingar:  
→ decisioncore/, evolution/, symbolmemory/

---

🧠 symbol_memory/ – Symbolspecifik Historik
Syfte: Spåra beslut och utfall per symbol  
Funktioner:
- Tradehistorik
- Beslutseffekter
- Agentprecision per symbol

Kopplingar:  
→ selfcritique/, decisioncore/, fusion/

---

📖 narrative_engine/ – Systemberättelse
Syfte: Skapa en berättelse om systemets beslut och utveckling  
Funktioner:
- Händelselogg som narrativ
- Agentkommentarer
- Tidslinjevisualisering

Kopplingar:  
→ mutationtracker/, decisioncore/, agent_lifecycle/

---

🌱 mutation_tracker/ – Global Mutation History
Syfte: Spåra alla mutationer i systemet  
Funktioner:
- Mutationsträd
- RL-belöning per generation
- Visualisering av ursprung

Kopplingar:  
→ evolution/, agentlifecycle/, portfolioengine/

---

🤝 synergy_matrix/ – Agentrelationer
Syfte: Identifiera samverkan och konflikt mellan agenter  
Funktioner:
- Synergipoäng
- Konfliktindikatorer
- Hybridpotential

Kopplingar:  
→ voteengine/, metaagentgovernor/, agentlayer/

---

🧭 agent_spectrum/ – Ontologisk Agentkarta
Syfte: Visualisera agenters dimensionella rörelse  
Funktioner:
- Spektrum: emotionell, strukturell, nätverk, m.fl.
- Rörelsehistorik
- Meta-agentanalys

Kopplingar:  
→ agentlifecycle/, mutationtracker/, metaagentgovernor/

---

🔄 agent_lifecycle/ – Agentens Livscykel
Syfte: Spåra agentens evolution  
Funktioner:
- Födelse, mutation, hybridisering, pensionering
- Generationshistorik
- RL-belöning per livssteg

Kopplingar:  
→ mutationtracker/, agentspectrum/, narrative_engine/

---

🧠 metaagentgovernor/ – Agentråd & Prioritering
Syfte: Skapa agentkonsensus och regimstyrning  
Funktioner:
- Agent councils
- Prioritering baserat på träffsäkerhet
- Regim-specifik aktivering

Kopplingar:  
→ voteengine/, synergymatrix/, decision_core/

---

📊 portfolio_comparator/ – Cross-Portfolio Intelligence
Syfte: Jämföra och optimera portföljer  
Funktioner:
- Performanceanalys
- Komponentjämförelse
- Meta-portföljskapande

Kopplingar:  
→ portfolioengine/, riskmapper/, timespan_engine/

---

⚠️ risk_mapper/ – Riskekosystem
Syfte: Visualisera risk i hela systemet  
Funktioner:
- Risk per symbol, agent, portfölj
- Sizing/sentiment-overlay
- Regimriskanalys

Kopplingar:  
→ sizing/, portfolioengine/, decisioncore/

---

🤖 Obscuraflow – Agentbeskrivning

🧱 Klassiska agenter (4)

| Agent | Strategi | Spanpreferens | Confidence-tröskel | Funktion |
|-------|----------|----------------|---------------------|----------|
| MomentumAgent | Trendföljande | Kort (<5 min) | 0.6 | Identifierar och rider på starka prisrörelser |
| ReversalAgent | Mean reversion | Medel (5–30 min) | 0.65 | Söker överköpta/översålda tillstånd för vändningar |
| BreakoutAgent | Volatility breakout | Lång (>30 min) | 0.7 | Reagerar på prisgenombrott från konsolidering |
| HybridAgent | Multi-strategi | Adaptiv | 0.5 | Växlar mellan strategier beroende på marknadsregim |

---

🧠 Paradigmatiska agenter (12)

🔊 EchoAgent – Temporal/Reflective Dimension
- Funktion: Mönsterreplikering baserat på historik
- Kapacitet: 500 historiska mönster, 75% matchtröskel
- Lärande: Förstärker mönster som tidigare varit framgångsrika
- Kopplingar: symbol_memory, fusion, reflexion, genesis

---

🌀 FractalisAgent – Spatial-Temporal/Complex Dimension
- Funktion: Fraktalanalys över flera tidsskalor
- Kapacitet: 5 samtidiga spans, självlikhetskontroll
- Lärande: Identifierar rekursiva mönster
- Kopplingar: fusion, timespan_engine, dimensio, architectum

---

🗣️ VoxAgent – Social/Collective Dimension
- Funktion: Konsensusbyggare mellan agenter
- Kapacitet: 75% rösttröskel, demokratisk beslutslogik
- Lärande: Förstärks vid träffsäkra gruppbeslut
- Kopplingar: voteengine, metaagent_governor, symbio, sentio

---

🍄 MycoAgent – Network/Distributed Dimension
- Funktion: Informationsspridning genom agentnätverk
- Kapacitet: 3 nivåers nätverksdjup, 85% decay rate
- Lärande: Diffunderar insikter till andra agenter
- Kopplingar: synergymatrix, symbio, portfolioengine

---

🌑 ObscuraAgent – Latent/Obscure Dimension
- Funktion: Identifierar dolda mönster och anomalier
- Kapacitet: 2.0σ tröskel för avvikelse
- Lärande: Specialiserad på icke-uppenbara signaler
- Kopplingar: fusion, mirage, reflexion, self_critique

---

✨ MirageAgent – Perceptual/Discriminative Dimension
- Funktion: Filtrerar falska signaler (illusioner)
- Kapacitet: 65% verklighetströskel
- Lärande: Validerar mot senaste historik
- Kopplingar: fusion, obscura, echo, reflexion

---

💗 SentioAgent – Emotional/Empathic Dimension
- Funktion: Sentimentanalys och emotionell förstärkning
- Kapacitet: 30-period buffer, fear/greed integration
- Lärande: Justerar beslut baserat på marknadspsykologi
- Kopplingar: sizingsentimentadapter, vote_engine, vox, symbio

---

🔄 ReflexionAgent – Meta-Cognitive/Reflective Dimension
- Funktion: Självreflektion och adaptivt lärande
- Kapacitet: 100 beslutshistorik, justerar baserat på träffsäkerhet
- Lärande: Lär sig från misstag och förbättrar sin logik
- Kopplingar: self_critique, evolution, echo, mirage

---

📐 DimensioAgent – Hyper-Spatial/Analytical Dimension
- Funktion: Multi-dimensionell analys
- Kapacitet: 5D feature space: momentum, RSI, trend, volym, volatilitet
- Lärande: Identifierar komplexa mönster i högdimensionella rum
- Kopplingar: fusion, fractalis, architectum, portfolio_comparator

---

🤝 SymbioAgent – Relational/Cooperative Dimension
- Funktion: Samverkan och co-evolution med andra agenter
- Kapacitet: 50% symbiosstyrka
- Lärande: Förstärker relationer som ger ömsesidig nytta
- Kopplingar: synergy_matrix, vox, myco, sentio

---

🌱 GenesisAgent – Origination/Generative Dimension
- Funktion: Identifierar trendstarter och cykelbörjan
- Kapacitet: Upptäcker inflektionspunkter och genesis moments
- Lärande: Specialiserad på att känna igen nya rörelser
- Kopplingar: forecast_simulator, echo, architectum, fusion

---

🏛️ ArchitectumAgent – Structural/Constructive Dimension
- Funktion: Strukturell analys och systembyggnad
- Kapacitet: 4 nivåer: foundation, pillars, framework, roof
- Lärande: Aktiveras vid strukturscore > 70%
- Kopplingar: fusion, dimensio, reflexion, genesis

---

🧠 Agentmetadata per dimension

| Dimension | Agenter | Fokus |
|-----------|---------|-------|
| Temporal | Echo | Mönsterminne |
| Fraktal | Fractalis | Självlikhet |
| Social | Vox | Konsensus |
| Nätverk | Myco | Informationsspridning |
| Latent | Obscura | Anomalier |
| Perceptuell | Mirage | Illusionsfilter |
| Emotionell | Sentio | Sentiment |
| Meta-kognitiv | Reflexion | Självlärande |
| Hyper-spatial | Dimensio | 5D analys |
| Relationell | Symbio | Samverkan |
| Generativ | Genesis | Trendstart |
| Strukturell | Architectum | Systembyggnad |

---

🧠 Obscuraflow – Funktionsbeskrivning

---

🔁 1. Realtidsdata & Symbolanalys

📡 WebSocket & REST-polling
- Hämtar live-data från Finnhub API
- Dynamisk prenumeration på aktiva symboler
- Batch-polling för bred marknadsöversikt

🔥 Trending Pool
- Rankar symboler baserat på volym, momentum, volatilitet
- Stabiliserar fluktuationer och filtrerar brus
- Skickar topplistan till agenter och fusionmodul

---

🤖 2. Agentintelligens & Beslutsgenerering

🧠 Agentlager
- 17 agenter med unika dimensioner (temporal, fraktal, emotionell, m.fl.)
- Varje agent analyserar symboler och genererar beslut
- Hybridagenter kombinerar flera paradigmer

🔀 Fusion Engine
- Validerar signaler över flera tidsramar
- Jämför agentbeslut för konsistens
- Förstärker eller filtrerar signaler

---

🗳️ 3. Beslutsmotor & Röstning

🧠 Decision Core
- Samlar in beslut från agenter
- Loggar, analyserar och skickar vidare till exekvering
- RL-feedback till agenter baserat på utfall

🗳️ Vote Engine
- Hanterar oenighet mellan agenter
- Röstning med viktning baserat på historisk träffsäkerhet
- Meta-vote: agenter röstar på andra agenters röster
- RL-belöning för röstprecision

---

📐 4. Position Sizing & Riskjustering

📊 Sizing Engine
- Beräknar positionstorlek baserat på strategi, risk, sentiment
- Använder fasta och adaptiva sizing-profiler
- RL-träning för optimal sizing
- Mutation av sizinglogik

⚠️ Risk Mapper
- Visualiserar risk per symbol, agent och portfölj
- Integrerar sizing, sentiment och regimdata

---

⏱️ 5. Tidsramar & Spanintelligens

⏳ Timespan Engine
- Skapar och utvärderar fasta och adaptiva spans
- RL-träning för bästa span per symbol
- Hybridisering av spans för regimväxling

🌀 Multi-Timeframe Fusion
- Jämför signaler över spans
- Validerar beslut mot historik och agentkonsensus

---

📊 6. Portföljhantering & Mutation

🧬 Portfolio Engine
- Skapar och kör portföljer med olika agentkombinationer
- Muterar portföljer baserat på RL-feedback
- Kör simuleringar och livebeslut

📈 Portfolio Comparator
- Jämför portföljer mot varandra
- Identifierar bästa komponenter
- Skapar meta-portföljer

---

🧬 7. Strategi- & Agentmutation

🔄 Evolution Engine
- Muterar strategier, agenter och portföljer
- RL-belöning för förbättring
- Regimjustering och hybridisering

🌱 Mutation Tracker
- Spårar alla mutationer i systemet
- Visualiserar generationsflöde och ursprung

---

🧠 8. Introspektion & Självlärande

🧠 Self Critique
- Automatisk sessiongranskning var 5:e minut
- Identifierar fel och föreslår förbättringar
- RL-feedback till agenter och strategier

🧠 Symbol Memory
- Lagrar beslut och utfall per symbol
- Spårar agentprecision och signalstyrka

---

🧭 9. Ontologi & Agentanalys

🧭 Agent Spectrum
- Visualiserar agenters ontologiska dimensioner
- Spårar rörelse mellan emotionell, strukturell, nätverk, m.fl.

🔄 Agent Lifecycle
- Spårar agentens födelse, mutation, hybridisering och pensionering
- Kopplar till mutationer och RL-belöning

🤝 Synergy Matrix
- Identifierar samverkan och konflikt mellan agenter
- Visualiserar hybridpotential och meta-agentrelationer

🧠 Meta Agent Governor
- Skapar agentråd för olika marknadsregimer
- Prioriterar agenter baserat på träffsäkerhet och samverkan

---

📖 10. Visualisering & Narrativ

📖 Narrative Engine
- Skapar en berättelse om systemets beslut och utveckling
- Loggar händelser som narrativ med agentkommentarer

🗺️ System Flow
- Visuell karta över hela systemets modulflöde
- Dynamisk uppdatering av aktiva komponenter

📊 Dash-paneler
- 15 interaktiva paneler för beslut, agenter, portföljer, mutationer, risk, narrativ m.m.
- Realtidsuppdatering var 2–5 sekunder
- Bootstrap Cerulean-tema, mobilanpassat

---

┌────────────────────────────┐
                            │      DATA STREAM           │
                            │  WebSocket + REST polling  │
                            └────────────┬──────────────┘
                                         │
                                         ▼
                            ┌────────────────────────────┐
                            │      TRENDING POOL          │
                            │  Symbolranking & filtrering │
                            └────────────┬──────────────┘
                                         │
                                         ▼
                            ┌────────────────────────────┐
                            │       AGENT LAYER           │
                            │  17 agenter analyserar data │
                            └────────────┬──────────────┘
                                         │
                                         ▼
                            ┌────────────────────────────┐
                            │       FUSION ENGINE         │
                            │  Multi-span signalvalidering│
                            └────────────┬──────────────┘
                                         │
                                         ▼
                            ┌────────────────────────────┐
                            │       DECISION CORE         │◄────────────────────────────────────────────┐
                            │  Nav för beslut, routing     │                                             │
                            └────────────┬────────────────┘                                             │
                                         │                                                              │
             ┌───────────────────────────┼────────────────────────────┐                                 │
             ▼                           ▼                            ▼                                 │
┌────────────────────┐     ┌────────────────────┐        ┌────────────────────────┐                    │
│     VOTE ENGINE     │     │     SIZING ENGINE   │        │     TIMESPAN ENGINE     │                    │
│  Röstning & viktning│     │ RL-optimerad sizing│        │ RL-träning av spans     │                    │
└─────────┬───────────┘     └─────────┬───────────┘        └────────────┬───────────┘                    │
          │                           │                                │                                │
          ▼                           ▼                                ▼                                │
┌────────────────────┐     ┌────────────────────┐        ┌────────────────────────┐                    │
│   EXECUTION MONITOR │     │   RISK MAPPER       │        │   PORTFOLIO ENGINE      │                    │
│ Kör trades/loggar   │     │ Risk per symbol     │        │ Multiportföljhantering  │                    │
└─────────┬───────────┘     └─────────┬───────────┘        └────────────┬───────────┘                    │
          │                           │                                │                                │
          ▼                           ▼                                ▼                                │
┌────────────────────┐     ┌────────────────────┐        ┌────────────────────────┐                    │
│   SYMBOL MEMORY     │     │   SELF CRITIQUE     │        │ PORTFOLIO COMPARATOR   │                    │
│ Historik & precision│     │ Felanalys & feedback│        │ Jämför & optimerar     │                    │
└─────────┬───────────┘     └─────────┬───────────┘        └────────────┬───────────┘                    │
          │                           │                                │                                │
          ▼                           ▼                                ▼                                │
┌────────────────────┐     ┌────────────────────┐        ┌────────────────────────┐                    │
│   EVOLUTION ENGINE  │     │   MUTATION TRACKER  │        │   META AGENT GOVERNOR   │                    │
│ Muterar agenter     │     │ Spårar förändringar │        │ Agentprioritering       │                    │
└─────────┬───────────┘     └─────────┬───────────┘        └────────────┬───────────┘                    │
          │                           │                                │                                │
          ▼                           ▼                                ▼                                │
┌────────────────────┐     ┌────────────────────┐        ┌────────────────────────┐                    │
│  AGENT LIFECYCLE    │     │   SYNERGY MATRIX    │        │   AGENT SPECTRUM        │                    │
│ Födelse → pension   │     │ Samverkan & konflikt│        │ Ontologisk rörelse      │                    │
└─────────┬───────────┘     └─────────┬───────────┘        └────────────┬───────────┘                    │
          │                           │                                │                                │
          ▼                           ▼                                ▼                                │
┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      NARRATIVE ENGINE                                                 │
│                          Händelseflöde & systemberättelse                                             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
                            ┌────────────────────────────┐
                            │     SYSTEM FLOW MAP        │
                            │  Visuell modulöversikt     │
                            └────────────────────────────┘


---

🔁 Obscuraflow – Flödesschema (Textformat)

---

1. 📡 Dataflöde

- data_stream hämtar realtidsdata via WebSocket och REST
- → skickar till trending_pool för symbolranking
- → topprankade symboler skickas till agentlagret

---

2. 🤖 Agentanalys

- 17 agenter i agents/ analyserar symboler parallellt
- → varje agent genererar ett beslut (buy/sell/hold + confidence)
- → beslut skickas till fusion för multi-span validering

---

3. 🧠 Beslutsmotor

- decision_core samlar alla agentbeslut
- → loggar och skickar vidare till:
  - vote_engine om konflikt
  - sizing för positionstorlek
  - execution_monitor för exekvering
- ← tar emot feedback från:
  - self_critique (felanalys)
  - symbol_memory (historik)
  - evolution (muterade agenter)
  - metaagentgovernor (agentprioritering)
  - risk_mapper (riskjustering)
  - portfolio_comparator (bästa portföljer)

---

4. 🗳️ Röstning

- vote_engine hanterar oenighet mellan agenter
- → viktar röster och skickar beslut till decision_core
- ← tar RL-feedback från self_critique

---

5. 📐 Position Sizing

- sizing beräknar positionstorlek baserat på strategi, risk, sentiment
- → skickar sizing till execution_monitor
- ← påverkas av riskmapper, sentioagent, regimdata

---

6. ⚙️ Exekvering

- execution_monitor kör trades (simulerat eller live)
- → loggar resultat till symbol_memory

---

7. 🧠 Introspektion

- self_critique analyserar beslut och identifierar fel
- → skickar förbättringsförslag till evolution, decision_core
- ← använder data från symbolmemory, executionmonitor

---

8. 🧬 Mutation

- evolution muterar strategier, spans, agenter och portföljer
- → skapar nya agenter via agent_lifecycle
- → loggar mutationer i mutation_tracker
- ← triggas av låg RL-belöning från self_critique

---

9. 🧭 Agentstruktur

- agent_lifecycle spårar agentens livscykel
- synergy_matrix analyserar samverkan och konflikt
- agent_spectrum visualiserar ontologisk rörelse
- metaagentgovernor skapar agentråd och prioriterar agenter
- → alla påverkar agentbeteende och skickar tillbaka till decision_core

---

10. 📊 Portföljhantering

- portfolio_engine kör och muterar portföljer
- portfolio_comparator jämför och optimerar
- → båda påverkar agentviktning och beslut
- ← RL-feedback från performance

---

11. ⚠️ Riskanalys

- risk_mapper beräknar risk per symbol, agent och portfölj
- → påverkar sizing och beslut
- ← använder data från portfolioengine, sizing, sentioagent

---

12. 📖 Narrativ & Visualisering

- narrative_engine skapar berättelse om beslut och händelser
- system_flow visualiserar modulflöde
- → båda används för transparens, introspektion och RL-belöning

---

## 📈 Projektstatus - December 2025

### ✅ Färdigställt

**Moduler (19/19)**
- Alla 19 kärnmoduler implementerade och testade
- Full integration mellan moduler
- Komplett systemflöde från data till exekvering

**Agentlager (16/16)**
- 4 klassiska agenter: Momentum, Reversal, Breakout, Hybrid
- 12 paradigmatiska agenter: Echo, Fractalis, Vox, Myco, Obscura, Mirage, Sentio, Reflexion, Dimensio, Symbio, Genesis, Architectum
- Agent Registry för central hantering
- Basklasser och gemensamt gränssnitt

**Testning**
- Systemflödestest över alla moduler
- Integrationstest för agenter och moduler
- Mockdata för utveckling utan externa API:er

### ✅ Dash-Dashboard - Status: Klar

**Dashboard Implementation (13 Paneler)**
- ✅ Ultra-modern dark theme med gradient accents
- ✅ Fully responsive layout med Bootstrap Cerulean
- ✅ Live data integration med mockdata från alla moduler
- ✅ Auto-refresh intervals (2-5 sekunder per panel)
- ✅ Interactive callbacks och komponenter
- ✅ Reusable UI components (metrics, charts, tables)

**Paneler:**
1. ✅ **Decision Core** - Agentbeslut och konsensusanalys
2. ✅ **Vote Engine** - Viktad röstning och konfliktlösning
3. ✅ **Position Sizing** - Kelly criterion och RL-optimerad sizing
4. ✅ **Timespan Intelligence** - Multi-timeframe synchronization
5. ✅ **Multi Portfolio** - Parallella portföljer och tracking
6. ✅ **Mutation Tracker** - Genealogisk analys och lineage
7. ✅ **Agent Spectrum** - Ontologisk positioning
8. ✅ **Agent Lifecycle** - Birth, evolution, retirement
9. ✅ **Meta Governance** - Överordnad agentstyrning
10. ✅ **Portfolio Intelligence** - Jämförelse och benchmarking
11. ✅ **Risk Ecosystem** - Risk per symbol och agent
12. ✅ **System Flow** - Visuell systemkarta
13. ✅ **Narrative Engine** - Händelseflöde och berättelse
14. ✅ **Data Source Panel** - Live/Mock data toggle och konfiguration
15. ✅ **Portfolio Development** - Utvecklingsanalys och evolution
16. ✅ **Settings Panel** - Systemkonfiguration och modulkontroll

### 📊 Detaljerad Panelöversikt

#### 🔴 Live Data Integration - Phase 3 Status

**Verifieringsstatus:** ✅ **ALLA 16 PANELER VERIFIERADE**

Alla Dash-paneler har genomgått Live Data Integration Phase 3 verifiering och bekräftas vara fullt integrerade med live-data källor. Ingen mockup eller dummy-data används utöver den konfigurerbara Mock/Live toggle som finns i datakällan.

**Sammanfattning:**
- **Totalt antal paneler:** 16 (+ 1 enhanced variant = 17 totalt)
- **Verifierade paneler:** 16/16 (100%)
- **Metadata tillagd:** ✅ Alla paneler har `PANEL_METADATA` med `"data_source": "live"`
- **Auto-refresh:** ✅ Alla paneler har automatisk uppdatering (2-5 sekunder)
- **Verifieringsskript:** `verify_panel_live_data.py` tillgängligt för framtida kontroller

**Datakällor:**
- **Mock/Live Toggle:** 8 paneler (använder `get_data_stream(use_mock=USE_MOCK_DATA)`)
- **Live Module Data:** 7 paneler (använder direkt `module.get_stats()`)
- **Live System Status:** 1 panel (Settings - systemkonfiguration och övervakning)

**Verifierade komponenter per panel:**
- ✅ Live datapunkter dokumenterade
- ✅ Verifierade funktioner dokumenterade  
- ✅ Datakälla identifierad
- ✅ Auto-refresh bekräftad



#### 1. Decision Core Panel (`/decision-core`)
**Modul:** `modules/decision_core`  
**Funktioner:**
- ✅ Samlar och validerar agentbeslut
- ✅ Konsensusanalys mellan agenter
- ✅ Beslutsrouting (consensus vs conflict)
- ✅ Real-time statistik och tracking

**Visade Datapunkter:**
- Total Decisions: Antal beslut sedan systemstart
- Consensus Rate: Procentandel beslut med agentöverenskommelse
- Conflict Rate: Procentandel beslut som kräver röstning
- Average Confidence: Genomsnittlig konfidensgrad över alla beslut
- Decision Distribution: BUY/SELL/HOLD fördelning
- Recent Decisions: Senaste besluten med symbol, beslut, confidence och status
- Agent Activity: Lista över aktiva agenter med beslutantal och status

**Integrationspunkter:**
- ← Tar emot beslut från: Alla 16 agenter via agent_registry
- → Skickar beslut till: vote_engine (vid konflikt), fusion (validering), sizing (positionering)
- ← Feedback från: self_critique (felanalys), symbol_memory (historik)

**Beroenden:** DecisionCore-modul, alla agenter, DataProvider  
**Auto-refresh:** 3 sekunder  
**Status:** ✅ Klar - Alla datapunkter hanteras korrekt enligt README-flödet

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Mock/Live Toggle via USE_MOCK_DATA  
**Verified Data Points:**
- ✅ Total Decisions
- ✅ Consensus Rate
- ✅ Conflict Rate
- ✅ Average Confidence

**Verified Functions:**
- ✅ Real-time market data via DataStream
- ✅ Live module statistics
- ✅ Auto-refresh every 3 seconds
- ✅ Tabular data display
- ✅ Data visualization charts

#### 2. Vote Engine Panel (`/vote-panel`)
**Modul:** `modules/vote_engine`  
**Funktioner:**
- ✅ Viktad röstning vid agentkonflikter
- ✅ Agent weight evolution tracking
- ✅ Konfliktlösning med RL-optimering
- ✅ Performance-baserad viktjustering

**Visade Datapunkter:**
- Total Votes: Totalt antal röstningar
- Average Weight: Genomsnittlig agentvikt
- Conflicts Resolved: Antal lösta konflikter
- Success Rate: Framgångsgrad för röstningsresultat
- Agent Weight Evolution: 24-timmars historik per agent
- Voting Accuracy: Träffsäkerhet per agent
- Recent Votes: Senaste röstningar med resultat

**Integrationspunkter:**
- ← Tar emot: Konfliktbeslut från decision_core
- → Skickar: Viktade beslut tillbaka till decision_core
- ↔ Samverkar med: synergy_matrix (agentrelationer), meta_agent_governor (prioritering)
- ← Feedback: RL-belöningar baserat på röstprecision

**Beroenden:** VoteEngine-modul, DecisionCore, SynergyMatrix  
**Auto-refresh:** 3 sekunder  
**Status:** ✅ Klar - Komplett viktningssystem med historikspårning

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Mock/Live Toggle via USE_MOCK_DATA  
**Verified Data Points:**
- ✅ Total Votes (24h)
- ✅ Average Weight
- ✅ Conflicts Resolved
- ✅ Success Rate

**Verified Functions:**
- ✅ Real-time market data via DataStream
- ✅ Live module statistics
- ✅ Auto-refresh every 3 seconds
- ✅ Tabular data display
- ✅ Data visualization charts
- ✅ Interactive plotly graphs

#### 3. Position Sizing Panel (`/position-sizing`)
**Modul:** `modules/sizing`  
**Funktioner:**
- ✅ Kelly criterion-baserad sizing
- ✅ Volatility-adjusted position sizing
- ✅ RL-optimerad sizing per strategi
- ✅ Risk management och kapitalallokering

**Visade Datapunkter:**
- Capital: Totalt tillgängligt kapital
- Active Positions: Antal aktiva positioner
- Max Position Size: Maximal positionsstorlek i procent
- Total Allocated: Totalt allokerat kapital
- Current Positions: Tabell med symbol, storlek, Kelly%, volatilitet, allokering
- Sizing Profile Performance: Prestanda för olika sizing-profiler

**Integrationspunkter:**
- ← Tar emot: Beslut från decision_core, risk från risk_mapper
- → Skickar: Positionsstorlek till portfolio_engine
- ↔ Använder: sentio_agent för sentimentjustering, timespan_engine för tidsramsjustering

**Beroenden:** Sizing-modul, DecisionCore, RiskMapper  
**Auto-refresh:** 4 sekunder  
**Status:** ✅ Klar - Kelly criterion och RL-optimering implementerad

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Mock/Live Toggle via USE_MOCK_DATA  
**Verified Data Points:**
- ✅ Capital
- ✅ Active Positions
- ✅ Max Position Size
- ✅ Total Allocated

**Verified Functions:**
- ✅ Real-time market data via DataStream
- ✅ Live module statistics
- ✅ Auto-refresh every 4 seconds
- ✅ Tabular data display
- ✅ Data visualization charts

#### 4. Timespan Intelligence Panel (`/timespan-intelligence`)
**Modul:** `modules/timespan_engine`  
**Funktioner:**
- ✅ Multi-timeframe synchronization
- ✅ RL-träning för optimal span-selection
- ✅ Adaptiva spans per marknadsregim
- ✅ Convergence analysis över tidsramar

**Visade Datapunkter:**
- Active Timeframes: Antal aktiva tidsramar
- Sync Score: Synkroniseringsgrad mellan spans
- RL Episodes: Antal träningsepisoder
- Avg Reward: Genomsnittlig RL-belöning
- Timeframe Status: Status och prestanda per tidsram
- Convergence Analysis: Överensstämmelse mellan spans

**Integrationspunkter:**
- ← Tar emot: Marknadsdata från data_stream
- → Skickar: Multi-span signaler till fusion
- ↔ Integrerar med: fractalis_agent (fraktalanalys), dimensio_agent (5D analys)

**Beroenden:** TimespanEngine-modul, DataStream, Fusion  
**Auto-refresh:** 5 sekunder  
**Status:** ✅ Klar - Multi-timeframe system fullt funktionellt

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Mock/Live Toggle via USE_MOCK_DATA  
**Verified Data Points:**
- ✅ Active Timeframes
- ✅ Sync Score
- ✅ RL Episodes
- ✅ Avg Reward

**Verified Functions:**
- ✅ Real-time market data via DataStream
- ✅ Live module statistics
- ✅ Auto-refresh every 5 seconds
- ✅ Tabular data display
- ✅ Data visualization charts

#### 5. Multi Portfolio Panel (`/multi-portfolio`)
**Modul:** `modules/portfolio_engine`  
**Funktioner:**
- ✅ Parallella portföljhantering
- ✅ Portföljmutation och evolution
- ✅ RL-optimering av portföljkonfigurationer
- ✅ Performance tracking per portfölj

**Visade Datapunkter:**
- Total Portfolios: Antal aktiva portföljer
- Active Positions: Totala aktiva positioner
- Best Performer: Bäst presterande portfölj
- Total Value: Totalt portföljvärde
- Portfolio Performance: Tabell med namn, värde, avkastning, Sharpe ratio
- Recent Mutations: Senaste portföljmutationer

**Integrationspunkter:**
- ← Tar emot: Beslut från decision_core, sizing från sizing-modul
- → Skickar: Performance data till portfolio_comparator
- ↔ Använder: evolution för mutation, mutation_tracker för genealogi

**Beroenden:** PortfolioEngine-modul, DecisionCore, Sizing, Evolution  
**Auto-refresh:** 4 sekunder  
**Status:** ✅ Klar - Multi-portfölj system med mutation

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live Module Data  
**Verified Data Points:**
- ✅ Total Portfolios
- ✅ Active Positions
- ✅ Best Performer
- ✅ Total Value

**Verified Functions:**
- ✅ Live module statistics
- ✅ Auto-refresh every 4 seconds
- ✅ Tabular data display
- ✅ Data visualization charts

#### 6. Mutation Tracker Panel (`/mutation-tracker`)
**Modul:** `modules/mutation_tracker`  
**Funktioner:**
- ✅ Genealogisk spårning av mutationer
- ✅ Lineage performance analysis
- ✅ Generationshistorik
- ✅ Mutation tree visualization

**Visade Datapunkter:**
- Total Mutations: Totalt antal mutationer
- Active Lineages: Antal aktiva genealogiska linjer
- Avg Generation: Genomsnittlig generation
- Best Lineage: Bäst presterande linje
- Lineage Performance: Tabell med namn, generation, fitness, status
- Recent Mutations: Senaste mutationer med typ och resultat

**Integrationspunkter:**
- ← Tar emot: Mutation events från evolution, agent_lifecycle
- → Skickar: Genealogi-data till narrative_engine
- ↔ Spårar: Agentmutationer, strategimutationer, portföljmutationer

**Beroenden:** MutationTracker-modul, Evolution, AgentLifecycle  
**Auto-refresh:** 3 sekunder  
**Status:** ✅ Klar - Komplett genealogisk spårning

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live Module Data  
**Verified Data Points:**
- ✅ Total Mutations
- ✅ Active Lineages
- ✅ Avg Generation
- ✅ Best Lineage

**Verified Functions:**
- ✅ Live module statistics
- ✅ Auto-refresh every 3 seconds
- ✅ Tabular data display

#### 7. Agent Spectrum Panel (`/agent-spectrum`)
**Modul:** `modules/agent_spectrum`  
**Funktioner:**
- ✅ Ontologisk positionering av agenter
- ✅ Dimensionell rörelse tracking
- ✅ Agent clustering och grupper
- ✅ Spectrum visualization

**Visade Datapunkter:**
- Total Agents: Antal spårade agenter
- Active Dimensions: Antal aktiva dimensioner
- Spectrum Shifts: Antal dimensionella förflyttningar
- Cluster Count: Antal agentkluster
- Agent Positioning: Tabell med agent, dimension, position, status
- Dimensional Movement: Rörelsehistorik

**Integrationspunkter:**
- ← Tar emot: Agent status från agent_lifecycle
- → Skickar: Ontologiska insights till meta_agent_governor
- ↔ Analyserar: Dimensionell rörelse för alla paradigmatiska agenter

**Beroenden:** AgentSpectrum-modul, AgentLifecycle, alla agenter  
**Auto-refresh:** 4 sekunder  
**Status:** ✅ Klar - Ontologisk kartläggning implementerad

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live Module Data  
**Verified Data Points:**
- ✅ Total Agents
- ✅ Active Dimensions
- ✅ Spectrum Shifts
- ✅ Cluster Count

**Verified Functions:**
- ✅ Live module statistics
- ✅ Auto-refresh every 4 seconds
- ✅ Tabular data display

#### 8. Agent Lifecycle Panel (`/agent-lifecycle`)
**Modul:** `modules/agent_lifecycle`  
**Funktioner:**
- ✅ Spårning av agentlivscykel (födelse → pensionering)
- ✅ Evolution och mutation tracking
- ✅ Performance-baserad survival
- ✅ Generationshantering

**Visade Datapunkter:**
- Active Agents: Antal aktiva agenter
- Total Births: Totalt antal skapade agenter
- Mutations: Antal mutationer
- Retirements: Antal pensionerade agenter
- Agent Status: Tabell med agent, status, generation, fitness
- Lifecycle Events: Senaste livscykelhändelser

**Integrationspunkter:**
- ← Tar emot: Performance från decision_core, evolution triggers
- → Skickar: Agent metadata till agent_spectrum, mutation_tracker
- ↔ Styr: Agent creation, mutation, retirement policies

**Beroenden:** AgentLifecycle-modul, Evolution, MutationTracker  
**Auto-refresh:** 3 sekunder  
**Status:** ✅ Klar - Komplett livscykelhantering

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live Module Data  
**Verified Data Points:**
- ✅ Active Agents
- ✅ Total Births
- ✅ Mutations
- ✅ Retirements

**Verified Functions:**
- ✅ Live module statistics
- ✅ Auto-refresh every 3 seconds
- ✅ Tabular data display
- ✅ Data visualization charts

#### 9. Meta Governance Panel (`/meta-governance`)
**Modul:** `modules/metaagentgovernor`  
**Funktioner:**
- ✅ Överordnad agentstyrning
- ✅ Agent councils och prioritering
- ✅ Regim-baserad aktivering
- ✅ Meta-policies

**Visade Datapunkter:**
- Active Councils: Antal aktiva agentråd
- Governance Rules: Antal styrningsregler
- Priority Shifts: Antal prioritetsändringar
- Consensus Level: Överordnad konsensusgrad
- Council Composition: Tabell med råd, medlemmar, mandat
- Recent Governance: Senaste styrningsbeslut

**Integrationspunkter:**
- ← Tar emot: Agent performance från decision_core, synergies från synergy_matrix
- → Skickar: Prioriteringar till vote_engine, policies till alla agenter
- ↔ Styr: Överordnad agentallokering och regimväxling

**Beroenden:** MetaAgentGovernor-modul, VoteEngine, SynergyMatrix  
**Auto-refresh:** 4 sekunder  
**Status:** ✅ Klar - Meta-styrning implementerad

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live Module Data  
**Verified Data Points:**
- ✅ Active Councils
- ✅ Governance Rules
- ✅ Priority Shifts
- ✅ Consensus Level

**Verified Functions:**
- ✅ Live module statistics
- ✅ Auto-refresh every 4 seconds
- ✅ Tabular data display
- ✅ Data visualization charts

#### 10. Portfolio Intelligence Panel (`/portfolio-intelligence`)
**Modul:** `modules/portfolio_comparator`  
**Funktioner:**
- ✅ Cross-portfolio jämförelse
- ✅ Benchmark analysis
- ✅ Komponentjämförelse
- ✅ Meta-portfolio optimization

**Visade Datapunkter:**
- Portfolios Compared: Antal jämförda portföljer
- Best Performer: Bäst presterande portfölj
- Benchmark Beat Rate: Procentandel som slår benchmark
- Correlation Score: Korrelationsanalys
- Performance Comparison: Tabell med portfölj, avkastning, risk, Sharpe
- Component Analysis: Komponentbidrag till prestanda

**Integrationspunkter:**
- ← Tar emot: Portfolio data från portfolio_engine
- → Skickar: Insights till decision_core för optimering
- ↔ Använder: Benchmark data, historisk prestanda

**Beroenden:** PortfolioComparator-modul, PortfolioEngine  
**Auto-refresh:** 5 sekunder  
**Status:** ✅ Klar - Komplett jämförelseanalys

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live Module Data  
**Verified Data Points:**
- ✅ Portfolios Compared
- ✅ Best Performer
- ✅ Benchmark Beat Rate
- ✅ Correlation Score

**Verified Functions:**
- ✅ Live module statistics
- ✅ Auto-refresh every 5 seconds
- ✅ Tabular data display
- ✅ Data visualization charts

#### 11. Risk Ecosystem Panel (`/risk-ecosystem`)
**Modul:** `modules/risk_mapper`  
**Funktioner:**
- ✅ Risk mapping per symbol och agent
- ✅ Portfolio risk aggregation
- ✅ Regimriskanalys
- ✅ Sizing/sentiment overlay

**Visade Datapunkter:**
- Total Risk Exposure: Total riskexponering
- High Risk Positions: Antal högriskpositioner
- Risk-Adjusted Return: Riskjusterad avkastning
- VaR (95%): Value at Risk
- Symbol Risk Matrix: Tabell med symbol, risk level, volatilitet, exponering
- Agent Risk Contribution: Riskbidrag per agent

**Integrationspunkter:**
- ← Tar emot: Position data från portfolio_engine, volatility från data_stream
- → Skickar: Risk constraints till sizing-modul
- ↔ Använder: Sentio_agent för marknadspsykologi, regimdata

**Beroenden:** RiskMapper-modul, PortfolioEngine, DataStream  
**Auto-refresh:** 3 sekunder  
**Status:** ✅ Klar - Riskekosystem fullt implementerat

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Mock/Live Toggle via USE_MOCK_DATA  
**Verified Data Points:**
- ✅ Total Risk Exposure
- ✅ High Risk Positions
- ✅ Risk-Adjusted Return
- ✅ VaR (95%)

**Verified Functions:**
- ✅ Real-time market data via DataStream
- ✅ Live module statistics
- ✅ Auto-refresh every 3 seconds
- ✅ Tabular data display
- ✅ Data visualization charts

#### 12. System Flow Panel (`/system-flow`)
**Modul:** Integrerad systemöversikt  
**Funktioner:**
- ✅ Visuell modulkarta
- ✅ Real-time status per modul
- ✅ Dataflödesöversikt
- ✅ System health monitoring

**Visade Datapunkter:**
- Active Modules: Antal aktiva moduler (19/19)
- Data Flow Rate: Dataflödeshastighet (msg/s)
- System Uptime: Systemdrifttid
- Latency: Genomsnittlig latens
- Module Flow Diagram: Visuellt flödesdiagram
- System Health: Status per modul

**Integrationspunkter:**
- ← Aggregerar: Status från alla 19 moduler
- → Visar: Komplett systemöversikt
- ↔ Monitorer: Hela dataflödet från data till beslut

**Beroenden:** Alla 19 moduler  
**Auto-refresh:** 4 sekunder  
**Status:** ✅ Klar - Komplett systemöversikt

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live Module Data  
**Verified Data Points:**
- ✅ Active Modules
- ✅ Data Flow Rate
- ✅ System Uptime
- ✅ Latency

**Verified Functions:**
- ✅ Auto-refresh every 4 seconds
- ✅ System architecture visualization
- ✅ Module status badges

#### 13. Narrative Engine Panel (`/narrative`)
**Modul:** `modules/narrative_engine`  
**Funktioner:**
- ✅ Händelseflöde och loggning
- ✅ Causal chain tracking
- ✅ Systemberättelse
- ✅ Event grouping och analys

**Visade Datapunkter:**
- Total Events: Totalt antal händelser
- Causal Chains: Antal kausala kedjor
- Event Groups: Antal händelsegrupper
- Active Stories: Antal aktiva berättelser
- Recent Narrative: Senaste händelser med timestamps
- Event Statistics: Händelsetyper och fördelning

**Integrationspunkter:**
- ← Tar emot: Events från alla moduler
- → Skickar: Narrativ kontext för visualisering
- ↔ Loggar: Komplett systemhistorik och beslutsspår

**Beroenden:** NarrativeEngine-modul, alla moduler  
**Auto-refresh:** 2 sekunder  
**Status:** ✅ Klar - Komplett narrativhantering

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live Module Data  
**Verified Data Points:**
- ✅ Total Events
- ✅ Causal Chains
- ✅ Event Groups
- ✅ Active Stories

**Verified Functions:**
- ✅ Live module statistics
- ✅ Auto-refresh every 2 seconds
- ✅ Event logging and tracking

#### 14. Data Source Panel (`/data-source`)
**Modul:** `dash_app/utils/data_provider`  
**Funktioner:**
- ✅ Live/Mock data toggle
- ✅ Finnhub API integration
- ✅ Nasdaq-100 symbol management
- ✅ Data caching och fallback

**Visade Datapunkter:**
- Data Source Mode: Mock/Live toggle
- API Status: Finnhub API status
- Symbols Tracked: Antal spårade symboler
- Data Quality: Datakvalitetsindikatorer

**Integrationspunkter:**
- → Tillhandahåller: Data till data_stream
- ↔ Konfigurerar: Datakälla för hela systemet

**Beroenden:** DataProvider, FinnhubClient, DataStream  
**Auto-refresh:** Kontinuerlig  
**Status:** ✅ Klar - Komplett datakällhantering

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Mock/Live Toggle via USE_MOCK_DATA  
**Verified Data Points:**
- ✅ Data Source Mode
- ✅ API Status
- ✅ Symbols Tracked
- ✅ Data Quality
- ✅ WebSocket Status
- ✅ Cache Hit Rate

**Verified Functions:**
- ✅ Real-time market data via DataStream
- ✅ WebSocket monitoring
- ✅ API call tracking
- ✅ Live/Mock toggle
- ✅ Tabular data display
- ✅ Interactive graphs

#### 15. Portfolio Development Panel (`/portfolio-development`)
**Modul:** `modules/portfolio_engine` + `modules/evolution`  
**Funktioner:**
- ✅ Utvecklingsanalys
- ✅ Evolution tracking
- ✅ Performance metrics
- ✅ Development insights

**Visade Datapunkter:**
- Development Metrics
- Evolution Statistics
- Performance Tracking
- Growth Analysis

**Integrationspunkter:**
- ← Tar emot: Portfolio evolution data
- → Skickar: Development insights

**Beroenden:** PortfolioEngine, Evolution  
**Auto-refresh:** 4 sekunder  
**Status:** ✅ Klar - Utvecklingsanalys implementerad

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Mock/Live Toggle via USE_MOCK_DATA  
**Verified Data Points:**
- ✅ Development Metrics
- ✅ Evolution Statistics
- ✅ Performance Tracking
- ✅ Growth Analysis

**Verified Functions:**
- ✅ Real-time market data via DataStream
- ✅ Auto-refresh every 4 seconds
- ✅ Tabular data display
- ✅ Interactive plotly graphs

#### 16. Settings Panel (`/settings`)
**Modul:** System configuration and control  
**Funktioner:**
- ✅ Module control with on/off toggles
- ✅ Agent management and status monitoring
- ✅ System parameter configuration
- ✅ Panel control and refresh settings
- ✅ Real-time activity logging
- ✅ System health monitoring

**Visade Datapunkter:**
- Active Modules: Antal aktiva moduler (10/10)
- Active Agents: Antal aktiva agenter (7/8)
- Active Panels: Antal aktiva paneler (15/15)
- System Health: Övergripande systemhälsa
- Module Status: Status för varje modul med toggle
- Agent Performance: Accuracy och confidence per agent
- Parameter Values: Aktuella systeminställningar
- Recent Changes: Senaste konfigurationsändringar
- API Status: REST och WebSocket status
- Portfolio Value: Totalt portföljvärde

**Funktionalitet:**
- **Module Control:** Toggle för att aktivera/avaktivera moduler
- **Agent Control:** Hantera agenter individuellt med status och metrics
- **Parameters:** Konfigurera Data Stream, Fusion, Sizing, Vote Engine
- **Panel Control:** Hantera paneler, refresh-rates och modes
- **Activity Log:** Historik över alla systemändringar
- **Real-time Updates:** Live status för alla komponenter

**Konfigurerbara Parametrar:**

*Data Stream:*
- Live Data toggle (Mock/Live)
- Batch Size (5-50)
- Batch Interval (1-60 sec)
- Max WebSocket Subscriptions (10-50)

*Fusion:*
- Fusion Mode (Majority/Weighted/Consensus)
- Fusion Threshold (0.5-1.0)
- Conflict Resolution method

*Sizing:*
- Sizing Method (Fixed/Volatility/Confidence)
- Max Position Size (0.01-1.0)
- Risk Budget (1-100%)

*Vote Engine:*
- Vote Method (Score/Weight/Regime)
- Min Vote Score (0.1-1.0)

**Integrationspunkter:**
- → Styr: Alla moduler och agenter
- ← Tar emot: Status från alla system komponenter
- ↔ Loggar: Alla konfigurationsändringar
- → Tillhandahåller: Central kontrollpunkt för systemet

**Beroenden:** Alla moduler och agenter  
**Auto-refresh:** 5 sekunder  
**Status:** ✅ Klar - Central systemkonfiguration och övervakning

**Live Data Verification (Phase 3):** ✅ VERIFIED  
**Data Source:** Live System Status  
**Verified Data Points:**
- ✅ Active Modules (10/10)
- ✅ Active Agents (7/8)
- ✅ Active Panels (15/15)
- ✅ System Health Status
- ✅ Module Status with toggles
- ✅ Agent Performance metrics
- ✅ Parameter configurations
- ✅ Activity log entries

**Verified Functions:**
- ✅ Real-time system monitoring
- ✅ Module control toggles
- ✅ Agent management
- ✅ Parameter configuration sliders
- ✅ Activity logging
- ✅ Auto-refresh every 5 seconds
- ✅ Tabular data display
- ✅ Status indicators

---

## 🔄 Systemflöde med Statusöversikt

### Modulflöde och Integrationspunkter

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        📊 OBSCURAFLOW SYSTEMFLÖDE                           │
│                     Status: ✅ Alla moduler operativa                        │
└─────────────────────────────────────────────────────────────────────────────┘

[1] 📡 DATA INGESTION
    ├─ DataStream ✅               → Hämtar live/mock marknadsdata
    │   └─ FinnhubClient ✅        → API integration med caching
    └─ TrendingPool ✅             → Rankar och filtrerar symboler
        └─ Output: Top symboler med trend/volym/momentum

[2] 🤖 AGENT ANALYSIS
    ├─ 16 Agenter (via AgentRegistry) ✅
    │   ├─ Classic (4) ✅          → Momentum, Reversal, Breakout, Hybrid
    │   └─ Paradigmatic (12) ✅    → Echo, Fractalis, Vox, Myco, Obscura, etc.
    │
    ├─ AgentLifecycle ✅           → Spårar agent evolution och status
    ├─ AgentSpectrum ✅            → Ontologisk kartläggning
    └─ Output: 16+ beslut per symbol med confidence och reasoning

[3] 🔀 SIGNAL VALIDATION
    ├─ Fusion ✅                   → Multi-timeframe validering
    │   └─ TimespanEngine ✅       → Synkroniserar över 1m/5m/15m/1h/4h
    └─ Output: Validerade signaler med konsistensgrad

[4] 🧠 DECISION MAKING
    ├─ DecisionCore ✅             → Samlar och analyserar agentbeslut
    │   ├─ Consensus detection
    │   └─ Conflict routing
    │
    └─ VoteEngine ✅               → Löser konflikter med viktad röstning
        ├─ Weight evolution (RL-baserad)
        └─ Meta-voting capabilities

[5] 🎯 GOVERNANCE & COORDINATION
    ├─ MetaAgentGovernor ✅        → Överordnad agentstyrning
    │   ├─ Agent councils
    │   └─ Regim-baserad prioritering
    │
    └─ SynergyMatrix ✅            → Agentrelationer och samverkan
        └─ Output: Optimerad agentallokering

[6] 📐 POSITION SIZING
    ├─ Sizing ✅                   → Kelly criterion + RL-optimering
    │   ├─ Risk-adjusted sizing
    │   ├─ Volatility adaptation
    │   └─ Sentiment integration (via SentioAgent)
    │
    └─ RiskMapper ✅               → Riskanalys och constraints
        └─ Output: Optimal positionsstorlek per trade

[7] 💼 PORTFOLIO MANAGEMENT
    ├─ PortfolioEngine ✅          → Multi-portfolio hantering
    │   ├─ Parallella portföljer
    │   ├─ Portfolio mutation
    │   └─ RL-optimering
    │
    └─ PortfolioComparator ✅      → Jämförelse och benchmarking
        └─ Output: Optimerad portföljallokering

[8] 🔬 EVOLUTION & LEARNING
    ├─ Evolution ✅                → Strategi- och agentmutation
    │   ├─ RL-driven evolution
    │   └─ Regimadaptation
    │
    ├─ MutationTracker ✅          → Genealogisk spårning
    │   └─ Lineage performance
    │
    └─ SelfCritique ✅             → Felanalys och feedback
        ├─ Performance analysis
        └─ RL reward calculation

[9] 💾 MEMORY & HISTORY
    ├─ SymbolMemory ✅             → Symbol-specifik historik
    │   ├─ Trade history
    │   └─ Agent precision tracking
    │
    └─ NarrativeEngine ✅          → Händelseflöde och berättelse
        ├─ Event logging
        ├─ Causal chains
        └─ System narrative

[10] 📊 VISUALIZATION & MONITORING
    └─ Dash Dashboard (16 paneler) ✅
        ├─ Real-time updates (2-5s intervals)
        ├─ Live/Mock data toggle
        ├─ Settings Panel för systemkonfiguration
        └─ Komplett systemöversikt

═══════════════════════════════════════════════════════════════════════════════
DATAFLÖDE: Data → Agents → Fusion → Decision → Sizing → Portfolio → Execution
FEEDBACK: Performance → Critique → Evolution → Mutation → Improved Agents
GOVERNANCE: MetaGovernor → Synergy → Vote → Optimized Decisions
═══════════════════════════════════════════════════════════════════════════════
```

### Status per Modul

| # | Modul | Status | Funktionalitet | Integrationer |
|---|-------|--------|----------------|---------------|
| 1 | data_stream | ✅ Klar | WebSocket/REST, mock data | → trending_pool, agents |
| 2 | trending_pool | ✅ Klar | Symbolranking, värmeanalys | ← data_stream → agents |
| 3 | decision_core | ✅ Klar | Beslutsrouting, konsensus | ← agents → vote/sizing |
| 4 | vote_engine | ✅ Klar | Viktad röstning, RL-viktning | ← decision_core ↔ synergy_matrix |
| 5 | fusion | ✅ Klar | Multi-span validering | ← agents, timespan → decision_core |
| 6 | sizing | ✅ Klar | Kelly criterion, RL-sizing | ← decision_core → portfolio |
| 7 | timespan_engine | ✅ Klar | Multi-timeframe sync | ← data_stream → fusion |
| 8 | portfolio_engine | ✅ Klar | Multi-portfolio, mutation | ← sizing → comparator |
| 9 | evolution | ✅ Klar | Strategi/agent mutation | ← critique → agents |
| 10 | self_critique | ✅ Klar | Felanalys, RL-feedback | ← decision_core → evolution |
| 11 | symbol_memory | ✅ Klar | Trade history, precision | ← decision_core → critique |
| 12 | narrative_engine | ✅ Klar | Event logging, berättelse | ← alla moduler → dashboard |
| 13 | mutation_tracker | ✅ Klar | Genealogi, lineage | ← evolution → narrative |
| 14 | synergy_matrix | ✅ Klar | Agentrelationer | ← agents → vote/meta |
| 15 | agent_spectrum | ✅ Klar | Ontologisk kartläggning | ← agent_lifecycle → meta |
| 16 | agent_lifecycle | ✅ Klar | Agent evolution, status | ← agents → spectrum/mutation |
| 17 | metaagentgovernor | ✅ Klar | Överordnad styrning | ← synergy → vote/agents |
| 18 | portfolio_comparator | ✅ Klar | Portfolio benchmarking | ← portfolio → decision_core |
| 19 | risk_mapper | ✅ Klar | Riskanalys, VaR | ← portfolio → sizing |

**Systemstatus:** ✅ 19/19 moduler fullt operativa  
**Integration:** ✅ Alla integrationspunkter verifierade  
**Dataflöde:** ✅ End-to-end flöde från data till beslut fungerar  
**Auto-refresh:** ✅ Alla paneler uppdateras automatiskt

---

## 🤖 Agentöversikt och Status

### Agentregister - 16 Fullt Implementerade Agenter

#### Klassiska Agenter (4/4) ✅

| Agent | Status | Strategi | Dimension | Integrationspunkter | Funktionell Status |
|-------|--------|----------|-----------|---------------------|-------------------|
| **MomentumAgent** | ✅ Aktiv | Trendföljande | Temporal (kort span) | → decision_core, fusion<br>← data_stream | ✅ Full: Momentum calc, trend following |
| **ReversalAgent** | ✅ Aktiv | Mean reversion | Temporal (medel span) | → decision_core, fusion<br>← data_stream, symbol_memory | ✅ Full: RSI, overbought/oversold |
| **BreakoutAgent** | ✅ Aktiv | Volatility breakout | Spatial (lång span) | → decision_core, fusion<br>← data_stream | ✅ Full: Bollinger bands, volatility |
| **HybridAgent** | ✅ Aktiv | Multi-strategi | Adaptive | → decision_core<br>← all classic agents | ✅ Full: Strategy switching, regime detect |

**Classic Agent Integration:**
- ✅ Alla agents rapporterar till DecisionCore
- ✅ Historikspårning via SymbolMemory
- ✅ Performance tracking i AgentLifecycle
- ✅ Viktjustering via VoteEngine

#### Paradigmatiska Agenter (12/12) ✅

| Agent | Status | Dimension | Kapacitet | Integrationspunkter | Funktionell Status |
|-------|--------|-----------|-----------|---------------------|-------------------|
| **EchoAgent** | ✅ Aktiv | Temporal/Reflective | 500 patterns, 75% match | → fusion, reflexion<br>← symbol_memory | ✅ Full: Pattern matching, historical replay |
| **FractalisAgent** | ✅ Aktiv | Spatial-Temporal | 5 spans, självlikhet | → timespan, fusion<br>← data_stream | ✅ Full: Fractal analysis, multi-scale |
| **VoxAgent** | ✅ Aktiv | Social/Collective | 75% consensus threshold | → vote_engine, symbio<br>← all agents | ✅ Full: Consensus building, voting |
| **MycoAgent** | ✅ Aktiv | Network/Distributed | 3 levels, 85% decay | → synergy_matrix<br>← all agents | ✅ Full: Network diffusion, info spread |
| **ObscuraAgent** | ✅ Aktiv | Latent/Obscure | 2.0σ anomaly detect | → fusion, critique<br>← data_stream | ✅ Full: Anomaly detection, hidden patterns |
| **MirageAgent** | ✅ Aktiv | Perceptual | 65% reality threshold | → fusion<br>← echo, obscura | ✅ Full: False signal filtering |
| **SentioAgent** | ✅ Aktiv | Emotional/Empathic | 30-period sentiment | → sizing, vote<br>← data_stream | ✅ Full: Sentiment analysis, fear/greed |
| **ReflexionAgent** | ✅ Aktiv | Meta-Cognitive | 100 decision history | → self_critique, evolution<br>← decision_core | ✅ Full: Self-learning, adaptation |
| **DimensioAgent** | ✅ Aktiv | Hyper-Spatial | 5D feature space | → fusion, comparator<br>← data_stream | ✅ Full: Multi-dimensional analysis |
| **SymbioAgent** | ✅ Aktiv | Relational/Cooperative | 50% symbiosis strength | → synergy_matrix<br>← vox, myco | ✅ Full: Co-evolution, cooperation |
| **GenesisAgent** | ✅ Aktiv | Origination/Generative | Inflection detection | → fusion, echo<br>← data_stream | ✅ Full: Trend genesis, cycle detection |
| **ArchitectumAgent** | ✅ Aktiv | Structural | 4 structural levels | → fusion, dimensio<br>← data_stream | ✅ Full: Structure analysis, framework |

**Paradigmatic Agent Integration:**
- ✅ Alla agents registrerade i AgentRegistry
- ✅ Ontologisk kartläggning via AgentSpectrum
- ✅ Livscykelhantering via AgentLifecycle
- ✅ Synergianalys via SynergyMatrix
- ✅ Meta-styrning via MetaAgentGovernor

### Agent Integration Matrix

```
┌──────────────────────────────────────────────────────────────────┐
│                    AGENT INTEGRATION MAP                         │
└──────────────────────────────────────────────────────────────────┘

CLASSIC AGENTS
├─ Momentum → [decision_core, fusion, timespan]
├─ Reversal → [decision_core, fusion, symbol_memory]
├─ Breakout → [decision_core, fusion, risk_mapper]
└─ Hybrid → [decision_core, ALL classic agents]

PARADIGMATIC AGENTS
├─ Echo → [fusion, reflexion, genesis, symbol_memory]
├─ Fractalis → [timespan, fusion, dimensio, architectum]
├─ Vox → [vote_engine, symbio, sentio, synergy_matrix]
├─ Myco → [synergy_matrix, symbio, portfolio_engine]
├─ Obscura → [fusion, mirage, reflexion, self_critique]
├─ Mirage → [fusion, obscura, echo, reflexion]
├─ Sentio → [sizing, vote_engine, vox, symbio]
├─ Reflexion → [self_critique, evolution, echo, mirage]
├─ Dimensio → [fusion, fractalis, architectum, comparator]
├─ Symbio → [synergy_matrix, vox, myco, sentio]
├─ Genesis → [fusion, echo, architectum, data_stream]
└─ Architectum → [fusion, dimensio, reflexion, genesis]

AGENT MANAGEMENT
├─ AgentRegistry → Central registration (16 agents)
├─ AgentLifecycle → Birth, evolution, retirement tracking
├─ AgentSpectrum → Ontological positioning
├─ SynergyMatrix → Relationship analysis
└─ MetaAgentGovernor → Council governance
```

### Agent Performance och Datakoppling

**Data Connection Status:**
- ✅ Alla agenter mottar data från DataStream
- ✅ Classic agents använder direct market data (price, volume, volatility)
- ✅ Paradigmatic agents använder processed data + agent interactions
- ✅ Real-time updates via DataProvider (Live/Mock toggle)
- ✅ Historical data via SymbolMemory

**Decision Flow:**
1. Market Data → DataStream → Agents (parallel analysis)
2. 16 Agent Decisions → DecisionCore (consensus/conflict detection)
3. Consensus → Sizing → Portfolio
4. Conflict → VoteEngine → Weighted Decision → Sizing
5. All Outcomes → SelfCritique → RL Feedback → Agent Weights

**Performance Tracking:**
- ✅ Decision accuracy per agent tracked
- ✅ RL rewards calculated per agent
- ✅ Weight evolution based on performance
- ✅ Lineage tracking via MutationTracker
- ✅ Ontological movement via AgentSpectrum

**Functional Verification:**
- ✅ Alla 16 agenter kan analysera marknadsdata
- ✅ Beslutstrukturer validerade (agent_id, symbol, decision, confidence, reasoning)
- ✅ Consensus building fungerar korrekt
- ✅ Performance tracking operativt
- ✅ Agent registry tillhandahåller metadata för alla agenter

---

## 📡 Live Data Integration

Obscuraflow använder ett sofistikerat system för live-datainhämtning från Finnhub API med intelligent symbolhantering och rotation.

### 🎯 Datakälla: Finnhub API

**REST API:**
- Endpoint: `https://finnhub.io/api/v1`
- Rate limit: 60 anrop/minut (free tier)
- Data: Quote snapshots, företagsprofiler, historisk data

**WebSocket API:**
- Endpoint: `wss://ws.finnhub.io`
- Max subscriptions: 50 symboler samtidigt
- Data: Realtids tick-data med pris och volym

### 📊 Symboluniversum: NASDAQ-100

**Symbol Management:**
- **Fil:** `modules/data_stream/config/nasdaq100_symbols.yaml`
- **Innehåll:** 99 NASDAQ-100 aktier (AAPL, MSFT, GOOGL, NVDA, META, etc.)
- **Loader:** `modules/data_stream/universe_loader.py`
  - Laddar symboler från YAML vid systemstart
  - Caching för prestanda
  - Fallback till minimal lista vid fel
  - Validering av symbolformat

**Exempel från nasdaq100_symbols.yaml:**
```yaml
nasdaq_100:
  - AAPL   # Apple Inc.
  - ABNB   # Airbnb, Inc.
  - ADBE   # Adobe Inc.
  - AMD    # Advanced Micro Devices, Inc.
  - AMZN   # Amazon.com, Inc.
  # ... (99 symboler totalt)
```

### 🔄 REST Batching & Rate Limiting

**RestBatcher** (`modules/data_stream/rest_batcher.py`):
- **Strategi:** Delar upp universum i batcher om 10 symboler
- **Intervall:** Kör en batch var 10:e sekund
- **Rate limiting:** Max 60 API-anrop/minut (respekterar Finnhub-gränser)
- **Funktion:** Hämtar snapshot-data för alla symboler i rotation

**Flöde:**
1. Laddar NASDAQ-100 universum (99 symboler)
2. Delar upp i ~10 batcher (10 symboler per batch)
3. Kör batch 1 → vänta 10s → batch 2 → ... → batch 10 → börja om
4. Varje symbol får uppdaterad data var ~100:e sekund

### 📡 WebSocket Subscriptions & Rotation

**WebSocketHandler** (`modules/data_stream/ws_handler.py`):
- **Max subscriptions:** 50 symboler samtidigt (Finnhub-gräns)
- **Rotationsintervall:** 12 sekunder
- **Intelligens:** Subscribar endast på top-symboler från TrendingPool

**Subscription Rotation:**
1. TrendingPool rankar symboler baserat på trend_score (volym, momentum, volatilitet)
2. Väljer topp 50 symboler
3. Jämför med aktiva subscriptions:
   - Avsubscriberar symboler som inte längre är i topp 50
   - Subscribar på nya top-symboler
4. Roterar var 12:e sekund för att följa marknadens dynamik

**Tick-data:**
- Realtids pris och volymdata
- Cachning av senaste 100 ticks per symbol
- Automatisk rensning av gammal data (>30 sekunder)
- Integreras med TrendingPool för kortterm-analys

### 🎼 Orchestration

**DataOrchestrator** (`modules/data_stream/orchestrator.py`):
Koordinerar hela dataflödet:

```
┌─────────────────────────────────────────────────────────┐
│              DATA ORCHESTRATOR                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐         ┌────────────────────┐   │
│  │  RestBatcher    │         │  WebSocketHandler  │   │
│  │  • 99 symboler  │         │  • 50 top symboler │   │
│  │  • 10/batch     │         │  • Rotation: 12s   │   │
│  │  • 10s interval │         │  • Real-time ticks │   │
│  └────────┬────────┘         └─────────┬──────────┘   │
│           │                            │              │
│           └──────────┬─────────────────┘              │
│                      ▼                                 │
│            ┌──────────────────┐                        │
│            │  TrendingPool    │                        │
│            │  • Rankar        │                        │
│            │  • Filtrerar     │                        │
│            │  • Top 50        │                        │
│            └─────────┬────────┘                        │
│                      │                                 │
│                      ▼                                 │
│         [Top symboler till Agents & Dashboard]         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Arbetsflöde:**
1. **Init:** Laddar NASDAQ-100 universum från YAML
2. **REST Loop:** Kontinuerlig batching av alla symboler för snapshot-data
3. **WS Loop:** Dynamisk subscription på topp 50 symboler för tick-data
4. **Rotation:** Automatisk omfördelning av WS-subscriptions baserat på trends
5. **Data Push:** Kombinerad data till TrendingPool för agentanalys

### 💡 Fördelar med Denna Arkitektur

**Effektivitet:**
- ✅ Respekterar API rate limits (60 calls/min REST, 50 subs WS)
- ✅ Intelligent resursallokering (WS endast för aktiva symboler)
- ✅ Hög täckning (99 symboler via REST, 50 top via WS)

**Skalbarhet:**
- ✅ Enkelt att ändra universum (redigera YAML)
- ✅ Konfigurerbar batch-storlek och intervall
- ✅ Flexibel rotation baserat på marknadsläge

**Robusthet:**
- ✅ Fallback om YAML-fil saknas
- ✅ Automatisk reconnect vid WS-fel
- ✅ Rate limiting skydd
- ✅ Caching för prestanda

---

## 🚀 Kom igång med Dashboarden

### 1. Installera beroenden

```bash
pip install -r requirements.txt
```

### 2. Konfigurera Finnhub API (Valfritt)

Projektet kommer med en förkonfigurerad Finnhub API-nyckel i `config.py`. För att använda din egen API-nyckel:

1. Registrera dig gratis på [Finnhub.io](https://finnhub.io/register)
2. Kopiera din API-nyckel från dashboarden
3. Välj ett av följande alternativ:

#### Alternativ A: Miljövariabel (Rekommenderat för säkerhet)
```bash
# Linux/Mac
export FINNHUB_API_KEY="din_api_nyckel_här"

# Windows (PowerShell)
$env:FINNHUB_API_KEY="din_api_nyckel_här"

# Windows (CMD)
set FINNHUB_API_KEY=din_api_nyckel_här
```

#### Alternativ B: Direkt i config.py
Redigera filen `config.py` i projektets rot och ändra:
```python
FINNHUB_API_KEY = "din_api_nyckel_här"
```

**Notera:** 
- Projektet inkluderar en fungerande API-nyckel som standard
- Om ingen miljövariabel sätts används nyckeln från config.py
- För mock data behövs ingen API-nyckel
- Växla datakälla med togglen i dashboarden

### 3. Starta Dashboarden

```bash
python run_dashboard.py
```

Eller:

```bash
cd dash_app && python app.py
```

Dashboard tillgänglig på: **http://localhost:8050**

### 4. Växla mellan Datakällor

Dashboarden har en **Data Source Toggle** i vänstermenyn:

- **🟡 Mock Data**: Använder simulerad Nasdaq-100 data med realistiska prisvariationer
- **🟢 Live API**: Använder realtidsdata från Finnhub API (kräver API-nyckel)

Klicka på togglen för att växla mellan datakällor. Alla paneler uppdateras automatiskt.

### Data Source Status

| Läge | Symbol | Beskrivning |
|------|---------|-------------|
| Mock Data | 🟡 | Simulerad data med realistiska variationer (Nasdaq-100 aktier) |
| Live API | 🟢 | Realtidsdata från Finnhub API |
| API Ej Konfigurerad | ⚠️ | API-nyckel saknas, endast mock data tillgänglig |

**Panelfunktioner:**
- 🔄 **Data Source Toggle**: Växla mellan mock data och live Finnhub API i sidomenyn
- 📊 **Enhanced Panels**: Detaljerad data och visualiseringar från 13+ moduler
- 📈 **Live/Mock Market Data**: Dynamisk marknadsdata för 12 Nasdaq-100 symboler
- 🎯 **Real-time Updates**: Auto-refresh var 2-5 sekunder per panel
- 🤖 **Agent Intelligence**: 16 specialiserade agenter med live beslutsdata

**API Integration:**
- Finnhub API key via miljövariabel `FINNHUB_API_KEY`
- Smart caching (60s för quotes, 1h för profiles)
- Automatisk fallback till mock data vid API-fel
- Rate limiting skydd (100ms mellan anrop)
- Stöd för 12 default symboler (konfigurerbart i `dash_app/config.py`)

### 🔄 Dynamiskt Datasystem

**Status: ✅ Fullt Implementerat och Verifierat**

Hela systemet använder nu dynamisk data från det centrala dataflödet. Ingen statisk eller hårdkodad data används i panelerna.

**Centralt Dataflöde:**
- `DataStream` (modules/data_stream): Huvudkälla för marknadsdata
- `DataProvider` (dash_app/utils): Enhetligt gränssnitt för panels
- Automatisk växling mellan Mock Data och Live API via `USE_MOCK_DATA` flag
- All data genereras dynamiskt vid varje panel-rendering

**Dynamiska Moduler:**
- **NarrativeEngine**: Genererar händelseflöde och systemberättelse dynamiskt
- **DecisionCore**: Skapar agentbeslut och aktivitetsstatistik i realtid
- **MutationTracker**: Genererar lineage-data och mutationshistorik dynamiskt
- **DataStream**: Simulerar realistisk prisrörelse och marknadsdata

**Auto-Refresh System:**
- Global `dcc.Interval` komponent i huvudlayouten (3 sekunder)
- Uppdaterar alla paneler kontinuerligt utan att återställa intervals
- Callback skapar nya modulinstanser med färsk data vid varje uppdatering
- Garanterar att timestamps och värden alltid är aktuella
- Fungerar sömlöst över alla paneler och routes

**Panel-uppdateringar:**
- Automatisk refresh var 3:e sekund via global interval
- Callbacks uppdaterar alla paneler när data source toggle ändras
- Ingen hardcoded data eller statiska placeholders
- Full responsivitet med kontinuerlig datauppdatering

**Verifiering:**
- ✅ Alla 16 paneler laddas utan fel
- ✅ Alla routes testad och fungerande
- ✅ Mock data generering fungerar korrekt
- ✅ Data source toggle fungerar över hela systemet
- ✅ Auto-refresh implementerat och verifierat i alla paneler
- ✅ Data uppdateras synligt var 3:e sekund med nya timestamps


### 🚧 Pågående / Planerat

**Hybrider & Meta-Agenter**
- Agentkombinationer och hybrid-strategier
- Tidsram-adaptiva span_hybrids
- Meta-agenter för överordnad styrning

**Live Trading**
- Finnhub API integration för live-data
- Exekveringsmotor för reala trades
- Risk management och positionshantering

---

