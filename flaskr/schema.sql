DROP TABLE IF EXISTS subject;
DROP TABLE IF EXISTS teacher;


CREATE TABLE teacher(
    id integer primary key AUTOINCREMENT,
    first_name text not null,
    last_name text not null,
    email text not null

);
CREATE TABLE subject(
    id integer primary key AUTOINCREMENT,
    subject_name text not null,
    subject_code text not null,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)

);

Insert into teacher(first_name,last_name,email) values 
('Emily', 'Johnson', 'emily.johnson@yopmail.com'),
    ('Michael', 'Thompson', 'michael.thompson@yopmail.com'),
    ('Sarah', 'Davis', 'sarah.davis@yopmail.com'),
    ('John', 'Rodriguez', 'john.rodriguez@yopmail.com');

INSERT INTO subject (subject_name, subject_code, teacher_id) VALUES
    ('Mathematics', 'MATH101', 1),
    ('Physics', 'PHYS102', 2),
    ('Biology', 'BIOL103', 3),
    ('History', 'HIST104', 4);