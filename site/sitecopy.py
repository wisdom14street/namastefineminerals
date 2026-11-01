"""Namaste Fine Minerals (namastefineminerals.com): a collector's showcase of natural mineral specimens and statement display
pieces drawn from the Namaste inventory. Mineralogy only: species, locality, size and price. Copy written for this site only."""
import re, types
from mincls import kind_of, species_of, locality_of, size_of, SPECIES, LOC
E = __import__('html').escape
ICON = 'gem'
FAM_LABEL, FAM_ALL, STYLE_LABEL, STYLE_ALL = 'Mineral', 'All minerals', 'Size class', 'All sizes'
NO_FAMILY = ()
QUIZ = None
NAV_AISLES = True
NAV_BRANDS = True
PRICE_OPTS = '<option value="0-100">Under $100</option><option value="100-250">$100 to $250</option><option value="250-500">$250 to $500</option><option value="500-999999">$500 and up</option>'
PRICE_BANDS = [('Under $100', 0, 100), ('$100 to $300', 100, 300), ('$300 and up', 300, 1e9)]
DEFAULT_SORT = 'hi'
def SHOP_ORDER(xs): return sorted(xs, key=lambda x: (x['noimg'], -x['price']))
INFO = {}
def category(p):
    k = kind_of(p)
    if not k: return None
    t = p['title']; sz, meas = size_of(p)
    INFO[p['handle']] = {'species': species_of(t), 'loc': locality_of(t), 'size': sz, 'meas': meas}
    _BY_TITLE[t.strip()] = sz
    return k
def assign(x): return x['base']
def _slug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
FAMILIES = [(_slug(n), n, rx) for n, rx in SPECIES]
def style_of(t, b, base): return _BY_TITLE.get(t, '')
_BY_TITLE = {}
# localities act as the engine's "brand" so each gets a page
BR = types.SimpleNamespace(NAME={_slug(n): n for n, _ in LOC}, brand_of=lambda t, v='': _slug(locality_of(t)) if locality_of(t) else '', FACTS={})
def BRAND_ABOUT(name): return {"@type": "Place", "name": name}

AISLES = {
 'clusters': ('Clusters, Druses & Geodes', 'Clusters & geodes', 'clusters-druses-geodes', 'Groups of crystals grown together, open geodes and botryoidal masses such as grape agate.', '#4b6a88'),
 'matrix':   ('Matrix & Multi-Mineral Specimens', 'On matrix', 'matrix-multi-mineral-specimens', 'Crystals still sitting on their host rock, and pieces where two or more minerals share one specimen.', '#8a6a3b'),
 'single':   ('Single Crystals & Natural Rough', 'Single crystals', 'single-crystals-natural-rough', 'Individual crystals and natural rough, as the ground gave them up.', '#5a7a5a'),
 'polished': ('Slices, Slabs & Polished Faces', 'Slices & slabs', 'slices-slabs-polished-faces', 'Cut and polished faces that open up banding, stalactite rings and internal structure.', '#8a3b4b'),
 'rare':     ('Tektites & Rare Materials', 'Rare materials', 'tektites-rare-materials', 'Moldavite and other natural glasses, and uncommon materials such as elite shungite.', '#2f5a4a'),
 'treated':  ('Aura & Coated Quartz', 'Aura quartz', 'aura-coated-quartz', 'Natural quartz clusters given a thin metal-vapor coating in a lab, which makes the rainbow, blue or gold sheen. The crystals are real; the color is added, and we label it that way.', '#3b6a8a'),
 'display':  ('Statement Display Pieces', 'Display pieces', 'statement-display-pieces', 'Large polished towers, spheres and free forms priced as centerpieces.', '#5a4b7a'),
}
def CARD_TAG(x):
    i = INFO.get(x['handle'], {})
    return ' \u00b7 '.join(v for v in (i.get('species'), i.get('loc')) if v) or AISLES[x['aisle']][1]

