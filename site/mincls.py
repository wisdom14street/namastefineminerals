import re
SPEC_TYPES = {'Crystals Specimens', 'Crystal specimen', 'Crystal Specimen', 'Crystal specime', 'Clusters Crystal', 'Crystal Geode', 'Enhydro Quartz', 'Gallery Pieces Crystals Stones',
              'Crystal Polished Slabs, POF, Irregular', 'Crystal Polished Slabs, POF', 'Crystals Slabs POF', 'Crystal Rough Raw', 'Crystals', 'Crystal', 'Stones', 'Polished Crystal',
              'Naturally Polished Faceted Crystal', 'Fossils Crystal', 'Cutbase Cluster / Point', 'Top Polished Cut Base'}
DISPLAY_TYPES = {'Crystal Tower Obeliak', 'Crystal Tower Obeliak Generator', 'Crystal Tower Obelisk', 'Crystal Tower Obelisk Generator', 'CrystalS Point', 'Cut Base Crystal Point', 'Crystal D/T Stones Points', 'Crystal Sphere', 'Free Form Crystals', 'Crystal Points', 'Crystal Carving', 'Crystal Eggs',
                 'Aura Quartz Points, Cluster, Tower', 'Pyramid'}
NOT_MIN = re.compile(r'\b(?:ring|pendant|bracelet|necklace|earring|bead|mala|chain|charm|keychain|candle|incense|oil|spray|soap|book|deck|card|pouch|bag|stand|holder|lamp|tumbled|tumble|worry|palm ?stone|gallet|chip|orgon\w*|pyramid|aura|titanium|dyed|reiki|chakra|massage|gua sha|wand|roller|grid|tree|bottle|dish|bowl|statue|skull|heart|angel|buddha|carving|carved|animal|kit|set|assorted|bundle|lot|grab|mystery|coral|with hole)(?:e?s)?\b', re.I)
SPECIES = [('Kunzite & Spodumene', r'kunzite|spodumene|hiddenite'), ('Dioptase', r'dioptase'), ('Azurite & Malachite', r'azurite|malachite'), ('Chrysocolla', r'chrysocolla'),
 ('Shattuckite', r'shattuckite'), ('Rhodochrosite', r'rhodochrosite'), ('Barite', r'barite|baryte'), ('Chalcopyrite', r'chalcopyrite'), ('Pyrite', r'pyrite'), ('Hematite', r'hematite|iron rose'),
 ('Fluorite', r'fluorite'), ('Calcite', r'calcite'), ('Aragonite', r'aragonite'), ('Celestite', r'celestite|celestine'), ('Apophyllite', r'apophyllite'), ('Stilbite', r'stilbite'),
 ('Okenite', r'okenite'), ('Cavansite', r'cavansite'), ('Vanadinite', r'vanadinite'), ('Wulfenite', r'wulfenite'), ('Tourmaline', r'tourmaline|schorl|rubellite'), ('Aquamarine & Beryl', r'aquamarine|beryl|emerald|morganite|heliodor'),
 ('Kyanite', r'kyanite'), ('Garnet', r'garnet'), ('Apatite', r'apatite'), ('Epidote', r'epidote'), ('Prehnite', r'prehnite'), ('Astrophyllite', r'astrophyl'), ('Mica & Lepidolite', r'lepidolite|mica\b|muscovite'),
 ('Selenite & Gypsum', r'selenite|gypsum|desert rose'), ('Chalcedony & Agate', r'grape agate|agate|chalcedony|chrysoprase|carnelian'), ('Jasper', r'jasper'), ('Labradorite & Feldspar', r'labradorite|feldspar|felspar|amazonite|moonstone|sunstone'),
 ('Moldavite & Tektites', r'moldavite|tektite|libyan desert glass|meteorite'), ('Shungite', r'shungite'), ('Obsidian', r'obsidian'), ('Gabbro', r'gabbro|merlinite'),
 ('Amethyst', r'amethyst'), ('Citrine', r'citrine'), ('Smoky Quartz', r'smok(e)?y'), ('Rutilated & Included Quartz', r'rutil|lodolite|garden quartz|faden|enhydro|phantom|dream quartz|tourmalinated'),
 ('Rose Quartz', r'rose quartz'), ('Quartz', r'quartz|vogel|lemurian|herkimer')]
