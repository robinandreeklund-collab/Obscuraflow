
🌀 Obscuraflow – Projektbeskrivning

Obscuraflow är ett avancerat, modulärt och självlärande AI-tradingekosystem byggt i Dash. Systemet kombinerar realtidsmarknadsdata, 17 specialiserade agenter, adaptiva portföljer, RL-träning och en central beslutsmotor. Det är designat för att simulera och exekvera intelligenta tradingbeslut genom agentkonsensus, signalvalidering och ontologisk analys.

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
