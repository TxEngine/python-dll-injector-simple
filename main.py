import ctypes
import psutil	
import os
process_name = "notepad.exe" 
path_dll = "test.dll"


def inject_dll(pid):
    dll_path = os.path.join(os.getcwd(), path_dll)
    dll = ctypes.WinDLL(dll_path)
    PROCESS_ALL_ACCESS = 0x1F0FFF
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    path_addr = ctypes.windll.kernel32.VirtualAllocEx(handle, 0, len(dll_path), 0x1000, 0x40)
    ctypes.windll.kernel32.WriteProcessMemory(handle, path_addr, dll_path.encode('utf-8'), len(dll_path), 0)
    thread_id = ctypes.c_ulong(0)
    ctypes.windll.kernel32.CreateRemoteThread(handle, None, 0, ctypes.c_void_p(int(dll._handle)), path_addr, 0, ctypes.byref(thread_id))
def pid():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    return None


#inject dll 
pid = pid() 
if pid :
    inject_dll(pid)
else:
    print( process_name,"not found")