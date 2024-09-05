CREATE DATABASE education_kit_db;

USE education_kit_db;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    father_name VARCHAR(255) NOT NULL,
    login VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    type ENUM('student', 'teacher') NOT NULL,
    photo BLOB
);

CREATE TABLE Teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id) REFERENCES Users(id)
        ON DELETE CASCADE
);

CREATE TABLE Classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    supervisor_id INT,
    CONSTRAINT fk_supervisor
        FOREIGN KEY (supervisor_id) REFERENCES Teachers(id)
        ON DELETE CASCADE
);

CREATE TABLE Students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    class_id INT,
    CONSTRAINT fk_user_student
        FOREIGN KEY (user_id) REFERENCES Users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_class_student
        FOREIGN KEY (class_id) REFERENCES Classes(id)
        ON DELETE SET NULL
);

CREATE TABLE Subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description VARCHAR(255),
    photo BLOB,
    teacher_id INT,
    CONSTRAINT fk_teacher_subject
        FOREIGN KEY (teacher_id) REFERENCES Teachers(id)
        ON DELETE SET NULL
);

CREATE TABLE Requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    father_name VARCHAR(255) NOT NULL,
    login VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    class_id INT, -- поле не було оголошено
    CONSTRAINT fk_class_request
        FOREIGN KEY (class_id) REFERENCES Classes(id)
        ON DELETE SET NULL
);

CREATE TABLE Meetings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    subject_id INT,
    CONSTRAINT fk_subject_meeting
        FOREIGN KEY (subject_id) REFERENCES Subjects(id)
        ON DELETE SET NULL
);

CREATE TABLE TeachersClasses (
    teacher_id INT,
    class_id INT,
    CONSTRAINT fk_teacher_class_teacher
        FOREIGN KEY (teacher_id) REFERENCES Teachers(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_teacher_class_class
        FOREIGN KEY (class_id) REFERENCES Classes(id)
        ON DELETE CASCADE
);
