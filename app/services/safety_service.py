from typing import List, Dict, Any, Optional

SAFETY_GUIDES: Dict[str, Dict[str, Any]] = {
    "Food Delivery": {
        "title": "Food & Grocery Delivery Safety",
        "title_hi": "फूड व ग्रॉसरी डिलीवरी सुरक्षा निर्देश",
        "emergency_numbers": [
            {"service": "National Emergency Helpline", "number": "112", "service_hi": "राष्ट्रीय आपातकालीन नंबर"},
            {"service": "Ambulance / Medical", "number": "108 / 102", "service_hi": "एम्बुलेंस / चिकित्सा"},
            {"service": "Women Safety Helpline", "number": "1091", "service_hi": "महिला सुरक्षा हेल्पलाइन"},
            {"service": "Traffic Police", "number": "103 / 1073", "service_hi": "ट्रैफिक पुलिस"}
        ],
        "categories": [
            {
                "topic": "Road & Traffic Safety",
                "topic_hi": "सड़क और यातायात सुरक्षा",
                "checkpoints": [
                    "Always wear an ISI-marked full-face helmet with chin strap securely fastened.",
                    "Never operate phone mounts while moving; pull over safely to check navigation maps.",
                    "Keep bike headlights, taillights, and indicators clean and functional at all times.",
                    "Maintain safe braking distance in rain or heavy urban traffic; avoid sudden overtaking on left."
                ],
                "checkpoints_hi": [
                    "हमेशा ISI मार्क वाला हेलमेट पहनें और स्ट्रैप अच्छी तरह बांधें।",
                    "चलती बाइक पर फोन न देखें; मैप या कॉल देखने के लिए बाइक को सुरक्षित किनारे रोकें।",
                    "हेडलाइट, टेललाइट और इंडिकेटर ठीक रखें, खासकर रात में।",
                    "बारिश में सुरक्षित दूरी बनाए रखें और कभी भी बाईं तरफ से तेज गति में ओवरटेक न करें।"
                ]
            },
            {
                "topic": "Fatigue & Hydration Protocol",
                "topic_hi": "थकान, आराम और जलपान नियम",
                "checkpoints": [
                    "Take a mandatory 10-minute rest after every 2.5 hours of continuous riding.",
                    "Carry a refillable water bottle; hydrate frequently to prevent heat exhaustion.",
                    "If experiencing blurred vision or micro-sleep sensations, log off immediately and rest in a shaded area."
                ],
                "checkpoints_hi": [
                    "हर 2.5 घंटे लगातार ड्राइविंग के बाद 10 मिनट का ब्रेक लें।",
                    "पानी की बोतल साथ रखें; लू और डिहाइड्रेशन से बचने के लिए समय-समय पर पानी पिएं।",
                    "यदि चक्कर आए या आंखें भारी हों, तो तुरंत ऐप से ब्रेक लें और छायादार जगह पर आराम करें।"
                ]
            },
            {
                "topic": "Handling Aggressive Customers or Unsafe Locations",
                "topic_hi": "उग्र ग्राहकों या असुरक्षित स्थानों से निपटना",
                "checkpoints": [
                    "Stay in well-lit, public corridors when delivering to unfamiliar apartments or secluded lanes.",
                    "If a customer becomes verbally abusive, do not engage in argument. Maintain calm tone and step back.",
                    "Do not enter inside customer homes; hand deliveries over at the main door threshold.",
                    "If physically threatened, immediately withdraw to a public location and trigger the in-app SOS and dial 112."
                ],
                "checkpoints_hi": [
                    "अनजान गलियों या फ्लैट में डिलीवरी करते समय हमेशा रोशनी वाली जगह पर खड़े रहें।",
                    "यदि ग्राहक बहस या दुर्व्यवहार करे, तो बहस न करें, शांत रहें और एक कदम पीछे हटें।",
                    "ग्राहक के घर के अंदर न जाएं; दरवाजे की चौखट पर ही पार्सल सौंपें।",
                    "यदि जान या शरीर पर खतरा लगे, तो तुरंत भीड़-भाड़ वाली जगह पर जाएं और 112 पर कॉल करें।"
                ]
            },
            {
                "topic": "Accident & Incident Response",
                "topic_hi": "दुर्घटना के समय तुरंत उठाए जाने वाले कदम",
                "checkpoints": [
                    "First check yourself and others for injuries. Call 108 / 112 immediately for medical aid.",
                    "Turn on hazard lights or place vehicle safely off the driving carriageway if possible.",
                    "Take photos of vehicle registration plates and the scene without creating a altercation.",
                    "Notify platform rider support via the emergency button to log accident insurance coverage."
                ],
                "checkpoints_hi": [
                    "सबसे पहले देखें कि किसी को गंभीर चोट तो नहीं आई। तुरंत 108/112 पर एम्बुलेंस बुलाएं।",
                    "यदि संभव हो तो गाड़ी को सड़क के किनारे सुरक्षित स्थान पर लगाएं।",
                    "बिना विवाद किए दुर्घटना स्थल और संबंधित गाड़ियों की तस्वीरें लें।",
                    "कंपनी की हेल्पलाइन या ऐप के इमरजेंसी बटन से दुर्घटना की सूचना दें ताकि इंश्योरेंस क्लेम हो सके।"
                ]
            }
        ]
    },
    "Cab/Ride-hailing": {
        "title": "Cab & Auto Driver Safety Protocol",
        "title_hi": "कैब व ऑटो चालक सुरक्षा नियम",
        "emergency_numbers": [
            {"service": "National Emergency Helpline", "number": "112", "service_hi": "राष्ट्रीय आपातकालीन नंबर"},
            {"service": "Highway Police Helpline", "number": "1033", "service_hi": "हाईवे हेल्पलाइन"},
            {"service": "Ambulance", "number": "108", "service_hi": "एम्बुलेंस"}
        ],
        "categories": [
            {
                "topic": "Pre-Trip Inspection & Night Driving",
                "topic_hi": "सवारी से पहले जांच और रात्रि सुरक्षा",
                "checkpoints": [
                    "Check tyre pressure, brake fluid, working dashboard dashcam, and central door lock functioning.",
                    "During late night trips, share live trip location with a trusted family member or peer driver group.",
                    "Avoid picking up unverified offline passengers hailing from dark highway junctions."
                ],
                "checkpoints_hi": [
                    "टायर प्रेशर, ब्रेक, डैशकैम और दरवाजों के लॉक की जांच कर लें।",
                    "रात के समय लंबी यात्रा में अपने परिवार या साथी ड्राइवरों के ग्रुप में लाइव लोकेशन शेयर करें।",
                    "हाईवे पर सुनसान जगह से अनजान अनाम यात्रियों को ऑफलाइन बैठाने से बचें।"
                ]
            },
            {
                "topic": "In-Cab Conflict Resolution",
                "topic_hi": "गाड़ी में विवाद की स्थिति में क्या करें",
                "checkpoints": [
                    "Keep cabin voice calm. If riders dispute fares, direct them to the app receipts rather than arguing.",
                    "If passengers become unruly or intoxicated, pull over in front of an active police outpost or petrol station.",
                    "Use the vehicle horn to alert surrounding public if passenger attempts physical coercion."
                ],
                "checkpoints_hi": [
                    "हमेशा आवाज शांत रखें। किराए को लेकर बहस होने पर उन्हें ऐप की रसीद दिखाएं।",
                    "यदि सवारी अभद्र व्यवहार करे या नशे में हो, तो गाड़ी को तुरंत किसी पेट्रोल पंप या पुलिस चौकी पर रोकें।",
                    "यदि कोई जबरदस्ती करे, तो हॉर्न बजाकर आसपास के लोगों का ध्यान आकर्षित करें।"
                ]
            }
        ]
    },
    "Construction/Daily Wage": {
        "title": "Construction & Daily-Wage Workplace Safety",
        "title_hi": "निर्माण व दिहाड़ी श्रमिक कार्यस्थल सुरक्षा",
        "emergency_numbers": [
            {"service": "National Emergency", "number": "112", "service_hi": "राष्ट्रीय आपातकाल"},
            {"service": "Ambulance", "number": "108", "service_hi": "एम्बुलेंस"},
            {"service": "Labour Helpline", "number": "14434", "service_hi": "श्रम हेल्पलाइन"}
        ],
        "categories": [
            {
                "topic": "PPE & Hazard Prevention",
                "topic_hi": "सुरक्षा उपकरण और खतरे से बचाव",
                "checkpoints": [
                    "Always wear a hard hat (helmet) and steel-toe or durable non-slip safety shoes on active sites.",
                    "Wear a safety harness when working at heights exceeding 2 metres (6 feet).",
                    "Ensure scaffolding and bamboo scaffolding have sound anchor points before ascending."
                ],
                "checkpoints_hi": [
                    "साइट पर हमेशा सुरक्षा हेलमेट और मजबूत जूते पहनें।",
                    "2 मीटर (6 फीट) से अधिक ऊंचाई पर काम करते समय सेफ्टी बेल्ट (हार्नेस) अनिवार्य रूप से बांधें।",
                    "पाड़ (मचान) पर चढ़ने से पहले देख लें कि वह हिल तो नहीं रहा और मजबूत बंधा है।"
                ]
            },
            {
                "topic": "Dust, Chemical, and Electrical Protection",
                "topic_hi": "धूल, बिजली और भारी वजन से सुरक्षा",
                "checkpoints": [
                    "Wear N95 or dust mask when mixing dry cement, sand, or cutting tiles to protect lungs from silicosis.",
                    "Never touch bare electrical wires or run power tools through standing puddles of water.",
                    "Lift heavy cement bags with bent knees and straight back to prevent chronic lumbar spine injury."
                ],
                "checkpoints_hi": [
                    "सीमेंट या रेत मिलाते समय और टाइल काटते समय मास्क पहनें ताकि फेफड़ों को नुकसान न पहुंचे।",
                    "खुले तारों को न छुएं और पानी भरे फर्श पर बिजली के उपकरण न चलाएं।",
                    "भारी बोरी उठाते समय कमर झुकाने के बजाय घुटने मोड़कर वजन उठाएं।"
                ]
            }
        ]
    }
}

def get_safety_guide(category: str) -> Dict[str, Any]:
    return SAFETY_GUIDES.get(category, SAFETY_GUIDES["Food Delivery"])

def get_all_safety_categories() -> List[str]:
    return list(SAFETY_GUIDES.keys())
