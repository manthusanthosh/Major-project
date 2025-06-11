drop database if exists cellular_traffic;
create database cellular_traffic;
use cellular_traffic;

create table users (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(225),
    email VARCHAR(50), 
    password VARCHAR(50)
    );
