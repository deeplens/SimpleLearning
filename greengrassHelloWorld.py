#
# Copyright Amazon AWS DeepLens, 2017
#
import os
import greengrasssdk
from threading import Timer
import time
import awscam
import cv2
import mxnet as mx
from threading import Thread
import json
import boto3
from botocore.session import Session
import csv

json_string = '{"0": "tench, Tinca tinca", \
	"1": "goldfish, Carassius auratus", \
	"2": "great white shark, white shark, man-eater, man-eating shark, Carcharodon carcharias", \
	"3": "tiger shark, Galeocerdo cuvieri", \
	"4": "hammerhead, hammerhead shark", \
	"5": "electric ray, crampfish, numbfish, torpedo", \
	"6": "stingray", \
	"7": "cock", \
	"8": "hen", \
	"9": "ostrich, Struthio camelus", \
	"10": "brambling, Fringilla montifringilla", \
	"11": "goldfinch, Carduelis carduelis", \
	"12": "house finch, linnet, Carpodacus mexicanus", \
	"13": "junco, snowbird", \
	"14": "indigo bunting, indigo finch, indigo bird, Passerina cyanea", \
	"15": "robin, American robin, Turdus migratorius", \
	"16": "bulbul", \
	"17": "jay", \
	"18": "magpie", \
	"19": "chickadee", \
	"20": "water ouzel, dipper", \
	"21": "kite", \
	"22": "bald eagle, American eagle, Haliaeetus leucocephalus", \
	"23": "vulture", \
	"24": "great grey owl, great gray owl, Strix nebulosa", \
	"25": "European fire salamander, Salamandra salamandra", \
	"26": "common newt, Triturus vulgaris", \
	"27": "eft", \
	"28": "spotted salamander, Ambystoma maculatum", \
	"29": "axolotl, mud puppy, Ambystoma mexicanum", \
	"30": "bullfrog, Rana catesbeiana", \
	"31": "tree frog, tree-frog", \
	"32": "tailed frog, bell toad, ribbed toad, tailed toad, Ascaphus trui", \
	"33": "loggerhead, loggerhead turtle, Caretta caretta", \
	"34": "leatherback turtle, leatherback, leathery turtle, Dermochelys coriacea", \
	"35": "mud turtle", \
	"36": "terrapin", \
	"37": "box turtle, box tortoise", \
	"38": "banded gecko", \
	"39": "common iguana, iguana, Iguana iguana", \
	"40": "American chameleon, anole, Anolis carolinensis", \
	"41": "whiptail, whiptail lizard", \
	"42": "agama", \
	"43": "frilled lizard, Chlamydosaurus kingi", \
	"44": "alligator lizard", \
	"45": "Gila monster, Heloderma suspectum", \
	"46": "green lizard, Lacerta viridis", \
	"47": "African chameleon, Chamaeleo chamaeleon", \
	"48": "Komodo dragon, Komodo lizard, dragon lizard, giant lizard, Varanus komodoensis", \
	"49": "African crocodile, Nile crocodile, Crocodylus niloticus", \
	"50": "American alligator, Alligator mississipiensis", \
	"51": "triceratops", \
	"52": "thunder snake, worm snake, Carphophis amoenus", \
	"53": "ringneck snake, ring-necked snake, ring snake", \
	"54": "hognose snake, puff adder, sand viper", \
	"55": "green snake, grass snake", \
	"56": "king snake, kingsnake", \
	"57": "garter snake, grass snake", \
	"58": "water snake", \
	"59": "vine snake", \
	"60": "night snake, Hypsiglena torquata", \
	"61": "boa constrictor, Constrictor constrictor", \
	"62": "rock python, rock snake, Python sebae", \
	"63": "Indian cobra, Naja naja", \
	"64": "green mamba", \
	"65": "sea snake", \
	"66": "horned viper, cerastes, sand viper, horned asp, Cerastes cornutus", \
	"67": "diamondback, diamondback rattlesnake, Crotalus adamanteus", \
	"68": "sidewinder horned rattlesnake, Crotalus cerastes", \
	"69": "trilobite", \
	"70": "harvestman, daddy longlegs, Phalangium opilio", \
	"71": "scorpion", \
	"72": "black and gold garden spider, Argiope aurantia", \
	"73": "barn spider, Araneus cavaticus", \
	"74": "garden spider, Aranea diademata", \
	"75": "black widow, Latrodectus mactans", \
	"76": "tarantula", \
	"77": "wolf spider, hunting spider", \
	"78": "tick", \
	"79": "centipede", \
	"80": "black grouse", \
	"81": "ptarmigan", \
	"82": "ruffed grouse, partridge, Bonasa umbellus", \
	"83": "prairie chicken, prairie grouse, prairie fowl", \
	"84": "peacock", \
	"85": "quail", \
	"86": "partridge", \
	"87": "African grey, African gray, Psittacus erithacus", \
	"88": "macaw", \
	"89": "sulphur-crested cockatoo, Kakatoe galerita, Cacatua galerita", \
	"90": "lorikeet", \
	"91": "coucal", \
	"92": "bee eater", \
	"93": "hornbill", \
	"94": "hummingbird", \
	"95": "jacamar", \
	"96": "toucan", \
	"97": "drake", \
	"98": "red-breasted merganser, Mergus serrator", \
	"99": "goose", \
	"100": "black swan, Cygnus atratus", \
	"101": "tusker", \
	"102": "echidna, spiny anteater, anteater", \
	"103": "platypus, duckbill, duckbilled platypus, duck-billed platypus, Ornithorhynchus anatinus", \
	"104": "wallaby, brush kangaroo", \
	"105": "koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus", \
	"106": "wombat", \
	"107": "jellyfish", \
	"108": "sea anemone, anemone", \
	"109": "brain coral", \
	"110": "flatworm, platyhelminth", \
	"111": "nematode, nematode worm, roundworm", \
	"112": "conch", \
	"113": "snail", \
	"114": "slug", \
	"115": "sea slug, nudibranch", \
	"116": "chiton, coat-of-mail shell, sea cradle, polyplacophore", \
	"117": "chambered nautilus, pearly nautilus, nautilus", \
	"118": "Dungeness crab, Cancer magister", \
	"119": "rock crab, Cancer irroratus", \
	"120": "fiddler crab", \
	"121": "king crab, Alaska crab, Alaskan king crab, Alaska king crab, Paralithodes camtschatica", \
	"122": "American lobster, Northern lobster, Maine lobster, Homarus americanus", \
	"123": "spiny lobster, langouste, rock lobster, crawfish, crayfish, sea crawfish", \
	"124": "crayfish, crawfish, crawdad, crawdaddy", \
	"125": "hermit crab", \
	"126": "isopod", \
	"127": "white stork, Ciconia ciconia", \
	"128": "black stork, Ciconia nigra", \
	"129": "spoonbill", \
	"130": "flamingo", \
	"131": "little blue heron, Egretta caerulea", \
	"132": "American egret, great white heron, Egretta albus", \
	"133": "bittern", \
	"134": "crane", \
	"135": "limpkin, Aramus pictus", \
	"136": "European gallinule, Porphyrio porphyrio", \
	"137": "American coot, marsh hen, mud hen, water hen, Fulica americana", \
	"138": "bustard", \
	"139": "ruddy turnstone, Arenaria interpres", \
	"140": "red-backed sandpiper, dunlin, Erolia alpina", \
	"141": "redshank, Tringa totanus", \
	"142": "dowitcher", \
	"143": "oystercatcher, oyster catcher", \
	"144": "pelican", \
	"145": "king penguin, Aptenodytes patagonica", \
	"146": "albatross, mollymawk", \
	"147": "grey whale, gray whale, devilfish, Eschrichtius gibbosus, Eschrichtius robustus", \
	"148": "killer whale, killer, orca, grampus, sea wolf, Orcinus orca", \
	"149": "dugong, Dugong dugon", \
	"150": "sea lion", \
	"151": "Chihuahua", \
	"152": "Japanese spaniel", \
	"153": "Maltese dog, Maltese terrier, Maltese", \
	"154": "Pekinese, Pekingese, Peke", \
	"155": "Shih-Tzu", \
	"156": "Blenheim spaniel", \
	"157": "papillon", \
	"158": "toy terrier", \
	"159": "Rhodesian ridgeback", \
	"160": "Afghan hound, Afghan", \
	"161": "basset, basset hound", \
	"162": "beagle", \
	"163": "bloodhound, sleuthhound", \
	"164": "bluetick", \
	"165": "black-and-tan coonhound", \
	"166": "Walker hound, Walker foxhound", \
	"167": "English foxhound", \
	"168": "redbone", \
	"169": "borzoi, Russian wolfhound", \
	"170": "Irish wolfhound", \
	"171": "Italian greyhound", \
	"172": "whippet", \
	"173": "Ibizan hound, Ibizan Podenco", \
	"174": "Norwegian elkhound, elkhound", \
	"175": "otterhound, otter hound", \
	"176": "Saluki, gazelle hound", \
	"177": "Scottish deerhound, deerhound", \
	"178": "Weimaraner", \
	"179": "Staffordshire bullterrier, Staffordshire bull terrier", \
	"180": "American Staffordshire terrier, Staffordshire terrier, American pit bull terrier, pit bull terrier", \
	"181": "Bedlington terrier", \
	"182": "Border terrier", \
	"183": "Kerry blue terrier", \
	"184": "Irish terrier", \
	"185": "Norfolk terrier", \
	"186": "Norwich terrier", \
	"187": "Yorkshire terrier", \
	"188": "wire-haired fox terrier", \
	"189": "Lakeland terrier", \
	"190": "Sealyham terrier, Sealyham", \
	"191": "Airedale, Airedale terrier", \
	"192": "cairn, cairn terrier", \
	"193": "Australian terrier", \
	"194": "Dandie Dinmont, Dandie Dinmont terrier", \
	"195": "Boston bull, Boston terrier", \
	"196": "miniature schnauzer", \
	"197": "giant schnauzer", \
	"198": "standard schnauzer", \
	"199": "Scotch terrier, Scottish terrier, Scottie", \
	"200": "Tibetan terrier, chrysanthemum dog", \
	"201": "silky terrier, Sydney silky", \
	"202": "soft-coated wheaten terrier", \
	"203": "West Highland white terrier", \
	"204": "Lhasa, Lhasa apso", \
	"205": "flat-coated retriever", \
	"206": "curly-coated retriever", \
	"207": "golden retriever", \
	"208": "Labrador retriever", \
	"209": "Chesapeake Bay retriever", \
	"210": "German short-haired pointer", \
	"211": "vizsla, Hungarian pointer", \
	"212": "English setter", \
	"213": "Irish setter, red setter", \
	"214": "Gordon setter", \
	"215": "Brittany spaniel", \
	"216": "clumber, clumber spaniel", \
	"217": "English springer, English springer spaniel", \
	"218": "Welsh springer spaniel", \
	"219": "cocker spaniel, English cocker spaniel, cocker", \
	"220": "Sussex spaniel", \
	"221": "Irish water spaniel", \
	"222": "kuvasz", \
	"223": "schipperke", \
	"224": "groenendael", \
	"225": "malinois", \
	"226": "briard", \
	"227": "kelpie", \
	"228": "komondor", \
	"229": "Old English sheepdog, bobtail", \
	"230": "Shetland sheepdog, Shetland sheep dog, Shetland", \
	"231": "collie", \
	"232": "Border collie", \
	"233": "Bouvier des Flandres, Bouviers des Flandres", \
	"234": "Rottweiler", \
	"235": "German shepherd, German shepherd dog, German police dog, alsatian", \
	"236": "Doberman, Doberman pinscher", \
	"237": "miniature pinscher", \
	"238": "Greater Swiss Mountain dog", \
	"239": "Bernese mountain dog", \
	"240": "Appenzeller", \
	"241": "EntleBucher", \
	"242": "boxer", \
	"243": "bull mastiff", \
	"244": "Tibetan mastiff", \
	"245": "French bulldog", \
	"246": "Great Dane", \
	"247": "Saint Bernard, St Bernard", \
	"248": "Eskimo dog, husky", \
	"249": "malamute, malemute, Alaskan malamute", \
	"250": "Siberian husky", \
	"251": "dalmatian, coach dog, carriage dog", \
	"252": "affenpinscher, monkey pinscher, monkey dog", \
	"253": "basenji", \
	"254": "pug, pug-dog", \
	"255": "Leonberg", \
	"256": "Newfoundland, Newfoundland dog", \
	"257": "Great Pyrenees", \
	"258": "Samoyed, Samoyede", \
	"259": "Pomeranian", \
	"260": "chow, chow chow", \
	"261": "keeshond", \
	"262": "Brabancon griffon", \
	"263": "Pembroke, Pembroke Welsh corgi", \
	"264": "Cardigan, Cardigan Welsh corgi", \
	"265": "toy poodle", \
	"266": "miniature poodle", \
	"267": "standard poodle", \
	"268": "Mexican hairless", \
	"269": "timber wolf, grey wolf, gray wolf, Canis lupus", \
	"270": "white wolf, Arctic wolf, Canis lupus tundrarum", \
	"271": "red wolf, maned wolf, Canis rufus, Canis niger", \
	"272": "coyote, prairie wolf, brush wolf, Canis latrans", \
	"273": "dingo, warrigal, warragal, Canis dingo", \
	"274": "dhole, Cuon alpinus", \
	"275": "African hunting dog, hyena dog, Cape hunting dog, Lycaon pictus", \
	"276": "hyena, hyaena", \
	"277": "red fox, Vulpes vulpes", \
	"278": "kit fox, Vulpes macrotis", \
	"279": "raccoon", \
	"280": "raccoon", \
	"281": "tabby, tabby cat", \
	"282": "tiger cat", \
	"283": "Persian cat", \
	"284": "Siamese cat, Siamese", \
	"285": "Egyptian cat", \
	"286": "cougar, puma, catamount, mountain lion, painter, panther, Felis concolor", \
	"287": "lynx, catamount", \
	"288": "leopard, Panthera pardus", \
	"289": "snow leopard, ounce, Panthera uncia", \
	"290": "jaguar, panther, Panthera onca, Felis onca", \
	"291": "lion, king of beasts, Panthera leo", \
	"292": "tiger, Panthera tigris", \
	"293": "cheetah, chetah, Acinonyx jubatus", \
	"294": "brown bear, bruin, Ursus arctos", \
	"295": "American black bear, black bear, Ursus americanus, Euarctos americanus", \
	"296": "ice bear, polar bear, Ursus Maritimus, Thalarctos maritimus", \
	"297": "sloth bear, Melursus ursinus, Ursus ursinus", \
	"298": "mongoose", \
	"299": "meerkat, mierkat", \
	"300": "tiger beetle", \
	"301": "ladybug, ladybeetle, lady beetle, ladybird, ladybird beetle", \
	"302": "ground beetle, carabid beetle", \
	"303": "long-horned beetle, longicorn, longicorn beetle", \
	"304": "leaf beetle, chrysomelid", \
	"305": "dung beetle", \
	"306": "rhinoceros beetle", \
	"307": "weevil", \
	"308": "fly", \
	"309": "bee", \
	"310": "ant, emmet, pismire", \
	"311": "grasshopper, hopper", \
	"312": "cricket", \
	"313": "walking stick, walkingstick, stick insect", \
	"314": "cockroach, roach", \
	"315": "mantis, mantid", \
	"316": "cicada, cicala", \
	"317": "leafhopper", \
	"318": "lacewing, lacewing fly", \
	"319": "dragonfly, darning needle, devils darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk", \
	"320": "damselfly", \
	"321": "admiral", \
	"322": "ringlet, ringlet butterfly", \
	"323": "monarch, monarch butterfly, milkweed butterfly, Danaus plexippus", \
	"324": "cabbage butterfly", \
	"325": "sulphur butterfly, sulfur butterfly", \
	"326": "lycaenid, lycaenid butterfly", \
	"327": "starfish, sea star", \
	"328": "sea urchin", \
	"329": "sea cucumber, holothurian", \
	"330": "wood rabbit, cottontail, cottontail rabbit", \
	"331": "hare", \
	"332": "Angora, Angora rabbit", \
	"333": "opossum", \
	"334": "porcupine, hedgehog", \
	"335": "fox squirrel, eastern fox squirrel, Sciurus niger", \
	"336": "marmot", \
	"337": "beaver", \
	"338": "guinea pig, Cavia cobaya", \
	"339": "sorrel", \
	"340": "zebra", \
	"341": "hog, pig, grunter, squealer, Sus scrofa", \
	"342": "wild boar, boar, Sus scrofa", \
	"343": "warthog", \
	"344": "hippopotamus, hippo, river horse, Hippopotamus amphibius", \
	"345": "ox", \
	"346": "water buffalo, water ox, Asiatic buffalo, Bubalus bubalis", \
	"347": "bison", \
	"348": "ram, tup", \
	"349": "bighorn, bighorn sheep, cimarron, Rocky Mountain bighorn, Rocky Mountain sheep, Ovis canadensis", \
	"350": "ibex, Capra ibex", \
	"351": "hartebeest", \
	"352": "impala, Aepyceros melampus", \
	"353": "gazelle", \
	"354": "Arabian camel, dromedary, Camelus dromedarius", \
	"355": "llama", \
	"356": "weasel", \
	"357": "mink", \
	"358": "polecat, fitch, foulmart, foumart, Mustela putorius", \
	"359": "black-footed ferret, ferret, Mustela nigripes", \
	"360": "otter", \
	"361": "skunk, polecat, wood pussy", \
	"362": "badger", \
	"363": "armadillo", \
	"364": "three-toed sloth, ai, Bradypus tridactylus", \
	"365": "orangutan, orang, orangutang, Pongo pygmaeus", \
	"366": "gorilla, Gorilla gorilla", \
	"367": "chimpanzee, chimp, Pan troglodytes", \
	"368": "gibbon, Hylobates lar", \
	"369": "siamang, Hylobates syndactylus, Symphalangus syndactylus", \
	"370": "guenon, guenon monkey", \
	"371": "patas, hussar monkey, Erythrocebus patas", \
	"372": "baboon", \
	"373": "macaque", \
	"374": "langur", \
	"375": "colobus, colobus monkey", \
	"376": "proboscis monkey, Nasalis larvatus", \
	"377": "marmoset", \
	"378": "capuchin, ringtail, Cebus capucinus", \
	"379": "howler monkey, howler", \
	"380": "titi, titi monkey", \
	"381": "spider monkey, Ateles geoffroyi", \
	"382": "squirrel monkey, Saimiri sciureus", \
	"383": "Madagascar cat, ring-tailed lemur, Lemur catta", \
	"384": "indri, indris, Indri indri, Indri brevicaudatus", \
	"385": "Indian elephant, Elephas maximus", \
	"386": "African elephant, Loxodonta africana", \
	"387": "lesser panda, red panda, panda, bear cat, cat bear, Ailurus fulgens", \
	"388": "giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca", \
	"389": "barracouta, snoek", \
	"390": "eel", \
	"391": "coho, cohoe, coho salmon, blue jack, silver salmon, Oncorhynchus kisutch", \
	"392": "rock beauty, Holocanthus tricolor", \
	"393": "anemone fish", \
	"394": "sturgeon", \
	"395": "gar, garfish, garpike, billfish, Lepisosteus osseus", \
	"396": "lionfish", \
	"397": "puffer, pufferfish, blowfish, globefish", \
	"398": "abacus", \
	"399": "abaya", \
	"400": "academic gown, academic robe, judges robe", \
	"401": "accordion, piano accordion, squeeze box", \
	"402": "acoustic guitar", \
	"403": "aircraft carrier, carrier, flattop, attack aircraft carrier", \
	"404": "airliner", \
	"405": "airship, dirigible", \
	"406": "altar", \
	"407": "ambulance", \
	"408": "amphibian, amphibious vehicle", \
	"409": "analog clock", \
	"410": "apiary, bee house", \
	"411": "apron", \
	"412": "ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin", \
	"413": "assault rifle, assault gun", \
	"414": "backpack, back pack, knapsack, packsack, rucksack, haversack", \
	"415": "bakery, bakeshop, bakehouse", \
	"416": "balance beam, beam", \
	"417": "balloon", \
	"418": "ballpoint, ballpoint pen, ballpen, Biro", \
	"419": "Band Aid", \
	"420": "banjo", \
	"421": "bannister, banister, balustrade, balusters, handrail", \
	"422": "barbell", \
	"423": "barber chair", \
	"424": "barbershop", \
	"425": "barn", \
	"426": "barometer", \
	"427": "barrel, cask", \
	"428": "barrow, garden cart, lawn cart, wheelbarrow", \
	"429": "baseball", \
	"430": "basketball", \
	"431": "bassinet", \
	"432": "bassoon", \
	"433": "bathing cap, swimming cap", \
	"434": "bath towel", \
	"435": "bathtub, bathing tub, bath, tub", \
	"436": "beach wagon, station wagon, wagon, estate car, beach waggon, station waggon, waggon", \
	"437": "beacon, lighthouse, beacon light, pharos", \
	"438": "beaker", \
	"439": "bearskin, busby, shako", \
	"440": "beer bottle", \
	"441": "beer glass", \
	"442": "bell cote, bell cot", \
	"443": "bib", \
	"444": "bicycle-built-for-two, tandem bicycle, tandem", \
	"445": "bikini, two-piece", \
	"446": "binder, ring-binder", \
	"447": "binoculars, field glasses, opera glasses", \
	"448": "birdhouse", \
	"449": "boathouse", \
	"450": "bobsled, bobsleigh, bob", \
	"451": "bolo tie, bolo, bola tie, bola", \
	"452": "bonnet, poke bonnet", \
	"453": "bookcase", \
	"454": "bookshop, bookstore, bookstall", \
	"455": "bottlecap", \
	"456": "bow", \
	"457": "bow tie, bow-tie, bowtie", \
	"458": "brass, memorial tablet, plaque", \
	"459": "brassiere, bra, bandeau", \
	"460": "breakwater, groin, groyne, mole, bulwark, seawall, jetty", \
	"461": "breastplate, aegis, egis", \
	"462": "broom", \
	"463": "bucket, pail", \
	"464": "buckle", \
	"465": "bulletproof vest", \
	"466": "bullet train, bullet", \
	"467": "butcher shop, meat market", \
	"468": "cab, hack, taxi, taxicab", \
	"469": "caldron, cauldron", \
	"470": "candle, taper, wax light", \
	"471": "cannon", \
	"472": "canoe", \
	"473": "can opener, tin opener", \
	"474": "cardigan", \
	"475": "car mirror", \
	"476": "carousel, carrousel, merry-go-round, roundabout, whirligig", \
	"477": "carpenters kit, tool kit", \
	"478": "carton", \
	"479": "car wheel", \
	"480": "cash machine, cash dispenser, automated teller machine, automatic teller machine, automated teller, automatic teller, ATM", \
	"481": "cassette", \
	"482": "cassette player", \
	"483": "castle", \
	"484": "catamaran", \
	"485": "CD player", \
	"486": "cello, violoncello", \
	"487": "cellular telephone, cellular phone, cellphone, cell, mobile phone", \
	"488": "chain", \
	"489": "chainlink fence", \
	"490": "chain mail, ring mail, mail, chain armor, chain armour, ring armor, ring armour", \
	"491": "chain saw, chainsaw", \
	"492": "chest", \
	"493": "chiffonier, commode", \
	"494": "chime, bell, gong", \
	"495": "china cabinet, china closet", \
	"496": "Christmas stocking", \
	"497": "church, church building", \
	"498": "cinema, movie theater, movie theatre, movie house, picture palace", \
	"499": "cleaver, meat cleaver, chopper", \
	"500": "cliff dwelling", \
	"501": "cloak", \
	"502": "clog, geta, patten, sabot", \
	"503": "cocktail shaker", \
	"504": "coffee mug", \
	"505": "coffeepot", \
	"506": "coil, spiral, volute, whorl, helix", \
	"507": "combination lock", \
	"508": "computer keyboard, keypad", \
	"509": "confectionery, confectionary, candy store", \
	"510": "container ship, containership, container vessel", \
	"511": "convertible", \
	"512": "corkscrew, bottle screw", \
	"513": "cornet, horn, trumpet, trump", \
	"514": "cowboy boot", \
	"515": "cowboy hat, ten-gallon hat", \
	"516": "cradle", \
	"517": "crane", \
	"518": "crash helmet", \
	"519": "crate", \
	"520": "crib, cot", \
	"521": "Crock Pot", \
	"522": "croquet ball", \
	"523": "crutch", \
	"524": "cuirass", \
	"525": "dam, dike, dyke", \
	"526": "desk", \
	"527": "desktop computer", \
	"528": "dial telephone, dial phone", \
	"529": "diaper, nappy, napkin", \
	"530": "digital clock", \
	"531": "digital watch", \
	"532": "dining table, board", \
	"533": "dishrag, dishcloth", \
	"534": "dishwasher, dish washer, dishwashing machine", \
	"535": "disk brake, disc brake", \
	"536": "dock, dockage, docking facility", \
	"537": "dogsled, dog sled, dog sleigh", \
	"538": "dome", \
	"539": "doormat, welcome mat", \
	"540": "drilling platform, offshore rig", \
	"541": "drum, membranophone, tympan", \
	"542": "drumstick", \
	"543": "dumbbell", \
	"544": "Dutch oven", \
	"545": "electric fan, blower", \
	"546": "electric guitar", \
	"547": "electric locomotive", \
	"548": "entertainment center", \
	"549": "envelope", \
	"550": "espresso maker", \
	"551": "face powder", \
	"552": "feather boa, boa", \
	"553": "file, file cabinet, filing cabinet", \
	"554": "fireboat", \
	"555": "fire engine, fire truck", \
	"556": "fire screen, fireguard", \
	"557": "flagpole, flagstaff", \
	"558": "flute, transverse flute", \
	"559": "folding chair", \
	"560": "football helmet", \
	"561": "forklift", \
	"562": "fountain", \
	"563": "fountain pen", \
	"564": "four-poster", \
	"565": "freight car", \
	"566": "French horn, horn", \
	"567": "frying pan, frypan, skillet", \
	"568": "fur coat", \
	"569": "garbage truck, dustcart", \
	"570": "gasmask, respirator, gas helmet", \
	"571": "gas pump, gasoline pump, petrol pump, island dispenser", \
	"572": "goblet", \
	"573": "go-kart", \
	"574": "golf ball", \
	"575": "golfcart, golf cart", \
	"576": "gondola", \
	"577": "gong, tam-tam", \
	"578": "gown", \
	"579": "grand piano, grand", \
	"580": "greenhouse, nursery, glasshouse", \
	"581": "grille, radiator grille", \
	"582": "grocery store, grocery, food market, market", \
	"583": "guillotine", \
	"584": "hair slide", \
	"585": "hair spray", \
	"586": "half track", \
	"587": "hammer", \
	"588": "hamper", \
	"589": "hand blower, blow dryer, blow drier, hair dryer, hair drier", \
	"590": "hand-held computer, hand-held microcomputer", \
	"591": "handkerchief, hankie, hanky, hankey", \
	"592": "hard disc, hard disk, fixed disk", \
	"593": "harmonica, mouth organ, harp, mouth harp", \
	"594": "harp", \
	"595": "harvester, reaper", \
	"596": "hatchet", \
	"597": "holster", \
	"598": "home theater, home theatre", \
	"599": "honeycomb", \
	"600": "hook, claw", \
	"601": "hoopskirt, crinoline", \
	"602": "horizontal bar, high bar", \
	"603": "horse cart, horse-cart", \
	"604": "hourglass", \
	"605": "iPod", \
	"606": "iron, smoothing iron", \
	"607": "jack-o-lantern", \
	"608": "jean, blue jean, denim", \
	"609": "jeep, landrover", \
	"610": "jersey, T-shirt, tee shirt", \
	"611": "jigsaw puzzle", \
	"612": "jinrikisha, ricksha, rickshaw", \
	"613": "joystick", \
	"614": "kimono", \
	"615": "knee pad", \
	"616": "knot", \
	"617": "lab coat, laboratory coat", \
	"618": "ladle", \
	"619": "lampshade, lamp shade", \
	"620": "laptop, laptop computer", \
	"621": "lawn mower, mower", \
	"622": "lens cap, lens cover", \
	"623": "letter opener, paper knife, paperknife", \
	"624": "library", \
	"625": "lifeboat", \
	"626": "lighter, light, igniter, ignitor", \
	"627": "limousine, limo", \
	"628": "liner, ocean liner", \
	"629": "lipstick, lip rouge", \
	"630": "Loafer", \
	"631": "lotion", \
	"632": "loudspeaker, speaker, speaker unit, loudspeaker system, speaker system", \
	"633": "loupe, jewelers loupe", \
	"634": "lumbermill, sawmill", \
	"635": "magnetic compass", \
	"636": "mailbag, postbag", \
	"637": "mailbox, letter box", \
	"638": "maillot", \
	"639": "maillot, tank suit", \
	"640": "manhole cover", \
	"641": "maraca", \
	"642": "marimba, xylophone", \
	"643": "mask", \
	"644": "matchstick", \
	"645": "maypole", \
	"646": "maze, labyrinth", \
	"647": "measuring cup", \
	"648": "medicine chest, medicine cabinet", \
	"649": "megalith, megalithic structure", \
	"650": "microphone, mike", \
	"651": "microwave, microwave oven", \
	"652": "military uniform", \
	"653": "milk can", \
	"654": "minibus", \
	"655": "miniskirt, mini", \
	"656": "minivan", \
	"657": "missile", \
	"658": "mitten", \
	"659": "mixing bowl", \
	"660": "mobile home, manufactured home", \
	"661": "Model T", \
	"662": "modem", \
	"663": "monastery", \
	"664": "monitor", \
	"665": "moped", \
	"666": "mortar", \
	"667": "mortarboard", \
	"668": "mosque", \
	"669": "mosquito net", \
	"670": "motor scooter, scooter", \
	"671": "mountain bike, all-terrain bike, off-roader", \
	"672": "mountain tent", \
	"673": "mouse, computer mouse", \
	"674": "mousetrap", \
	"675": "moving van", \
	"676": "muzzle", \
	"677": "nail", \
	"678": "neck brace", \
	"679": "necklace", \
	"680": "nipple", \
	"681": "notebook, notebook computer", \
	"682": "obelisk", \
	"683": "oboe, hautboy, hautbois", \
	"684": "ocarina, sweet potato", \
	"685": "odometer, hodometer, mileometer, milometer", \
	"686": "oil filter", \
	"687": "organ, pipe organ", \
	"688": "oscilloscope, scope, cathode-ray oscilloscope, CRO", \
	"689": "overskirt", \
	"690": "oxcart", \
	"691": "oxygen mask", \
	"692": "packet", \
	"693": "paddle, boat paddle", \
	"694": "paddlewheel, paddle wheel", \
	"695": "padlock", \
	"696": "paintbrush", \
	"697": "pajama, pyjama, pjs, jammies", \
	"698": "palace", \
	"699": "panpipe, pandean pipe, syrinx", \
	"700": "paper towel", \
	"701": "parachute, chute", \
	"702": "parallel bars, bars", \
	"703": "park bench", \
	"704": "parking meter", \
	"705": "passenger car, coach, carriage", \
	"706": "patio, terrace", \
	"707": "pay-phone, pay-station", \
	"708": "pedestal, plinth, footstall", \
	"709": "pencil box, pencil case", \
	"710": "pencil sharpener", \
	"711": "perfume, essence", \
	"712": "Petri dish", \
	"713": "photocopier", \
	"714": "pick, plectrum, plectron", \
	"715": "pickelhaube", \
	"716": "picket fence, paling", \
	"717": "pickup, pickup truck", \
	"718": "pier", \
	"719": "piggy bank, penny bank", \
	"720": "pill bottle", \
	"721": "pillow", \
	"722": "ping-pong ball", \
	"723": "pinwheel", \
	"724": "pirate, pirate ship", \
	"725": "pitcher, ewer", \
	"726": "plane, carpenters plane, woodworking plane", \
	"727": "planetarium", \
	"728": "plastic bag", \
	"729": "plate rack", \
	"730": "plow, plough", \
	"731": "plunger, plumbers helper", \
	"732": "Polaroid camera, Polaroid Land camera", \
	"733": "pole", \
	"734": "police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria", \
	"735": "poncho", \
	"736": "pool table, billiard table, snooker table", \
	"737": "pop bottle, soda bottle", \
	"738": "pot, flowerpot", \
	"739": "potters wheel", \
	"740": "power drill", \
	"741": "prayer rug, prayer mat", \
	"742": "printer", \
	"743": "prison, prison house", \
	"744": "projectile, missile", \
	"745": "projector", \
	"746": "puck, hockey puck", \
	"747": "punching bag, punch bag, punching ball, punchball", \
	"748": "purse", \
	"749": "quill, quill pen", \
	"750": "quilt, comforter, comfort, puff", \
	"751": "racer, race car, racing car", \
	"752": "racket, racquet", \
	"753": "radiator", \
	"754": "radio, wireless", \
	"755": "radio telescope, radio reflector", \
	"756": "rain barrel", \
	"757": "recreational vehicle, RV, R.V.", \
	"758": "reel", \
	"759": "reflex camera", \
	"760": "refrigerator, icebox", \
	"761": "remote control, remote", \
	"762": "restaurant, eating house, eating place, eatery", \
	"763": "revolver, six-gun, six-shooter", \
	"764": "rifle", \
	"765": "rocking chair, rocker", \
	"766": "rotisserie", \
	"767": "rubber eraser, rubber, pencil eraser", \
	"768": "rugby ball", \
	"769": "rule, ruler", \
	"770": "running shoe", \
	"771": "safe", \
	"772": "safety pin", \
	"773": "saltshaker, salt shaker", \
	"774": "sandal", \
	"775": "sarong", \
	"776": "sax, saxophone", \
	"777": "scabbard", \
	"778": "scale, weighing machine", \
	"779": "school bus", \
	"780": "schooner", \
	"781": "scoreboard", \
	"782": "screen, CRT screen", \
	"783": "screw", \
	"784": "screwdriver", \
	"785": "seat belt, seatbelt", \
	"786": "sewing machine", \
	"787": "shield, buckler", \
	"788": "shoe shop, shoe-shop, shoe store", \
	"789": "shoji", \
	"790": "shopping basket", \
	"791": "shopping cart", \
	"792": "shovel", \
	"793": "shower cap", \
	"794": "shower curtain", \
	"795": "ski", \
	"796": "ski mask", \
	"797": "sleeping bag", \
	"798": "slide rule, slipstick", \
	"799": "sliding door", \
	"800": "slot, one-armed bandit", \
	"801": "snorkel", \
	"802": "snowmobile", \
	"803": "snowplow, snowplough", \
	"804": "soap dispenser", \
	"805": "soccer ball", \
	"806": "sock", \
	"807": "solar dish, solar collector, solar furnace", \
	"808": "sombrero", \
	"809": "soup bowl", \
	"810": "space bar", \
	"811": "space heater", \
	"812": "space shuttle", \
	"813": "spatula", \
	"814": "speedboat", \
	"815": "spider web, spiders web", \
	"816": "spindle", \
	"817": "sports car, sport car", \
	"818": "spotlight, spot", \
	"819": "stage", \
	"820": "steam locomotive", \
	"821": "steel arch bridge", \
	"822": "steel drum", \
	"823": "stethoscope", \
	"824": "stole", \
	"825": "stone wall", \
	"826": "stopwatch, stop watch", \
	"827": "stove", \
	"828": "strainer", \
	"829": "streetcar, tram, tramcar, trolley, trolley car", \
	"830": "stretcher", \
	"831": "studio couch, day bed", \
	"832": "stupa, tope", \
	"833": "submarine, pigboat, sub, U-boat", \
	"834": "suit, suit of clothes", \
	"835": "sundial", \
	"836": "sunglass", \
	"837": "sunglasses, dark glasses, shades", \
	"838": "sunscreen, sunblock, sun blocker", \
	"839": "suspension bridge", \
	"840": "swab, swob, mop", \
	"841": "sweatshirt", \
	"842": "swimming trunks, bathing trunks", \
	"843": "swing", \
	"844": "switch, electric switch, electrical switch", \
	"845": "syringe", \
	"846": "table lamp", \
	"847": "tank, army tank, armored combat vehicle, armoured combat vehicle", \
	"848": "tape player", \
	"849": "teapot", \
	"850": "teddy, teddy bear", \
	"851": "television, television system", \
	"852": "tennis ball", \
	"853": "thatch, thatched roof", \
	"854": "theater curtain, theatre curtain", \
	"855": "thimble", \
	"856": "thresher, thrasher, threshing machine", \
	"857": "throne", \
	"858": "tile roof", \
	"859": "opossum", \
	"860": "tobacco shop, tobacconist shop, tobacconist", \
	"861": "toilet seat", \
	"862": "torch", \
	"863": "totem pole", \
	"864": "tow truck, tow car, wrecker", \
	"865": "toyshop", \
	"866": "tractor", \
	"867": "trailer truck, tractor trailer, trucking rig, rig, articulated lorry, semi", \
	"868": "tray", \
	"869": "trench coat", \
	"870": "tricycle, trike, velocipede", \
	"871": "trimaran", \
	"872": "tripod", \
	"873": "triumphal arch", \
	"874": "trolleybus, trolley coach, trackless trolley", \
	"875": "trombone", \
	"876": "tub, vat", \
	"877": "turnstile", \
	"878": "typewriter keyboard", \
	"879": "umbrella", \
	"880": "unicycle, monocycle", \
	"881": "upright, upright piano", \
	"882": "vacuum, vacuum cleaner", \
	"883": "vase", \
	"884": "vault", \
	"885": "velvet", \
	"886": "vending machine", \
	"887": "vestment", \
	"888": "viaduct", \
	"889": "violin, fiddle", \
	"890": "volleyball", \
	"891": "waffle iron", \
	"892": "wall clock", \
	"893": "wallet, billfold, notecase, pocketbook", \
	"894": "wardrobe, closet, press", \
	"895": "warplane, military plane", \
	"896": "washbasin, handbasin, washbowl, lavabo, wash-hand basin", \
	"897": "washer, automatic washer, washing machine", \
	"898": "water bottle", \
	"899": "water jug", \
	"900": "water tower", \
	"901": "whiskey jug", \
	"902": "whistle", \
	"903": "wig", \
	"904": "window screen", \
	"905": "window shade", \
	"906": "Windsor tie", \
	"907": "wine bottle", \
	"908": "wing", \
	"909": "wok", \
	"910": "wooden spoon", \
	"911": "wool, woolen, woollen", \
	"912": "worm fence, snake fence, snake-rail fence, Virginia fence", \
	"913": "wreck", \
	"914": "yawl", \
	"915": "yurt", \
	"916": "web site, website, internet site, site", \
	"917": "comic book", \
	"918": "crossword puzzle, crossword", \
	"919": "street sign", \
	"920": "traffic light, traffic signal, stoplight", \
	"921": "book jacket, dust cover, dust jacket, dust wrapper", \
	"922": "menu", \
	"923": "plate", \
	"924": "guacamole", \
	"925": "consomme", \
	"926": "hot pot, hotpot", \
	"927": "trifle", \
	"928": "ice cream, icecream", \
	"929": "ice lolly, lolly, lollipop, popsicle", \
	"930": "French loaf", \
	"931": "bagel, beigel", \
	"932": "pretzel", \
	"933": "cheeseburger", \
	"934": "hotdog, hot dog, red hot", \
	"935": "mashed potato", \
	"936": "head cabbage", \
	"937": "broccoli", \
	"938": "cauliflower", \
	"939": "zucchini, courgette", \
	"940": "spaghetti squash", \
	"941": "acorn squash", \
	"942": "butternut squash", \
	"943": "cucumber, cuke", \
	"944": "artichoke, globe artichoke", \
	"945": "bell pepper", \
	"946": "cardoon", \
	"947": "mushroom", \
	"948": "Granny Smith", \
	"949": "strawberry", \
	"950": "orange", \
	"951": "lemon", \
	"952": "fig", \
	"953": "pineapple, ananas", \
	"954": "banana", \
	"955": "jackfruit, jak, jack", \
	"956": "custard apple", \
	"957": "pomegranate", \
	"958": "hay", \
	"959": "carbonara", \
	"960": "chocolate sauce, chocolate syrup", \
	"961": "dough", \
	"962": "meat loaf, meatloaf", \
	"963": "pizza, pizza pie", \
	"964": "potpie", \
	"965": "burrito", \
	"966": "red wine", \
	"967": "espresso", \
	"968": "cup", \
	"969": "eggnog", \
	"970": "alp", \
	"971": "bubble", \
	"972": "cliff, drop, drop-off", \
	"973": "coral reef", \
	"974": "geyser", \
	"975": "lakeside, lakeshore", \
	"976": "promontory, headland, head, foreland", \
	"977": "sandbar, sand bar", \
	"978": "seashore, coast, seacoast, sea-coast", \
	"979": "valley, vale", \
	"980": "volcano", \
	"981": "ballplayer, baseball player", \
	"982": "groom, bridegroom", \
	"983": "scuba diver", \
	"984": "rapeseed", \
	"985": "daisy", \
	"986": "yellow ladys slipper, yellow lady-slipper, Cypripedium calceolus, Cypripedium parviflorum", \
	"987": "corn", \
	"988": "acorn", \
	"989": "hip, rose hip, rosehip", \
	"990": "buckeye, horse chestnut, conker", \
	"991": "coral fungus", \
	"992": "agaric", \
	"993": "gyromitra", \
	"994": "stinkhorn, carrion fungus", \
	"995": "earthstar", \
	"996": "hen-of-the-woods, hen of the woods, Polyporus frondosus, Grifola frondosa", \
	"997": "bolete", \
	"998": "ear, spike, capitulum", \
	"999": "toilet tissue, toilet paper, bathroom tissue"}'

