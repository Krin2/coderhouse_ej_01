# Ejercicio:
# Simular el llamado de 3 subprocesos con concurrencia.
import asyncio
import random
import time
from datetime import datetime

# Simulacion de llamados a subprocesos
async def subprocess_call(process: str, sem: asyncio.Semaphore) -> dict:
  async with sem:                           # respeta el límite de concurrencia 
    startTime = datetime.now()
    print(f"Subproceso llamado: {process}, inicio: {startTime:%H:%M:%S.%f}s")
    latency = random.uniform(0.5, 2.5)      # simulacion de la latencia de red
    try:
        async with asyncio.timeout(2.0):    # timeout para evitar que se cuelgue
            await asyncio.sleep(latency)
            return {"text": process, "dim": 1536, "ok": True}
    except TimeoutError:
        return {"text": process, "ok": False, "error": "timeout"}


# LLama de forma simultanea a los sub-processos
async def call_simultaneously_batch(process: list[str]) -> list[dict]:
    concurrency = asyncio.Semaphore(2)          # definicion de concurrencia: 2 llamados
    tasks = [subprocess_call(t, concurrency) for t in process]
    return await asyncio.gather(*tasks, return_exceptions=True)

# Funcion principal
async def main():
    subprocessList = ["gpt_4", "claude_3", "local_llama"]
    startTime = time.perf_counter()
    results = await call_simultaneously_batch(subprocessList)
    processTime = time.perf_counter() - startTime
    successful = [r for r in results if isinstance(r, dict) and r.get("ok")]
    failed = [r for r in results if isinstance(r, dict) and not r.get("ok")]
    print(f"Procesados OK: {len(successful)}/{len(subprocessList)} en {processTime:.2f}s")
    for f in failed:
        print(f"  Falló: {f['text']} -> {f['error']}")
if __name__ == "__main__":
    asyncio.run(main())