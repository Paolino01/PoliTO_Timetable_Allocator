CREATE TABLE Teachers_Unavailability (
	Surname VARCHAR(50) NOT NULL,
	Unavailable_Slot INT,
	PRIMARY KEY (Surname, Unavailable_Slot)
)