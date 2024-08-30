import ctypes
import time
import random
import string
import threading


GENERIC_WRITE = 0x40000000
GENERIC_READ = 0x80000000
OPEN_ALWAYS = 4
FILE_ATTRIBUTE_NORMAL = 0x80


HKEY_CURRENT_USER = 0x80000001
KEY_WRITE = 0x20006


INTERNET_OPEN_TYPE_DIRECT = 1


kernel32 = ctypes.windll.kernel32
advapi32 = ctypes.windll.advapi32
wininet = ctypes.windll.wininet

def random_string(length):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def hammer_create_file():
    """Repeatedly create, write, and close files."""
    while True:
        filename = f"example_{random_string(6)}.txt"
        handle = kernel32.CreateFileW(
            filename, GENERIC_WRITE | GENERIC_READ, 0, None, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, None
        )
        if handle != -1:
            random_data = random_string(100).encode("utf-8")
            written = ctypes.c_ulong(0)
            kernel32.WriteFile(handle, random_data, len(random_data), ctypes.byref(written), None)
            kernel32.CloseHandle(handle)
        time.sleep(0.01)


def hammer_open_process():
    """Repeatedly open processes to create noise."""
    while True:
        pid = random.randint(1000, 5000)
        process_handle = kernel32.OpenProcess(0x1F0FFF, False, pid)
        if process_handle:
            kernel32.CloseHandle(process_handle)
        time.sleep(0.01)


def hammer_memory_allocation():
    """Repeatedly allocate and free memory in the process."""
    while True:
        allocation_size = 1024
        address = kernel32.VirtualAlloc(None, allocation_size, 0x3000, 0x40)
        if address:
            random_data = random_string(allocation_size).encode("utf-8")
            ctypes.memmove(address, random_data, allocation_size)
            kernel32.VirtualFree(address, 0, 0x8000)
        time.sleep(0.01)


def hammer_registry():
    """Repeatedly create and delete registry keys/values."""
    while True:
        hKey = ctypes.c_void_p()
        subkey = f"Software\\Example_{random_string(6)}"
        advapi32.RegCreateKeyExW(
            HKEY_CURRENT_USER, subkey, 0, None, 0, KEY_WRITE, None, ctypes.byref(hKey), None
        )
        advapi32.RegSetValueExW(hKey, "ExampleValue", 0, 1, ctypes.c_wchar_p("RandomValue"), 20)
        advapi32.RegCloseKey(hKey)
        time.sleep(0.01)


def hammer_network():
    """Repeatedly perform HTTP requests to generate network noise."""
    while True:
        h_internet = wininet.InternetOpenW("API Hammering", INTERNET_OPEN_TYPE_DIRECT, None, None, 0)
        if h_internet:
            url = random.choice(["http://example.com", "http://test.com"])
            h_url = wininet.InternetOpenUrlW(h_internet, url, None, 0, 0, 0)
            if h_url:
                wininet.InternetCloseHandle(h_url)
            wininet.InternetCloseHandle(h_internet)
        time.sleep(0.01)


def hammer_create_process():
    """Repeatedly create new processes to generate noise."""
    while True:
        process_info = ctypes.create_string_buffer(16)
        startup_info = ctypes.create_string_buffer(68)
        success = kernel32.CreateProcessW(
            None, ctypes.c_wchar_p("notepad.exe"), None, None, False, 0, None, None, startup_info, process_info
        )
        if success:
            kernel32.CloseHandle(process_info)
        time.sleep(0.01)


def hammer_load_library():
    """Repeatedly load and free DLLs to generate noise."""
    while True:
        library_name = ctypes.c_wchar_p("kernel32.dll")
        handle = kernel32.LoadLibraryW(library_name)
        if handle:
            kernel32.FreeLibrary(handle)
        time.sleep(0.01)

def quick_sand():
    """Launch multiple hammering threads."""
    # Create separate threads for each hammering task
    threads = [
        threading.Thread(target=hammer_create_file),
        threading.Thread(target=hammer_open_process),
        threading.Thread(target=hammer_memory_allocation),
        threading.Thread(target=hammer_registry),
        threading.Thread(target=hammer_network),
        threading.Thread(target=hammer_create_process),
        threading.Thread(target=hammer_load_library)
    ]
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Keep the main thread alive
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    quick_sand()
