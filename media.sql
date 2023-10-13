CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(1024),
    file_path VARCHAR(1024)
);

CREATE TABLE tv_shows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(1024),
    season INT,
    episode INT,
    file_path VARCHAR(1024)
);

CREATE TABLE programming (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(1024),
    file_path VARCHAR(1024)
);
