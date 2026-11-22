# A New Shape for Work, independent replication: phrases-pilot, message 2 of 2

Several models are doing this same task separately so their answers can be compared. Work only from this message. Do not look for, ask for or use anyone else's answers, and do not ask another AI to do any of it.

## Instructions

You tag skill phrases from job postings with the phase of work they point to, or mark them neutral. Only tagged phrases count when a job's postings are summarised by phase, so a neutral phrase tagged with a phase inflates that phase for every job that lists it.

The six phases of work. Every job's work can be described with these six, whatever the field:

- understand: finding out what is needed or what is the case. Gathering information, reading, investigating, interviewing, assessing a situation, diagnosing, researching.
- plan: deciding what to do and how. Setting goals, designing, specifying, estimating, budgeting, scheduling, choosing an approach.
- produce: doing the work that makes the job's output. Building, writing, making, treating, teaching, serving, selling, installing, recording.
- check: judging whether work, things or people meet a standard. Testing, inspecting, reviewing, auditing, evaluating quality or compliance.
- sustain: keeping something running once it exists. Monitoring, maintaining, repairing, troubleshooting, securing, cleaning, upkeep.
- coordinate: working through other people. Communicating with colleagues or clients, directing, supervising, training, negotiating, liaising, staffing.

Software names for the same phases: specify (understand), design (plan), build (produce), verify (check), operate (sustain); coordinate is cross-cutting.

