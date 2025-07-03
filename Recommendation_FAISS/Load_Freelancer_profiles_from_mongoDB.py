from pymongo import MongoClient

# MongoDB connection config
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "Freelancer_AI_database"
COLLECTION_NAME = "profiles_from_mysql_v3"

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Load all freelancer profiles
profiles = list(collection.find({}))
print(f"✅ Loaded {len(profiles)} profiles from MongoDB.")

# Function to convert each profile into a single rich text
def extract_profile_text(profile):
    # 1. Full name with fallback
    f_name = profile.get('fName', '') or ''
    l_name = profile.get('lName', '') or ''
    name = f"{f_name} {l_name}".strip() or "Unnamed Freelancer"

    # 2. Skills
    skills = ', '.join(profile.get('skills', []) or [])

    # 3. Top keywords
    top_keywords = ', '.join(profile.get('top_keywords', []) or [])

    # 4. Offers (concatenate non-null descriptions)
    descriptions = []
    for pkg in profile.get("packages", []):
        for offer in pkg.get("offers", []):
            desc = offer.get("description")
            if desc:
                descriptions.append(desc.replace('\n', ' ').replace('\r', '').strip())
    offers_text = ' '.join(descriptions)

    # 5. Profile type
    if profile.get('is_ingenieur', 0) == 1:
        profile_type = "This freelancer is an engineer."
    elif profile.get('is_technicien', 0) == 1:
        profile_type = "This freelancer is a technician."
    else:
        profile_type = "Freelancer profile type not specified."

    # Combine everything into final text
    id_freelancer = profile.get('idFreelancer', 'N/A')
    final_text = (
        f"idFreelancer: {id_freelancer}. "
        f"{name}. "
        f"Skills: {skills}. "
        f"Top keywords: {top_keywords}. "
        f"Offers: {offers_text} "
        f"{profile_type}"
    )

    return final_text

# Generate text for each profile
texts = [extract_profile_text(p) for p in profiles]

# Optional: Preview a few results
print("\n--- Preview ---\n")
for i, profile in enumerate(profiles[:3]):
    id_freelancer = profile.get('idFreelancer', 'N/A')
    f_name = profile.get('fName', '') or ''
    l_name = profile.get('lName', '') or ''
    name = f"{f_name} {l_name}".strip() or "Unnamed Freelancer"
    text = extract_profile_text(profile)
    print(f"Profile {i+1} (idFreelancer: {id_freelancer}, Name: {name}):\n{text}\n")