# species notes: (chemistry, crystal system, Mohs hardness, one plain collector note). Mineralogy only.
NOTES = {
 'kunzite-spodumene': ('LiAlSi\u2082O\u2086, a lithium pyroxene', 'monoclinic', '6.5 to 7', 'Kunzite is the pink to lilac color of spodumene and hiddenite the green. Its color can fade in long, strong light, so collectors keep it out of sunny windows.'),
 'dioptase': ('CuSiO\u2082(OH)\u2082, a copper silicate', 'trigonal', '5', 'Prized for an emerald-green color deeper than most green minerals. Crystals are small and brittle, so handle the matrix rather than the crystals.'),
 'azurite-malachite': ('copper carbonates: azurite Cu\u2083(CO\u2083)\u2082(OH)\u2082 and malachite Cu\u2082CO\u2083(OH)\u2082', 'monoclinic', '3.5 to 4', 'The two often form together; blue azurite slowly alters to green malachite. Soft, so dust them rather than washing.'),
 'chrysocolla': ('a hydrous copper silicate', 'orthorhombic (usually without visible crystals)', '2 to 4', 'Usually found as blue-green crusts and masses, often mixed with malachite or quartz.'),
 'shattuckite': ('Cu\u2085(SiO\u2083)\u2084(OH)\u2082, a copper silicate', 'orthorhombic', '3.5', 'A deep blue copper mineral, seen far less often than azurite or chrysocolla.'),
 'rhodochrosite': ('MnCO\u2083, manganese carbonate', 'trigonal', '3.5 to 4', 'Argentina is known for banded stalactitic rhodochrosite; cutting across a stalactite shows its concentric rings. Soft and sensitive to acids.'),
 'barite': ('BaSO\u2084, barium sulfate', 'orthorhombic', '3 to 3.5', 'Unusually heavy in the hand for its size, because of the barium.'),
 'chalcopyrite': ('CuFeS\u2082, copper iron sulfide', 'tetragonal', '3.5 to 4', 'A brassy copper ore that can tarnish to iridescent blues and purples; keep it dry.'),
 'pyrite': ('FeS\u2082, iron sulfide', 'cubic', '6 to 6.5', 'Grows as sharp cubes and pyritohedrons. Keep it dry and away from humidity, which can make it tarnish or decay.'),
 'hematite': ('Fe\u2082O\u2083, iron oxide', 'trigonal', '5.5 to 6.5', 'Leaves a red-brown streak even when the specimen looks metallic gray. Rosette-shaped groups are called iron roses.'),
 'fluorite': ('CaF\u2082, calcium fluoride', 'cubic', '4', 'Forms cubes and octahedrons and splits cleanly along four directions, so edges chip if knocked.'),
 'calcite': ('CaCO\u2083, calcium carbonate', 'trigonal', '3', 'Fizzes in weak acid and shows double refraction in clear pieces. One of the most varied minerals in crystal shape.'),
 'celestite': ('SrSO\u2084, strontium sulfate', 'orthorhombic', '3 to 3.5', 'Pale blue crystals that can fade in strong light.'),
 'tourmaline': ('a group of complex borosilicates', 'trigonal', '7 to 7.5', 'Crystals are striated along their length and often change color from one end to the other.'),
 'aquamarine-beryl': ('Be\u2083Al\u2082Si\u2086O\u2081\u2088, beryllium aluminum silicate', 'hexagonal', '7.5 to 8', 'Emerald, aquamarine, morganite and heliodor are all beryl in different colors.'),
 'kyanite': ('Al\u2082SiO\u2085, aluminum silicate', 'triclinic', '4.5 to 7, depending on direction', 'One of the few minerals whose hardness changes noticeably with direction along the blade.'),
 'garnet': ('a group of silicates', 'cubic', '6.5 to 7.5', 'Often grows as rounded twelve-sided crystals.'),
 'apatite': ('Ca\u2085(PO\u2084)\u2083(F,Cl,OH), calcium phosphate', 'hexagonal', '5', 'The mineral that marks 5 on the Mohs scale.'),
 'astrophyllite': ('a potassium iron titanium silicate', 'triclinic', '3', 'Bronze blades that radiate like stars through the host rock.'),
 'mica-lepidolite': ('sheet silicates', 'monoclinic', '2.5 to 3', 'Peels into thin sheets; lepidolite is the lilac, lithium-bearing mica.'),
 'selenite-gypsum': ('CaSO\u2084\u00b72H\u2082O, calcium sulfate', 'monoclinic', '2', 'Soft enough to scratch with a fingernail and slowly damaged by water.'),
 'chalcedony-agate': ('SiO\u2082 in microcrystalline form', 'trigonal (microcrystalline)', '6.5 to 7', 'Agate is banded chalcedony; grape agate is the rounded, grape-like (botryoidal) form.'),
 'jasper': ('SiO\u2082 with other minerals, an opaque chalcedony', 'trigonal (microcrystalline)', '6.5 to 7', 'Its colors come from iron and other included minerals.'),
 'labradorite-feldspar': ('feldspar group aluminosilicates', 'triclinic or monoclinic', '6 to 6.5', 'Labradorite flashes color as light scatters between thin internal layers.'),
 'moldavite-tektites': ('natural silica glass', 'amorphous', 'about 5.5', 'Moldavite formed in a meteorite impact in what is now southern Germany around 15 million years ago, and is found in the Czech Republic. Glass imitations exist, so its source matters.'),
 'shungite': ('a carbon-rich rock (a mineraloid)', 'amorphous', '3.5 to 4', 'From the Karelia region of Russia. The silvery, high-carbon pieces are sold as elite or noble shungite.'),
 'obsidian': ('volcanic glass', 'amorphous', '5 to 5.5', 'Breaks with sharp, shell-shaped fractures.'),
 'gabbro': ('a coarse-grained igneous rock', 'a rock, not a single mineral', 'varies', 'Polished gabbro shows its mix of dark and light minerals.'),
 'amethyst': ('SiO\u2082, quartz colored by iron and natural irradiation', 'trigonal', '7', 'Its purple can fade with years of direct sun.'),
 'citrine': ('SiO\u2082, yellow to orange quartz', 'trigonal', '7', 'The color can be natural or produced by heating amethyst; we follow the wording in each listing title.'),
 'smoky-quartz': ('SiO\u2082, quartz darkened by natural irradiation', 'trigonal', '7', 'Shades run from pale tea to almost black.'),
 'rutilated-included-quartz': ('SiO\u2082 holding inclusions of other minerals', 'trigonal', '7', 'Needles of rutile, chlorite gardens, phantoms or water bubbles sealed inside the quartz are what collectors look for.'),
 'rose-quartz': ('SiO\u2082, pink quartz', 'trigonal', '7', 'Usually massive; well-formed rose quartz crystals are rare.'),
 'quartz': ('SiO\u2082, silicon dioxide', 'trigonal', '7', 'Brazil and Madagascar supply many of the large clear clusters and points on the market.'),
}
VISIT_EYEBROW = 'See a specimen in person'
def STORE_DESC(S): return f'Collector mineral specimens and display pieces: {S.N} natural pieces sorted by mineral, locality, size and price, from the cases at Namaste Bookshop, Manhattan.'
REVIEW_TITLE = 'Added a specimen to your collection?'
REVIEW_TEXT = 'A Google review helps other collectors find these pieces.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><path d="M8 30l6-17 7 6 5-11 6 22z" fill="none" stroke="#b8955a" stroke-width="2" stroke-linejoin="round"/><path d="M4 33h32" stroke="currentColor" stroke-width="1.6"/></svg>'
WORDMARK = 'Namaste <b>Fine Minerals</b>'
SEARCH_PLACEHOLDER = 'Search a mineral or locality: kunzite, Peru'
NAV_EXTRA = '<a href="/minerals/">By mineral</a><a href="/collector-pieces-500-and-up/">$500 and up</a>'

