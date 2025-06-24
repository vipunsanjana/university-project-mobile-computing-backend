import logging

# Logging
logging.basicConfig(
    level=getattr(logging, "INFO", logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

# Logger
LOGGER = logging.getLogger(__name__)

# web page content types
VALID_CONTENT_TYPE = "application/json"

# List of valid subject streams
DISTRICT_PROXIMITY = {
    "Colombo": ["Gampaha", "Kalutara"],
    "Gampaha": ["Colombo", "Kurunegala"],
    "Kalutara": ["Colombo", "Ratnapura"],
    "Kandy": ["Matale", "Nuwara Eliya", "Kegalle"],
    "Matale": ["Kandy", "Anuradhapura"],
    "Nuwara Eliya": ["Kandy", "Badulla"],
    "Galle": ["Matara", "Ratnapura"],
    "Matara": ["Galle", "Hambantota"],
    "Hambantota": ["Matara", "Monaragala"],
    "Jaffna": ["Kilinochchi"],
    "Kilinochchi": ["Jaffna", "Mullaitivu"],
    "Mannar": ["Vavuniya"],
    "Vavuniya": ["Mullaitivu", "Mannar"],
    "Mullaitivu": ["Kilinochchi", "Vavuniya"],
    "Batticaloa": ["Ampara"],
    "Ampara": ["Batticaloa", "Monaragala"],
    "Trincomalee": ["Polonnaruwa"],
    "Kurunegala": ["Gampaha", "Kegalle"],
    "Puttalam": ["Kurunegala"],
    "Anuradhapura": ["Matale"],
    "Polonnaruwa": ["Badulla"],
    "Badulla": ["Nuwara Eliya", "Monaragala"],
    "Monaragala": ["Badulla", "Hambantota"],
    "Ratnapura": ["Kalutara", "Galle", "Kegalle"],
    "Kegalle": ["Ratnapura", "Kandy", "Kurunegala"]
}
