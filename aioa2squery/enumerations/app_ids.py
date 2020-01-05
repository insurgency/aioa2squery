from enum import IntEnum


__all__ = (
    'AppID',
    'GOLDSOURCE_APPS_USE_NEW_INFO',
    'APPS_NO_PACKET_SIZE_FIELD',
)


class AppID(IntEnum):
    """
    An enumeration of common :valve-wiki:`Steam Application IDs <Steam_Application_IDs>` that handle queries
    differently. Can be used with the ``app_id`` parameter of the
    :class:`A2SQueryContext <aioa2squery.A2SQueryContext>` constructor.
    """

    COUNTER_STRIKE = 10
    """:steam-app:`Counter-Strike <10>`"""
    TEAM_FORTRESS_CLASSIC = 20
    """:steam-app:`Team Fortress Classic <20>`"""
    DAY_OF_DEFEAT = 30
    """:steam-app:`Day of Defeat <30>`"""
    DEATHMATCH_CLASSIC = 40
    """:steam-app:`Deathmatch Classic <40>`"""
    HALF_LIFE_OPPOSING_FORCE = 50
    """:steam-app:`Half-Life: Opposing Force <50>`"""
    RICOCHET = 60
    """:steam-app:`Ricochet <60>`"""
    HALF_LIFE = 70
    """:steam-app:`Half-Life <70>`"""
    COUNTER_STRIKE_CONDITION_ZERO = 80
    """:steam-app:`Counter-Strike: Condition Zero <80>`"""
    SOURCE_SDK_BASE_2006 = 215
    """:steam-app:`Source SDK Base 2006 <215>`"""
    SOURCE_SDK_BASE_2007 = 218
    """:steam-app:`Source SDK Base 2007 <218>`"""
    COUNTER_STRIKE_SOURCE = 240
    """:steam-app:`Counter-Strike: Source <240>`"""
    DAY_OF_DEFEAT_SOURCE = 300
    """:steam-app:`Day of Defeat: Source <300>`"""
    HALF_LIFE_2_DEATHMATCH = 320
    """:steam-app:`Half-Life 2: Deathmatch <320>`"""
    HALF_LIFE_DEATHMATCH_SOURCE = 360
    """:steam-app:`Half-Life Deathmatch: Source <360>`"""
    TEAM_FORTRESS_2 = 440
    """:steam-app:`Team Fortress 2 <440>`"""
    SPACEWAR = 480
    """:steam-app:`Spacewar <480>`"""
    LEFT_4_DEAD = 500
    """:steam-app:`Left 4 Dead <500>`"""
    LEFT_4_DEAD_2 = 550
    """:steam-app:`Left 4 Dead 2 <550>`"""
    ALIEN_SWARM = 630
    """:steam-app:`Alien Swarm <630>`"""
    RAG_DOLL_KUNG_FU = 1002
    """:steam-app:`Rag Doll Kung Fu <1002>`"""
    SIN_EPISODES_EMERGENCE = 1300
    """:steam-app:`SiN Episodes: Emergence <1300>`"""
    SIN_MULTIPLAYER = 1309
    """:steam-app:`SiN Multiplayer <1309>`"""
    DARK_MESSIAH_OF_MIGHT_AND_MAGIC_MULTI_PLAYER = 2130
    """:steam-app:`Dark Messiah of Might & Magic Multi-Player <2130>`"""
    THE_SHIP = 2400
    """:steam-app:`The Ship <2400>`"""
    BLOODY_GOOD_TIME = 2450
    """:steam-app:`Bloody Good Time <2450>`"""
    GARRYS_MOD = 4000
    """:steam-app:`Garry's Mod <4000>`"""
    CALL_OF_DUTY_4_MODERN_WARFARE = 7940
    """:steam-app:`Call of Duty 4: Modern Warfare <7940>`"""
    GROUND_BRANCH = 16900
    """:steam-app:`GROUND BRANCH <16900>`"""
    ZOMBIE_PANIC_SOURCE = 17500
    """:steam-app:`Zombie Panic! Source <17500>`"""
    ZOMBIE_PANIC_SOURCE_DEDICATED_SERVER = 17505
    """:steam-app:`Zombie Panic! Source Dedicated Server <17505>`"""
    AGE_OF_CHIVALRY = 17510
    """:steam-app:`Age of Chivalry <17510>`"""
    SYNERGY = 17520
    """:steam-app:`Synergy <17520>`"""
    DIPRIP_WARM_UP = 17530
    """:steam-app:`D.I.P.R.I.P. Warm Up <17530>`"""
    ETERNAL_SILENCE = 17550
    """:steam-app:`Eternal Silence <17550>`"""
    PIRATES_VIKINGS_AND_KNIGHTS_II = 17570
    """:steam-app:`Pirates, Vikings, & Knights II <17570>`"""
    DYSTOPIA = 17580
    """:steam-app:`Dystopia <17580>`"""
    INSURGENCY_MODERN_INFANTRY_COMBAT = 17700
    """:steam-app:`Insurgency: Modern Infantry Combat <17700>`"""
    NUCLEAR_DAWN = 17710
    """:steam-app:`Nuclear Dawn <17710>`"""
    SMASHBALL = 17730
    """:steam-app:`Smashball <17730>`"""
    EMPIRES = 17740
    """:steam-app:`Empires <17740>`"""
    TOM_CLANCY_S_ENDWAR = 21800
    """:steam-app:`Tom Clancy's EndWar <21800>`"""
    BOOSTER_TROOPER = 27920
    """:steam-app:`Booster Trooper <27920>`"""
    RISING_STORM_RED_ORCHESTRA_2_MULTIPLAYER = 35450
    """:steam-app:`Rising Storm/Red Orchestra 2 Multiplayer <35450>`"""
    HOMEFRONT = 55100
    """:steam-app:`Homefront <55100>`"""
    SNIPER_ELITE_V2 = 63380
    """:steam-app:`Sniper Elite V2 <63380>`"""
    DINO_D_DAY = 70000
    """:steam-app:`Dino D-Day <70000>`"""
    EYE_DIVINE_CYBERMANCY = 91700
    """:steam-app:`E.Y.E: Divine Cybermancy <91700>`"""
    PROJECT_ZOMBOID = 108600
    """:steam-app:`Project Zomboid <108600>`"""
    AMERICAS_ARMY_PROVING_GROUNDS = 203290
    """:steam-app:`America's Army: Proving Grounds <203290>`"""
    PRIMAL_CARNAGE = 215470
    """:steam-app:`Primal Carnage <215470>`"""
    CHIVALRY_MEDIEVAL_WARFARE = 219640
    """:steam-app:`Chivalry: Medieval Warfare <219640>`"""
    DAYZ = 221100
    """:steam-app:`DayZ <221100>`"""
    LEFT_4_DEAD_2_DEDICATED_SERVER = 222860
    """:steam-app:`Left 4 Dead 2 Dedicated Server <222860>`"""
    INSURGENCY = 222880
    """:steam-app:`Insurgency <222880>`"""
    NO_MORE_ROOM_IN_HELL = 224260
    """:steam-app:`No More Room in Hell <224260>`"""
    BLADE_SYMPHONY = 225600
    """:steam-app:`Blade Symphony <225600>`"""
    SVEN_CO_OP = 225840
    """:steam-app:`Sven Co-op <225840>`"""
    WRECKFEST = 228380
    """:steam-app:`Wreckfest <228380>`"""
    KILLING_FLOOR_2 = 232090
    """:steam-app:`Killing Floor 2 <232090>`"""
    SNIPER_ELITE_3 = 238090
    """:steam-app:`Sniper Elite 3 <238090>`"""
    CONTAGION = 238430
    """:steam-app:`Contagion <238430>`"""
    SOURCE_SDK_BASE_2013_MULTIPLAYER = 243750
    """:steam-app:`Source SDK Base 2013 Multiplayer <243750>`"""
    NEOTOKYO = 244630
    """:steam-app:`NEOTOKYO° <244630>`"""
    SPACE_ENGINEERS = 244850
    """:steam-app:`Space Engineers <244850>`"""
    STRIKE_VECTOR = 246700
    """:steam-app:`Strike Vector <246700>`"""
    NETHER = 247730
    """:steam-app:`Nether <247730>`"""
    SEVEN_DAYS_TO_DIE = 251570
    """:steam-app:`7 Days to Die <251570>`"""
    RUST = 252490
    """:steam-app:`Rust <252490>`"""
    FORTRESS_FOREVER = 253530
    """:steam-app:`Fortress Forever <253530>`"""
    BLOCKSTORM = 263060
    """:steam-app:`Blockstorm <263060>`"""
    FISTFUL_OF_FRAGS = 265630
    """:steam-app:`Fistful of Frags <265630>`"""
    DEPTH = 274940
    """:steam-app:`Depth <274940>`"""
    ROAD_REDEMPTION = 300380
    """:steam-app:`Road Redemption <300380>`"""
    UNTURNED = 304930
    """:steam-app:`Unturned <304930>`"""
    DOUBLE_ACTION_BOOGALOO = 317360
    """:steam-app:`Double Action: Boogaloo <317360>`"""
    PRIMAL_CARNAGE_EXTINCTION = 321360
    """:steam-app:`Primal Carnage: Extinction <321360>`"""
    SUPRABALL = 321400
    """:steam-app:`Supraball <321400>`"""
    DONT_STARVE_TOGETHER = 322330
    """:steam-app:`Don't Starve Together <322330>`"""
    RISING_WORLD = 324080
    """:steam-app:`Rising World <324080>`"""
    TOKXIKK = 324810
    """:steam-app:`TOXIKK <324810>`"""
    GRAV = 332500
    """:steam-app:`GRAV <332500>`"""
    MEDIEVAL_ENGINEERS = 333950
    """:steam-app:`Medieval Engineers <333950>`"""
    REIGN_OF_KINGS = 344760
    """:steam-app:`Reign Of Kings <344760>`"""
    ARK_SURVIVAL_EVOLVED = 346110
    """:steam-app:`ARK: Survival Evolved <346110>`"""
    BRAINBREAD_2 = 346330
    """:steam-app:`BrainBread 2 <346330>`"""
    MODULAR_COMBAT = 349480
    """:steam-app:`Modular Combat <349480>`"""
    HANAKO_HONOR_AND_BLADE_EARLY_ACCESS = 349510
    """:steam-app:`Hanako: Honor & Blade Early Access <349510>`"""
    CODENAME_CURE = 355180
    """:steam-app:`Codename CURE <355180>`"""
    DIESEL_GUNS = 355400
    """:steam-app:`Diesel Guns <355400>`"""
    THE_MEAN_GREENS_PLASTIC_WARFARE = 360940
    """:steam-app:`The Mean Greens - Plastic Warfare <360940>`"""
    BLACK_MESA = 362890
    """:steam-app:`Black Mesa <362890>`"""
    RFACTOR_2 = 365960
    """:steam-app:`rFactor 2 <365960>`"""
    ANGELS_FALL_FIRST = 367270
    """:steam-app:`Angels Fall First <367270>`"""
    THE_ISLE = 376210
    """:steam-app:`The Isle <376210>`"""
    PRIMAL_CARNAGE_EXTINCTION_OPEN_TESTING = 392990
    """:steam-app:`Primal Carnage Extinction Open Testing <392990>`"""
    SQUAD = 393380
    """:steam-app:`Squad <393380>`"""
    TOWER_UNITE = 394690
    """:steam-app:`Tower Unite <394690>`"""
    OUT_OF_REACH_DEDICATED_SERVER = 406800
    """:steam-app:`Out of Reach Dedicated Server <406800>`"""
    ARK_SURVIVAL_OF_THE_FITTEST = 407530
    """:steam-app:`ARK: Survival Of The Fittest <407530>`"""
    BATTLECREW_SPACE_PIRATES = 411480
    """:steam-app:`BATTLECREW Space Pirates <411480>`"""
    THE_BLACK_DEATH = 412450
    """:steam-app:`The Black Death <412450>`"""
    SUBSISTENCE = 418030
    """:steam-app:`Subsistence <418030>`"""
    RISING_STORM_2_VIETNAM = 418460
    """:steam-app:`Rising Storm 2: Vietnam <418460>`"""
    BLACKWAKE = 420290
    """:steam-app:`Blackwake <420290>`"""
    INTO_ARCADE = 422880
    """:steam-app:`Into Arcade <422880>`"""
    AUTOMOBILISTA = 431600
    """:steam-app:`Automobilista <431600>`"""
    SQUIDS_FROM_SPACE = 437610
    """:steam-app:`SQUIDS FROM SPACE <437610>`"""
    MIDAIR = 439370
    """:steam-app:`Midair <439370>`"""
    CONAN_EXILES = 440900
    """:steam-app:`Conan Exiles <440900>`"""
    FARMING_SIMULATOR_17 = 447020
    """:steam-app:`Farming Simulator 17 <447020>`"""
    FARMING_SIMULATOR_19 = 447020
    """:steam-app:`Farming Simulator 19 <447020>`"""
    DAY_OF_INFAMY = 447820
    """:steam-app:`Day of Infamy <447820>`"""
    DAYS_OF_WAR = 454350
    """:steam-app:`Days of War <454350>`"""
    ZERO_G_ARENA = 467820
    """:steam-app:`Zero G Arena <467820>`"""
    STRIKE_VECTOR_EX = 476360
    """:steam-app:`Strike Vector EX <476360>`"""
    CITADEL_FORGED_WITH_FIRE = 487120
    """:steam-app:`Citadel: Forged With Fire <487120>`"""
    BATTALION_1944 = 489940
    """:steam-app:`BATTALION 1944 <489940>`"""
    DARK_AND_LIGHT = 529180
    """:steam-app:`Dark and Light <529180>`"""
    STATIONEERS = 544550
    """:steam-app:`Stationeers <544550>`"""
    WITCH_IT = 559650
    """:steam-app:`Witch It <559650>`"""
    ALIEN_SWARM_REACTIVE_DROP = 563560
    """:steam-app:`Alien Swarm: Reactive Drop <563560>`"""
    INSURGENCY_SANDSTORM = 581320
    """:steam-app:`Insurgency: Sandstorm <581320>`"""
    CASPA = 588120
    """:steam-app:`Capsa <588120>`"""
    PIXARK = 593600
    """:steam-app:`PixARK <593600>`"""
    JUST_US = 612660
    """:steam-app:`Just Us <612660>`"""
    KREEDZ_CLIMBING = 626680
    """:steam-app:`Kreedz Climbing <626680>`"""
    MORDHAU = 629760
    """:steam-app:`MORDHAU <629760>`"""
    BASE_DEFENSE = 632730
    """:steam-app:`Base Defense <632730>`"""
    AIRMEN = 647740
    """:steam-app:`Airmen <647740>`"""
    HEAT = 656240
    """:steam-app:`Heat <656240>`"""
    URBAN_TERROR = 659280
    """:steam-app:`Urban Terror <659280>`"""
    THE_WARHORN = 660920
    """:steam-app:`The Warhorn <660920>`"""
    JETBALL = 666590
    """:steam-app:`Jetball <666590>`"""
    DAYS_OF_WAR_DEMO = 669980
    IOSOCCER = 673560
    """:steam-app:`IOSoccer <673560>`"""
    WORLD_WAR_3 = 674020
    """:steam-app:`World War 3 <674020>`"""
    PANTROPY = 677180
    """:steam-app:`Pantropy <677180>`"""
    OUTPOST_ZERO = 677480
    """:steam-app:`Outpost Zero <677480>`"""
    HELL_LET_LOOSE = 686810
    """:steam-app:`Hell Let Loose <686810>`"""
    TACTICAL_OPERATIONS = 690980
    """:steam-app:`Tactical Operations <690980>`"""
    PROTOBALL = 703970
    """:steam-app:`Protoball <703970>`"""
    WILL_TO_LIVE_ONLINE = 707010
    """:steam-app:`Will To Live Online <707010>`"""
    FROZEN_FLAME = 715400
    """:steam-app:`Frozen Flame <715400>`"""
    BEASTS_OF_BERMUDA = 719890
    """:steam-app:`Beasts of Bermuda <719890>`"""
    POST_SCRIPTUM = 736220
    """:steam-app:`Post Scriptum <736220>`"""
    SPOXEL = 746880
    """:steam-app:`Spoxel <746880>`"""
    VILLAGES = 749820
    """:steam-app:`Villages <749820>`"""
    EGRESS = 750800
    """:steam-app:`Egress <750800>`"""
    IL_2_STURMOVIK_CLIFFS_OF_DOVER_BLITZ = 754530
    """:steam-app:`IL-2 Sturmovik: Cliffs of Dover Blitz <754530>`"""
    FEAR_THE_NIGHT = 764920
    """:steam-app:`Fear the Night <764920>`"""
    DARCO_REIGN_OF_ELEMENTS = 789960
    """:steam-app:`DARCO - Reign of Elements <789960>`"""
    SUNBURNT = 792320
    """:steam-app:`Sunburnt <792320>`"""
    IDENTITY = 792990
    """:steam-app:`Identity <792990>`"""
    WARFARE_1944 = 793560
    """:steam-app:`Warfare 1944 <793560>`"""
    HELLS_NEW_WORLD = 823350
    """:steam-app:`HELL'S NEW WORLD <823350>`"""
    SWORDS_OF_GURRAH = 833090
    """:steam-app:`Swords of Gurrah <833090>`"""
    ATLAS = 834910
    """:steam-app:`ATLAS <834910>`"""
    OUTLAWS_OF_THE_OLD_WEST = 840800
    """:steam-app:`Outlaws of the Old West <840800>`"""
    JABRONI_BRAWL_EPISODE_3 = 869480
    """:steam-app:`Jabroni Brawl: Episode 3 <869480>`"""
    BATTLERUSH_2 = 871990
    """:steam-app:`BattleRush 2 <871990>`"""
    STICKYBOTS = 889400
    """:steam-app:`StickyBots <889400>`"""
    WORLD_WAR_3_PTE = 892520
    """:steam-app:`World War 3 PTE <892520>`"""
    # noinspection NonAsciiCharacters
    利刃 = 916940
    """:steam-app:`利刃 <916940>`"""
    ROAD_TO_EDEN = 929060
    """:steam-app:`Road to Eden <929060>`"""
    STARCROSS_ARENA = 945870
    """:steam-app:`Starcross Arena <945870>`"""
    BROOMSTICK_LEAGUE = 972780
    """:steam-app:`Broomstick League <972780>`"""
    MEDIEVAL_TOWNS = 982760
    """:steam-app:`Medieval Towns <982760>`"""
    RUINS_SURVIVAL = 985720
    """:steam-app:`RUINS Survival <985720>`"""
    SURVIVAL_FRENZY = 1039870
    """:steam-app:`Survival Frenzy <1039870>`"""
    SPECIAL_FORCE_VR_INFINITY_WAR = 1049130
    """:steam-app:`SPECIAL FORCE VR: INFINITY WAR <1049130>`"""
    BATTLE_GROUNDS_III = 1057700
    """:steam-app:`Battle Grounds III <1057700>`"""
    DAY_OF_DRAGONS = 1088090
    """:steam-app:`Day of Dragons <1088090>`"""
    KARL_BOOM = 1099470
    """:steam-app:`Karl BOOM <1099470>`"""
    SIX_TEMPLES = 1103980
    """:steam-app:`Six Temples <1103980>`"""
    TIP_OF_THE_SPEAR_TASK_FORCE_ELITE = 1148810
    """:steam-app:`Tip of the Spear: Task Force Elite <1148810>`"""
    GALAXY_IN_TURMOIL_DEMO = 1212060
    """:steam-app:`Galaxy in Turmoil Demo <1212060>`"""


#: Pre-:valve-wiki:`orange box <Orange_Box>` games that use the updated Source Engine response protocol format for
# ``A2S_INFO`` queries
GOLDSOURCE_APPS_USE_NEW_INFO = frozenset({
    AppID.SIN_MULTIPLAYER,
    AppID.RAG_DOLL_KUNG_FU,
})
#: :valve-wiki:`App IDs <Steam_Application_IDs>` which are known not to contain a packet cut-off size field in
# multi-packeted responses
APPS_NO_PACKET_SIZE_FIELD = frozenset({
    AppID.SOURCE_SDK_BASE_2006,
    # FIXME: 240 when protocol = 7? AppID.COUNTER_STRIKE_SOURCE,
    AppID.ETERNAL_SILENCE,
    AppID.INSURGENCY_MODERN_INFANTRY_COMBAT,
})