def FOOTER_EXPLORE(S):
    return [('Minerals A to Z', '/minerals/'), ('Localities', '/localities/'), ('Size classes explained', '/guide/specimen-size-classes/'), ('Caring for specimens', '/guide/caring-for-mineral-specimens/'),
            ('$500 and up', '/collector-pieces-500-and-up/'), ('$100 to $500', '/specimens-100-to-500/')]
FOOT_BLURB = 'A gallery of natural mineral specimens: what each piece is, where it was found when the label says so, and how big it is.'
HERO_BASES = ('clusters',)
def HERO(S): return {'eyebrow': '', 'h1': '', 'lede': ''}

def _finest(S): return sorted([x for x in S.leaders if not x['noimg']], key=lambda x: -x['price'])
def _label(S, x):
    i = INFO.get(x['handle'], {})
    return ' \u00b7 '.join(E(v) for v in (i.get('species'), i.get('loc'), i.get('meas')) if v)
def plate(S, x, eager=False):
    u = x['images'][0]
    return (f'<a class="plate" href="/products/{x["handle"]}/"><div class="pimg"><img {"fetchpriority=\"high\" " if eager else "loading=\"lazy\" "}decoding="async" src="{S.img(u, 900)}" srcset="{S.srcset(u, (360, 500, 700, 900, 1200))}" sizes="(min-width:1000px) 33vw,(min-width:640px) 50vw,calc(100vw - 36px)" alt="{E(x["title"])}" width="900" height="900"></div>'
            f'<div class="plabel"><span class="lab">{_label(S, x) or E(AISLES[x["aisle"]][1])}</span><h3>{E(x["title"])}</h3><p class="price">{S.money(x["price"])}</p></div></a>')
