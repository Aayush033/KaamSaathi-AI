// Comprehensive Multilingual Translation Dictionary (English, Hindi, Hinglish)
const I18N = {
  en: {
    app_title: "KaamSaathi AI",
    app_tagline: "AI Companion for India's Gig & Informal Workforce",
    nav_assistant: "AI Assistant",
    nav_earnings: "Earnings Tracker",
    nav_safety: "Safety Guidance",
    nav_welfare: "Rights & Schemes",
    nav_documents: "Document Reader",
    nav_grievance: "Dispute & Grievance",
    
    // Assistant Module
    assistant_title: "KaamSaathi AI Assistant",
    assistant_subtitle: "Ask any question about your earnings, safety, rights, or documents in your language.",
    chat_placeholder: "Type your question or tap the microphone...",
    send: "Send",
    listening: "Listening... Speak now",
    
    // Suggested Prompts
    chip_calc_earnings: "Calculate my earnings this week",
    chip_customer_threat: "What should I do if a customer threatens me?",
    chip_welfare_schemes: "Find welfare schemes that may apply to me",
    chip_unpaid_payout: "Draft a complaint about an unpaid payout",
    chip_read_statement: "Help me understand this payment statement",
    
    // Earnings Module
    earnings_title: "Earnings & Income Tracker",
    earnings_subtitle: "Accurate tracking based on actual entries. Net = Gross + Tips/Incentives - Expenses.",
    add_entry: "Add Earning Record",
    explain_earnings_ai: "Explain My Earnings with AI",
    stat_today: "Today's Net",
    stat_week: "Last 7 Days Net",
    stat_month: "This Month Net",
    stat_alltime: "All-Time Net",
    table_date: "Date",
    table_category: "Category",
    table_platform: "Platform",
    table_gross: "Gross",
    table_tips: "Tips/Incentives",
    table_expenses: "Expenses",
    table_net: "Net Take-Home",
    table_actions: "Actions",
    no_records_title: "No earnings recorded yet",
    no_records_desc: "Add your first work day's income and fuel/maintenance expenses to see live calculations and AI breakdowns.",
    dispute_this: "Dispute This",
    edit: "Edit",
    delete: "Delete",
    
    // Safety Module
    safety_title: "Worker Safety & Emergency Guidance",
    safety_subtitle: "Practical on-the-job safety guidelines, fatigue management, and instant emergency helplines.",
    sos_title: "Emergency Helplines (Tap to Call)",
    category_food: "Food & Grocery Delivery",
    category_cab: "Cab & Auto Driver",
    category_daily: "Construction & Daily Wage",
    safety_disclaimer: "Notice: KaamSaathi AI provides safety guidance and does not replace emergency medical or police dispatch.",
    
    // Welfare Module
    welfare_title: "Rights & Welfare Scheme Explorer",
    welfare_subtitle: "Verified Central & State Government social security benefits for informal and gig workers.",
    filter_category: "Filter by Work Type",
    filter_location: "Filter by State / Location",
    search_scheme_placeholder: "Search schemes by name or benefit...",
    view_details: "View Details & Apply",
    ask_ai_scheme: "Explain in Simple Terms",
    
    // Document Module
    doc_title: "Work Document & Contract Assistant",
    doc_subtitle: "Understand payout statements, aggregator agreements, and penalty notices in plain language.",
    upload_tab: "Upload Document (PDF / Text)",
    paste_tab: "Paste Document Text",
    drop_file_here: "Drag & drop your document here, or click to browse",
    paste_placeholder: "Paste contract clauses, payment terms, or notice text here...",
    analyze_btn: "Analyze Document with AI",
    doc_summary: "Document Summary",
    key_amounts: "Key Amounts & Deductions",
    critical_dates: "Important Dates & Timelines",
    missing_info: "Missing Information Checklist",
    questions_to_ask: "Recommended Questions to Ask",
    
    // Grievance Module
    grievance_title: "Grievance & Dispute Drafter",
    grievance_subtitle: "Draft clear, professional, and respectful complaint letters for unpaid wages, unfair penalties, or app suspensions.",
    field_category: "Grievance Category",
    field_employer: "Platform or Employer Name",
    field_date: "Date of Incident / Payout",
    field_amount: "Disputed Amount (₹)",
    field_details: "Describe what happened",
    field_evidence: "Evidence you have (screenshots, receipts)",
    generate_draft_btn: "Generate Professional Draft with AI",
    copy_draft: "Copy to Clipboard",
    download_draft: "Download as Text File",
    supporting_checklist: "Supporting Documents Checklist",
    next_steps: "Recommended Next Steps",
    
    // Settings
    settings_title: "KaamSaathi AI Settings & System Health",
    system_status: "System Status"
  },
  
  hi: {
    app_title: "कामसाथी AI",
    app_tagline: "भारत के गिग और असंगठित कामगारों का भरोसेमंद डिजिटल साथी",
    nav_assistant: "AI साथी",
    nav_earnings: "कमाई और खर्च",
    nav_safety: "सुरक्षा निर्देश",
    nav_welfare: "योजनाएं व अधिकार",
    nav_documents: "दस्तावेज़ समझें",
    nav_grievance: "शिकायत ड्राफ्ट",
    
    // Assistant Module
    assistant_title: "कामसाथी AI सहायक",
    assistant_subtitle: "अपनी कमाई, सुरक्षा, सरकारी योजनाओं या कागज़ातों के बारे में सरल हिंदी में सवाल पूछें।",
    chat_placeholder: "अपना सवाल लिखें या माइक पर बोलें...",
    send: "भेजें",
    listening: "सुन रहे हैं... बोलिए",
    
    // Suggested Prompts
    chip_calc_earnings: "इस हफ्ते की मेरी कुल कमाई और बचत बताएं",
    chip_customer_threat: "यदि कोई ग्राहक धमकी दे या दुर्व्यवहार करे तो क्या करूं?",
    chip_welfare_schemes: "मेरे काम के अनुसार सरकारी योजनाएं खोजें",
    chip_unpaid_payout: "बकाया पेमेंट के लिए शिकायत पत्र तैयार करें",
    chip_read_statement: "इस पेमेंट रसीद को सरल भाषा में समझाएं",
    
    // Earnings Module
    earnings_title: "कमाई एवं खर्च हिसाब",
    earnings_subtitle: "सच्चे रिकॉर्ड पर आधारित सटीक हिसाब। शुद्ध कमाई = कुल कमाई + टिप्स/प्रोत्साहन − कार्य खर्च।",
    add_entry: "नया हिसाब जोड़ें",
    explain_earnings_ai: "AI से अपनी कमाई समझें",
    stat_today: "आज की शुद्ध बचत",
    stat_week: "पिछले 7 दिन की शुद्ध बचत",
    stat_month: "इस महीने की शुद्ध बचत",
    stat_alltime: "कुल कुल बचत",
    table_date: "तारीख",
    table_category: "कार्य श्रेणी",
    table_platform: "कंपनी / प्लेटफॉर्म",
    table_gross: "कुल कमाई",
    table_tips: "टिप्स/इंसेंटिव",
    table_expenses: "पेट्रोल/खर्च",
    table_net: "घर ले जाने वाली कमाई (नेट)",
    table_actions: "विकल्प",
    no_records_title: "अभी तक कोई कमाई दर्ज नहीं है",
    no_records_desc: "सटीक हिसाब और AI विश्लेषण देखने के लिए अपना पहला दिन का हिसाब दर्ज करें।",
    dispute_this: "विवाद दर्ज करें",
    edit: "बदलें",
    delete: "हटाएं",
    
    // Safety Module
    safety_title: "कार्यस्थल व सड़क सुरक्षा निर्देश",
    safety_subtitle: "सड़क सुरक्षा नियम, थकान से बचाव, आपातकालीन हेल्पलाइन और दुर्घटना सहायता।",
    sos_title: "आपातकालीन नंबर (कॉल करने के लिए टैप करें)",
    category_food: "फूड व पार्सल डिलीवरी",
    category_cab: "कैब व ऑटो चालक",
    category_daily: "निर्माण व दिहाड़ी मजदूर",
    safety_disclaimer: "सूचना: कामसाथी AI सुरक्षा सलाह देता है; गंभीर आपातकाल में सीधे 112 या 108 डायल करें।",
    
    // Welfare Module
    welfare_title: "मजदूर अधिकार एवं कल्याणकारी योजनाएं",
    welfare_subtitle: "केंद्र और राज्य सरकार की प्रमाणित सामाजिक सुरक्षा योजनाएं और पेंशन लाभ।",
    filter_category: "कार्य के अनुसार चुनें",
    filter_location: "राज्य के अनुसार चुनें",
    search_scheme_placeholder: "योजना का नाम या लाभ खोजें...",
    view_details: "विवरण और आवेदन लिंक",
    ask_ai_scheme: "AI से सरल भाषा में समझें",
    
    // Document Module
    doc_title: "दस्तावेज़ एवं अनुबंध सहायक",
    doc_subtitle: "पेमेंट स्लिप, कंपनी एग्रीमेंट या नोटिस को सरल भाषा में समझें।",
    upload_tab: "दस्तावेज़ अपलोड करें (PDF/टेक्स्ट)",
    paste_tab: "कागज़ का टेक्स्ट यहां पेस्ट करें",
    drop_file_here: "फाइल यहां खींचकर लाएं या चुनने के लिए क्लिक करें",
    paste_placeholder: "नियम, शर्तें या पेमेंट रसीद का टेक्स्ट यहां पेस्ट करें...",
    analyze_btn: "AI से दस्तावेज़ की जांच करें",
    doc_summary: "दस्तावेज़ का सरल सारांश",
    key_amounts: "मुख्य राशियां व कटौतियां",
    critical_dates: "जरूरी तारीखें व समय सीमा",
    missing_info: "लापता जानकारी की चेकलिस्ट",
    questions_to_ask: "कंपनी से पूछने लायक जरूरी सवाल",
    
    // Grievance Module
    grievance_title: "शिकायत एवं विवाद पत्र तैयार करें",
    grievance_subtitle: "रुके हुए पैसे, गलत कटौती या आईडी सस्पेंड होने पर सम्मानजनक और असरदार शिकायत ड्राफ्ट बनाएं।",
    field_category: "शिकायत का विषय",
    field_employer: "कंपनी या ठेकेदार का नाम",
    field_date: "घटना / पेमेंट की तारीख",
    field_amount: "विवादित राशि (₹)",
    field_details: "विस्तार से बताएं क्या हुआ",
    field_evidence: "आपके पास क्या सबूत हैं (स्क्रीनशॉट, रसीद)",
    generate_draft_btn: "AI से औपचारिक शिकायत पत्र बनाएं",
    copy_draft: "कॉपी करें",
    download_draft: "टेक्स्ट फाइल डाउनलोड करें",
    supporting_checklist: "साथ में लगाने वाले जरूरी सबूत",
    next_steps: "आगे उठाए जाने वाले कदम",
    
    // Settings
    settings_title: "कामसाथी AI सेटिंग्स एवं सिस्टम स्थिति",
    system_status: "सिस्टम स्थिति"
  }
};
