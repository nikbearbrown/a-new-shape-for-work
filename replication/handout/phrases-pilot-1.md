# A New Shape for Work, independent replication: phrases-pilot, message 1 of 2

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

{"id": "p0001", "phrase": "communication", "mentions": 68188, "occupations": ["Registered Nurses", "Customer Service Representatives", "Project Management Specialists"]}
{"id": "p0002", "phrase": "teamwork", "mentions": 41523, "occupations": ["Registered Nurses", "Customer Service Representatives", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0003", "phrase": "communication skills", "mentions": 36824, "occupations": ["Registered Nurses", "Customer Service Representatives", "First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services"]}
{"id": "p0004", "phrase": "customer service", "mentions": 36763, "occupations": ["Customer Service Representatives", "First-Line Supervisors of Office and Administrative Support Workers", "First-Line Supervisors of Retail Sales Workers"]}
{"id": "p0005", "phrase": "patient care", "mentions": 34040, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0006", "phrase": "nursing", "mentions": 31788, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Nurse Practitioners"]}
{"id": "p0007", "phrase": "leadership", "mentions": 31378, "occupations": ["Registered Nurses", "Project Management Specialists", "Medical and Health Services Managers"]}
{"id": "p0008", "phrase": "time management", "mentions": 27336, "occupations": ["Registered Nurses", "Executive Secretaries and Executive Administrative Assistants", "Project Management Specialists"]}
{"id": "p0009", "phrase": "problem solving", "mentions": 26618, "occupations": ["Registered Nurses", "Customer Service Representatives", "Project Management Specialists"]}
{"id": "p0010", "phrase": "project management", "mentions": 25524, "occupations": ["Project Management Specialists", "Construction Managers", "Marketing Managers"]}
{"id": "p0011", "phrase": "attention to detail", "mentions": 23889, "occupations": ["Registered Nurses", "Accountants and Auditors", "Customer Service Representatives"]}
{"id": "p0012", "phrase": "problemsolving", "mentions": 23830, "occupations": ["Registered Nurses", "Customer Service Representatives", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0013", "phrase": "interpersonal skills", "mentions": 20188, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Project Management Specialists"]}
{"id": "p0014", "phrase": "collaboration", "mentions": 18760, "occupations": ["Registered Nurses", "Nurse Practitioners", "Project Management Specialists"]}
{"id": "p0015", "phrase": "organizational skills", "mentions": 16498, "occupations": ["Registered Nurses", "Executive Secretaries and Executive Administrative Assistants", "Accountants and Auditors"]}
{"id": "p0016", "phrase": "microsoft office suite", "mentions": 16069, "occupations": ["Project Management Specialists", "Executive Secretaries and Executive Administrative Assistants", "Accountants and Auditors"]}
{"id": "p0017", "phrase": "data analysis", "mentions": 15636, "occupations": ["Business Intelligence Analysts", "Registered Nurses", "Accountants and Auditors"]}
{"id": "p0018", "phrase": "critical thinking", "mentions": 15464, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Psychiatric Technicians"]}
{"id": "p0019", "phrase": "documentation", "mentions": 14867, "occupations": ["Registered Nurses", "Nurse Practitioners", "Physical Therapists"]}
{"id": "p0020", "phrase": "bachelor's degree", "mentions": 14246, "occupations": ["Project Management Specialists", "Sales Managers", "Registered Nurses"]}
{"id": "p0021", "phrase": "multitasking", "mentions": 12852, "occupations": ["Customer Service Representatives", "Registered Nurses", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0022", "phrase": "microsoft office", "mentions": 12542, "occupations": ["Project Management Specialists", "Customer Service Representatives", "Registered Nurses"]}
{"id": "p0023", "phrase": "scheduling", "mentions": 12369, "occupations": ["Project Management Specialists", "Construction Managers", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0024", "phrase": "training", "mentions": 12188, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "General and Operations Managers"]}
{"id": "p0025", "phrase": "analytical skills", "mentions": 11891, "occupations": ["Accountants and Auditors", "Lawyers", "Project Management Specialists"]}
{"id": "p0026", "phrase": "registered nurse", "mentions": 11853, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Clinical Nurse Specialists"]}
{"id": "p0027", "phrase": "sales", "mentions": 11125, "occupations": ["Sales Managers", "Customer Service Representatives", "First-Line Supervisors of Retail Sales Workers"]}
{"id": "p0028", "phrase": "patient education", "mentions": 10222, "occupations": ["Registered Nurses", "Nurse Practitioners", "Physical Therapists"]}
{"id": "p0029", "phrase": "budgeting", "mentions": 10184, "occupations": ["Project Management Specialists", "Accountants and Auditors", "Construction Managers"]}
{"id": "p0030", "phrase": "life insurance", "mentions": 10110, "occupations": ["Registered Nurses", "Veterinarians", "Physical Therapists"]}
{"id": "p0031", "phrase": "bls", "mentions": 10038, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0032", "phrase": "high school diploma", "mentions": 9925, "occupations": ["Customer Service Representatives", "Sales Managers", "Personal Financial Advisors"]}
{"id": "p0033", "phrase": "flexibility", "mentions": 9898, "occupations": ["Registered Nurses", "First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services", "First-Line Supervisors of Retail Sales Workers"]}
{"id": "p0034", "phrase": "paid time off", "mentions": 9831, "occupations": ["Registered Nurses", "Veterinarians", "Nurse Practitioners"]}
{"id": "p0035", "phrase": "adaptability", "mentions": 9539, "occupations": ["Registered Nurses", "Customer Service Representatives", "Sales Managers"]}
{"id": "p0036", "phrase": "organization", "mentions": 9526, "occupations": ["First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services", "Registered Nurses", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0037", "phrase": "written communication", "mentions": 9318, "occupations": ["Registered Nurses", "Project Management Specialists", "Accountants and Auditors"]}
{"id": "p0038", "phrase": "dental insurance", "mentions": 8993, "occupations": ["Registered Nurses", "Veterinarians", "Nurse Practitioners"]}
{"id": "p0039", "phrase": "healthcare", "mentions": 8990, "occupations": ["Registered Nurses", "Nurse Practitioners", "General Internal Medicine Physicians"]}
{"id": "p0040", "phrase": "excel", "mentions": 8781, "occupations": ["Accountants and Auditors", "Project Management Specialists", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0041", "phrase": "bls certification", "mentions": 8603, "occupations": ["Registered Nurses", "Nurse Practitioners", "Radiologic Technologists and Technicians"]}
{"id": "p0042", "phrase": "health insurance", "mentions": 8566, "occupations": ["Registered Nurses", "Veterinarians", "Nurse Practitioners"]}
{"id": "p0043", "phrase": "acls", "mentions": 8548, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0044", "phrase": "vision insurance", "mentions": 8319, "occupations": ["Registered Nurses", "Veterinarians", "Nurse Practitioners"]}
{"id": "p0045", "phrase": "accounting", "mentions": 8222, "occupations": ["Accountants and Auditors", "Financial Managers", "Bookkeeping, Accounting, and Auditing Clerks"]}
{"id": "p0046", "phrase": "verbal communication", "mentions": 8074, "occupations": ["Registered Nurses", "Project Management Specialists", "Customer Service Representatives"]}
{"id": "p0047", "phrase": "problemsolving skills", "mentions": 7808, "occupations": ["Registered Nurses", "Accountants and Auditors", "Customer Service Representatives"]}
{"id": "p0048", "phrase": "inventory management", "mentions": 7779, "occupations": ["First-Line Supervisors of Retail Sales Workers", "General and Operations Managers", "Chefs and Head Cooks"]}
{"id": "p0049", "phrase": "computer skills", "mentions": 7731, "occupations": ["Registered Nurses", "Customer Service Representatives", "Nurse Practitioners"]}
{"id": "p0050", "phrase": "supervision", "mentions": 7700, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0051", "phrase": "cpr", "mentions": 7570, "occupations": ["Registered Nurses", "Nurse Practitioners", "Radiologic Technologists and Technicians"]}
{"id": "p0052", "phrase": "quality assurance", "mentions": 7424, "occupations": ["Registered Nurses", "Project Management Specialists", "Industrial Production Managers"]}
{"id": "p0053", "phrase": "medication administration", "mentions": 7412, "occupations": ["Registered Nurses", "Licensed Practical and Licensed Vocational Nurses", "Psychiatric Technicians"]}
{"id": "p0054", "phrase": "conflict resolution", "mentions": 7328, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Customer Service Representatives"]}
{"id": "p0055", "phrase": "safety", "mentions": 7099, "occupations": ["Registered Nurses", "Project Management Specialists", "Construction Managers"]}
{"id": "p0056", "phrase": "confidentiality", "mentions": 7080, "occupations": ["Registered Nurses", "Executive Secretaries and Executive Administrative Assistants", "Nurse Practitioners"]}
{"id": "p0057", "phrase": "travel", "mentions": 7072, "occupations": ["Registered Nurses", "Sales Managers", "Project Management Specialists"]}
{"id": "p0058", "phrase": "troubleshooting", "mentions": 6989, "occupations": ["Software Developers", "Computer User Support Specialists", "Electricians"]}
{"id": "p0059", "phrase": "reporting", "mentions": 6851, "occupations": ["Registered Nurses", "Accountants and Auditors", "Project Management Specialists"]}
{"id": "p0060", "phrase": "research", "mentions": 6781, "occupations": ["Registered Nurses", "Lawyers", "Nurse Practitioners"]}
{"id": "p0061", "phrase": "driver's license", "mentions": 6688, "occupations": ["Registered Nurses", "Sales Managers", "Project Management Specialists"]}
{"id": "p0062", "phrase": "quality control", "mentions": 6669, "occupations": ["Construction Managers", "Project Management Specialists", "Industrial Production Managers"]}
{"id": "p0063", "phrase": "cpr certification", "mentions": 6562, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0064", "phrase": "planning", "mentions": 6329, "occupations": ["Registered Nurses", "Project Management Specialists", "Construction Managers"]}
{"id": "p0065", "phrase": "negotiation", "mentions": 6191, "occupations": ["Lawyers", "Sales Managers", "Project Management Specialists"]}
{"id": "p0066", "phrase": "professionalism", "mentions": 6190, "occupations": ["Registered Nurses", "Executive Secretaries and Executive Administrative Assistants", "Customer Service Representatives"]}
{"id": "p0067", "phrase": "decision making", "mentions": 5790, "occupations": ["Registered Nurses", "Project Management Specialists", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0068", "phrase": "prioritization", "mentions": 5774, "occupations": ["Registered Nurses", "Executive Secretaries and Executive Administrative Assistants", "Accountants and Auditors"]}
{"id": "p0069", "phrase": "equal opportunity employer", "mentions": 5698, "occupations": ["Registered Nurses", "Nurse Practitioners", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0070", "phrase": "coaching", "mentions": 5618, "occupations": ["Managers, All Other", "First-Line Supervisors of Office and Administrative Support Workers", "Sales Managers"]}
{"id": "p0071", "phrase": "medical", "mentions": 5576, "occupations": ["Registered Nurses", "Nurse Practitioners", "Veterinarians"]}
{"id": "p0072", "phrase": "microsoft excel", "mentions": 5491, "occupations": ["Accountants and Auditors", "Project Management Specialists", "Customer Service Representatives"]}
{"id": "p0073", "phrase": "data entry", "mentions": 5472, "occupations": ["Customer Service Representatives", "Registered Nurses", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0074", "phrase": "marketing", "mentions": 5412, "occupations": ["Marketing Managers", "Sales Managers", "Property, Real Estate, and Community Association Managers"]}
{"id": "p0075", "phrase": "mentoring", "mentions": 5411, "occupations": ["Registered Nurses", "Project Management Specialists", "Software Developers"]}
{"id": "p0076", "phrase": "rn license", "mentions": 5401, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Nurse Practitioners"]}
{"id": "p0077", "phrase": "valid driver's license", "mentions": 5351, "occupations": ["Registered Nurses", "Sales Managers", "Construction Managers"]}
{"id": "p0078", "phrase": "case management", "mentions": 5331, "occupations": ["Registered Nurses", "Lawyers", "Mental Health Counselors"]}
{"id": "p0079", "phrase": "rn", "mentions": 5247, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Nurse Practitioners"]}
{"id": "p0080", "phrase": "engineering", "mentions": 5230, "occupations": ["Project Management Specialists", "Construction Managers", "Software Developers"]}
{"id": "p0081", "phrase": "education", "mentions": 5221, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0082", "phrase": "401k", "mentions": 5206, "occupations": ["Registered Nurses", "Veterinarians", "Nurse Practitioners"]}
{"id": "p0083", "phrase": "quality improvement", "mentions": 5151, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Nurse Practitioners"]}
{"id": "p0084", "phrase": "professional development", "mentions": 5141, "occupations": ["Registered Nurses", "Mental Health Counselors", "Marriage and Family Therapists"]}
{"id": "p0085", "phrase": "risk management", "mentions": 5138, "occupations": ["Project Management Specialists", "Construction Managers", "Information Technology Project Managers"]}
{"id": "p0086", "phrase": "medical terminology", "mentions": 5114, "occupations": ["Registered Nurses", "Medical Assistants", "Radiologic Technologists and Technicians"]}
{"id": "p0087", "phrase": "compassion", "mentions": 5038, "occupations": ["Registered Nurses", "Veterinarians", "Mental Health Counselors"]}
{"id": "p0088", "phrase": "continuing education", "mentions": 4981, "occupations": ["Registered Nurses", "Dentists, General", "Veterinarians"]}
{"id": "p0089", "phrase": "compliance", "mentions": 4980, "occupations": ["Registered Nurses", "Pharmacists", "Accountants and Auditors"]}
{"id": "p0090", "phrase": "construction management", "mentions": 4919, "occupations": ["Construction Managers", "Project Management Specialists", "Construction and Building Inspectors"]}
{"id": "p0091", "phrase": "presentation skills", "mentions": 4907, "occupations": ["Sales Managers", "Project Management Specialists", "Marketing Managers"]}
{"id": "p0092", "phrase": "lifting", "mentions": 4887, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Managers, All Other"]}
{"id": "p0093", "phrase": "vision", "mentions": 4868, "occupations": ["Registered Nurses", "Project Management Specialists", "Nurse Practitioners"]}
{"id": "p0094", "phrase": "python", "mentions": 4852, "occupations": ["Software Developers", "Data Scientists", "Business Intelligence Analysts"]}
{"id": "p0095", "phrase": "infection control", "mentions": 4779, "occupations": ["Registered Nurses", "Radiologic Technologists and Technicians", "Surgical Technologists"]}
{"id": "p0096", "phrase": "assessment", "mentions": 4665, "occupations": ["Registered Nurses", "Nurse Practitioners", "Mental Health Counselors"]}
{"id": "p0097", "phrase": "team leadership", "mentions": 4539, "occupations": ["Project Management Specialists", "General and Operations Managers", "Sales Managers"]}
{"id": "p0098", "phrase": "401(k)", "mentions": 4493, "occupations": ["Registered Nurses", "Veterinarians", "Dentists, General"]}
{"id": "p0099", "phrase": "dental", "mentions": 4429, "occupations": ["Registered Nurses", "Nurse Practitioners", "Veterinarians"]}
{"id": "p0100", "phrase": "evaluation", "mentions": 4370, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Occupational Therapists"]}
{"id": "p0101", "phrase": "patient assessment", "mentions": 4366, "occupations": ["Registered Nurses", "Nurse Practitioners", "Clinical Nurse Specialists"]}
{"id": "p0102", "phrase": "budget management", "mentions": 4337, "occupations": ["Project Management Specialists", "Construction Managers", "Medical and Health Services Managers"]}
{"id": "p0103", "phrase": "decisionmaking", "mentions": 4309, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Project Management Specialists"]}
{"id": "p0104", "phrase": "sql", "mentions": 4245, "occupations": ["Software Developers", "Business Intelligence Analysts", "Data Scientists"]}
{"id": "p0105", "phrase": "registered nurse (rn)", "mentions": 4237, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Clinical Nurse Specialists"]}
{"id": "p0106", "phrase": "management", "mentions": 4225, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "General and Operations Managers"]}
{"id": "p0107", "phrase": "empathy", "mentions": 4219, "occupations": ["Registered Nurses", "Marriage and Family Therapists", "Mental Health Counselors"]}
{"id": "p0108", "phrase": "team management", "mentions": 4162, "occupations": ["General and Operations Managers", "Project Management Specialists", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0109", "phrase": "travel nursing", "mentions": 4115, "occupations": ["Registered Nurses", "Physical Therapists", "Cardiovascular Technologists and Technicians"]}
{"id": "p0110", "phrase": "microsoft word", "mentions": 4079, "occupations": ["Project Management Specialists", "Accountants and Auditors", "Customer Service Representatives"]}
{"id": "p0111", "phrase": "financial reporting", "mentions": 3969, "occupations": ["Accountants and Auditors", "Financial Managers", "Property, Real Estate, and Community Association Managers"]}
{"id": "p0112", "phrase": "counseling", "mentions": 3943, "occupations": ["Mental Health Counselors", "Registered Nurses", "Marriage and Family Therapists"]}
{"id": "p0113", "phrase": "business development", "mentions": 3899, "occupations": ["Sales Managers", "Wind Energy Development Managers", "Project Management Specialists"]}
{"id": "p0114", "phrase": "nurse practitioner", "mentions": 3858, "occupations": ["Nurse Practitioners", "Physician Assistants", "Obstetricians and Gynecologists"]}
{"id": "p0115", "phrase": "autocad", "mentions": 3854, "occupations": ["Project Management Specialists", "Mechanical Engineers", "Architects, Except Landscape and Naval"]}
{"id": "p0116", "phrase": "physician assistant", "mentions": 3765, "occupations": ["Nurse Practitioners", "Physician Assistants", "General Internal Medicine Physicians"]}
{"id": "p0117", "phrase": "weekly pay", "mentions": 3755, "occupations": ["Registered Nurses", "Physical Therapists", "Surgical Technologists"]}
{"id": "p0118", "phrase": "financial analysis", "mentions": 3700, "occupations": ["Accountants and Auditors", "Financial Managers", "Treasurers and Controllers"]}
{"id": "p0119", "phrase": "diversity", "mentions": 3684, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0120", "phrase": "medical benefits", "mentions": 3674, "occupations": ["Registered Nurses", "Physical Therapists", "Veterinarians"]}
{"id": "p0121", "phrase": "mechanical engineering", "mentions": 3661, "occupations": ["Mechanical Engineers", "Manufacturing Engineers", "Project Management Specialists"]}
{"id": "p0122", "phrase": "pals", "mentions": 3637, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Nurse Practitioners"]}
{"id": "p0123", "phrase": "paid holidays", "mentions": 3617, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Nurse Practitioners"]}
{"id": "p0124", "phrase": "high school diploma or ged", "mentions": 3570, "occupations": ["Customer Service Representatives", "Patient Representatives", "Production, Planning, and Expediting Clerks"]}
{"id": "p0125", "phrase": "master's degree", "mentions": 3562, "occupations": ["Nurse Practitioners", "Mental Health Counselors", "Project Management Specialists"]}
{"id": "p0126", "phrase": "leadership skills", "mentions": 3552, "occupations": ["Registered Nurses", "Managers, All Other", "Project Management Specialists"]}
{"id": "p0127", "phrase": "referral bonus", "mentions": 3548, "occupations": ["Registered Nurses", "Physical Therapists", "Surgical Technologists"]}
{"id": "p0128", "phrase": "background check", "mentions": 3522, "occupations": ["Registered Nurses", "Customer Service Representatives", "Project Management Specialists"]}
{"id": "p0129", "phrase": "regulatory compliance", "mentions": 3520, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Project Management Specialists"]}
{"id": "p0130", "phrase": "word", "mentions": 3518, "occupations": ["Accountants and Auditors", "Project Management Specialists", "Executive Secretaries and Executive Administrative Assistants"]}
{"id": "p0131", "phrase": "treatment planning", "mentions": 3516, "occupations": ["Dentists, General", "Registered Nurses", "Mental Health Counselors"]}
{"id": "p0132", "phrase": "tuition reimbursement", "mentions": 3405, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Project Management Specialists"]}
{"id": "p0133", "phrase": "finance", "mentions": 3350, "occupations": ["Accountants and Auditors", "Financial Managers", "Financial and Investment Analysts"]}
{"id": "p0134", "phrase": "civil engineering", "mentions": 3297, "occupations": ["Project Management Specialists", "Civil Engineers", "Construction Managers"]}
{"id": "p0135", "phrase": "standing", "mentions": 3295, "occupations": ["Registered Nurses", "First-Line Supervisors of Office and Administrative Support Workers", "Managers, All Other"]}
{"id": "p0136", "phrase": "relationship building", "mentions": 3228, "occupations": ["Sales Managers", "First-Line Supervisors of Office and Administrative Support Workers", "Project Management Specialists"]}
{"id": "p0137", "phrase": "dental benefits", "mentions": 3227, "occupations": ["Registered Nurses", "Physical Therapists", "Surgical Technologists"]}
{"id": "p0138", "phrase": "ethics", "mentions": 3216, "occupations": ["Registered Nurses", "Pharmacists", "Lawyers"]}
{"id": "p0139", "phrase": "bsn", "mentions": 3214, "occupations": ["Registered Nurses", "Medical and Health Services Managers", "Clinical Nurse Specialists"]}
{"id": "p0140", "phrase": "performance management", "mentions": 3185, "occupations": ["Human Resources Managers", "Human Resources Specialists", "First-Line Supervisors of Office and Administrative Support Workers"]}
{"id": "p0141", "phrase": "acls certification", "mentions": 3154, "occupations": ["Registered Nurses", "Nurse Practitioners", "Medical and Health Services Managers"]}
{"id": "p0142", "phrase": "initiative", "mentions": 3149, "occupations": ["Executive Secretaries and Executive Administrative Assistants", "Accountants and Auditors", "Sales Managers"]}
{"id": "p0143", "phrase": "medical insurance", "mentions": 3142, "occupations": ["Registered Nurses", "Veterinarians", "Lawyers"]}
{"id": "p0144", "phrase": "integrity", "mentions": 3090, "occupations": ["Registered Nurses", "Sales Managers", "Accountants and Auditors"]}
{"id": "p0145", "phrase": "radiology", "mentions": 3075, "occupations": ["Radiologic Technologists and Technicians", "Veterinarians", "Magnetic Resonance Imaging Technologists"]}
{"id": "p0146", "phrase": "java", "mentions": 3072, "occupations": ["Software Developers", "Computer Programmers", "Software Quality Assurance Analysts and Testers"]}
{"id": "p0147", "phrase": "motivation", "mentions": 3043, "occupations": ["First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services", "Customer Service Representatives", "General and Operations Managers"]}
{"id": "p0148", "phrase": "powerpoint", "mentions": 3030, "occupations": ["Executive Secretaries and Executive Administrative Assistants", "Project Management Specialists", "Sales Managers"]}
{"id": "p0149", "phrase": "forecasting", "mentions": 3013, "occupations": ["Accountants and Auditors", "Sales Managers", "Financial Managers"]}
{"id": "p0150", "phrase": "team player", "mentions": 2965, "occupations": ["Accountants and Auditors", "Customer Service Representatives", "Nurse Practitioners"]}

Return the JSON object described in your instructions, with one answer for each of the 150 items.

## What to send back

The JSON object described above, and nothing else. It is saved as `reply-phrases-pilot-1.json`.
