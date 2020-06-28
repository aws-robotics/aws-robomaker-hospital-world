#!/bin/bash
pip install -r requirements.txt
python3 fuel_utility.py download \
-q Hospital \
-m MopCart3 -m AdjTable -m BedTable -m FemaleVisitorSit -m VisitorKidSit \
-m ElderMalePatient -m OfficeChairBlack \
-m ElderLadyPatient -m MaleVisitorSit -m FemaleVisitor \
-m BedsideTable -m SurgicalTrolleyMed \
-m AnesthesiaMachine -m VendingMachine \
-m TrolleyBox2 -m TrolleyBox1 -m Toilet -m Shower -m PatientFSit \
-m Nurse -m MaleVisitorOnPhone -m MalePatientBed -m KitchenSink \
-m "Male visitor" \
-d fuel_models \
--verbose