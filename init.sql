CREATE DATABASE blog_db;

\c blog_db;

-- -- Suppression des tables existantes dans l'ordre des dépendances
-- DROP TABLE IF EXISTS blogpost CASCADE;
-- DROP TABLE IF EXISTS "user" CASCADE;

-- --------------------------------------------------
-- -- Création de la table des utilisateurs
-- --------------------------------------------------
-- CREATE TABLE "user" (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(255) NOT NULL,
--     email VARCHAR(255) NOT NULL UNIQUE,
--     password_hash VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT NOW()
-- );

-- --------------------------------------------------
-- -- Création de la table des posts (articles de blog)
-- --------------------------------------------------
-- CREATE TABLE blogpost (
--     id SERIAL PRIMARY KEY,
--     title VARCHAR(200) NOT NULL,
--     content TEXT NOT NULL,
--     image_url VARCHAR(255),
--     created_at TIMESTAMP DEFAULT NOW(),
--     user_id INTEGER,
--     CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL
-- );

-- --------------------------------------------------
-- -- Insertion de données dans la table "user"
-- --------------------------------------------------
-- INSERT INTO "user" (username, email, password_hash, created_at) VALUES
-- ('Luigi','luigi.carole@gmail.com','b3252bdb4f2160a89f4e8e0ba93592998c26c7f2431a708f98a17ec5656ff996',NOW());

-- --------------------------------------------------
-- -- Insertion de données dans la table blogpost
-- --------------------------------------------------
-- INSERT INTO blogpost (title, content, image_url, created_at, user_id) VALUES
-- ('Premier Post', 'Ceci est le contenu de mon premier post sur le blog. Bienvenue sur mon blog !', 'https://via.placeholder.com/600x400?text=Premier+Post', NOW(), 1),
-- ('Deuxième Post', 'Voici quelques réflexions dans le deuxième post. Restez connectés !', 'https://via.placeholder.com/600x400?text=Deuxi%C3%A8me+Post', NOW(), 1),
-- ('Troisième Post', 'Contenu détaillé du troisième post, plein d''idées innovantes.', NULL, NOW(), 1);