Each item gives a phrase from the skill lists of US LinkedIn postings (January 2024; the lists were extracted from the postings by the dataset's author), how often it was mentioned, and the occupations that mention it most.

For each item:

1. Set `answer` to a phase only when the phrase names an activity that clearly sits in that phase, for example "testing" (check) or "scheduling" (plan).
2. Otherwise set `answer` to "neutral". Neutral covers: tools, software, programming languages and platforms; general traits and soft skills ("communication", "attention to detail", "problem solving"); degrees, certifications and licences; knowledge areas and subjects ("accounting", "pharmacology"); and conditions of employment (pay, benefits, schedules, screening, eligibility to work).
3. When a phrase could point to two phases, pick the better fit, put the other in `alt`, and set confidence to medium or low. When the answer is neutral or one phase is clearly right, set `alt` to null.
4. Write one sentence of reason.

`answer` must be one of: understand, plan, produce, check, sustain, coordinate, neutral. `alt` must be one of the six phases or null.

Return only a JSON object, with no preamble and no code fences:

{"answers": [{"id": "the item's id", "answer": "...", "alt": "... or null", "confidence": "high, medium or low", "reason": "one sentence"}]}

Give exactly one answer for every item you were sent, in any order, using each item's id exactly as given. Answer each item on its own merits; do not make items agree with each other for consistency's sake.

## Items

Here are 150 items. Each line is one item, as JSON.

{"id": "p0151", "phrase": "registered nurse license", "mentions": 2924, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Clinical Nurse Specialists"]}
{"id": "p0152", "phrase": "innovation", "mentions": 2916, "occupations": ["Registered Nurses", "Marketing Managers", "Software Developers"]}
{"id": "p0153", "phrase": "nursing process", "mentions": 2897, "occupations": ["Registered Nurses", "Clinical Nurse Specialists", "Medical and Health Services Managers"]}
{"id": "p0154", "phrase": "vision benefits", "mentions": 2880, "occupations": ["Registered Nurses", "Physical Therapists", "Surgical Technologists"]}
{"id": "p0155", "phrase": "delegation", "mentions": 2850, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "General and Operations Managers"]}
{"id": "p0156", "phrase": "critical care", "mentions": 2848, "occupations": ["Registered Nurses", "Veterinarians", "Nurse Practitioners"]}
{"id": "p0157", "phrase": "disability insurance", "mentions": 2838, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Nurse Practitioners"]}
{"id": "p0158", "phrase": "construction", "mentions": 2815, "occupations": ["Project Management Specialists", "Construction Managers", "First-Line Supervisors of Construction Trades and Extraction Workers"]}
{"id": "p0159", "phrase": "maintenance", "mentions": 2806, "occupations": ["Property, Real Estate, and Community Association Managers", "Plumbers, Pipefitters, and Steamfitters", "Electricians"]}
{"id": "p0160", "phrase": "physical stamina", "mentions": 2795, "occupations": ["Registered Nurses", "Customer Service Representatives", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0161", "phrase": "manufacturing", "mentions": 2779, "occupations": ["Mechanical Engineers", "Industrial Production Managers", "Manufacturing Engineers"]}
{"id": "p0162", "phrase": "pto", "mentions": 2779, "occupations": ["Registered Nurses", "Veterinarians", "Nurse Practitioners"]}
{"id": "p0163", "phrase": "strategic planning", "mentions": 2732, "occupations": ["Sales Managers", "Project Management Specialists", "Medical and Health Services Managers"]}
{"id": "p0164", "phrase": "team collaboration", "mentions": 2710, "occupations": ["Registered Nurses", "Project Management Specialists", "Sales Managers"]}
{"id": "p0165", "phrase": "human resources", "mentions": 2709, "occupations": ["Human Resources Specialists", "First-Line Supervisors of Office and Administrative Support Workers", "Human Resources Managers"]}
{"id": "p0166", "phrase": "discharge planning", "mentions": 2704, "occupations": ["Registered Nurses", "Physical Therapists", "Nurse Practitioners"]}
{"id": "p0167", "phrase": "high school diploma or equivalent", "mentions": 2694, "occupations": ["Customer Service Representatives", "Medical Assistants", "First-Line Supervisors of Retail Sales Workers"]}
{"id": "p0168", "phrase": "process improvement", "mentions": 2689, "occupations": ["Accountants and Auditors", "Manufacturing Engineers", "Project Management Specialists"]}
{"id": "p0169", "phrase": "bending", "mentions": 2666, "occupations": ["Registered Nurses", "Managers, All Other", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0170", "phrase": "outlook", "mentions": 2642, "occupations": ["Executive Secretaries and Executive Administrative Assistants", "Project Management Specialists", "Accountants and Auditors"]}
{"id": "p0171", "phrase": "teaching", "mentions": 2640, "occupations": ["Registered Nurses", "Nursing Instructors and Teachers, Postsecondary", "Nurse Practitioners"]}
{"id": "p0172", "phrase": "pediatrics", "mentions": 2629, "occupations": ["Registered Nurses", "Pediatricians, General", "Nurse Practitioners"]}
{"id": "p0173", "phrase": "walking", "mentions": 2625, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Nurse Practitioners"]}
{"id": "p0174", "phrase": "fastpaced environment", "mentions": 2620, "occupations": ["Customer Service Representatives", "Accountants and Auditors", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0175", "phrase": "financial management", "mentions": 2605, "occupations": ["Project Management Specialists", "General and Operations Managers", "Managers, All Other"]}
{"id": "p0176", "phrase": "medical records", "mentions": 2590, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical Assistants"]}
{"id": "p0177", "phrase": "hipaa", "mentions": 2588, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical Assistants"]}
{"id": "p0178", "phrase": "sap", "mentions": 2585, "occupations": ["Accountants and Auditors", "Financial Managers", "Purchasing Managers"]}
{"id": "p0179", "phrase": "401(k) plan", "mentions": 2583, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Veterinarians"]}
{"id": "p0180", "phrase": "stress management", "mentions": 2581, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Nurse Practitioners"]}
{"id": "p0181", "phrase": "patient safety", "mentions": 2561, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Surgical Technologists"]}
{"id": "p0182", "phrase": "dentistry", "mentions": 2551, "occupations": ["Dentists, General", "Veterinarians", "Oral and Maxillofacial Surgeons"]}
{"id": "p0183", "phrase": "legal research", "mentions": 2550, "occupations": ["Lawyers", "Paralegals and Legal Assistants", "Judicial Law Clerks"]}
{"id": "p0184", "phrase": "employee assistance program", "mentions": 2537, "occupations": ["Registered Nurses", "Veterinarians", "Project Management Specialists"]}
{"id": "p0185", "phrase": "clinical experience", "mentions": 2525, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0186", "phrase": "networking", "mentions": 2523, "occupations": ["Dentists, General", "Software Developers", "Sales Managers"]}
{"id": "p0187", "phrase": "implementation", "mentions": 2518, "occupations": ["Registered Nurses", "Software Developers", "Clinical Nurse Specialists"]}
{"id": "p0188", "phrase": "electrical engineering", "mentions": 2514, "occupations": ["Electrical Engineers", "Software Developers", "Project Management Specialists"]}
{"id": "p0189", "phrase": "accuracy", "mentions": 2503, "occupations": ["Accountants and Auditors", "Customer Service Representatives", "Pharmacists"]}
{"id": "p0190", "phrase": "physical strength", "mentions": 2500, "occupations": ["Registered Nurses", "Customer Service Representatives", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0191", "phrase": "coordination", "mentions": 2464, "occupations": ["Registered Nurses", "Project Management Specialists", "Construction Managers"]}
{"id": "p0192", "phrase": "supervisory experience", "mentions": 2437, "occupations": ["First-Line Supervisors of Office and Administrative Support Workers", "Medical and Health Services Managers", "Managers, All Other"]}
{"id": "p0193", "phrase": "evidencebased practice", "mentions": 2430, "occupations": ["Registered Nurses", "Clinical Nurse Specialists", "Medical and Health Services Managers"]}
{"id": "p0194", "phrase": "detailoriented", "mentions": 2429, "occupations": ["Accountants and Auditors", "Customer Service Representatives", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0195", "phrase": "team work", "mentions": 2372, "occupations": ["Registered Nurses", "Customer Service Representatives", "Accountants and Auditors"]}
{"id": "p0196", "phrase": "physical therapy", "mentions": 2362, "occupations": ["Physical Therapists", "Physical Therapist Assistants", "Athletic Trainers"]}
{"id": "p0197", "phrase": "change management", "mentions": 2357, "occupations": ["Project Management Specialists", "Construction Managers", "Human Resources Specialists"]}
{"id": "p0198", "phrase": "litigation", "mentions": 2353, "occupations": ["Lawyers", "Paralegals and Legal Assistants", "Claims Adjusters, Examiners, and Investigators"]}
{"id": "p0199", "phrase": "hiring", "mentions": 2324, "occupations": ["General and Operations Managers", "Medical and Health Services Managers", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0200", "phrase": "computer science", "mentions": 2308, "occupations": ["Software Developers", "Lawyers", "Data Scientists"]}
{"id": "p0201", "phrase": "pet insurance", "mentions": 2308, "occupations": ["Registered Nurses", "Veterinarians", "Physical Therapists"]}
{"id": "p0202", "phrase": "data collection", "mentions": 2297, "occupations": ["Registered Nurses", "Business Intelligence Analysts", "Clinical Research Coordinators"]}
{"id": "p0203", "phrase": "selfmotivation", "mentions": 2294, "occupations": ["Sales Managers", "Customer Service Representatives", "Project Management Specialists"]}
{"id": "p0204", "phrase": "bachelor's degree in nursing", "mentions": 2274, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Clinical Nurse Specialists"]}
{"id": "p0205", "phrase": "diversity and inclusion", "mentions": 2269, "occupations": ["Registered Nurses", "Human Resources Specialists", "Human Resources Managers"]}
{"id": "p0206", "phrase": "ms office", "mentions": 2247, "occupations": ["Project Management Specialists", "Accountants and Auditors", "Construction Managers"]}
{"id": "p0207", "phrase": "continuous improvement", "mentions": 2246, "occupations": ["Industrial Production Managers", "Manufacturing Engineers", "First-Line Supervisors of Production and Operating Workers"]}
{"id": "p0208", "phrase": "rehabilitation", "mentions": 2245, "occupations": ["Registered Nurses", "Athletic Trainers", "Physical Therapists"]}
{"id": "p0209", "phrase": "ability to work independently", "mentions": 2243, "occupations": ["First-Line Supervisors of Office and Administrative Support Workers", "Customer Service Representatives", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0210", "phrase": "english proficiency", "mentions": 2242, "occupations": ["Registered Nurses", "Medical Assistants", "Nursing Assistants"]}
{"id": "p0211", "phrase": "independent work", "mentions": 2241, "occupations": ["Accountants and Auditors", "Lawyers", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0212", "phrase": "time management skills", "mentions": 2240, "occupations": ["Registered Nurses", "Executive Secretaries and Executive Administrative Assistants", "Project Management Specialists"]}
{"id": "p0213", "phrase": "software development", "mentions": 2235, "occupations": ["Software Developers", "Information Technology Project Managers", "Project Management Specialists"]}
{"id": "p0214", "phrase": "holiday pay", "mentions": 2220, "occupations": ["Registered Nurses", "Physical Therapists", "Surgical Technologists"]}
{"id": "p0215", "phrase": "aws", "mentions": 2206, "occupations": ["Software Developers", "Computer Systems Engineers/Architects", "Data Scientists"]}
{"id": "p0216", "phrase": "first aid", "mentions": 2172, "occupations": ["Registered Nurses", "Athletic Trainers", "Coaches and Scouts"]}
{"id": "p0217", "phrase": "diagnosis", "mentions": 2167, "occupations": ["Nurse Practitioners", "Registered Nurses", "Dentists, General"]}
{"id": "p0218", "phrase": "mental health", "mentions": 2167, "occupations": ["Registered Nurses", "Psychiatrists", "Mental Health Counselors"]}
{"id": "p0219", "phrase": "agile", "mentions": 2164, "occupations": ["Software Developers", "Project Management Specialists", "Information Technology Project Managers"]}
{"id": "p0220", "phrase": "inclusion", "mentions": 2159, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0221", "phrase": "technical writing", "mentions": 2144, "occupations": ["Project Management Specialists", "Mechanical Engineers", "Software Developers"]}
{"id": "p0222", "phrase": "business administration", "mentions": 2133, "occupations": ["Production, Planning, and Expediting Clerks", "Sales Managers", "Project Management Specialists"]}
{"id": "p0223", "phrase": "emr", "mentions": 2129, "occupations": ["Registered Nurses", "Nurse Practitioners", "Obstetricians and Gynecologists"]}
{"id": "p0224", "phrase": "javascript", "mentions": 2122, "occupations": ["Software Developers", "Web Developers", "Computer Programmers"]}
{"id": "p0225", "phrase": "positive attitude", "mentions": 2121, "occupations": ["First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services", "First-Line Supervisors of Office and Administrative Support Workers", "Customer Service Representatives"]}
{"id": "p0226", "phrase": "veterinary medicine", "mentions": 2112, "occupations": ["Veterinarians", "Veterinary Technologists and Technicians", "Veterinary Assistants and Laboratory Animal Caretakers"]}
{"id": "p0227", "phrase": "surgery", "mentions": 2110, "occupations": ["Veterinarians", "Obstetricians and Gynecologists", "Physician Assistants"]}
{"id": "p0228", "phrase": "physician", "mentions": 2102, "occupations": ["General Internal Medicine Physicians", "Anesthesiologists", "Pediatricians, General"]}
{"id": "p0229", "phrase": "retail", "mentions": 2092, "occupations": ["Customer Service Representatives", "First-Line Supervisors of Retail Sales Workers", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0230", "phrase": "wound care", "mentions": 2091, "occupations": ["Registered Nurses", "Nurse Practitioners", "Licensed Practical and Licensed Vocational Nurses"]}
{"id": "p0231", "phrase": "client relations", "mentions": 2082, "occupations": ["Project Management Specialists", "Lawyers", "Veterinarians"]}
{"id": "p0232", "phrase": "retail experience", "mentions": 2082, "occupations": ["Customer Service Representatives", "First-Line Supervisors of Retail Sales Workers", "Managers, All Other"]}
{"id": "p0233", "phrase": "merchandising", "mentions": 2078, "occupations": ["First-Line Supervisors of Retail Sales Workers", "First-Line Supervisors of Office and Administrative Support Workers", "Sales Managers"]}
{"id": "p0234", "phrase": "care planning", "mentions": 2068, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0235", "phrase": "malpractice insurance", "mentions": 2067, "occupations": ["Dentists, General", "Nurse Practitioners", "Obstetricians and Gynecologists"]}
{"id": "p0236", "phrase": "oncology", "mentions": 2065, "occupations": ["Registered Nurses", "Veterinarians", "General Internal Medicine Physicians"]}
{"id": "p0237", "phrase": "contract management", "mentions": 2064, "occupations": ["Project Management Specialists", "Construction Managers", "Purchasing Managers"]}
{"id": "p0238", "phrase": "design", "mentions": 2062, "occupations": ["Project Management Specialists", "Mechanical Engineers", "Software Developers"]}
{"id": "p0239", "phrase": "vendor management", "mentions": 2044, "occupations": ["Project Management Specialists", "Purchasing Managers", "Property, Real Estate, and Community Association Managers"]}
{"id": "p0240", "phrase": "writing", "mentions": 2032, "occupations": ["Lawyers", "Marketing Managers", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0241", "phrase": "team building", "mentions": 2020, "occupations": ["General and Operations Managers", "First-Line Supervisors of Office and Administrative Support Workers", "Project Management Specialists"]}
{"id": "p0242", "phrase": "crisis intervention", "mentions": 2019, "occupations": ["Mental Health Counselors", "Registered Nurses", "Substance Abuse and Behavioral Disorder Counselors"]}
{"id": "p0243", "phrase": "physical demands", "mentions": 2006, "occupations": ["Registered Nurses", "Nurse Practitioners", "Sales Managers"]}
{"id": "p0244", "phrase": "record keeping", "mentions": 2001, "occupations": ["Registered Nurses", "Production, Planning, and Expediting Clerks", "Radiologic Technologists and Technicians"]}
{"id": "p0245", "phrase": "software engineering", "mentions": 1987, "occupations": ["Software Developers", "Lawyers", "Computer Systems Engineers/Architects"]}
{"id": "p0246", "phrase": "401k retirement plan", "mentions": 1976, "occupations": ["Registered Nurses", "Physical Therapists", "Surgical Technologists"]}
{"id": "p0247", "phrase": "care coordination", "mentions": 1975, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0248", "phrase": "food preparation", "mentions": 1954, "occupations": ["Chefs and Head Cooks", "Hosts and Hostesses, Restaurant, Lounge, and Coffee Shop", "Managers, All Other"]}
{"id": "p0249", "phrase": "account management", "mentions": 1951, "occupations": ["Sales Managers", "Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0250", "phrase": "equipment maintenance", "mentions": 1948, "occupations": ["Radiologic Technologists and Technicians", "Magnetic Resonance Imaging Technologists", "Diagnostic Medical Sonographers"]}
{"id": "p0251", "phrase": "licensure", "mentions": 1933, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0252", "phrase": "technical skills", "mentions": 1924, "occupations": ["First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services", "Project Management Specialists", "Radiologic Technologists and Technicians"]}
{"id": "p0253", "phrase": "ultrasound", "mentions": 1922, "occupations": ["Veterinarians", "Diagnostic Medical Sonographers", "Radiologic Technologists and Technicians"]}
{"id": "p0254", "phrase": "social work", "mentions": 1919, "occupations": ["Mental Health Counselors", "Medical and Health Services Managers", "Mental Health and Substance Abuse Social Workers"]}
{"id": "p0255", "phrase": "referral bonuses", "mentions": 1886, "occupations": ["Registered Nurses", "Surgical Technologists", "Licensed Practical and Licensed Vocational Nurses"]}
{"id": "p0256", "phrase": "food safety", "mentions": 1881, "occupations": ["Chefs and Head Cooks", "General and Operations Managers", "First-Line Supervisors of Retail Sales Workers"]}
{"id": "p0257", "phrase": "flexible schedule", "mentions": 1867, "occupations": ["Nurse Practitioners", "General and Operations Managers", "First-Line Supervisors of Retail Sales Workers"]}
{"id": "p0258", "phrase": "payroll", "mentions": 1867, "occupations": ["Accountants and Auditors", "Human Resources Managers", "Human Resources Specialists"]}
{"id": "p0259", "phrase": "report writing", "mentions": 1859, "occupations": ["Executive Secretaries and Executive Administrative Assistants", "Project Management Specialists", "Accountants and Auditors"]}
{"id": "p0260", "phrase": "internal medicine", "mentions": 1845, "occupations": ["Veterinarians", "Nurse Practitioners", "General Internal Medicine Physicians"]}
{"id": "p0261", "phrase": "basic life support (bls)", "mentions": 1821, "occupations": ["Registered Nurses", "Surgical Technologists", "Radiologic Technologists and Technicians"]}
{"id": "p0262", "phrase": "performance improvement", "mentions": 1815, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Clinical Nurse Specialists"]}
{"id": "p0263", "phrase": "reaching", "mentions": 1808, "occupations": ["Registered Nurses", "Managers, All Other", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0264", "phrase": "customer service skills", "mentions": 1802, "occupations": ["Customer Service Representatives", "Patient Representatives", "Medical Assistants"]}
{"id": "p0265", "phrase": "medication management", "mentions": 1798, "occupations": ["Registered Nurses", "Nurse Practitioners", "Psychiatrists"]}
{"id": "p0266", "phrase": "cleaning", "mentions": 1783, "occupations": ["Maids and Housekeeping Cleaners", "Janitors and Cleaners, Except Maids and Housekeeping Cleaners", "Managers, All Other"]}
{"id": "p0267", "phrase": "sanitation", "mentions": 1776, "occupations": ["Chefs and Head Cooks", "General and Operations Managers", "Managers, All Other"]}
{"id": "p0268", "phrase": "basic life support", "mentions": 1775, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Nurse Practitioners"]}
{"id": "p0269", "phrase": "employee relations", "mentions": 1766, "occupations": ["Human Resources Managers", "Human Resources Specialists", "Labor Relations Specialists"]}
{"id": "p0270", "phrase": "data management", "mentions": 1765, "occupations": ["Business Intelligence Analysts", "Clinical Research Coordinators", "Project Management Specialists"]}
{"id": "p0271", "phrase": "supply chain management", "mentions": 1758, "occupations": ["Purchasing Managers", "Supply Chain Managers", "Production, Planning, and Expediting Clerks"]}
{"id": "p0272", "phrase": "training and development", "mentions": 1754, "occupations": ["Human Resources Managers", "First-Line Supervisors of Office and Administrative Support Workers", "Human Resources Specialists"]}
{"id": "p0273", "phrase": "primary care", "mentions": 1752, "occupations": ["Nurse Practitioners", "Physician Assistants", "Family Medicine Physicians"]}
{"id": "p0274", "phrase": "behavioral health", "mentions": 1739, "occupations": ["Registered Nurses", "Psychiatrists", "Mental Health Counselors"]}
{"id": "p0275", "phrase": "electronic medical records", "mentions": 1736, "occupations": ["Registered Nurses", "Nurse Practitioners", "Physical Therapists"]}
{"id": "p0276", "phrase": "project planning", "mentions": 1736, "occupations": ["Project Management Specialists", "Construction Managers", "Information Technology Project Managers"]}
{"id": "p0277", "phrase": "testing", "mentions": 1730, "occupations": ["Software Developers", "Mechanical Engineers", "Project Management Specialists"]}
{"id": "p0278", "phrase": "psychology", "mentions": 1729, "occupations": ["Mental Health Counselors", "Clinical and Counseling Psychologists", "Marriage and Family Therapists"]}
{"id": "p0279", "phrase": "computer literacy", "mentions": 1717, "occupations": ["Registered Nurses", "Customer Service Representatives", "Medical and Health Services Managers"]}
{"id": "p0280", "phrase": "osha", "mentions": 1706, "occupations": ["Registered Nurses", "Dentists, General", "Nurse Practitioners"]}
{"id": "p0281", "phrase": "treatment", "mentions": 1702, "occupations": ["Nurse Practitioners", "Registered Nurses", "Athletic Trainers"]}
{"id": "p0282", "phrase": "event planning", "mentions": 1700, "occupations": ["Executive Secretaries and Executive Administrative Assistants", "Meeting, Convention, and Event Planners", "Sales Managers"]}
{"id": "p0283", "phrase": "epic", "mentions": 1676, "occupations": ["Registered Nurses", "Nurse Practitioners", "Radiologic Technologists and Technicians"]}
{"id": "p0284", "phrase": "accounts payable", "mentions": 1674, "occupations": ["Accountants and Auditors", "Bookkeeping, Accounting, and Auditing Clerks", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0285", "phrase": "physical requirements", "mentions": 1673, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Nurse Practitioners"]}
{"id": "p0286", "phrase": "public speaking", "mentions": 1673, "occupations": ["Lawyers", "Sales Managers", "Educational, Guidance, and Career Counselors and Advisors"]}
{"id": "p0287", "phrase": "product knowledge", "mentions": 1670, "occupations": ["Sales Managers", "Customer Service Representatives", "First-Line Supervisors of Retail Sales Workers"]}
{"id": "p0288", "phrase": "interpersonal communication", "mentions": 1665, "occupations": ["Registered Nurses", "Psychiatric Technicians", "First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services"]}
{"id": "p0289", "phrase": "mileage reimbursement", "mentions": 1664, "occupations": ["Registered Nurses", "Physical Therapists", "Occupational Therapists"]}
{"id": "p0290", "phrase": "c++", "mentions": 1663, "occupations": ["Software Developers", "Computer Hardware Engineers", "Computer Programmers"]}
{"id": "p0291", "phrase": "clinical skills", "mentions": 1648, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Nurse Practitioners"]}
{"id": "p0292", "phrase": "procurement", "mentions": 1648, "occupations": ["Project Management Specialists", "Purchasing Managers", "Construction Managers"]}
{"id": "p0293", "phrase": "reliable transportation", "mentions": 1644, "occupations": ["Registered Nurses", "Nurse Practitioners", "Nursing Assistants"]}
{"id": "p0294", "phrase": "analytical thinking", "mentions": 1642, "occupations": ["Lawyers", "Accountants and Auditors", "Sales Managers"]}
{"id": "p0295", "phrase": "12hour shifts", "mentions": 1639, "occupations": ["Registered Nurses", "Surgical Technologists", "Respiratory Therapists"]}
{"id": "p0296", "phrase": "billing", "mentions": 1634, "occupations": ["Dentists, General", "Accountants and Auditors", "Customer Service Representatives"]}
{"id": "p0297", "phrase": "architecture", "mentions": 1629, "occupations": ["Project Management Specialists", "Architects, Except Landscape and Naval", "Construction Managers"]}
{"id": "p0298", "phrase": "auditing", "mentions": 1627, "occupations": ["Accountants and Auditors", "Compliance Managers", "Financial Managers"]}
{"id": "p0299", "phrase": "recruiting", "mentions": 1609, "occupations": ["Human Resources Specialists", "First-Line Supervisors of Office and Administrative Support Workers", "Human Resources Managers"]}
{"id": "p0300", "phrase": "inventory control", "mentions": 1607, "occupations": ["General and Operations Managers", "Clinical Nurse Specialists", "First-Line Supervisors of Retail Sales Workers"]}

Return the JSON object described in your instructions, with one answer for each of the 150 items.

## What to send back

The JSON object described above, and nothing else. It is saved as `reply-phrases-pilot-2.json`.
