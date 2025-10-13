#!/usr/bin/env python
"""
Demo script för automatisk DataOrchestrator start/stopp

Detta script demonstrerar hur orchestrator startar automatiskt
när man byter till Live API-läge.
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.data_stream import (
    get_data_stream,
    get_global_orchestrator_status,
    stop_global_orchestrator
)


def print_status():
    """Skriv ut orchestrator status."""
    status = get_global_orchestrator_status()
    print(f"\n{'='*60}")
    print(f"Orchestrator Status:")
    print(f"{'='*60}")
    print(f"Running:      {status['running']}")
    print(f"Mode:         {status['mode']}")
    print(f"Uptime:       {status.get('uptime', 'N/A')}")
    print(f"Error:        {status.get('error', 'None')}")
    print(f"Thread alive: {status.get('thread_alive', 'N/A')}")
    print(f"Loop running: {status.get('loop_running', 'N/A')}")
    print(f"{'='*60}\n")


def demo():
    """Kör demonstration."""
    print("\n" + "="*60)
    print("DataOrchestrator Autostart Demo")
    print("="*60 + "\n")
    
    # Steg 1: Mock mode
    print("📝 Steg 1: Starta med Mock Data")
    print("-" * 60)
    data_stream_mock = get_data_stream(use_mock=True)
    print(f"✓ DataStream skapad (typ: {type(data_stream_mock).__name__})")
    print_status()
    
    # Steg 2: Byt till Live API
    print("📝 Steg 2: Byt till Live API")
    print("-" * 60)
    print("Detta startar automatiskt DataOrchestrator i bakgrunden...")
    
    data_stream_live = get_data_stream(use_mock=False)
    print(f"✓ DataStream/Orchestrator skapad (typ: {type(data_stream_live).__name__})")
    
    # Vänta lite på att orchestrator startar
    print("\nVäntar 3 sekunder på att orchestrator startar...")
    for i in range(3, 0, -1):
        print(f"  {i}...", end='', flush=True)
        time.sleep(1)
    print()
    
    print_status()
    
    # Steg 3: Kontrollera task status
    print("📝 Steg 3: Kontrollera Task Status")
    print("-" * 60)
    
    if hasattr(data_stream_live, 'get_debug_stats'):
        debug_stats = data_stream_live.get_debug_stats()
        task_stats = debug_stats.get('tasks', {})
        
        print(f"REST Task:        {task_stats.get('rest_task', 'unknown')}")
        print(f"WS Listen Task:   {task_stats.get('ws_listen_task', 'unknown')}")
        print(f"WS Rotation Task: {task_stats.get('ws_rotation_task', 'unknown')}")
        
        rest_stats = debug_stats.get('rest_batcher', {})
        ws_stats = debug_stats.get('websocket', {})
        
        print(f"\nREST Batcher:")
        print(f"  Status:         {rest_stats.get('status', 'unknown')}")
        print(f"  Total calls:    {rest_stats.get('total_calls', 0)}")
        print(f"  Cached symbols: {rest_stats.get('cached_symbols', 0)}")
        
        print(f"\nWebSocket:")
        print(f"  Status:         {ws_stats.get('status', 'unknown')}")
        print(f"  Connected:      {ws_stats.get('connected', False)}")
        print(f"  Subscriptions:  {ws_stats.get('active_subscriptions', 0)}")
    
    # Steg 4: Hämta data
    print("\n📝 Steg 4: Hämta Marknadsdata")
    print("-" * 60)
    
    try:
        market_summary = data_stream_live.get_market_summary()
        print(f"Total symbols: {market_summary.get('total_symbols', 0)}")
        print(f"Gainers:       {market_summary.get('gainers', 0)}")
        print(f"Losers:        {market_summary.get('losers', 0)}")
        print(f"Avg change:    {market_summary.get('avg_change_percent', 0)}%")
    except Exception as e:
        print(f"⚠️  Kunde inte hämta data: {e}")
    
    # Steg 5: Stoppa orchestrator
    print("\n📝 Steg 5: Stoppa Orchestrator")
    print("-" * 60)
    print("Byter tillbaka till Mock Data...")
    
    success = stop_global_orchestrator()
    print(f"Stop result: {success}")
    
    time.sleep(1)
    print_status()
    
    # Steg 6: Verifiera mock mode
    print("📝 Steg 6: Verifiera Mock Mode")
    print("-" * 60)
    
    data_stream_mock2 = get_data_stream(use_mock=True)
    print(f"✓ DataStream skapad i mock-läge (typ: {type(data_stream_mock2).__name__})")
    print_status()
    
    print("\n" + "="*60)
    print("✅ Demo slutförd!")
    print("="*60)
    print("\nSammanfattning:")
    print("- Orchestrator startar automatiskt i Live API-läge")
    print("- Tasks (REST, WebSocket) körs i bakgrunden")
    print("- Orchestrator stoppar korrekt vid Mock Data-byte")
    print("- Felhantering fungerar (t.ex. nätverksfel)")
    print("="*60 + "\n")


if __name__ == '__main__':
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo avbruten av användare")
        stop_global_orchestrator()
    except Exception as e:
        print(f"\n\n❌ Fel under demo: {e}")
        import traceback
        traceback.print_exc()
        stop_global_orchestrator()
