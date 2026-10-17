from typing import List, Dict, Any, Optional

WELFARE_SCHEMES: List[Dict[str, Any]] = [
    {
        "id": "eshram",
        "name": "e-Shram Portal (National Database of Unorganised Workers)",
        "name_hi": "ई-श्रम पोर्टल (असंगठित कर्मकार राष्ट्रीय डेटाबेस)",
        "authority": "Ministry of Labour and Employment, Government of India",
        "category_eligibility": ["Food Delivery", "Cab/Ride-hailing", "Parcel Delivery", "Construction/Daily Wage", "Domestic Workers", "Other"],
        "location": "All India",
        "benefits": "Universal Account Number (UAN) card, accidental death/disability insurance up to ₹2,00,000 under PMSBY integration, social security benefits portability across states, disaster assistance eligibility.",
        "benefits_hi": "यूएएन (UAN) कार्ड, दुर्घटना में मृत्यु या स्थायी विकलांगता पर ₹2 लाख तक का बीमा कवर, राज्यों के बीच सामाजिक सुरक्षा लाभों की सुवाह्यता।",
        "eligibility_criteria": "Age 16-59 years, not an EPFO/ESIC member, not an income tax payer, engaged in informal or gig/platform work.",
        "documents_required": ["Aadhaar Number", "Aadhaar-linked Mobile Number", "Active Bank Account details (IFSC, Account Number)"],
        "application_process": "Self-registration online via official portal (eshram.gov.in) using Aadhaar OTP or via nearest Common Services Centre (CSC).",
        "official_url": "https://eshram.gov.in",
        "contact_helpline": "14434 (Toll-Free National Labour Helpline)",
        "source": "Official Portal of Ministry of Labour and Employment (eshram.gov.in)",
        "last_verified": "2024-12-01"
    },
    {
        "id": "pmsym",
        "name": "Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM Pension Scheme)",
        "name_hi": "प्रधानमंत्री श्रम योगी मान-धन (PM-SYM पेंशन योजना)",
        "authority": "Ministry of Labour and Employment & LIC of India",
        "category_eligibility": ["Food Delivery", "Cab/Ride-hailing", "Parcel Delivery", "Construction/Daily Wage", "Other"],
        "location": "All India",
        "benefits": "Guaranteed minimum monthly pension of ₹3,000 after attaining the age of 60 years. 50% matching monthly contribution by Central Government.",
        "benefits_hi": "60 वर्ष की आयु के बाद ₹3,000 प्रति माह की निश्चित पेंशन। 50% अंशदान केंद्र सरकार द्वारा वहन किया जाता है।",
        "eligibility_criteria": "Age 18-40 years, monthly income ₹15,000 or less, unorganised worker, not covered under EPFO, ESIC, or NPS.",
        "documents_required": ["Aadhaar Card", "Savings/Jan Dhan Bank Account details", "Mobile Number"],
        "application_process": "Enroll at any Common Services Centre (CSC) or online on the Maandhan portal. Monthly contribution (₹55 - ₹200 based on age) auto-debited.",
        "official_url": "https://maandhan.in",
        "contact_helpline": "1800-267-6888 (Toll Free)",
        "source": "Official Ministry of Labour & Employment Portal (maandhan.in)",
        "last_verified": "2024-11-15"
    },
    {
        "id": "pmjay",
        "name": "Ayushman Bharat PM-JAY (Pradhan Mantri Jan Arogya Yojana)",
        "name_hi": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना (PM-JAY)",
        "authority": "National Health Authority (NHA), Government of India",
        "category_eligibility": ["Construction/Daily Wage", "Food Delivery", "Cab/Ride-hailing", "Parcel Delivery", "Other"],
        "location": "All India (Participating States)",
        "benefits": "Cashless secondary and tertiary healthcare hospitalisation coverage up to ₹5,00,000 per family per year at empannelled public and private hospitals.",
        "benefits_hi": "संबद्ध सरकारी और निजी अस्पतालों में प्रति परिवार प्रति वर्ष ₹5,00,000 तक का कैशलेस इलाज।",
        "eligibility_criteria": "Deprivation criteria based on SECC 2011 or identified informal worker welfare board roll-ins depending on state.",
        "documents_required": ["Aadhaar Card", "Ration Card / Family ID", "Mobile Number"],
        "application_process": "Check eligibility online at beneficiary.nha.gov.in or visit any Ayushman Mitra desk at an empanelled hospital/CSC to generate Ayushman Card.",
        "official_url": "https://beneficiary.nha.gov.in",
        "contact_helpline": "14555",
        "source": "National Health Authority (nha.gov.in)",
        "last_verified": "2024-12-10"
    },
    {
        "id": "pmsvanidhi",
        "name": "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
        "name_hi": "पीएम स्ट्रीट वेंडर्स आत्मनिर्भर निधि (पीएम स्वनिधि)",
        "authority": "Ministry of Housing and Urban Affairs (MoHUA)",
        "category_eligibility": ["Daily-wage & Street Vendors", "Construction/Daily Wage", "Other"],
        "location": "All India (Urban Areas)",
        "benefits": "Collateral-free working capital micro-loans: 1st tranche up to ₹10,000 (repayable in 1 year), 2nd tranche up to ₹20,000, 3rd tranche up to ₹50,000 with 7% interest subsidy on timely repayment and digital transaction cashback.",
        "benefits_hi": "बिना किसी गारंटी के कार्यशील पूंजी ऋण: पहली किश्त ₹10,000 तक, दूसरी किश्त ₹20,000 और तीसरी किश्त ₹50,000 तक, समय पर चुकाने पर 7% ब्याज सब्सिडी।",
        "eligibility_criteria": "Vendors and informal service providers engaged in urban areas prior to guidelines or holding Certificate of Vending/ID card.",
        "documents_required": ["Aadhaar Card", "Voter Card", "Bank Passbook", "Proof of Vending / Letter of Recommendation from ULB"],
        "application_process": "Apply online at pmsvanidhi.mohua.gov.in or through Urban Local Body (ULB) / Banking Correspondents.",
        "official_url": "https://pmsvanidhi.mohua.gov.in",
        "contact_helpline": "1800-11-1979",
        "source": "Ministry of Housing and Urban Affairs (pmsvanidhi.mohua.gov.in)",
        "last_verified": "2024-10-30"
    },
    {
        "id": "rajasthan_gig_act",
        "name": "Rajasthan Platform Based Gig Workers Welfare Board",
        "name_hi": "राजस्थान प्लेटफॉर्म आधारित गिग कर्मकार कल्याण बोर्ड",
        "authority": "Department of Labour, Government of Rajasthan",
        "category_eligibility": ["Food Delivery", "Cab/Ride-hailing", "Parcel Delivery"],
        "location": "Rajasthan",
        "benefits": "Registration with unique Gig Worker ID, access to state Social Security and Welfare Fund funded by fee on aggregator transactions, grievance redressal officers, and accidental/health safety nets.",
        "benefits_hi": "विशिष्ट गिग वर्कर आईडी, लेन-देन शुल्क से पोषित राज्य सामाजिक सुरक्षा कल्याण कोष, शिकायत निवारण और स्वास्थ्य/दुर्घटना सहायता।",
        "eligibility_criteria": "Platform-based delivery partners or cab/auto drivers registered and operating in Rajasthan.",
        "documents_required": ["Aggregator App Driver/Partner ID", "Aadhaar Card", "Bank Account in Rajasthan"],
        "application_process": "Aggregators mandatorily submit partner lists to Rajasthan Welfare Board; workers register or verify on state labour portal.",
        "official_url": "https://labour.rajasthan.gov.in",
        "contact_helpline": "0141-2450700",
        "source": "Rajasthan Platform Based Gig Workers (Registration and Welfare) Act, 2023",
        "last_verified": "2024-09-20"
    },
    {
        "id": "karnataka_gig_act",
        "name": "Karnataka Platform-Based Gig Workers Social Security & Welfare",
        "name_hi": "कर्नाटक प्लेटफॉर्म-आधारित गिग श्रमिक सामाजिक सुरक्षा बोर्ड",
        "authority": "Department of Labour, Government of Karnataka",
        "category_eligibility": ["Food Delivery", "Cab/Ride-hailing", "Parcel Delivery"],
        "location": "Karnataka",
        "benefits": "Welfare fee cess on aggregator transactions to fund social security, occupational health and safety standards, minimum 14-day notice before platform account deactivation, dispute resolution mechanism.",
        "benefits_hi": "खाता निलंबित करने से पहले अनिवार्य 14 दिनों की पूर्व सूचना, कल्याण निधि से सामाजिक सुरक्षा लाभ और विवाद निवारण तंत्र।",
        "eligibility_criteria": "Gig and platform workers in ride hailing, food/grocery delivery, or logistics within Karnataka.",
        "documents_required": ["Platform Partner ID", "Aadhaar Card", "Bank Account"],
        "application_process": "Through Karnataka Labour Department portal / Aggregator registered database.",
        "official_url": "https://labour.karnataka.gov.in",
        "contact_helpline": "155214",
        "source": "Karnataka Platform-Based Gig Workers (Social Security and Welfare) Bill & Board Initiatives",
        "last_verified": "2024-11-01"
    },
    {
        "id": "bocw",
        "name": "Building and Other Construction Workers (BOCW) Welfare Board",
        "name_hi": "भवन एवं अन्य सन्निर्माण कर्मकार (BOCW) कल्याण बोर्ड",
        "authority": "State Labour Departments / Ministry of Labour and Employment",
        "category_eligibility": ["Construction/Daily Wage"],
        "location": "All India (State-administered)",
        "benefits": "Financial assistance for children's education, maternity benefits (₹10,000 - ₹25,000 depending on state), death compensation, house construction assistance, tool kit purchase allowance, and daughter marriage aid.",
        "benefits_hi": "बच्चों की पढ़ाई हेतु छात्रवृत्ति, प्रसूति सहायता, दुर्घटना मुआवजा, औजार खरीदने हेतु सहायता और आवास सहायता।",
        "eligibility_criteria": "Age 18-60 years, engaged in construction or masonry work for at least 90 days in the preceding 12 months.",
        "documents_required": ["90-day Work Certificate from employer/trade union", "Aadhaar Card", "Bank Passbook", "Passport-size photos"],
        "application_process": "Apply through respective State BOCW Board portal (e.g. upbocw.in, bocw.delhi.gov.in) or district labour welfare office.",
        "official_url": "https://labour.gov.in/bocw",
        "contact_helpline": "Contact District Labour Office",
        "source": "Building and Other Construction Workers Welfare Act, 1996",
        "last_verified": "2024-11-20"
    }
]

def search_welfare_schemes(category: Optional[str] = None, location: Optional[str] = None, query: Optional[str] = None) -> List[Dict[str, Any]]:
    results = []
    for s in WELFARE_SCHEMES:
        # Category check
        if category and category != "All":
            if category not in s["category_eligibility"] and "Other" not in s["category_eligibility"]:
                continue
        # Location check
        if location and location != "All India" and location != "All":
            if s["location"] != "All India" and s["location"].lower() != location.lower():
                continue
        # Text query check
        if query:
            q = query.lower()
            text_haystack = f"{s['name']} {s['name_hi']} {s['authority']} {s['benefits']} {s['eligibility_criteria']}".lower()
            if q not in text_haystack:
                continue
        results.append(s)
    return results

def get_scheme_by_id(scheme_id: str) -> Optional[Dict[str, Any]]:
    for s in WELFARE_SCHEMES:
        if s["id"] == scheme_id:
            return s
    return None
