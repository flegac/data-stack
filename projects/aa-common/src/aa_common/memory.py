import psutil


def get_memory_usage() -> float:
    """
    Retourne l'utilisation mémoire en MB.
    Fonctionne sur Windows, Linux, et MacOS.
    """
    try:
        process = psutil.Process()
        # rss = Resident Set Size (mémoire physique utilisée)
        mem = process.memory_info().rss
        return mem / (1024 * 1024)  # Conversion en MB
    except Exception as e:
        print(f"Warning: Impossible de mesurer la mémoire: {e}")
        return 0.0


from dataclasses import dataclass


@dataclass
class ProcessMemoryStats:
    rss: float  # Mémoire physique en MB
    vms: float  # Mémoire virtuelle en MB

    def __repr__(self):
        return f"RSS: {self.rss:3.0f} MB, VMS: {self.vms:3.0f} MB"


@dataclass
class SystemMemoryStats:
    total: float  # Mémoire totale en GB
    used: float  # Mémoire utilisée en GB
    free: float  # Mémoire libre en GB
    percent: float  # Pourcentage d'utilisation

    def __repr__(self):
        return f"Used: {self.percent:2.2f}% ({self.used:.2f}/{self.total:.2f} GB)"


@dataclass
class MemoryStats:
    process: ProcessMemoryStats
    system: SystemMemoryStats

    def __repr__(self):
        return f"Memory: process={self.process}, System={self.system}"


def get_detailed_memory_info() -> MemoryStats:
    """
    Retourne les statistiques détaillées de l'utilisation mémoire.
    Process memory en MB, System memory en GB.
    """
    process = psutil.Process()
    mem_info = process.memory_info()
    sys_mem = psutil.virtual_memory()

    # Conversion des valeurs en MB pour process et GB pour system
    process_stats = ProcessMemoryStats(
        rss=mem_info.rss / (1024 * 1024), vms=mem_info.vms / (1024 * 1024)
    )

    gb_factor = 1024 * 1024 * 1024
    system_stats = SystemMemoryStats(
        total=sys_mem.total / gb_factor,
        used=(sys_mem.total - sys_mem.available) / gb_factor,
        free=sys_mem.available / gb_factor,
        percent=sys_mem.percent,
    )

    return MemoryStats(process=process_stats, system=system_stats)


def print_memory_usage(message: str | None = None) -> None:
    mem_mb = get_memory_usage()
    msg = f" - {message}" if message else ""
    print(f"Utilisation mémoire{msg}: {mem_mb:.2f} MB")
