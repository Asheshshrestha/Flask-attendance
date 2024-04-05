DROP TABLE IF EXISTS subject;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);
CREATE TABLE teacher(
    id integer primary key AUTOINCREMENT,
    first_name text not null,
    last_name text not null,
    email text not null,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
CREATE TABLE subject(
    id integer primary key AUTOINCREMENT,
    subject_name text not null,
    subject_code text not null,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)

);
CREATE TABLE student(
    id integer primary key AUTOINCREMENT,
    first_name text not null,
    last_name text not null,
    email text NOT NULL

);
INSERT INTO user (username,role, password)
VALUES 
    ('admin@yopmail.com','admin', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17'),
    ('emily.johnson@yopmail.com','teacher', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17'),
    ('michael.thompson@yopmail.com','teacher', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17'),
    ('sarah.davis@yopmail.com','teacher', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17'),
    ('john.rodriguez@yopmail.com','teacher', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17');

Insert into teacher(first_name,last_name,email,user_id) values 
('Emily', 'Johnson', 'emily.johnson@yopmail.com',2),
    ('Michael', 'Thompson', 'michael.thompson@yopmail.com',3),
    ('Sarah', 'Davis', 'sarah.davis@yopmail.com',4),
    ('John', 'Rodriguez', 'john.rodriguez@yopmail.com',5);

INSERT INTO subject (subject_name, subject_code, teacher_id) VALUES
    ('Mathematics', 'MATH101', 1),
    ('Physics', 'PHYS102', 2),
    ('Biology', 'BIOL103', 3),
    ('History', 'HIST104', 4);

INSERT INTO student (first_name, last_name, email) VALUES
    ('John', 'Doe', 'john.doe@yopmail.com'),
    ('Jane', 'Smith', 'jane.smith@yopmail.com'),
    ('Michael', 'Johnson', 'michael.johnson@yopmail.com'),
    ('Emily', 'Brown', 'emily.brown@yopmail.com'),
    ('David', 'Williams', 'david.williams@yopmail.com'),
    ('Sarah', 'Jones', 'sarah.jones@yopmail.com'),
    ('Daniel', 'Garcia', 'daniel.garcia@yopmail.com'),
    ('Jennifer', 'Martinez', 'jennifer.martinez@yopmail.com'),
    ('James', 'Hernandez', 'james.hernandez@yopmail.com'),
    ('Jessica', 'Lopez', 'jessica.lopez@yopmail.com');