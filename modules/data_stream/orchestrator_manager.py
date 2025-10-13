"""
Orchestrator Manager - Hanterar DataOrchestrator i bakgrundstråd

Denna modul möjliggör att köra DataOrchestrator från synkron kod (t.ex. Dash callbacks)
genom att hantera en separat tråd med asyncio event loop.
"""

import asyncio
import threading
import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class OrchestratorManager:
    """
    Hanterar DataOrchestrator i en bakgrundstråd med asyncio event loop.
    
    Tillåter synkron kod att starta/stoppa orchestrator som körs asynkront.
    """
    
    def __init__(self):
        self.orchestrator = None
        self.loop = None
        self.thread = None
        self.is_running = False
        self.start_time = None
        self.error = None
        self._lock = threading.Lock()
    
    def start_orchestrator(self, orchestrator) -> bool:
        """
        Startar orchestrator i en bakgrundstråd.
        
        Args:
            orchestrator: DataOrchestrator-instans att starta
            
        Returns:
            True om start lyckades, False annars
        """
        with self._lock:
            if self.is_running:
                logger.warning("Orchestrator körs redan")
                return True
            
            try:
                self.orchestrator = orchestrator
                self.error = None
                
                # Skapa ny tråd med event loop
                self.thread = threading.Thread(
                    target=self._run_orchestrator_thread,
                    daemon=True,
                    name="OrchestratorThread"
                )
                self.thread.start()
                
                # Vänta kort på att tråden startar
                for _ in range(10):  # Max 1 sekund
                    if self.is_running:
                        logger.info("Orchestrator startad i bakgrunden")
                        return True
                    threading.Event().wait(0.1)
                
                logger.warning("Orchestrator start tog längre tid än förväntat")
                return True  # Fortsätt ändå, det kan starta i bakgrunden
                
            except Exception as e:
                logger.error(f"Fel vid start av orchestrator: {e}")
                self.error = str(e)
                return False
    
    def stop_orchestrator(self) -> bool:
        """
        Stoppar orchestrator och avslutar bakgrundstråden.
        
        Returns:
            True om stopp lyckades, False annars
        """
        with self._lock:
            if not self.is_running:
                logger.info("Orchestrator körs inte")
                return True
            
            try:
                logger.info("Stoppar orchestrator...")
                
                # Signalera loop att stoppa
                if self.loop and self.loop.is_running():
                    asyncio.run_coroutine_threadsafe(
                        self._stop_orchestrator_async(),
                        self.loop
                    )
                
                # Vänta på att tråden avslutas
                if self.thread and self.thread.is_alive():
                    self.thread.join(timeout=5.0)
                
                self.is_running = False
                self.orchestrator = None
                self.loop = None
                self.thread = None
                
                logger.info("Orchestrator stoppad")
                return True
                
            except Exception as e:
                logger.error(f"Fel vid stopp av orchestrator: {e}")
                self.error = str(e)
                return False
    
    def _run_orchestrator_thread(self):
        """Kör orchestrator i en separat tråd med asyncio event loop."""
        try:
            # Skapa ny event loop för denna tråd
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # Starta orchestrator
            self.loop.run_until_complete(self._start_orchestrator_async())
            
            # Håll loop igång tills den stängs
            self.loop.run_forever()
            
        except Exception as e:
            logger.error(f"Fel i orchestrator-tråden: {e}")
            self.error = str(e)
            self.is_running = False
        finally:
            if self.loop:
                self.loop.close()
    
    async def _start_orchestrator_async(self):
        """Startar orchestrator asynkront."""
        try:
            logger.info("Startar orchestrator asynkront...")
            self.is_running = True
            self.start_time = datetime.now()
            await self.orchestrator.start()
            logger.info("Orchestrator startad framgångsrikt")
        except Exception as e:
            logger.error(f"Fel vid async start av orchestrator: {e}")
            self.error = str(e)
            self.is_running = False
            raise
    
    async def _stop_orchestrator_async(self):
        """Stoppar orchestrator asynkront."""
        try:
            if self.orchestrator:
                await self.orchestrator.stop()
            
            # Stoppa event loop
            if self.loop:
                self.loop.stop()
                
        except Exception as e:
            logger.error(f"Fel vid async stopp av orchestrator: {e}")
            self.error = str(e)
    
    def get_status(self) -> dict:
        """
        Hämtar status för orchestrator.
        
        Returns:
            Dict med statusinformation
        """
        if not self.is_running or not self.orchestrator:
            return {
                'running': False,
                'error': self.error,
                'uptime': None,
                'mode': 'stopped'
            }
        
        uptime = None
        if self.start_time:
            uptime = str(datetime.now() - self.start_time)
        
        return {
            'running': True,
            'error': self.error,
            'uptime': uptime,
            'mode': 'mock' if self.orchestrator.use_mock_data else 'live',
            'thread_alive': self.thread.is_alive() if self.thread else False,
            'loop_running': self.loop.is_running() if self.loop else False
        }


# Global orchestrator manager instans
_global_manager = None
_manager_lock = threading.Lock()


def get_orchestrator_manager() -> OrchestratorManager:
    """
    Hämtar global orchestrator manager instans (singleton).
    
    Returns:
        Global OrchestratorManager instans
    """
    global _global_manager
    
    with _manager_lock:
        if _global_manager is None:
            _global_manager = OrchestratorManager()
        return _global_manager


def start_global_orchestrator(orchestrator) -> bool:
    """
    Startar orchestrator globalt via manager.
    
    Args:
        orchestrator: DataOrchestrator att starta
        
    Returns:
        True om start lyckades
    """
    manager = get_orchestrator_manager()
    return manager.start_orchestrator(orchestrator)


def stop_global_orchestrator() -> bool:
    """
    Stoppar global orchestrator.
    
    Returns:
        True om stopp lyckades
    """
    manager = get_orchestrator_manager()
    return manager.stop_orchestrator()


def get_global_orchestrator_status() -> dict:
    """
    Hämtar status för global orchestrator.
    
    Returns:
        Status dict
    """
    manager = get_orchestrator_manager()
    return manager.get_status()