def HOME_BODY(S):
    fin = _finest(S)
    head = (f'<section class="galhead"><div class="wrap"><p class="eyebrow">The collection</p><h1>Fine minerals, finest first</h1>'
            f'<p>{S.N} natural specimens and display pieces, shown from the most important down. Every piece is real stock at <a href="{S.SHOP}">Namaste Bookshop</a>, 2 W 14th St, New York.</p></div></section>')
    g1 = '<section class="wrap"><h2 class="sr">Featured pieces</h2><div class="plates">' + ''.join(plate(S, x, i < 1) for i, x in enumerate(fin[:9])) + '</div><p class="more"><a class="btn" href="/shop/?sort=hi">See the whole collection</a></p></section>'
    sp = sorted([(k, n) for k, n in S.fam_count.items() if n >= 2], key=lambda kv: -kv[1])
    chips = ''.join(f'<a class="chip" href="/minerals/{k}/">{E(S.FAM_NAME[k])} <small>{n}</small></a>' for k, n in sp)
    locs = ''.join(f'<a class="chip" href="/localities/{k}/">{E(S.BRAND_NAME[k])} <small>{n}</small></a>' for k, n in S.brand_count.most_common())
    rooms = ''.join(f'<a class="room" href="/shop/{S.AISLES[k][2]}/"><b>{E(S.AISLES[k][0])}</b><span>{E(S.AISLES[k][3])}</span><small>{S.cat_count[k]} pieces</small></a>' for k in S.AISLE_KEYS)
    tiers = [('/collector-pieces-500-and-up/', '$500 and up', 500, 1e9), ('/specimens-250-to-500/', '$250 to $500', 250, 500), ('/specimens-100-to-500/', '$100 to $500', 100, 500), ('/specimens-under-100/', 'Under $100', 0, 100)]
    tchips = ''.join(f'<a class="chip" href="{h}">{l} <small>{sum(1 for x in S.products if lo <= x["price"] < hi)}</small></a>' for h, l, lo, hi in tiers if sum(1 for x in S.products if lo <= x["price"] < hi) >= 3)
    g2 = '<section class="wrap"><div class="sechead"><h2>Next in the cases</h2><a href="/shop/?sort=hi">All pieces &rarr;</a></div><div class="plates small">' + ''.join(plate(S, x) for x in fin[9:21]) + '</div></section>'
    return (head + g1 + f'<section class="wrap"><div class="sechead"><h2>Browse by mineral</h2><a href="/minerals/">Minerals A&ndash;Z &rarr;</a></div><div class="chips">{chips}</div></section>'
            + f'<section class="wrap"><div class="sechead"><h2>The rooms</h2></div><div class="rooms">{rooms}</div></section>' + g2
            + (f'<section class="wrap"><div class="sechead"><h2>By locality</h2><a href="/localities/">All localities &rarr;</a></div><p class="intro">Only where the listing names the source country.</p><div class="chips">{locs}</div></section>' if locs else '')
            + f'<section class="wrap"><div class="sechead"><h2>By price</h2></div><div class="chips">{tchips}</div></section>'
            + f'<section class="wrap">{S.p2_badges()}</section>' + S.section({'type': 'visit'}) + S.section({'type': 'review'}))