LOC = [('Brazil', r'brazil'), ('Peru', r'\bperu'), ('Madagascar', r'madagascar'), ('Mongolia', r'mongolia'), ('Colombia', r'colombia'), ('Congo', r'cong[o ]|conglo|congolese|\bcong\b'),
 ('Czech Republic', r'czech'), ('Russia', r'russia|karelia'), ('Pakistan', r'pakistan'), ('Kazakhstan', r'kazakh'), ('Argentina', r'argentin'), ('Mexico', r'mexic'), ('Morocco', r'morocc'),
 ('China', r'\bchina|chinese'), ('India', r'\bindia\b|indian'), ('Uruguay', r'uruguay'), ('Indonesia', r'indonesia'), ('United States', r'arkansas|herkimer|usa\b|u\.s\.a|new york state'),
 ('Namibia', r'namibia'), ('Spain', r'\bspain'), ('Bolivia', r'bolivia'), ('Australia', r'australia'), ('Afghanistan', r'afghan'), ('Nigeria', r'nigeria'), ('Tanzania', r'tanzania'), ('Canada', r'canada|quebec')]
def species_of(t):
    for n, rx in SPECIES:
        if re.search(rx, t, re.I): return n
    return ''
def locality_of(t):
    for n, rx in LOC:
        if re.search(rx, t, re.I): return n
    return ''
QFAM = {'Amethyst', 'Citrine', 'Smoky Quartz', 'Rutilated & Included Quartz', 'Rose Quartz', 'Quartz'}
def n_species(t): return len({('Quartz' if n in QFAM else n) for n, rx in SPECIES if re.search(rx, t, re.I)})
def kind_of(p):
    t, ty = p['title'], p.get('product_type', '') or ''
    price = min([float(v['price']) for v in p['variants'] if v['available'] and float(v['price']) > 0] or [0])
    if not price: return None
    if re.search(r'\bcoral\b|with hole|\bdyed\b', t, re.I): return None
    if ty == 'Aura Quartz Points, Cluster, Tower' or re.search(r'\baura\b', t, re.I):
        # vapor-coated quartz: shown in its own clearly labeled aisle, clusters and specimens only
        return 'treated' if price >= 25 and re.search(r'cluster|specimen|geode|druz', t, re.I) and not re.search(r'pendant|ring|bracelet|necklace|tower|wand|heart', t, re.I) else None
    if NOT_MIN.search(t) and not re.search(r'specimen|cluster|geode|matrix', t, re.I): return None
    if ty in SPEC_TYPES:
        if price < 25: return None
    elif ty in DISPLAY_TYPES:
        if re.search(r'cluster', t, re.I) and price >= 25 and not re.search(r'carv|skull|heart|egg|animal|angel|buddha|orgon|pyramid|tower|sphere', t, re.I): return 'clusters'
        if price < 95 or re.search(r'carv|skull|heart|egg|animal|angel|buddha|orgon|aura|pyramid', t, re.I): return None
        return 'display'
    elif ty == '':
        if p.get('vendor') not in ('Nirvana Inc', 'Namaste Bookshop') or price < 40 or not species_of(t): return None
        if re.search(r'\bby [A-Z]|silver|\.925|sterling|gold\b', t): return None
    else:
        return None
    if re.search(r'moldavite|tektite|meteorite|libyan|elite|noble shungite', t, re.I): return 'rare'
    if re.search(r'geode|grape agate|botryoid', t, re.I): return 'clusters'
    if re.search(r'stalactite|slice|slab|polished|\bpof\b', t, re.I): return 'polished'
    if re.search(r'tower|sphere|obelisk|free ?form', t, re.I): return 'display' if price >= 95 else None
    if re.search(r'matrix', t, re.I) or n_species(t) >= 2: return 'matrix'
    if re.search(r'cluster|druz|druse|vogel|cube', t, re.I): return 'clusters'
    return 'single'
def price_of(p): return min(float(v['price']) for v in p['variants'] if v['available'] and float(v['price']) > 0)
def size_of(p):
    t = p['title'] + ' ' + re.sub('<[^>]+>', ' ', p.get('body_html') or '')[:400]
    m = re.search(r'(\d+(?:\.\d+)?)\s*(kilo|kg)\b', t, re.I)
    g = float(m.group(1)) * 1000 if m else None
    if g is None:
        m = re.search(r'(\d+(?:\.\d+)?)\s*(?:grams?|gms?|g)\b', t, re.I); g = float(m.group(1)) if m else None
    if g:
        return ('Miniature (under 100 g)' if g < 100 else 'Small cabinet (100 to 500 g)' if g < 500 else 'Cabinet (500 g to 2 kg)' if g < 2000 else 'Large cabinet (over 2 kg)'), f'{g:,.0f} g' if g < 1000 else f'{g/1000:.2f} kg'
    m = re.search(r'(\d+(?:\.\d+)?)\s*(?:-|to)?\s*(\d+(?:\.\d+)?)?\s*(?:"|\u201d|in\b|inch)', p['title'], re.I)
    if m:
        v = float(m.group(2) or m.group(1))
        return ('Miniature (under 2 in)' if v < 2 else 'Small cabinet (2 to 4 in)' if v < 4 else 'Cabinet (4 to 7 in)' if v < 7 else 'Large cabinet (7 in and up)'), m.group(0).strip()
    return '', ''