parsed_json = json.loads(json_string)

ret, frame = awscam.getLastFrame()
ret, jpeg = cv2.imencode('.jpg', frame)
Write_To_FIFO = True


class FIFO_Thread(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

    def run(self):
        fifo_path = "/tmp/results.mjpeg"
        if not os.path.exists(fifo_path):
            os.mkfifo(fifo_path)
        f = open(fifo_path, 'w')
        client.publish(topic=iotTopic, payload="Opened Pipe")
        while Write_To_FIFO:
            try:
                f.write(jpeg.tobytes())
            except IOError as e:
                continue


# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

# The information exchanged between IoT and clould has
# a topic and a message body.
# This is the topic that this code uses to send messages to cloud
iotTopic = '$aws/things/{}/infer'.format(os.environ['AWS_IOT_THING_NAME'])

# When deployed to a Greengrass core, this code will be executed immediately
# as a long-lived lambda function.


def greengrass_infinite_infer_run():
    try:
        artifact_file = "/opt/awscam/artifacts/mxnet_squeezenet.xml"
        modelType = "classification"
        results_thread = FIFO_Thread()
        results_thread.start()

        # Send a starting message to IoT console
        client.publish(topic=iotTopic,
                       payload="Hotdog or not inference starts now")

        #session = Session()
        #s3 = session.create_client('s3')

        # Load model to GPU (use {"GPU": 0} for CPU)
        mcfg = {"GPU": 1}
        model = awscam.Model(artifact_file, mcfg)
        client.publish(topic=iotTopic, payload="Model loaded")
        ret, frame = awscam.getLastFrame()
        width = frame.shape[1]
        if ret == False:
            raise Exception("Failed to get frame from the stream")

        numFrames = 0
        doInfer = True
        csv_data = ""
        t_end = time.time() + 20

        #while doInfer:
        while time.time() < t_end:
            # Get a frame from the video stream
            ret, frame = awscam.getLastFrame()

            # Raise an exception if failing to get a frame
            if ret == False:
                raise Exception("Failed to get frame from the stream")

            # Resize frame to fit model input requirement
            frameResize = cv2.resize(frame, (224, 224))

            # Run model inference on the resized frame
            inferOutput = model.doInference(frameResize)

            outputProcessed = model.parseResult(modelType, inferOutput)
            results = outputProcessed[modelType]

            prob = ""
            #tops = results[modelType][0:5]

            for top in results[0:5]:
                prob = str(prob) + str(top['label']) + ": " + str(
                    top['prob'] * 100) + parsed_json[str(top['label'])] + "\n"

            client.publish(topic=iotTopic, payload=prob)

            matchingObjects = ""
            prob_hotdog = 0
            font = cv2.FONT_HERSHEY_SIMPLEX
            global jpeg
            ret, jpeg = cv2.imencode('.jpg', frame)

            session = Session()
            s3 = session.create_client('s3')

            # Here we get the state of Simple Learning. The states are:
            #
            #  Idle Requested
            #  Idle
            #  Training Requested
            #  Training Started
            #  Training Completed
            #  Detection Requested
            #  Detection Started
            #
            #  And then back to Idle again when detection is no longer required.
            #
            #  This functon reads the S3 bucket to obtain 'Requested' states and replies to the S3 bucket with 'Started' and 'Completed' states.
            #  The exception here is idle, where it is requested by setting the S3 bucket (with Alexa) and this module sets it to idle. This function
            #  keeps looping, of course, waiting for another 'Requested' state.
            #
            #  There is also a recognition threshold we would like controlable by the user. "Alexa - Tell Deep Lens to set recognition threshold to 70%"
            #
            #  And of coure, the query "Alexa - Ask Deep Lens what the recognition threshold is set to"
            #
            #
            s3_state = boto3.resource('s3')
            bucket = s3_state.Bucket('your-bucket')
            bucketString = 'your-bucket'

            trainingSecondsDefault = 60

            rootKey = 'deeplens/simplelearning/'
            baseKey = rootKey + 'admin/'
            currentStateKey = baseKey + 'state/currentstate.txt'
            requestedStateKey = baseKey + 'state/requestedstate.txt'
            trainingResultsKey = baseKey + 'training/trainingresults.txt'
            trainingStartTimeKey = baseKey + 'training/trainingstarttime.txt'
            trainingSecondsKey = baseKey + 'training/trainingseconds.txt'
            trainingMatchingObjectsKey = baseKey + 'training/matchingobjects.txt'

            imagesKey = rootKey + 'images/'
            #client.publish(topic=iotTopic, payload="1")
            # Check if the current state file exists. If so, then read it. If not, then set current state to idle and write to the currentstate file.
            objs = list(bucket.objects.filter(Prefix=currentStateKey))
            #client.publish(topic=iotTopic, payload="1dd")
            if len(objs) > 0 and objs[0].key == currentStateKey:
                # Exists!
                #client.publish(topic=iotTopic, payload="befpre get currentStateKey")
                data = s3.get_object(Bucket=bucketString, Key=currentStateKey)
                #client.publish(topic=iotTopic, payload="after get currentStateKey")
                currentState = data['Body'].read()
                client.publish(topic=iotTopic, payload="after read")
            else:
                # Does not exist. So set the current state to 'idle'
                #client.publish(topic=iotTopic, payload="before write to currentStateKey")
                #resp = s3.put_object(Body="Idle", Bucket=bucket, Key=currentStateKey)
                resp = s3.put_object(Body='Idle',
                                     Bucket=bucketString,
                                     Key=currentStateKey)
                currentState = "Idle"
                client.publish(topic=iotTopic, payload="1b")
                # Also, since the currentstate.txt file does not exist, it indicates it is the first time using this bucket. So let's set up some admin
                # parameters. Set TrainingSeconds to 60. Set DetectionThreshold to 50.
            client.publish(topic=iotTopic, payload=currentState)
            # Check if the trainingseconds.txt file exists. If not, let's create one with a default of 60 seconds.
            objs = list(bucket.objects.filter(Prefix=trainingSecondsKey))
            #client.publish(topic=iotTopic, payload="2")
            if len(objs) > 0 and objs[0].key == trainingSecondsKey:
                # Exists!
                data = s3.get_object(Bucket=bucketString,
                                     Key=trainingSecondsKey)
                trainingSeconds = data['Body'].read()
            else:
                # Does not exist. So set trainingSeconds to a default of 60 seconds and write it back to the S3 bucket.
                trainingSeconds = trainingSecondsDefault
                client.publish(topic=iotTopic,
                               payload="About to write trainingsecondskey")
                resp = s3.put_object(Body='60',
                                     Bucket=bucketString,
                                     Key=trainingSecondsKey)
                client.publish(topic=iotTopic,
                               payload="After trainingsecondskey")

            # Now see if there is a requested state
            # requestedStateKey = 'deeplens/simplelearning/admin/state/requestedstate.txt'
            objs = list(bucket.objects.filter(Prefix=requestedStateKey))
            if len(objs) > 0 and objs[0].key == requestedStateKey:
                # Exists!
                client.publish(topic=iotTopic,
                               payload="Requested state exists")
                data = s3.get_object(Bucket=bucketString,
                                     Key=requestedStateKey)
                requestedState = data['Body'].read()
                client.publish(topic=iotTopic,
                               payload="Requested state read as: " +
                               requestedState)

                # At this point, we have a requested state.
                # Here are all the possible states:
                #
                #  Idle Requested
                #  Idle
                #  Training Requested
                #  Training Started
                #  Training Completed
                #  Detection Requested
                #  Detection Started
                #
                # We respond to the three requested states and set the current state. State is managed in the two state files in the S3 bucket.
                #
                # If the requested state is "Training Requested", then delete the existing training results file, delete the requestedstate.txt file,
                # set the current state to "Training Started" and write that text to the currentstate.txt file.
                if (requestedState == "Training Requested"):
                    client.publish(topic=iotTopic,
                                   payload="Processing Training Requested")

                    resp = s3.put_object(
                        Body=' ', Bucket=bucketString, Key=trainingResultsKey
                    )  # Overwrite whatever is in the training results file.
                    client.publish(
                        topic=iotTopic,
                        payload="About to delete requested state file")

                    resp = s3.delete_object(
                        Bucket=bucketString, Key=requestedStateKey
                    )  # Delete the requested state file.
                    currentState = "Training Started"
                    client.publish(topic=iotTopic,
                                   payload="About to write current state file")

                    resp = s3.put_object(Body=currentState,
                                         Bucket=bucketString,
                                         Key=currentStateKey)
                    client.publish(
                        topic=iotTopic,
                        payload="About to write training start time.")

                    resp = s3.put_object(Body=str(datetime.datetime.now()),
                                         Bucket=bucketString,
                                         Key=trainingStartTimeKey)
                    client.publish(
                        topic=iotTopic,
                        payload="Done with writing training start time.")

                # If the requested state is "Detection Requested", then set the current state to detection started, write "Detection Started" to the currentstate.txt file.
                # Delete the requestedstate.txt file.
                # Stop writing detections to the training file. Instead, compare new detections against the background training data and eliminate those already in the file.
                if (requestedState == "Detection Requested"):
                    resp = s3.delete_object(
                        Bucket=bucketString, Key=requestedStateKey
                    )  # Delete the requested state file.
                    currentState = "Detection Started"
                    resp = s3.put_object(Body=currentState,
                                         Bucket=bucketString,
                                         Key=currentStateKey)

                # If the requested state is "Idle Requested", then set the current state to idle, delete the requestedstate.txt file, and write "Idle" to the currentstate file.
                if (requestedState == "Idle Requested"):
                    resp = s3.delete_object(
                        Bucket=bucketString, Key=requestedStateKey
                    )  # Delete the requested state file.
                    currentState = "Idle"
                    resp = s3.put_object(Body=currentState,
                                         Bucket=bucketString,
                                         Key=currentStateKey)

                # If Training Started is the current state we test if the time > the trainingstarttime + trainingseconds. If so, then we set the current state to
                # "Training Completed" and write this to the currentstate.txt file. Both the training completed and idle states skip the code execution below.

            # Now that we have handled any state updates, let's execute based on the current state.
            if (currentState == "Training Started"):
                # Get the current list of matching objects from previous executions in this training cycle.
                matchingObjects = ""
                objs = list(
                    bucket.objects.filter(Prefix=trainingMatchingObjectsKey))
                if len(objs) > 0 and objs[0].key == trainingMatchingObjectsKey:
                    # Exists!
                    data = s3.get_object(Bucket=bucketString,
                                         Key=trainingMatchingObjectsKey)
                    matchingObjects = data['Body'].read()

                client.publish(topic=iotTopic,
                               payload="Matching Objects: " +
                               str(matchingObjects))

                for obj in results[0:4]:
                    if obj['prob'] > 0.5:
                        if str(obj['label']) not in matchingObjects:
                            if len(matchingObjects) > 0:
                                matchingObjects = matchingObjects + ", "
                            matchingObjects = matchingObjects + str(
                                obj['label'])
                            client.publish(topic=iotTopic,
                                           payload="New Matching Objects: " +
                                           str(matchingObjects))
                            resp = s3.put_object(
                                Body=str(matchingObjects),
                                Bucket=bucketString,
                                Key=trainingMatchingObjectsKey)
                            client.publish(topic=iotTopic,
                                           payload="Updated training key")
                client.publish(topic=iotTopic, payload="Finished the obj loop")

            if (currentState == "Detection Started"):
                # Get the current list of matching objects from previous executions in this training cycle.
                matchingObjects = ""
                objs = list(
                    bucket.objects.filter(Prefix=trainingMatchingObjectsKey))
                if len(objs) > 0 and objs[0].key == trainingMatchingObjectsKey:
                    # Exists!
                    data = s3.get_object(Bucket=bucketString,
                                         Key=trainingMatchingObjectsKey)
                    matchingObjects = data['Body'].read()
                else:
                    currentState = "Deep Lens detection cannot be performed until training is done first. Please issue the command - Alexa, tell deep lens to start training."
                    resp = s3.put_object(Body=currentState,
                                         Bucket=bucketString,
                                         Key=currentStateKey)

                client.publish(topic=iotTopic,
                               payload="Detection Matching Objects: " +
                               str(matchingObjects))

                for obj in results[0:4]:
                    if obj['prob'] > 0.5:
                        if str(obj['label']) not in matchingObjects:
                            # We have detected an object. It's time to send an alert.
                            client.publish(topic=iotTopic,
                                           payload="We have a Detection!! " +
                                           str(obj['label']))
                            file_name = imagesKey + 'image-' + time.strftime(
                                "%Y%m%d-%H%M%S") + '.jpg'
                            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                            _, jpg_data = cv2.imencode('.jpg', frame,
                                                       encode_param)

                            response = s3.put_object(
                                Body=jpg_data.tostring(),
                                Bucket='deeplens-sagemaker-daniel-brennan',
                                Key=file_name)
                            image_url = 'https://s3.amazonaws.com/deeplens-sagemaker-daniel-brennan/' + file_name

                            # Now we construct a JSON structure with the fields required for the Simple Learning Notifier.
                            data = {
                                "key": "DeepLens Simple Learning",
                                "Label1":
                                parsed_json[str(results[0]['label'])],
                                "Obj1Prob": str(results[0]['prob'] * 100),
                                "Label2":
                                parsed_json[str(results[1]['label'])],
                                "Obj2Prob": str(results[1]['prob'] * 100),
                                "URL": image_url
                            }
                            '''dat['key'] = "DeepLens Simple Learning"
                            dat['Label1'] = parsed_json[str(results[0]['label'])]
                            dat['Obj1Prob'] = str(results[0]['prob'] * 100)
                            dat['Label2'] = parsed_json[str(results[1]['label'])]
                            dat['Obj2Prob'] = str(results[1]['prob'] * 100)
                            dat['URL'] = image_url'''
                            json_output = json.dumps(data)
                            client.publish(topic=iotTopic, payload=json_output)

    except Exception as e:
        msg = "Test failed: " + str(e)
        client.publish(topic=iotTopic, payload=msg)

    # Asynchronously schedule this function to be run again in 15 seconds
    Timer(15, greengrass_infinite_infer_run).start()


# Execute the function above
greengrass_infinite_infer_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
