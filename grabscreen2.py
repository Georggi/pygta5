"""
based on work by Frannecklp
changes by dandrews
"""

import win32ui
import win32gui
import win32con
import numpy as np


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(screen=None, _region=None, _scale=1.0, _window_title="Game")
def grab_screen2(scale=1.0, region=None, window_title='Game', window_handle=None):
    
    """
    Grabs screens from windows applications.
    Caches the windows api objects and reuses them as long as you call
    screen_grab with the same arguements
    Arguments:        
    :parameter scale: float to scale images by.            
    :parameter regions: tuple of (top, left, height, width). None grabs whole screen.   
    :parameter window_title: string to search title bars for. Defaults to 'Game'
    """
    
    if grab_screen2.screen is None or grab_screen2._region != region or grab_screen2._scale != scale or grab_screen2._window_title != window_title:
        # Cleanup old object and rebuild with new region.
        if grab_screen2.screen is not None:
            grab_screen2.screen.cleanup()
        
        if region is None:
            grab_screen2.screen = windows_screen_grab(window_title=window_title, scale=scale, window_handle=window_handle)
        else:
            grab_screen2.screen = windows_screen_grab(window_title=window_title, scale=scale, region=region, window_handle=window_handle)

    grab_screen2._region = region
    grab_screen2._scale = scale
    grab_screen2._window_title = window_title
    bits = grab_screen2.screen.get_screen_bits()
    rgb = grab_screen2.screen.get_rgb_from_bits(bits)
    
    return rgb

class windows_screen_grab:
    _hwnd = 0
    
    def enumHandler(self, hwnd, lParam):
        """
        Callback to find correct window handle.
        """
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)            
            if self._search_str in title:                
                self._hwnd = hwnd 

    def __init__(self, window_title: str, scale = 1.0, region = None, window_handle = None):
        """
        :parameter window_title: substring to search for in titles bars. required.
        :parameter scale: float to scale images by.          
        :parameter regions: tuple of (top, left, height, width). None grabs whole screen.            
        """
        self._scale = scale
        self._search_str = window_title
        if window_handle:        
            self._hwnd = window_handle
        else:
            # Look for window title, case sensitive.            
            win32gui.EnumWindows(self.enumHandler, None)
            if self._hwnd == 0:
                message = "window_title '{}' not found.".format(window_title)
                raise ValueError(message)
        
        hwnd = self._hwnd
             
        if region is None:
            rect = win32gui.GetWindowRect(hwnd)
        else:
            rect = region

        width = rect[0]
        height = rect[1]
    
        dest_w = int(width * self._scale)
        dest_h = int(height * self._scale)
        
        dataBitMap = win32ui.CreateBitmap()        
        w_handle_DC = win32gui.GetWindowDC(hwnd)
        windowDC = win32ui.CreateDCFromHandle(w_handle_DC)
        memDC = windowDC.CreateCompatibleDC()
        dataBitMap.CreateCompatibleBitmap(windowDC , dest_w, dest_h)
        memDC.SelectObject(dataBitMap)
        self._w_handle_DC = w_handle_DC
        self._dataBitMap = dataBitMap
        self._memDC = memDC
        self._windowDC = windowDC
        self._height = height
        self._width = width
        self._dest_width = dest_w
        self._dest_height = dest_h
        self._rgb = np.zeros((dest_h, dest_w,3))
    

    """
    Get the raw screen bits.
    returns: a numpy array of the bits in the format (r, g, b, a, r, g, b, a, ...)
    """
    def get_screen_bits(self):        
        self._memDC.StretchBlt((0,0), (self._dest_width, self._dest_height), self._windowDC, (0,0), (self._width,self._height), win32con.SRCCOPY)

##      This part deletes the alpha channel - I handle the case elsewhere, but it can be modified here
##      bits = np.delete(np.fromstring(self._dataBitMap.GetBitmapBits(True), np.uint8), slice(3, None, 4))

        bits = np.fromstring(self._dataBitMap.GetBitmapBits(True), np.uint8)
        return bits
    
    
    def get_rgb_from_bits(self, bits):
        bits.shape = (self._dest_height, self._dest_width, 4)
        self._rgb = bits[:,:,:3]
        return self._rgb

    
    def cleanup(self):
        """
        Release resources.    
        """        
        self._windowDC.DeleteDC()
        self._memDC.DeleteDC()
        win32gui.ReleaseDC(self._hwnd, self._w_handle_DC)
        win32gui.DeleteObject(self._dataBitMap.GetHandle())    

