from django.db import migrations


def seed_data(apps, schema_editor):
    MenuCategory = apps.get_model('menu', 'MenuCategory')
    MenuItem = apps.get_model('menu', 'MenuItem')
    GalleryImage = apps.get_model('menu', 'GalleryImage')

    # --- Categories ---
    starters = MenuCategory.objects.create(name='Starters', slug='starters', order=1)
    mains = MenuCategory.objects.create(name='Mains', slug='mains', order=2)
    desserts = MenuCategory.objects.create(name='Desserts', slug='desserts', order=3)
    drinks = MenuCategory.objects.create(name='Wines & Cocktails', slug='drinks', order=4)

    # --- Menu Items ---
    items = [
        {
            'category': starters, 'order': 1,
            'name': 'Artisanal Plum Crostini',
            'description': 'Whipped goat cheese, fresh plum slices, rosemary honey drizzle, and fresh thyme on toasted sourdough.',
            'price': 16.00,
            'image': '/images/pexels-gislaine-souza-1537222927-27200330.jpg',
            'ingredients': 'Roasted organic black plums, whipped French goat cheese, wild rosemary honey, fresh thyme, hand-pulled toasted sourdough.',
            'calories': 240, 'protein': '8g', 'carbs': '28g', 'fat': '12g',
            'allergens': 'Gluten, Dairy',
            'tags': 'Vegetarian',
            'chefs_note': 'The plum is the heart of this restaurant. I source these from a small orchard in Sonoma — they\'re roasted until they just begin to caramelize, bringing out a jammy richness that cuts through the creamy goat cheese beautifully.',
            'wine_pairing': 'Sommelier-selected Prosecco Extra Dry',
        },
        {
            'category': starters, 'order': 2,
            'name': 'Burrata & Heirloom Beets',
            'description': 'Creamy burrata, roasted baby beets, toasted pistachios, and aged white balsamic glaze.',
            'price': 20.00,
            'image': '/images/anna-pelzer-IGfIGP5ONV0-unsplash.jpg',
            'ingredients': 'Fresh pugliese burrata, roasted baby beets, salted Sicilian pistachios, organic micro-herbs, 25-year aged Modena white balsamic glaze.',
            'calories': 310, 'protein': '12g', 'carbs': '14g', 'fat': '22g',
            'allergens': 'Dairy, Nuts',
            'tags': 'Vegetarian, Gluten Free',
            'chefs_note': 'This dish was born from a trip to Puglia where I watched a nonna pull burrata by hand. The beets are roasted with sea salt and thyme until candy-sweet — a simple tribute to that beautiful memory.',
            'wine_pairing': 'Crisp Sauvignon Blanc',
        },
        {
            'category': starters, 'order': 3,
            'name': 'Plum & Lavender Spritz',
            'description': 'House-made plum liqueur, fresh organic lavender, premium Prosecco, and sparkling soda.',
            'price': 19.00,
            'image': '/images/pexels-valeriya-20505438.jpg',
            'ingredients': 'House-made plum liqueur, organic lavender flowers, premium Italian Prosecco, sparkling mineral water, fresh mint sprig.',
            'calories': 150, 'protein': '0g', 'carbs': '14g', 'fat': '0g',
            'allergens': '',
            'tags': 'Aperitif',
            'chefs_note': 'We grow the lavender ourselves on the restaurant\'s rooftop garden. The plum liqueur is macerated for a full lunar cycle — it turns a deep ruby color and smells like summer in a glass.',
            'wine_pairing': 'Excellent pairing with the Artisanal Plum Crostini',
        },
        {
            'category': mains, 'order': 1,
            'name': 'Plum Glazed Duck',
            'description': 'Slow-roasted duck breast with a spiced plum reduction, parsnip purée, and seasonal baby rainbow carrots.',
            'price': 38.00,
            'image': '/images/kevin-kelly-PPneSBqfCCU-unsplash.jpg',
            'ingredients': 'Slow-roasted free-range duck breast, spiced red plum and port reduction, organic parsnip purée, heirloom rainbow carrots, micro-herbs.',
            'calories': 580, 'protein': '42g', 'carbs': '18g', 'fat': '38g',
            'allergens': '',
            'tags': 'Chef\'s Signature',
            'chefs_note': 'Our signature for a reason. The glaze takes three days — we reduce the plums with star anise, cinnamon, and a splash of port until it coats the back of a spoon. The skin is basted every few minutes for that glass-like finish.',
            'wine_pairing': 'Reserve Cabernet Sauvignon',
        },
        {
            'category': mains, 'order': 2,
            'name': 'Gilded Saffron Risotto',
            'description': 'Creamy Carnaroli rice infused with premium saffron, wild chanterelles, and topped with edible 24k gold leaf.',
            'price': 32.00,
            'image': '/images/pexels-yulia-oliinychenko-849416506-19651271.jpg',
            'ingredients': 'Aged Carnaroli rice, premium Iranian saffron filaments, wild chanterelles, Parmigiano-Reggiano, edible 24k gold leaf flakes.',
            'calories': 450, 'protein': '14g', 'carbs': '62g', 'fat': '16g',
            'allergens': 'Dairy',
            'tags': 'Chef\'s Signature, Vegetarian',
            'chefs_note': 'I insist on Persian saffron from a single family farm in Khorasan. A pinch goes into the stock, another into the finish. The 24k gold is whimsical, but it\'s the earthiness of the chanterelles that truly gilds this dish.',
            'wine_pairing': 'Dry oaky Chardonnay or Pinot Noir',
        },
        {
            'category': mains, 'order': 3,
            'name': 'Truffle Butter Filet Mignon',
            'description': 'Pan-seared prime beef tenderloin with black truffle butter, charred asparagus, and potato fondant.',
            'price': 45.00,
            'image': '/images/lefteris-kallergis-etWlaoFnTl4-unsplash.jpg',
            'ingredients': 'Prime dry-aged beef tenderloin, black winter truffle butter, charred baby asparagus spears, gold potato fondant.',
            'calories': 620, 'protein': '48g', 'carbs': '12g', 'fat': '42g',
            'allergens': 'Dairy',
            'tags': 'Prime Cut',
            'chefs_note': 'We dry-age our beef for a minimum of 28 days. The truffle butter is made fresh each morning — black winter truffles from Provence whipped into French butter with a touch of sea salt. Decadence, pure and simple.',
            'wine_pairing': 'Reserve Cabernet Sauvignon (Vintage 2021)',
        },
        {
            'category': desserts, 'order': 1,
            'name': 'Wild Berry Soufflé',
            'description': 'Light and airy soufflé with hand-picked berries and a warm vanilla bean crème anglaise.',
            'price': 16.00,
            'image': '/images/brooke-lark-oaz0raysASk-unsplash.jpg',
            'ingredients': 'Organic local red raspberries, light egg-white soufflé base, hot vanilla bean crème anglaise pour-over.',
            'calories': 320, 'protein': '6g', 'carbs': '44g', 'fat': '14g',
            'allergens': 'Dairy, Eggs',
            'tags': 'Vegetarian',
            'chefs_note': 'A soufflé is a test of patience and timing. We pick the berries at their peak in July and freeze them immediately. The crème anglaise is my grandmother\'s recipe — it has never let me down.',
            'wine_pairing': 'Sauternes Sweet Dessert Wine',
        },
        {
            'category': desserts, 'order': 2,
            'name': 'Deconstructed Plum Tart',
            'description': 'Rich dark chocolate ganache, spiced plum compote, hazelnut praline, and gold dust.',
            'price': 18.00,
            'image': '/images/pexels-paul-17199062.jpg',
            'ingredients': '70% dark Belgian chocolate ganache, spiced plum compote, toasted hazelnut praline, edible gold dust, shortbread shards.',
            'calories': 480, 'protein': '7g', 'carbs': '52g', 'fat': '28g',
            'allergens': 'Gluten, Dairy, Nuts',
            'tags': 'Vegetarian',
            'chefs_note': 'I wanted to capture the nostalgia of the rustic plum tart my mother made, but deconstruct it into something modern. Each element is made from scratch — familiar yet entirely new.',
            'wine_pairing': '10-Year Tawny Port',
        },
        {
            'category': drinks, 'order': 1,
            'name': 'Gilded Old Fashioned',
            'description': 'Aged bourbon, plum bitters, demerara sugar syrup, orange peel, and edible gold flakes.',
            'price': 22.00,
            'image': '/images/pexels-pedrofurtadoo-28617327.jpg',
            'ingredients': 'Aged Kentucky bourbon, house-infused plum bitters, demerara sugar syrup, flame-orange peel expression, edible gold flakes.',
            'calories': 180, 'protein': '0g', 'carbs': '12g', 'fat': '0g',
            'allergens': '',
            'tags': 'Signature Cocktail',
            'chefs_note': 'Our plum bitters are steeped for six weeks with dried plums, cardamom, and clove. The gold flakes catch the candlelight in a way that just feels right for this room.',
            'wine_pairing': 'Pairs perfectly alongside our Truffle Butter Filet Mignon',
        },
        {
            'category': drinks, 'order': 2,
            'name': 'Reserve Cabernet Sauvignon',
            'description': 'A deep, complex red vintage selected specifically by our resident sommelier to pair with steaks.',
            'price': 25.00,
            'image': '/images/matthieu-joannon-6ciLddToTgM-unsplash.jpg',
            'ingredients': 'A rich red wine vintage from Napa Valley, oak-barrel aged for 24 months, with notes of dark blackberry, leather, and vanilla.',
            'calories': 125, 'protein': '0g', 'carbs': '4g', 'fat': '0g',
            'allergens': 'Sulfites',
            'tags': 'By the Glass',
            'chefs_note': 'Our sommelier travels to Napa personally each year to select our reserve barrels. This vintage spent 24 months in French oak — it has the structure to stand up to our heartiest dishes.',
            'wine_pairing': 'Specially curated for beef and game main courses',
        },
    ]

    for data in items:
        MenuItem.objects.create(**data)

    # --- Gallery Images ---
    gallery_images = [
        {'image': '/images/chad-montano-lP5MCM6nZ5A-unsplash.jpg', 'caption': 'Wood-fired flatbread with fresh herbs, cherry tomatoes, and shaved parmesan', 'alt_text': 'Wood-fired flatbread with fresh herbs', 'order': 1},
        {'image': '/images/lily-banse--YHSwy6uqvk-unsplash.jpg', 'caption': 'Pan-seared wild salmon served with asparagus and fresh salad', 'alt_text': 'Pan-seared wild salmon', 'order': 2},
        {'image': '/images/brooke-lark-oaz0raysASk-unsplash.jpg', 'caption': 'Signature wild berry soufflé dusted with powdered sugar and mint garnish', 'alt_text': 'Wild berry soufflé', 'order': 3},
        {'image': '/images/anna-pelzer-IGfIGP5ONV0-unsplash.jpg', 'caption': 'Artisanal spring harvest salad with organic microgreens, radishes, and edible flowers', 'alt_text': 'Spring harvest salad', 'order': 4},
        {'image': '/images/lefteris-kallergis-etWlaoFnTl4-unsplash.jpg', 'caption': 'Prime pan-seared steak cooked medium-rare and served with roasted baby asparagus', 'alt_text': 'Prime pan-seared steak', 'order': 5},
        {'image': '/images/kevin-kelly-PPneSBqfCCU-unsplash.jpg', 'caption': 'Plum glazed roasted duck breast with parsnip puree and gold flakes', 'alt_text': 'Plum glazed duck breast', 'order': 6},
    ]

    for img_data in gallery_images:
        GalleryImage.objects.create(**img_data)


def unseed_data(apps, schema_editor):
    MenuCategory = apps.get_model('menu', 'MenuCategory')
    MenuItem = apps.get_model('menu', 'MenuItem')
    GalleryImage = apps.get_model('menu', 'GalleryImage')
    MenuItem.objects.all().delete()
    MenuCategory.objects.all().delete()
    GalleryImage.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
