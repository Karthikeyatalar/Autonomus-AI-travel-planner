import sys
import os

# Add the current directory to sys.path so we can import from the app
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.database import SessionLocal, engine, Base
from app import models

def seed():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # ── Curated Data from ai_agent.py ──
    PLACES_DB = {
        "goa": ["Calangute Beach", "Anjuna Flea Market", "Fort Aguada", "Dudhsagar Falls", "Basilica of Bom Jesus", "Se Cathedral", "Panjim Latin Quarter", "Miramar Beach", "Reis Magos Fort", "Agonda Beach", "Dona Paula Viewpoint", "South Goa Backwaters", "Chapora Fort", "Colva Beach", "Grand Island", "Butterfly Beach", "Palolem Beach", "Baga Beach", "Candolim Beach", "Old Goa Heritage Walk"],
        "mumbai": ["Gateway of India", "Marine Drive", "Colaba Causeway", "Elephanta Caves", "Chhatrapati Shivaji Maharaj Terminus", "Haji Ali Dargah", "Dharavi Leather Market", "Bandra-Worli Sea Link", "Juhu Beach", "Siddhivinayak Temple", "Crawford Market", "Nehru Planetarium", "Jehangir Art Gallery", "Chhatrapati Shivaji Maharaj Vastu Sangrahalaya", "Kanheri Caves", "Global Vipassana Pagoda", "Hanging Gardens", "Mount Mary Church", "Taraporewala Aquarium", "Worli Fort", "Prithvi Theatre"],
        "delhi": ["India Gate", "Connaught Place", "Red Fort", "Qutub Minar", "Humayun's Tomb", "Lotus Temple", "Chandni Chowk", "Akshardham Temple", "Dilli Haat", "Jama Masjid", "Lodhi Gardens", "National Museum Delhi", "Raj Ghat", "Agrasen ki Baoli", "Purana Qila", "Sarojini Nagar Market", "Jantar Mantar Delhi", "National Gallery of Modern Art", "Safdarjung Tomb", "Tughlaqabad Fort"],
        "jaipur": ["Hawa Mahal", "City Palace", "Jantar Mantar", "Amber Fort", "Nahargarh Fort", "Jal Mahal", "Johari Bazaar", "Albert Hall Museum", "Birla Mandir", "Panna Meena Ka Kund", "Jaigarh Fort", "Galta Ji Temple", "Patrika Gate", "Bapu Bazaar", "Chokhi Dhani", "Amrapali Museum", "Sisodia Rani Garden", "Ishwar Lat", "Albert Hall Museum", "Central Park Jaipur"],
        "agra": ["Taj Mahal", "Mehtab Bagh", "Taj Ganj Market", "Agra Fort", "Itmad-ud-Daula Tomb", "Keetham Lake", "Fatehpur Sikri", "Sikandra", "Kinari Bazaar", "Akbar's Tomb", "Jama Masjid Agra", "Moti Masjid", "Anguri Bagh", "Paliwal Park", "Ram Bagh"],
        "kerala": ["Vembanad Lake", "Kumarakom Bird Sanctuary", "Fort Kochi", "Chinese Fishing Nets", "Mattancherry Palace", "Munnar Tea Gardens", "Eravikulam National Park", "Periyar Wildlife Sanctuary", "Alleppey Backwaters", "Varkala Beach", "Athirappilly Falls", "Padmanabhaswamy Temple", "Bekal Fort", "Wayanad Wildlife Sanctuary", "Guruvayur Temple", "Thekkady", "Kovalam Beach", "Silent Valley National Park"],
        "bangalore": ["Cubbon Park", "Commercial Street", "Lalbagh Botanical Garden", "Bangalore Palace", "ISKCON Temple", "Bannerghatta National Park", "UB City Lounge", "Ulsoor Lake", "Bull Temple", "Vidhana Soudha", "Tipu Sultan's Palace", "Wonderla", "Nandi Hills", "St. Mary's Basilica", "Jawaharlal Nehru Planetarium", "Karnataka Chitrakala Parishath"],
        "ooty": ["Ooty Lake", "Botanical Gardens", "Doddabetta Peak", "Avalanche Lake", "Emerald Lake", "Rose Garden", "Pykara Falls", "Tea Museum", "Pykara Boat House", "Thread Garden", "Glenmorgan View", "Nilgiri Mountain Railway", "Catherine Falls", "Kamraj Sagar Dam", "Government Museum Ooty"],
        "manali": ["Mall Road", "Hadimba Temple", "Old Manali", "Rohtang Pass", "Solang Valley", "Beas River", "Naggar Castle", "Great Himalayan National Park", "Manu Temple", "Jogini Falls", "Vashist Hot Springs", "Manali Sanctuary", "Gulaba", "Bhrigu Lake", "Hampta Pass"],
        "hyderabad": ["Charminar", "Golconda Fort", "Salar Jung Museum", "Hussain Sagar Lake", "Birla Mandir Hyderabad", "Ramoji Film City", "Chowmahalla Palace", "Laad Bazaar", "Chilkur Balaji Temple", "Lumbini Park", "Mecca Masjid", "Qutb Shahi Tombs", "Golconda Fort sound & light show", "Nehru Zoological Park", "Sudha Car Museum"],
        "kolkata": ["Victoria Memorial", "Howrah Bridge", "Dakshineswar Kali Temple", "Park Street", "Indian Museum", "Eco Park Kolkata", "Belur Math", "Princep Ghat", "Mother House", "Science City", "Kalighat Temple", "South Park Street Cemetery", "Indian Botanical Garden", "Marble Palace", "Eden Gardens"],
        "chennai": ["Marina Beach", "Kapaleeshwarar Temple", "Government Museum Chennai", "San Thome Basilica", "Guindy National Park", "Valluvar Kottam", "Edward Elliot's Beach", "DakshinaChitra", "Arignar Anna Zoological Park", "Mylapore Heritage Walking Area", "Fort St. George", "Besant Nagar Beach", "Thousand Lights Mosque", "VGP Universal Kingdom"],
        "kochi": ["Fort Kochi heritage area", "Mattancherry Palace", "Jewish Synagogue", "Marine Drive Kochi", "Santa Cruz Cathedral Basilica", "Cherai Beach", "Lulu Mall Kochi", "Kerala Folklore Museum", "Willingdon Island", "Hill Palace Museum", "Vypin Island", "Mangalavanam Bird Sanctuary", "Princess Street", "Indo-Portuguese Museum"],
        "udaipur": ["City Palace Udaipur", "Lake Pichola", "Jagmandir", "Saheliyon-ki-Bari", "Fateh Sagar Lake", "Monsoon Palace", "Bagore Ki Haveli", "Jagdish Temple", "Shilpgram", "Ambrai Ghat", "Sajjangarh Wildlife Sanctuary", "Vintage Car Museum", "Doodh Talai Lake", "Maharana Pratap Memorial"],
        "amritsar": ["Golden Temple", "Jallianwala Bagh", "Wagah Border Ceremony", "Partition Museum", "Durgiana Temple", "Gobindgarh Fort", "Ram Tirath Temple", "Hall Bazaar", "Akaal Takht", "Bibeksar Sahib", "Maharaja Ranjit Singh Museum", "Guru Ke Mahal"],
        "pune": ["Shaniwar Wada", "Dagdusheth Halwai Ganpati Temple", "Koregaon Park", "Sinhagad Fort", "Pataleshwar Cave Temple", "Aga Khan Palace", "Osho International Meditation Resort", "FC Road Shopping", "Saras Baug", "Lonavala point", "Raja Dinkar Kelkar Museum", "Mulshi Dam", "Vetal Tekdi", "Bund Garden"],
        "london": ["Big Ben", "Tower of London", "British Museum", "London Eye", "Buckingham Palace", "The Shard", "Hyde Park", "St. Paul's Cathedral", "Covent Garden", "Westminster Abbey", "Camden Market", "National Gallery", "Tate Modern", "Borough Market", "Southbank Centre"],
        "new york": ["Statue of Liberty", "Central Park", "Times Square", "Empire State Building", "Metropolitan Museum of Art", "Brooklyn Bridge", "The High Line", "One World Observatory", "Rockefeller Center", "Wall Street", "Broadway", "Grand Central Terminal", "MoMA", "Natural History Museum"],
        "paris": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Musée d'Orsay", "Montmartre district", "Sacré-Cœur Basilica", "Arc de Triomphe", "Champs-Élysées", "Shakespeare and Company bookstore", "Tuileries Garden", "Palais Garnier", "Seine River Cruise", "Le Marais", "Sainte-Chapelle"],
        "dubai": ["Burj Khalifa", "Dubai Mall", "Dubai Fountain", "Palm Jumeirah", "Dubai Frame", "Jumeirah Mosque", "Al Fahidi Historic District", "Gold Souk", "Spice Souk", "Museum of the Future", "Madinat Jumeirah", "Desert Safari basecamp", "Global Village", "Dubai Miracle Garden"],
        "singapore": ["Marina Bay Sands", "Gardens by the Bay", "Merlion Park", "Sentosa Island", "Universal Studios Singapore", "S.E.A. Aquarium", "Chinatown Singapore", "Little India", "Orchard Road", "Singapore Botanic Gardens", "Jewel Changi Airport", "Night Safari", "Clark Quay", "Raffles Hotel"],
        "tokyo": ["Shibuya Crossing", "Shinjuku Gyoen", "Harajuku street", "Senso-ji Temple", "teamLab Borderless", "Akihabara Electric Town", "Tsukiji Outer Market", "Odaiba Seaside Park", "Imperial Palace East Gardens", "Meiji Jingu Shrine", "Tokyo Skytree", "Roppongi Hills", "Ghibli Museum", "Ueno Park"],
        "bali": ["Tanah Lot Temple", "Kuta Beach", "Seminyak Square", "Ubud Monkey Forest", "Tegalalang Rice Terrace", "Tirta Empul Temple", "Uluwatu Temple", "Jimbaran Bay seafood", "Besakih Mother Temple", "Nusa Penida ferry point", "Ulun Danu Beratan Temple", "Mount Batur view", "Sanur Beach", "Campuhan Ridge Walk"],
        "rome": ["Colosseum", "Roman Forum", "Vatican Museums", "Sistine Chapel", "St. Peter's Basilica", "Trevi Fountain", "Pantheon", "Piazza Navona", "Spanish Steps", "Castel Sant'Angelo", "Trastevere district", "Villa Borghese", "Borghese Gallery", "Appian Way", "Capuchin Crypt"],
        "amsterdam": ["Rijksmuseum", "Anne Frank House", "Van Gogh Museum", "Vondelpark", "Dam Square", "Jordaan district", "Royal Palace", "Heineken Experience", "Albert Cup Market", "Bloemenmarkt", "Rembrandt House Museum", "Stedelijk Museum", "EYE Film Institute", "ARTIS Zoo", "Canal Belt cruise"],
        "sydney": ["Sydney Opera House", "Sydney Harbour Bridge", "Bondi Beach", "The Rocks district", "Darling Harbour", "Royal Botanic Garden", "Taronga Zoo", "Manly Beach", "Sydney Tower Eye", "Art Gallery of NSW", "Hyde Park Sydney", "Queen Victoria Building", "Cockatoo Island", "Watsons Bay", "Coogee Beach"],
    }

    HOTELS_DB = {
        "mumbai": [
            {"name": "The Taj Mahal Palace", "type": "Luxury", "price_per_night": "₹25,000+", "rating": "4.9/5", "location": "Colaba", "highlights": ["Iconic heritage", "Sea view", "Fine dining"]},
            {"name": "Trident Nariman Point", "type": "Mid-range", "price_per_night": "₹12,000", "rating": "4.6/5", "location": "Marine Drive", "highlights": ["Ocean view", "Business center", "Pool"]},
            {"name": "Hotel Sahara Star", "type": "Budget", "price_per_night": "₹6,000", "rating": "4.2/5", "location": "Near Airport", "highlights": ["Tropical lagoon", "Convenient location"]}
        ],
        "delhi": [
            {"name": "The Leela Palace Delhi", "type": "Luxury", "price_per_night": "₹22,000+", "rating": "4.8/5", "location": "Chanakyapuri", "highlights": ["Royal stay", "Spa", "Rooftop pool"]},
            {"name": "Taj Palace Delhi", "type": "Mid-range", "price_per_night": "₹14,000", "rating": "4.7/5", "location": "Diplomatic Enclave", "highlights": ["Luxury gardens", "Golf course access"]},
            {"name": "Bloomrooms @ Link Road", "type": "Budget", "price_per_night": "₹4,500", "rating": "4.1/5", "location": "Near Metro", "highlights": ["Clean & minimalist", "Free Wi-Fi"]}
        ],
        "jaipur": [
            {"name": "Rambagh Palace", "type": "Luxury", "price_per_night": "₹45,000+", "rating": "5.0/5", "location": "Bhawani Singh Rd", "highlights": ["Former royal residence", "Sprawling gardens"]},
            {"name": "ITC Rajputana", "type": "Mid-range", "price_per_night": "₹10,000", "rating": "4.5/5", "location": "Station Road", "highlights": ["Rajasthani architecture", "Luxury spa"]},
            {"name": "Pearl Palace Heritage", "type": "Budget", "price_per_night": "₹3,500", "rating": "4.4/5", "location": "Ajmer Road", "highlights": ["Artistic rooms", "Boutique feel"]}
        ],
        "goa": [
            {"name": "Taj Exotica Resort & Spa", "type": "Luxury", "price_per_night": "₹28,000+", "rating": "4.8/5", "location": "Benaulim", "highlights": ["Private beach", "Mediterranean style"]},
            {"name": "W Goa", "type": "Mid-range", "price_per_night": "₹18,000", "rating": "4.6/5", "location": "Vagator", "highlights": ["Party vibe", "Sunset views", "Trendy"]},
            {"name": "Zostel Goa", "type": "Budget", "price_per_night": "₹1,200", "rating": "4.3/5", "location": "Calangute", "highlights": ["Social atmosphere", "Backpacker friendly"]}
        ],
        "rome": [
            {"name": "Hotel Hassler Roma", "type": "Luxury", "price_per_night": "₹55,000+", "rating": "4.9/5", "location": "Spanish Steps", "highlights": ["Iconic luxury", "Panoramic views"]},
            {"name": "Hotel Artemide", "type": "Mid-range", "price_per_night": "₹22,000", "rating": "4.7/5", "location": "Via Nazionale", "highlights": ["Excellent service", "Great location"]},
            {"name": "Generator Rome", "type": "Budget", "price_per_night": "₹5,500", "rating": "4.0/5", "location": "Near Termini", "highlights": ["Trendy hostel", "Rooftop bar"]}
        ],
        "amsterdam": [
            {"name": "Waldorf Astoria Amsterdam", "type": "Luxury", "price_per_night": "₹65,000+", "rating": "4.9/5", "location": "Herengracht", "highlights": ["Canal palace", "Michelin dining"]},
            {"name": "Pulitzer Amsterdam", "type": "Mid-range", "price_per_night": "₹28,000", "rating": "4.7/5", "location": "Prinsengracht", "highlights": ["Historic houses", "Quirky design"]},
            {"name": "Flying Pig Downtown", "type": "Budget", "price_per_night": "₹4,200", "rating": "4.1/5", "location": "Near Central Station", "highlights": ["Backpacker favorite", "Social bar"]}
        ],
        "sydney": [
            {"name": "Park Hyatt Sydney", "type": "Luxury", "price_per_night": "₹75,000+", "rating": "4.8/5", "location": "The Rocks", "highlights": ["Opera House views", "Waterfront luxury"]},
            {"name": "The Fullerton Hotel Sydney", "type": "Mid-range", "price_per_night": "₹24,000", "rating": "4.6/5", "location": "Martin Place", "highlights": ["Historic GPO building", "Central location"]},
            {"name": "Wake Up! Sydney Central", "type": "Budget", "price_per_night": "₹3,800", "rating": "4.3/5", "location": "Near Central Station", "highlights": ["Award-winning hostel", "Daily activities"]}
        ]
    }

    print("Cleaning existing travel data...")
    db.query(models.Hotel).delete()
    db.query(models.Place).delete()
    db.query(models.Destination).delete()
    db.commit()

    print("Seeding new destinations, places, and hotels...")
    for city_key, place_list in PLACES_DB.items():
        # Create Destination
        dest = models.Destination(
            name=city_key,
            display_name=city_key.capitalize()
        )
        db.add(dest)
        db.flush() # Get dest.id

        # Add Places
        for p_name in place_list:
            place = models.Place(name=p_name, destination_id=dest.id)
            db.add(place)
        
        # Add Hotels if available
        if city_key in HOTELS_DB:
            for h_info in HOTELS_DB[city_key]:
                hotel = models.Hotel(
                    name=h_info["name"],
                    type=h_info["type"],
                    price_per_night=h_info["price_per_night"],
                    rating=h_info["rating"],
                    location=h_info["location"],
                    highlights=h_info["highlights"],
                    destination_id=dest.id
                )
                db.add(hotel)

    db.commit()
    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed()
