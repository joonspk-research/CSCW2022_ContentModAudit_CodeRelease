"""
Original author: Joon Sung Park, Stanford University 
Last updated: December 15, 2020
"""
# The list of subreddits included in our data collection. 
ALL_ACTIVE_SUBREDDITS = ["relationships", "personalfinance", "MMA", "nfl", "worldnews",
                         "atheism", "syriancivilwar", "pokemongo", "AskReddit", "science",
                         "jailbreak", "explainlikeimfive", "politics", "ShitRedditSays", "funny",
                         "fantasyfootball", "hearthstone", "hillaryclinton", "videos", "europe",

                         "dataisbeautiful", "Futurology", "books", "news", "nba", 
                         "leagueoflegends", "Games", "askscience", "photoshopbattles", "nosleep",
                         "legaladvice", "NeutralPolitics", "pokemon", "depression", "technology",
                         "DIY", "PoliticalDiscussion", "CFB", "socialism", "pokemontrades",
                        
                         "gonewild", "SubredditDrama", "hiphopheads", "AskHistorians", "gifs",
                         "TwoXChromosomes", "canada", "nottheonion", "Android", "aww",
                         "sex", "asoiaf", "tifu", "GetMotivated", "AskTrumpSupporters",
                         "GlobalOffensive", "LateStageCapitalism", "television", "movies", "PurplePillDebate",
                        
                         "SuicideWatch", "churning", "Showerthoughts", "me_irl", "philosophy",
                         "pics", "EnoughTrumpSpam", "gaming", "LifeProTips", "food",
                         "history", "DestinyTheGame", "creepyPMs", "india", "anime",
                         "pcmasterrace", "IAmA", "CanadaPolitics", "UpliftingNews", "Christianity",
                        
                         "changemyview", "wow", "GlobalOffensiveTrade", "BlackPeopleTwitter", "NSFW_GIF",
                         "AskWomen", "whatisthisthing", "conspiracy", "TheSilphRoad", "space",
                         "2007scape", "OldSchoolCool", "Overwatch", "OutOfTheLoop", "spacex",
                         "SandersForPresident", "gameofthrones"]


# Three-part separation of ALL_ACTIVE_SUBREDDITS
SECTION_1 = ["relationships", "personalfinance", "MMA", "nfl", "worldnews",
             "atheism", "syriancivilwar", "pokemongo", "AskReddit", "science",
             "jailbreak", "explainlikeimfive", "politics", "ShitRedditSays", "funny",
             "fantasyfootball", "hearthstone", "hillaryclinton", "videos", "europe",
             "dataisbeautiful", "Futurology", "books", "news", "nba", 
             "leagueoflegends", "Games", "askscience", "photoshopbattles", "nosleep",
             "SandersForPresident", "gameofthrones"]


SECTION_2 = ["legaladvice", "NeutralPolitics", "pokemon", "depression", "technology",
             "DIY", "PoliticalDiscussion", "CFB", "socialism", "pokemontrades",
             "gonewild", "SubredditDrama", "hiphopheads", "AskHistorians", "gifs",
             "TwoXChromosomes", "canada", "nottheonion", "Android", "aww",
             "sex", "asoiaf", "tifu", "GetMotivated", "AskTrumpSupporters",
             "GlobalOffensive", "LateStageCapitalism", "television", "movies", "PurplePillDebate",
             "OutOfTheLoop", "spacex",]


SECTION_3 = ["SuicideWatch", "churning", "Showerthoughts", "me_irl", "philosophy",
             "pics", "EnoughTrumpSpam", "gaming", "LifeProTips", "food",
             "history", "DestinyTheGame", "creepyPMs", "india", "anime",
             "pcmasterrace", "IAmA", "CanadaPolitics", "UpliftingNews", "Christianity",
             "changemyview", "wow", "GlobalOffensiveTrade", "BlackPeopleTwitter", "NSFW_GIF",
             "AskWomen", "whatisthisthing", "conspiracy", "TheSilphRoad", "space",
             "2007scape", "OldSchoolCool", "Overwatch",]
