
for mod, cls in (
    ('graphicsmagick', 'GraphicsMagicImage'),
    ('pil', 'PILImage'),
):
    try:
        _mod = __import__(mod, globals(), locals(), [cls], -1)
    except ImportError:
        continue
    Image = getattr(_mod, cls)
    break

if not 'Image' in globals():
    raise ImportError('could not import any of the image implementation modules')

