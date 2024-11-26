# Import MHWP and run tests
from mhwp_class_skeleton import MHWP

# Create an MHWP instance
mhwp = MHWP(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    user_type="MHWP",
    username="johndoe",
    password="password123"
)

# Add patient information
mhwp.add_patient_info("patient1@example.com", "Initial diagnosis of anxiety.", 3)
mhwp.add_patient_info("patient2@example.com", "Diagnosed with PTSD.", 5)
mhwp.add_patient_info("patient3@example.com", "Diagnosed with autism.", 1)

# Display patient information with colored moods
mhwp.display_patients_with_moods()