HOME_SECTIONS = []
def HOME_TITLE(S): return 'Namaste Fine Minerals | Collector Mineral Specimens & Display Pieces, NYC'
def HOME_DESC(S): return f'{S.N} natural mineral specimens, matrix pieces, clusters, tektites and display pieces, finest first. Browse by mineral, locality, size and price. Ships from NYC or see it at 2 W 14th St.'
def SHOP_TITLE(S): return 'The Whole Collection | Namaste Fine Minerals'
def SHOP_DESC(S): return f'All {S.N} mineral specimens and display pieces, sorted by price from the top. Filter by mineral, locality, size class and price.'
SHOP_H1 = 'The whole collection'
def SHOP_SUB(S): return f'{S.N} pieces, most valuable first. Narrow by mineral, locality, size or price.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]} | Namaste Fine Minerals'
def AISLE_DESC(S, k): return f'{AISLES[k][3]} {S.cat_count[k]} pieces, highest priced first, at Namaste Fine Minerals.'

def _notes_html(k, n):
    if k not in NOTES: return ''
    chem, sysm, mohs, note = NOTES[k]
    return (f'<dl class="minfacts"><div><dt>Chemistry</dt><dd>{E(chem)}</dd></div><div><dt>Crystal system</dt><dd>{E(sysm)}</dd></div><div><dt>Mohs hardness</dt><dd>{E(mohs)}</dd></div></dl><p class="intro">{E(note)}</p>')
def LANDINGS(S):
    L = []
    for k, n, _ in FAMILIES:
        c = S.fam_count[k]
        if c < 2: continue
        L.append({'path': f'/minerals/{k}/', 'title': f'{n} Specimens ({c}) | Namaste Fine Minerals', 'desc': f'{c} {n.lower()} specimens and pieces, finest first, with chemistry, crystal system and hardness.',
                  'h1': f'{n} specimens', 'sub': f'{c} pieces in the collection.', 'filter': {'fam': [k]}, 'intro': _notes_html(k, n)})
    for path, h1, lo, hi, d in [('/collector-pieces-500-and-up/', 'Collector pieces, $500 and up', 500, None, 'The top tier of the collection: large and uncommon pieces.'),
                                ('/specimens-250-to-500/', 'Specimens from $250 to $500', 250, 500, 'Serious display specimens below the top tier.'),
                                ('/specimens-100-to-500/', 'Specimens from $100 to $500', 100, 500, 'The middle of the collection, where most cabinet pieces sit.'),
                                ('/specimens-under-100/', 'Specimens under $100', None, 100, 'Smaller natural pieces to start or round out a collection.')]:
        f = {k2: v for k2, v in (('minp', lo), ('maxp', hi)) if v is not None}
        n = sum(1 for x in S.products if S.match(x, f))
        if n >= 3: L.append({'path': path, 'title': f'{h1} | Namaste Fine Minerals', 'desc': f'{d} {n} pieces.', 'h1': h1, 'sub': f'{n} pieces.', 'filter': f})
    return L

def brand_intro(S, k, st):
    return f'<p>{st["n"]} piece{"s" if st["n"] != 1 else ""} in the collection whose listing names {E(S.BRAND_NAME[k])} as the source, from {S.money(st["min"])}{" to " + S.money(st["max"]) if st["max"] > st["min"] else ""}.</p>'
def brand_faq(S, k, st): return []
def BRAND_H1(S, k): return f'Minerals from {S.BRAND_NAME[k]}'
def BRAND_TITLE(S, k, st): return f'Mineral Specimens from {S.BRAND_NAME[k]} | Namaste Fine Minerals'
def BRAND_DESC(S, k, st): return f'{st["n"]} mineral specimens whose listings name {S.BRAND_NAME[k]} as the locality, from {S.money(st["min"])}.'
def BRANDS_TITLE(S): return 'Mineral Localities | Namaste Fine Minerals'
def BRANDS_DESC(S): return 'Specimens grouped by the source country named in their listing.'
BRANDS_H1 = 'Localities'
def BRANDS_LEAD(S, n): return f'{n} countries are named in our listings. Pieces without a stated source are not guessed at; find them by <a href="/minerals/">mineral</a> instead.'

PAIR = {k: [k] for k in AISLES}
CART_PAIR_TITLE = 'Also in the cases'
REL_BRAND = 'Also from {brand}'
REL_SCENT = 'More {scent}'
REL_PAIR = 'Similar pieces'
REL_MORE = 'More {aisle}'
_KIND = {'clusters': 'crystal group or geode', 'matrix': 'specimen on matrix or with several minerals together', 'single': 'single crystal or natural rough piece', 'polished': 'cut and polished piece',
         'rare': 'rare natural material', 'treated': 'coated quartz cluster', 'display': 'polished display piece'}
