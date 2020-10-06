#!/bin/bash
pip install -r requirements.txt
python3 fuel_utility.py download \
-m XRayMachine -m IVStand -m BloodPressureMonitor -m BPCart -m BMWCart \
-m CGMClassic -m StorageRack -m Chair \
-m InstrumentCart1 -m Scrubs -m PatientWheelChair \
-m WhiteChipChair -m TrolleyBed -m SurgicalTrolley \
-m PotatoChipChair -m VisitorKidSit -m FemaleVisitorSit \
-m AdjTable -m MopCart3 -m MaleVisitorSit -m Drawer \
-m OfficeChairBlack -m ElderLadyPatient -m ElderMalePatient \
-m InstrumentCart2 -m MetalCabinet -m BedTable -m BedsideTable \
-m AnesthesiaMachine -m TrolleyBedPatient -m Shower \
-m SurgicalTrolleyMed -m StorageRackCovered -m KitchenSink \
-m Toilet -m VendingMachine -m ParkingTrolleyMin -m PatientFSit \
-m MaleVisitorOnPhone -m FemaleVisitor -m MalePatientBed \
-m StorageRackCoverOpen -m ParkingTrolleyMax \
-d fuel_models --verbose