import os.path
import wx

cached_bitmaps = {}
dont_use_cached_bitmaps = False
max_cached_bmps = 500

# @todo: decide on directory structure and fix this
locationMap = {"pack": os.path.join("icons"),
               "ships": os.path.join("icons/ships")}

def getBitmap(name, location):

    global cached_bitmaps
    global dont_use_cached_bitmaps
    global max_cached_bmps

    if dont_use_cached_bitmaps:
        img = getImage(name, location)
        if img is not None:
            return img.ConvertToBitmap()

    path = "%s%s" % (name, location)

    if len(cached_bitmaps) == max_cached_bmps:
        cached_bitmaps.popitem(False)

    if path not in cached_bitmaps:
        img = getImage(name, location)
        if img is not None:
            bmp = img.ConvertToBitmap()
        else:
            bmp = None
        cached_bitmaps[path] = bmp
    else:
        bmp = cached_bitmaps[path]

    return bmp

def getImage(name, location):
    if location in locationMap:
        if location == "pack":
            location = locationMap[location]
            filename = "icon{0}.png".format(name)
            path = os.path.join(location, filename)
        else:
            location = locationMap[location]
            filename = "{0}.png".format(name)
            path = os.path.join(location, filename)

    else:
        location = os.path.join(location)
        filename = "{0}.png".format(name)
        path = os.path.join(location, filename)

    if os.path.exists(path):
        return wx.Image(path)
    else:
        print("Missing icon file: {0}".format(filename))

def getStaticBitmap(parent, name, location):
    static = wx.StaticBitmap(parent)
    static.SetBitmap(getBitmap(name, location))
    return static