def describe(S, x):
    i = INFO.get(x['handle'], {}); k = x['family']; s = [f"{E(x['title'])}: a {_KIND[x['aisle']]} in the Namaste Fine Minerals collection."]
    if i.get('loc'): s.append(f"The listing names {E(i['loc'])} as its locality.")
    if i.get('meas'): s.append(f"Stated size: {E(i['meas'])} ({E(i['size'].lower())}).")
    if k in NOTES:
        chem, sysm, mohs, note = NOTES[k]
        s.append(f'{E(S.FAM_NAME[k])} is {E(chem)}, {E(sysm)}, Mohs {E(mohs)}. {E(note)} <a href="/minerals/{k}/">All {E(S.FAM_NAME[k].lower())}</a>.')
    s.append(f'This piece has not been photographed yet. Call {S.PHONE} and the shop can describe it or send a picture before you buy.' if x['noimg'] else 'Natural specimens are one of a kind; the photo shows the type of piece, so ask us if you want a closer look before buying.')
    s.append(f'Ships from New York City, or see and collect it inside Namaste Bookshop, 2 West 14th Street. Questions: call {S.PHONE}.')
    return s
def PRODUCT_DESC(S, x, v0):
    i = INFO.get(x['handle'], {})
    return f"{x['title']}, {S.money(v0['price'])}." + (f" {i['species']}." if i.get('species') else '') + (f" Locality: {i['loc']}." if i.get('loc') else '') + ' Collector specimen from Namaste Fine Minerals, NYC.'
def _weight(x):
    t = x['title'] + ' ' + re.sub('<[^>]+>', ' ', x.get('raw_body') or '')[:1500]
    m = re.search(r'(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*(?:grams?|gms?|g)\b', t, re.I)
    if m: return f'{m.group(1)} to {m.group(2)} g'
    m = re.search(r'(\d+(?:\.\d+)?)\s*(kg|kilograms?|kilos?)\b', t, re.I)
    if m: return f'{m.group(1)} kg'
    m = re.search(r'(?<![\w.])(\d+(?:\.\d+)?)\s*(?:grams?|gms?|g)\b', t, re.I)
    return f'{m.group(1)} g' if m else ''
def _dims(x):
    t = x['title'] + ' ' + re.sub('<[^>]+>', ' ', x.get('raw_body') or '')[:1500]
    m = re.search(r'(\d+(?:\.\d+)?\s*[x\u00d7]\s*\d+(?:\.\d+)?(?:\s*[x\u00d7]\s*\d+(?:\.\d+)?)?)\s*(cm|mm|in|inch(?:es)?|")', t, re.I)
    if m: return f"{m.group(1).replace(' ', '')} {'in' if m.group(2) in ('"', 'inch', 'inches') else m.group(2).lower()}"
    m = re.search(r'(\d+(?:\.\d+)?\s*(?:-|to)\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?)\s*(?:"|\u201d|\u2033|in\b|inch(?:es)?\b)', x['title'], re.I)
    return f'{m.group(1).replace(" ", "")} in' if m else ''
def FACTS_EXTRA(S, x, v0):
    i = INFO.get(x['handle'], {}); f = []
    d, w = _dims(x), _weight(x)
    if d: f.append(('Dimensions', E(d)))
    if w: f.append(('Weight', E(w)))
    if i.get('meas') and not d and not w: f.append(('Stated size', E(i['meas'])))
    if v0['sku']: f.append(('Stock no.', E(v0['sku'])))
    return f
def LD_EXTRA(S, x, v0):
    i = INFO.get(x['handle'], {})
    d = {'brand': None, 'itemCondition': None, 'category': 'Mineral specimens > ' + AISLES[x['aisle']][0]}
    props = [{'@type': 'PropertyValue', 'name': n, 'value': v} for n, v in (('Mineral', i.get('species')), ('Locality', i.get('loc')), ('Size', i.get('meas')), ('Size class', i.get('size'))) if v]
    if props: d['additionalProperty'] = props
    if i.get('loc'): d['countryOfOrigin'] = i['loc']
    return d
