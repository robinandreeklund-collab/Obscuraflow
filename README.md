
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

### 🚧 Pågående / Planerat

**Dash-gränssnitt**
- 13 Dash-paneler för visualisering
- UI-komponenter och interaktivitet
- Real-time uppdateringar

**Hybrider & Meta-Agenter**
- Agentkombinationer och hybrid-strategier
- Tidsram-adaptiva span_hybrids
- Meta-agenter för överordnad styrning

**Live Trading**
- Finnhub API integration för live-data
- Exekveringsmotor för reala trades
- Risk management och positionshantering

---