def ABOUT_DESC(S): return 'About Namaste Fine Minerals, the collector mineral showcase of Namaste Bookshop, run by Wealth Edge Ventures Inc.'
ABOUT_H1 = 'About Namaste Fine Minerals'
def ABOUT(S):
    return f'''<p class="lead">Namaste Fine Minerals shows the specimen side of Namaste: natural mineral pieces bought for their form, color and rarity, presented the way a gallery would hang them.</p>
<p>The collection holds {S.N} pieces, from matrix specimens and crystal groups to polished slices, tektites and large display pieces. Pages describe minerals by their chemistry, crystal system and hardness. We name a locality only when the listing itself states it, and we do not attach healing or metaphysical claims to anything here.</p>
<h2>Who runs it</h2><p>{S.LEGAL} The same company owns Namaste Bookshop, where every piece is held. Checkout happens on Shopify through <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>, which takes payment and ships from New York City.</p>
<h2>Viewing a piece</h2><p>Want to see a specimen before you commit? Call <a href="tel:{S.TEL}">{S.PHONE}</a> or email <a href="mailto:info@namastebookshop.com">info@namastebookshop.com</a>, then visit {S.STORE_ADDR}.</p>{S.hours_html()}{S.visit_buttons()}'''
def FAQ_DESC(S): return 'Collector questions for Namaste Fine Minerals: viewing specimens in person, localities, sizes, shipping fragile pieces and pickup in Manhattan.'
FAQ_H1 = 'Collector questions'
def FAQ(S):
    return [('Is the specimen in the photo the one I receive?', 'Many listings show the exact piece, but some photos show the type of piece. If that matters to you, call or email before you order and we will check.'),
            ('How do you decide the locality?', 'We use the source country written in the listing. If the listing does not say, we leave it blank rather than guess.'),
            ('What do the size classes mean?', 'They come from the weight or measurement in the listing title. See <a href="/guide/specimen-size-classes/">specimen size classes</a>.'),
            ('Can I see a piece before buying?', f'Yes. Call {S.PHONE} so it can be set out, then visit Namaste Bookshop at {S.STORE_ADDR}.'),
            ('How are fragile specimens shipped?', 'Orders ship from New York City through namastebookshop.com. Costs and options show at checkout before you pay; for very large pieces, pickup is the safest option.'),
            ('Do you make healing claims about minerals?', 'No. This site covers mineralogy only.')]
def GUIDES(S):
    keys = sorted([k for k, n, _ in FAMILIES if S.fam_count[k] >= 2], key=lambda k: S.FAM_NAME[k])
    rows = ''.join(f'<tr><td><a href="/minerals/{k}/">{E(S.FAM_NAME[k])}</a></td><td>{E(NOTES[k][0]) if k in NOTES else ""}</td><td>{E(NOTES[k][1]) if k in NOTES else ""}</td><td>{E(NOTES[k][2]) if k in NOTES else ""}</td><td>{S.fam_count[k]}</td></tr>' for k in keys)
    return [
     {'path': '/minerals/', 'title': 'Minerals A to Z', 'desc': f'{len(keys)} minerals in the collection with chemistry, crystal system, hardness and the number of pieces.', 'h1': 'Minerals A to Z', 'wide': True,
      'html': f'<p class="lead">Every mineral with at least two pieces in the collection.</p><div class="tablewrap"><table class="hard"><thead><tr><th>Mineral</th><th>Chemistry</th><th>Crystal system</th><th>Mohs</th><th>Pieces</th></tr></thead><tbody>{rows}</tbody></table></div>'},
     {'path': '/guide/specimen-size-classes/', 'title': 'Mineral Specimen Size Classes', 'desc': 'Thumbnail, miniature, small cabinet and cabinet: the size words collectors use and how we apply them from listing weights and measurements.', 'h1': 'Specimen size classes',
      'html': '''<p class="lead">Collectors sort specimens by how much shelf or case they need. The names are informal, but they make a collection easier to plan.</p>
<h2>The usual classes</h2><ul><li><b>Thumbnail:</b> fits in a 1-inch box.</li><li><b>Miniature:</b> up to about 2 inches.</li><li><b>Small cabinet:</b> roughly 2 to 4 inches.</li><li><b>Cabinet:</b> roughly 4 to 7 inches, the classic display size.</li><li><b>Large cabinet:</b> anything bigger, usually a centerpiece.</li></ul>
<h2>How this site assigns them</h2><p>We read the weight or measurement in each listing title. By weight: under 100 g is miniature, 100 to 500 g small cabinet, 500 g to 2 kg cabinet, and over 2 kg large cabinet. By length we use the inch ranges above. Pieces without a stated size are left unclassed.</p>
<p><a class="btn" href="/shop/?sort=hi">Browse by size in the collection</a></p>'''},
     {'path': '/guide/caring-for-mineral-specimens/', 'title': 'Caring for Mineral Specimens', 'desc': 'Practical care for a mineral collection: handling, dust, light, humidity and the minerals that should never be washed.', 'h1': 'Caring for mineral specimens',
      'html': '''<p class="lead">Most specimens need very little: a stable shelf, little handling, and the right kind of cleaning.</p>
<h2>Handle the matrix, not the crystals</h2><p>Pick pieces up by the host rock. Fine crystal tips, especially on dioptase, fluorite or kyanite, break easily.</p>
<h2>Dust with air or a soft brush</h2><p>A blower or a soft makeup brush is enough for most pieces. Avoid wiping across crystal faces.</p>
<h2>Water is not for everything</h2><p>Soft or water-sensitive minerals such as gypsum, chrysocolla, azurite, malachite, rhodochrosite and calcite should stay dry. Sulfides like pyrite and chalcopyrite also prefer dry air.</p>
<h2>Light and humidity</h2><p>Kunzite, celestite, amethyst and some fluorite can fade under strong sun. Pyrite can decay in damp rooms; a dry cabinet helps.</p>
<h2>Keep the label</h2><p>A specimen's locality and size are part of its value. Keep the listing details with the piece.</p>'''},
    ]
NOT_FOUND = 'That specimen is not in the cases'
def ICON_DRAW(d, s, th):
    w = max(2, int(2 * s))
    d.line([(8*s, 30*s), (14*s, 13*s), (21*s, 19*s), (26*s, 8*s), (32*s, 30*s), (8*s, 30*s)], fill=th['accent'], width=w, joint='curve')
    d.line([(4*s, 33*s), (36*s, 33*s)], fill=th['paper'], width=max(1, int(1.6*s)))

# ---- presentation pass hooks ----
import present as _PR
GROUP_BY_TITLE = False          # every specimen is its own piece, never folded into "options"
DESC_MODE = 'mineral'           # original listing text, with health and metaphysical-property lines removed
DESC_HEAD = 'From the listing'
PH_LABEL = 'Photo on request'
PH_CLASS = 'label'
CARD_PICKUP = False
def DISPLAY_TITLE(x):
    t = _PR.clean_title(x['title'])
    t = re.sub(r'\s*[,(-]?\s*\d+(?:\.\d+)?\s*(?:-|to)?\s*\d*(?:\.\d+)?\s*(?:grams?|gms?|g)\b\.?(?:\s*approx\.?)?\)?', '', t, flags=re.I)
    t = re.sub(r'\s*\(per title\)|\s+approx\.?$', '', t, flags=re.I)
    t = re.sub(r'\s*[-\u2013,]\s*$', '', t).strip()
    return t or x['title']
def PH_LINES(x):
    i = INFO.get(x['handle'], {})
    return [(x['ctitle'], 't1'), (' \u00b7 '.join(v for v in (i.get('species'), i.get('loc')) if v), 't2')]
def H1_SUB(S, x):
    i = INFO.get(x['handle'], {}); bits = []
    if x['family']: bits.append(f'<a href="/minerals/{x["family"]}/">{E(S.FAM_NAME[x["family"]])}</a>')
    if x['brand']: bits.append(f'<a href="/localities/{x["brand"]}/">{E(S.BRAND_NAME[x["brand"]])}</a>')
    elif i.get('loc'): bits.append(E(i['loc']))
    return ' &middot; '.join(bits)
PH_HEAD = 'In the cases, not yet photographed'

PK_LABEL = 'Available for store pickup'
PH_FILTER = 'Photographed pieces only'
INSTOCK_NOTE = 'Each specimen listed is in the cases now; the list updates daily.'
